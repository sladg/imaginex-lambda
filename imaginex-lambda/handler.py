import tempfile
import requests
import io
import os
import boto3
import base64
import json
from PIL import Image
from urllib.parse import urlparse

# Pillow supported formats:
# BLP, BMP, DDS, DIB, EPS, GIF, ICNS, ICO, IM, JPG, JPEG, MSP, PCX, PNG, PPM, SPIDER, TGA, TIFF, WEBP, XBM

s3_client = boto3.client('s3')

# @TODO: Add typings for buffer.


def is_absolute(url):
    return bool(urlparse(url).netloc)


def download_image(buffer, img_url: str):
    print("Downloading image...")

    r = requests.get(img_url, stream=True)

    content_type = r.headers['content-type']
    extension = content_type.upper().replace('IMAGE/', '')
    content_size = int(r.headers['content-length'])
    print(content_type)

    if r.status_code != 200:
        raise Exception("Error downloading image")

    downloaded = 0

    for chunk in r.iter_content(chunk_size=1024):
        downloaded += len(chunk)
        buffer.write(chunk)

        # Print percent remaining.
        print(downloaded/content_size*100)
    buffer.seek(0)

    print("Downloaded!")
    return {'content_type': content_type, 'extension': extension, 'content_size': content_size}


def get_s3_image(buffer, bucket: str, key: str):
    print("Downloading image from S3...")
    r = s3_client.head_object(Bucket=bucket, Key=key)

    s3_client.download_file(bucket, key, buffer)
    content_type = r['ContentType']
    content_size = r['ContentLength']
    extension = content_type.upper().replace('IMAGE/', '')

    return {'content_type': content_type, 'extension': extension, 'content_size': content_size}


def optimize_image(buffer, ext: str, width: int = 0, quality: int = 70):
    print("Optimizing image...")
    img = Image.open(io.BytesIO(buffer.read()))

    if (width > 0 & width < img.width):
        print("Resizing image...")
        new_height = int(width * img.height / img.width)

        print(width, new_height)

        img = img.resize((width, new_height))
        print("Resized!")

    output = io.BytesIO()
    img.save(output, quality=quality, optimize=True, format=ext)

    print("Optimized!")
    return base64.b64encode(output.getvalue()).decode()


def handler(event, context):
    buffer = tempfile.TemporaryFile()
    try:
        print("Starting...")

        bucket_name = os.environ['S3_BUCKET_NAME']

        url = event['queryStringParameters']['url']
        width = int(event['queryStringParameters']['w'])
        quality = int(event['queryStringParameters']['q'])

        print(url, width, quality)

        response = None

        if (is_absolute(url)):
            response = download_image(buffer, url)
        else:
            key = url.strip('/')
            response = get_s3_image(buffer, bucket_name, key)

        print(response)

        content_type = response['content_type']
        content_size = response['content_size']
        extension = response['extension']

        image_data = optimize_image(
            buffer,
            ext=extension,
            width=width,
            quality=quality
        )

        print("Returning data...")
        return {
            'statusCode': 200,
            'body': image_data,
            'isBase64Encoded': True,
            'headers': {
                'Vary': 'Accept',
                'Content-Type': content_type
            }
        }
    finally:
        buffer.close()


if __name__ == '__main__':
    print("Running test...")

    data = json.load(open('example/event-absolute.json'))
    handler(data, None)
