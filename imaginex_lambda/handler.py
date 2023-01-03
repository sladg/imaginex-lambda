import json
import os
import shutil
from contextlib import ExitStack
from tempfile import TemporaryFile
from typing import IO
from urllib.request import urlopen

import botocore.session
from PIL import Image

from imaginex_lambda.utils import error, success, is_absolute, get_extension

DOWNLOAD_CHUNK_SIZE = int(os.getenv('DOWNLOAD_CHUNK_SIZE', 1024))
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', None)

# Pillow supported formats:
# BLP, BMP, DDS, DIB, EPS, GIF, ICNS, ICO, IM, JPG, JPEG, MSP, PCX, PNG, PPM, SPIDER, TGA, TIFF, WEBP, XBM

session = botocore.session.get_session()
s3_client = session.create_client('s3')


# @TODO: Add placeholder image for errors.


def download_image(buffer: IO[bytes], img_url: str):
    print("Downloading image...")

    with urlopen(img_url) as r:
        content_type = r.headers['content-type']
        content_size = int(r.headers['content-length'])

        shutil.copyfileobj(r, buffer, DOWNLOAD_CHUNK_SIZE)

    print("Downloaded!")
    return {'content_type': content_type, 'content_size': content_size}


def get_s3_image(buffer: IO[bytes], key: str):
    if not S3_BUCKET_NAME:
        raise Exception('must specify a value for S3_BUCKET_NAME for S3 support')

    print("Downloading image from S3...")
    r = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=key)

    content_type = r['ContentType']
    content_size = r['ContentLength']

    with r['Body'] as fin:
        shutil.copyfileobj(fin, buffer, DOWNLOAD_CHUNK_SIZE)

    return {'content_type': content_type, 'content_size': content_size}


def optimize_image(buffer: IO[bytes], ext: str, width: int, quality: int):
    print("Optimizing image...")
    with ExitStack() as stack:
        img = stack.enter_context(Image.open(buffer))
        if width < img.width:
            print("Resizing image...")
            new_height = int(width * img.height / img.width)

            print(width, new_height)

            img = stack.enter_context(img.resize((width, new_height)))
            print("Resized!")

        tmp = stack.enter_context(TemporaryFile())
        img.save(tmp, quality=quality, optimize=True, format=ext)
        tmp.seek(0)

        print("Optimized!")
        return tmp.read()


def handler(event, context):
    try:
        print("Starting...")

        qs = event['queryStringParameters']
        url = qs.get('url', None)
        width = int(qs.get('w', 0))
        quality = int(qs.get('q', 70))

        print(url, width, quality)

        if not url:
            return error('url is required')
        if width <= 0:
            return error('width must be greater than zero')

        with TemporaryFile() as buffer:
            if is_absolute(url):
                download_image(buffer, url)
            else:
                key = url.strip('/')
                get_s3_image(buffer, key)

            original = os.stat(buffer.name).st_size
            mime = get_extension(buffer)
            content_type = mime['content_type']
            extension = mime['extension']

            image_data = optimize_image(
                buffer,
                ext=extension,
                width=width,
                quality=quality
            )

        print("Returning data...")
        return success(image_data, {
            'Vary': 'Accept',
            'Content-Type': content_type,
            'X-Optimization-Ratio': f'{len(image_data) / original:.4f}',
        })
    except Exception as exc:
        return error(str(exc), code=500)


if __name__ == '__main__':
    print("Running test...")

    data = json.load(open('example/event-absolute-jfif.json'))
    handler(data, None)
