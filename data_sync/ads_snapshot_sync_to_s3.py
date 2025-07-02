import boto3
import os
from botocore.exceptions import ClientError 
import sys
import cv2
from io import BytesIO

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

def save_ad_snapshot_to_s3(bucket_name, aws_region,local_dir):
    s3_client = boto3.client('s3',region_name = aws_region)

    for root,_,files in os.walk(local_dir):
        root_mtime = str(os.path.getmtime(root))

        for file_name in files:
            print("file name ", file_name)
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
                        s3_client.upload_fileobj(img_bytes, bucket_name,s3_key, ExtraArgs={'ContentType': 'image/jpeg'})  
                        print(f'file successfully uploaded {s3_file_name}')
                try:
                    os.remove(full_path)
                    print(f"Local file {full_path} has been deleted.")
                except Exception as e:
                    print(f"Failed to delete local file {full_path}: {e}")
              
            

if __name__ == "__main__":
    save_ad_snapshot_to_s3(S3_BUCKET_NAME, AWS_REGION, LOCAL_SOURCE_DIR)

