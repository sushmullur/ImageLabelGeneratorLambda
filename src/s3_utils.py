# src/s3_utils.py

class S3Utils:
    def __init__(self, s3_client):
        self.s3_client = s3_client

    # Download image from S3
    def download_image(self, bucket, key, local_path):
        self.s3_client.download_file(bucket, key, local_path)

    # Upload image to S3
    def upload_image(self, file_path, bucket, key):
        self.s3_client.upload_file(file_path, bucket, key)
