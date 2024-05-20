# src/image_utils.py
import cv2
import os

from label_drawer import LabelDrawer
from rekognition_utils import RekognitionUtils
from s3_utils import S3Utils

class ImageProcessor:
    def __init__(self, s3_client, rekognition_client, logger):
        self.logger = logger
        self.s3_utils = S3Utils(s3_client)
        self.rekognition_utils = RekognitionUtils(rekognition_client)
        self.label_drawer = LabelDrawer()

    def process_image(self, event):
        input_bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        output_bucket = os.environ.get('OUTPUT_BUCKET')
        local_filename = f"/tmp/{key}"

        self.s3_utils.download_image(input_bucket, key, local_filename)
        img = cv2.imread(local_filename)
        labels = self.rekognition_utils.detect_labels(input_bucket, key)

        img = self.label_drawer.draw_labels(img, labels)
        output_filename = f"/tmp/labeled-{key}"
        cv2.imwrite(output_filename, img)
        self.s3_utils.upload_image(output_filename, output_bucket, key)
