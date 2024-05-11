# src/rekognition_utils.py

class RekognitionUtils:
    def __init__(self, rekognition_client):
        self.rekognition_client = rekognition_client

    # Detect labels in the image
    def detect_labels(self, bucket, key):
        response = self.rekognition_client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MaxLabels=20
        )
        return response['Labels']
