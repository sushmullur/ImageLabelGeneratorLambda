import boto3
import cv2
import json
import numpy as np
import os
import urllib.parse

from aws_lambda_powertools import Logger

logger = Logger()

s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

@logger.inject_lambda_context
def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))

    # Get the bucket name and key for uploaded object
    input_bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8'
    )
    output_bucket = os.environ.get('OUTPUT_BUCKET')
    local_filename = f"/tmp/{key}"

    # Download the image from S3 to the local filesystem
    try:
        s3.download_file(input_bucket, key, local_filename)
    except Exception as e:
        logger.error(f"Error downloading object {key} from bucket {input_bucket}. {e}")
        raise e

    # Load image with OpenCV
    img = cv2.imread(local_filename)
    # Convert color from BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Detect labels
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': input_bucket, 
                'Name': key
            }
        }, 
        MaxLabels=20
    )

    # Draw labels on image
    font = cv2.FONT_HERSHEY_SIMPLEX
    for label in response['Labels']:
        name = label['Name']
        confidence = label['Confidence']
        cv2.putText(img, f"{name} ({confidence:.2f}%)", (10, 30), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Save image with labels to a new file
    output_filename = f"/tmp/labeled-{key}"
    cv2.imwrite(output_filename, img)

    # Upload the labeled image to S3
    s3.upload_file(output_filename, output_bucket, f"labeled-{key}")

    return {
        'statusCode': 200,
        'body': json.dumps('Image labeled and uploaded to S3.')
    }
