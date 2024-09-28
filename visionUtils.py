import base64
from PIL import Image
import os
import uuid

def generate_s3_image_path(local_image_path):
    # Extract the file name and extension from the local image path
    file_name, file_extension = os.path.splitext(os.path.basename(local_image_path))

    # Generate a unique UUID for the S3 object key
    s3_object_key = str(uuid.uuid4()) + file_extension

    # Define the S3 bucket path
    s3_bucket_path = "s3://together-ai-uploaded-user-images-prod"

    # Construct the full S3 image path string
    s3_image_path = f"{s3_bucket_path}/{s3_object_key}"

    return s3_image_path

def image_to_base64(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()
    base64_string = base64.b64encode(image_data)
    return base64_string.decode('utf-8')