import boto3
import os
from botocore.exceptions import ClientError 
import sys
import cv2
from io import BytesIO
from datetime import datetime

current_script_dir = os.path.dirname(os.path.abspath(__file__))
print(current_script_dir)
project_root_dir = os.path.dirname(current_script_dir)
print(project_root_dir)
if project_root_dir not in sys.path:
    sys.path.insert(0, project_root_dir)
    print(f"DEBUG: Added '{project_root_dir}' to sys.path.")


from services.image_processing_service import crop_ad_banner


AWS_REGION = 'us-west-2'
S3_BUCKET_NAME = 'ads-snapshot-storage'
LOCAL_SOURCE_DIR = '/Users/shireen/Downloads/ad_screenshots/'  # The local folder you want to sync
S3_TARGET_PREFIX = 'ads-snapshot/'
TEN_KB = 10 * 1024 # 10 KB = 10 * 1024 bytes

def get_file_name(file_name, count):
    return f"{file_name}_{count}.jpg"

def valid_image_size(buffer):
    image_bytes = buffer.tobytes()
    byte_size = len(image_bytes)   
    return (byte_size > TEN_KB)


def get_file_creation_date(file_path):
    """
    Gets the creation date (birth time) of a file on macOS.
    Returns a datetime object or None if the file doesn't exist or an error occurs.
    """
    try:
        # Use os.stat() to get file status information
        stat_info = os.stat(file_path)

        # On macOS (and other systems supporting it), st_birthtime directly
        # provides the creation time.
        if hasattr(stat_info, 'st_birthtime'):
            creation_timestamp = stat_info.st_birthtime
            return datetime.fromtimestamp(creation_timestamp)
        else:
            # This 'else' block should ideally not be hit on modern macOS,
            # as st_birthtime is a standard attribute there.
            print(f"Warning: st_birthtime not found for {file_path}. "
                  f"This is unexpected on macOS for new files. "
                  f"Falling back to os.path.getctime().")
            creation_timestamp = os.path.getctime(file_path)
            return datetime.fromtimestamp(creation_timestamp)


    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def save_ad_snapshot_to_s3(bucket_name, aws_region,local_dir):
    s3_client = boto3.client('s3',region_name = aws_region)

    for root,_,files in os.walk(local_dir):
        parent_dir = os.path.basename(root)

        root_mtime = str(os.path.getmtime(root))
        for file_name in files:
            full_path = os.path.join(root, file_name) 
            if not file_name.startswith("."):
                s3_file_name = 'ads-snapshot/'+root_mtime+'/'+file_name

                # crop the image by finding the red bouding box 
                cropped_ads = crop_ad_banner(full_path)
                for i, crop in enumerate(cropped_ads):
                    success, buffer = cv2.imencode('.jpg', crop)

                    if success and valid_image_size(buffer):
                        img_bytes = BytesIO(buffer)
                        s3_key = get_file_name(s3_file_name, i)
                        s3_client.upload_fileobj(img_bytes, bucket_name,s3_key, 
                                                 ExtraArgs={'ContentType': 'image/jpeg','Metadata': {'creation-time': str(get_file_creation_date(full_path)), # Corrected key and value type
                                                                                                     'source-site': parent_dir 
                                                                                                     }})         # Corrected key (assuming parent_dir is already a string)}}
                                                                                                       
                        print(f'file successfully uploaded {s3_file_name}')
                try:
                    os.remove(full_path)
                    print(f"Local file {full_path} has been deleted.")
                except Exception as e:
                    print(f"Failed to delete local file {full_path}: {e}")
              
            

if __name__ == "__main__":
    save_ad_snapshot_to_s3(S3_BUCKET_NAME, AWS_REGION, LOCAL_SOURCE_DIR)

