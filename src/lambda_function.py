# src/lambda_function.py
from aws_lambda_powertools import Logger
from image_utils import ImageProcessor
import boto3

logger = Logger()
s3_client = boto3.client('s3')
rekognition_client = boto3.client('rekognition')

# Entry point for the lambda function
@logger.inject_lambda_context
def lambda_handler(event, context):
    processor = ImageProcessor(s3_client, rekognition_client, logger)
    processor.process_image(event)
