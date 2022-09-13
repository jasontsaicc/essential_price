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

s3 = boto3.client('s3')
s3.download_file('tests3buckettt', 'IMG_0426.jpg', 'IMG_0426.jpg')
                                   # s3 上傳的檔案   下載下來要存的名稱
