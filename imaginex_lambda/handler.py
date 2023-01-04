import os
import shutil
from contextlib import ExitStack
from tempfile import TemporaryFile
from typing import IO
from urllib.request import urlopen

import botocore.session
from PIL import Image

from imaginex_lambda.utils import error, success, is_absolute, get_extension, HandlerError

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
    """
    Lambda function handler.

    Its sole responsibility is to to parse the context and generate a formatted response, including error responses.
    Any image processing logic should be performed by other functions, to make unit testing easier.
    """
    try:
        print("Starting...")

        qs = event['queryStringParameters']
        url = qs.get('url', None)
        width = int(qs.get('w', 0))
        quality = int(qs.get('q', 70))

        print(url, width, quality)

        image_data, content_type, optimization_ratio = download_and_optimize(url, quality, width)

        return success(image_data, {
            'Vary': 'Accept',
            'Content-Type': content_type,
            'X-Optimization-Ratio': f'{optimization_ratio:.4f}',
        })
    except HandlerError as exc:
        return error(str(exc), code=exc.code)
    except Exception as exc:
        return error(str(exc), code=500)


def download_and_optimize(url: str, quality: int, width: int):
    """
    This is the function responsible for coordinating the download and optimization of the images. It should
    not concern itself with any lambda-specific information.
    """

    if not url:
        raise HandlerError('url is required')
    if width <= 0:
        raise HandlerError('width must be greater than zero')

    with TemporaryFile() as buffer:
        if is_absolute(url):
            download_image(buffer, url)
        else:
            key = url.strip('/')
            get_s3_image(buffer, key)

        buffer.flush()
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

    ratio = len(image_data) / original if original != 0 else 0

    print("Returning data...")
    return image_data, content_type, ratio


if __name__ == '__main__':
    print("Running test...")

    context = {'queryStringParameters':
               {'q': '40', 'w': '250',
                'url': 'https://s3.eu-central-1.amazonaws.com/fllite-dev-main/'
                       'business_case_custom_images/sun_valley_2_5f84953fef8c6_63a2668275433.jfif'}}
    handler(context, None)
