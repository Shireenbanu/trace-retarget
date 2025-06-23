import boto3
import os

AWS_REGION = 'us-west-2'
S3_BUCKET_NAME = 'ads-snapshot-storage'
LOCAL_SOURCE_DIR = '/Users/shireen/Downloads/ad_screenshots/'  # The local folder you want to sync
S3_TARGET_PREFIX = 'ads-snapshot/'


def check_if_file_exists(bucket_name, file_name):
    s3_client = boto3.client('s3')
    
    try:
        # Check if the file exists
        s3_client.head_object(Bucket=bucket_name, Key=file_name)
        return True  # File exists
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False  # File does not exist
        else:
            # Other errors
            raise


def save_ad_snapshot_to_s3(bucket_name, aws_region,local_dir):
    s3_client = boto3.client('s3',region_name = aws_region)
    s3_resource = boto3.resource('s3',region_name = aws_region)

    for root,_,files in os.walk(local_dir):
        for file_name in files:
            full_path = os.path.join(root, file_name)

            # Skip hidden files or specific patterns if needed
            if file_name.startswith('.'):
                continue

            s3_file_name = 'ads-snapshot/'+str(os.path.getmtime(root))+'/'+file_name
            
            if check_if_file_exists(bucket_name, s3_file_name):
                print(f'file already exist {s3_file_name}')
            else:
                s3_client.upload_file(full_path, bucket_name, s3_file_name)
                print(f'file successfully uploaded {s3_file_name}')
                
        

if __name__ == "__main__":
    save_ad_snapshot_to_s3(S3_BUCKET_NAME, AWS_REGION, LOCAL_SOURCE_DIR)

