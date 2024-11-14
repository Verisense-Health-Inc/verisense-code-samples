import boto3
import os
from dotenv import dotenv_values

config = dotenv_values(".env")
# Get AWS credentials from environment variables
aws_access_key_id = config["AWS_ACCESS_KEY_ID"]
aws_secret_access_key = config["AWS_SECRET_ACCESS_KEY"]
# Define the bucket name and local directory path
bucket_name = "bucket_name"
data_dir = "./data"

# Define the prefixes to filter the objects in the bucket
prefixes = [
    "1/A01/01010101AAAA/ParsedFiles/",
    "1/A02/01010101AAAA/ParsedFiles/",
]

# Create an S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# Iterate through each prefix
for prefix in prefixes:
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        if "Contents" in page:
            for obj in page["Contents"]:
                key = obj["Key"]
                # Construct the local file path
                local_file_path = os.path.join(data_dir, key.replace("/", os.sep))
                # Create directory structure if it does not exist
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                # Download the file
                s3.download_file(bucket_name, key, local_file_path)
                print(f"Downloaded {key} to {local_file_path}")
