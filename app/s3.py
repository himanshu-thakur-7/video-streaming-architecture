import boto3

s3_client = boto3.client(
    "s3",
    endpoint_url="http://youtube-localstack:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

BUCKET_NAME = "youtube-videos"

def create_bucket_if_not_exists():
    existing_buckets = s3_client.list_buckets()

    bucket_names = [
        bucket["name"] for bucket in existing_buckets.get("Buckets",[])
    ]
    if BUCKET_NAME not in bucket_names:
        s3_client.create_bucket(Bucket=BUCKET_NAME)
