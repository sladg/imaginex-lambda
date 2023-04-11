import logging
import os
import shutil
from contextlib import ExitStack
from tempfile import TemporaryFile
from typing import IO, Tuple, Dict, Any
from urllib.request import urlopen
from io import BytesIO

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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def download_image(buffer: IO[bytes], img_url: str) -> Tuple[IO[bytes], Dict[str, Any]]:
    """
    Function responsible for downloading an image file from a given URL and writing its contents to a buffer.
    It takes two arguments, buffer and img_url, and returns a dictionary containing information about the downloaded
    image.

    buffer: IO[bytes]
        A file-like object that the downloaded image will be written to.
    img_url: str
        A string representing the URL of the image to be downloaded.
    """
    logger.info("Downloading image from %s", img_url)

    with urlopen(img_url) as r:
        content_type = r.headers['content-type']
        content_size = int(r.headers['content-length'])

        shutil.copyfileobj(r, buffer, DOWNLOAD_CHUNK_SIZE)

    logger.info("Downloaded image from %s. Content type: %s, content size: %d", img_url, content_type, content_size)
    return buffer, {'content_type': content_type, 'content_size': content_size}


def get_s3_image(buffer: IO[bytes], key: str) -> Tuple[IO[bytes], Dict[str, Any]]:
    """
    Function responsible for downloading an image file from an Amazon S3 bucket and writing its contents to a buffer.
    It takes two arguments, buffer and key, and returns a dictionary containing information about the downloaded image.
    """
    if not S3_BUCKET_NAME:
        raise Exception('must specify a value for S3_BUCKET_NAME for S3 support')

    logger.info("Downloading image from S3 with key: %s", key)
    r = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=key)

    content_type = r['ContentType']
    content_size = r['ContentLength']

    with r['Body'] as fin:
        shutil.copyfileobj(fin, buffer, DOWNLOAD_CHUNK_SIZE)

    logger.info("Downloaded image from S3 with key: %s. Content type: %s, content size: %d", key, content_type,
                content_size)
    return buffer, {'content_type': content_type, 'content_size': content_size}


def optimize_image(buffer: IO[bytes], ext: str, width: int, quality: int) -> bytes:
    """
    The optimize_image function is designed to optimize an image that is passed in. It resizes the image
    to the given width (if necessary), compresses the image to reduce its size, and returns the optimized image data.

    buffer: IO[bytes]
        buffer containing the image data to be optimized.
    ext: str
        the file extension of the image, which is used to specify the format when saving the optimized image.
    width: int
        the maximum width of the image. If the image is wider than this value, it will be resized to fit within
        this width.
    quality: int
        the quality of the compressed image. A higher quality will result in a larger file size, while a lower quality
        will result in a smaller file size.
    """
    logger.info("Optimizing image...")
    with ExitStack() as stack:
        img = stack.enter_context(Image.open(buffer))
        if width < img.width:
            logger.info("Resizing image...")
            new_height = int(width * img.height / img.width)
            logger.info("New height: %d", new_height)
            img = stack.enter_context(img.resize((width, new_height)))
            logger.info("Resized image to width: %d and height: %d", width, new_height)
        tmp = stack.enter_context(BytesIO())
        img.save(tmp, quality=quality, optimize=True, format=ext)
        tmp.seek(0)

        logger.info("Optimized image!")
        return tmp.read()


def handler(event, context):
    """
    Lambda function handler.

    Its sole responsibility is to to parse the context and generate a formatted response, including error responses.
    Any image processing logic should be performed by other functions, to make unit testing easier.
    """
    try:
        logger.info("Lambda function started")

        qs = event['queryStringParameters']
        url = qs.get('url', None)
        width = int(qs.get('w', 0))
        quality = int(qs.get('q', 70))

        logger.info(f"url={url}, width={width}, quality={quality}")

        image_data, content_type, optimization_ratio = download_and_optimize(url, quality, width)
        logger.info("Returning success response")
        return success(image_data, {
            'Vary': 'Accept',
            'Content-Type': content_type,
            'X-Optimization-Ratio': f'{optimization_ratio:.4f}',
        })
    except HandlerError as exc:
        return error(str(exc), code=exc.code)
    except Exception as exc:
        return error(str(exc), code=500)


def download_and_optimize(url: str, quality: int, width: int) -> Tuple[bytes, str, float]:
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
            buffer, _ = download_image(buffer, url)
        else:
            key = url.strip('/')
            buffer, _ = get_s3_image(buffer, key)

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

    logger.info("Returning image and metadata")
    return image_data, content_type, ratio


if __name__ == '__main__':
    from io import BytesIO
    import base64

    print("Running test...")
    context = {'queryStringParameters':
                   {'q': '40', 'w': '250',
                    'url': 'https://s3.eu-central-1.amazonaws.com/fllite-dev-main/'
                           'business_case_custom_images/sun_valley_2_5f84953fef8c6_63a2668275433.jfif'}}
    res = handler(context, None)
    img = res['body']
    Image.open(BytesIO(base64.b64decode(img.encode()))).show()
    print('end')
