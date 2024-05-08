import json
import urllib.parse
import boto3

print("Loaded function")

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))

    # Get the bucket name and key for uploaded object
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8'
        )

    try:
        # Detect labels in the image
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket, 
                    'Name': key
                    }
                }, 
            MaxLabels=20
            )
        print("Detected labels for image: " + key + " : " + json.dumps(response['Labels'], indent=2))

    except Exception as e:
        print(e)
        print(f"Error processing object {key} from bucket {bucket}.")
        raise e
