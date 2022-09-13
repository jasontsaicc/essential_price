
import logging
import boto3
from botocore.exceptions import ClientError
import os
from boto3.session import Session
session = Session(aws_access_key_id='AKIAXLGUPNLYCONS5KRO', aws_secret_access_key='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', region_name='us-east-1')

#获取s3连接的session
s3 = session.resource('s3')
for bucket in s3.buckets.all():
    print('bucket name:%s'%bucket.name)



os.environ['AWS_ACCESS_KEY_ID'] = "AKIAXLGUPNLYCONS5KRO"
os.environ['AWS_SECRET_ACCESS_KEY'] = "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"


def upload_file(file_name, bucket, object_name):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

upload_file(r"C:\Users\TibeMe_user\Desktop\model_0830.h5", "tests3buckettt", 'model_0830.h5')
                           # 檔案路徑                         存在s3 哪個桶子     上傳檔案的名稱