# src/image_utils.py
import cv2
import os
from s3_utils import S3Utils
from rekognition_utils import RekognitionUtils

class ImageProcessor:
    def __init__(self, s3_client, rekognition_client):
        self.s3_utils = S3Utils(s3_client)
        self.rekognition_utils = RekognitionUtils(rekognition_client)

    # - Read image from S3 input bucket
    # - Detect labels using Rekognition
    # - Draw bounding boxes and labels on the image
    # - Save the image back to S3 output bucket
    def process_image(self, event):
        input_bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        output_bucket = os.environ.get('OUTPUT_BUCKET')
        local_filename = f"/tmp/{key}"

        self.s3_utils.download_image(input_bucket, key, local_filename)
        img = cv2.imread(local_filename)
        labels = self.rekognition_utils.detect_labels(input_bucket, key)

        self._draw_labels(img, labels)
        output_filename = f"/tmp/labeled-{key}"
        cv2.imwrite(output_filename, img)
        self.s3_utils.upload_image(output_filename, output_bucket, key)

    # Draw bounding boxes and labels on the image
    def _draw_labels(self, img, labels):
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 3
        font_thickness = 2
        for label in labels:
            name = label['Name']
            confidence = label['Confidence']
            if 'Instances' in label:
                for instance in label['Instances']:
                    box = instance['BoundingBox']
                    left = int(box['Left'] * img.shape[1])
                    top = int(box['Top'] * img.shape[0])
                    width = int(box['Width'] * img.shape[1])
                    height = int(box['Height'] * img.shape[0])
                    # Draw rectangle around the object
                    cv2.rectangle(img, (left, top), (left + width, top + height), (0, 255, 0), 2)
                    # Put the label text above the rectangle
                    label_text = f"{name} ({confidence:.2f}%)"
                    # Calculate text width & height to draw the text background
                    (text_width, text_height), _ = cv2.getTextSize(label_text, font, font_scale, font_thickness)
                    cv2.rectangle(img, (left, top - text_height - 10), (left + text_width, top), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, label_text, (left, top - 5), font, font_scale, (255, 255, 255), font_thickness)

        return img
