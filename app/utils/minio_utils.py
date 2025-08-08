import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    's3',
    endpoint_url=os.getenv("MINIO_ENDPOINT", "http://localhost:9000"),
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY", "Commission"),
    region_name='us-east-1'
)

BUCKET_NAME = os.getenv("MINIO_BUCKET", "commission-reports")

def upload_file_to_minio(file_path: str, key: str) -> str:
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
    except:
        s3.create_bucket(Bucket=BUCKET_NAME)

    s3.upload_file(file_path, BUCKET_NAME, key)
    return f"{os.getenv('MINIO_ENDPOINT')}/{BUCKET_NAME}/{key}"

def get_presigned_url(key: str) -> str:
    return s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': BUCKET_NAME, 'Key': key},
        ExpiresIn=3600
    )
