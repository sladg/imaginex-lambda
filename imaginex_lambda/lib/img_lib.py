import os
import shutil
from contextlib import ExitStack
from io import BytesIO
from tempfile import TemporaryFile
from typing import IO, Tuple, Dict, Any, Optional
from urllib.request import urlopen

import botocore.session
from PIL import Image

from imaginex_lambda.lib.exceptions import HandlerError
from imaginex_lambda.lib.utils import is_absolute, get_extension, logger

# Pillow supported formats:
# BLP, BMP, DDS, DIB, EPS, GIF, ICNS, ICO, IM, JPG, JPEG, MSP, PCX, PNG, PPM, SPIDER, TGA, TIFF, WEBP, XBM

session = botocore.session.get_session()
s3_client = session.create_client('s3')


# @TODO: Add placeholder image for errors.

def download_image(buffer: IO[bytes], img_url: str, chunk_size: int = 1024) -> Tuple[IO[bytes], Dict[str, Any]]:
    """
    Function responsible for downloading an image file from a given URL and writing its contents to a buffer.
    It takes two arguments, buffer and img_url, and returns a dictionary containing information about the downloaded
    image.

    Args:
        buffer: (IO[bytes]) A file-like object that the downloaded image will be written to.
        img_url: (str) A string representing the URL of the image to be downloaded.
    Returns:
        Tuple[IO[bytes], Dict[str, Any]]: dictionary containing information about the downloaded image
    """
    logger.info("Downloading image from %s", img_url)

    with urlopen(img_url) as r:
        content_type = r.headers['content-type']
        content_size = int(r.headers['content-length'])

        shutil.copyfileobj(r, buffer, chunk_size)

    logger.info("Downloaded image from %s. Content type: %s, content size: %d", img_url, content_type, content_size)
    return buffer, {'content_type': content_type, 'content_size': content_size}


def get_s3_image(buffer: IO[bytes], bucket_name: str, key: str, chunk_size: int = 1024) \
        -> Tuple[IO[bytes], Dict[str, Any]]:
    """
    Function responsible for downloading an image file from an Amazon S3 bucket and writing its contents to a buffer.
    It takes two arguments, buffer and key, and returns a dictionary containing information about the downloaded image.

    Args:
        buffer (IO[bytes]): The buffer to write the downloaded image contents to.
        bucket_name (str): The name of the S3 bucket to download the image from.
        key (str): The key of the S3 object to download.
        chunk_size (int): The chunk size to use when downloading the image.

    Returns:
        Tuple[IO[bytes], Dict[str, Any]]: A tuple containing the buffer with the downloaded image contents and a dictionary
        with information about the downloaded image (content_type and content_size).

    Raises:
        Exception: If `bucket_name` is not specified.
    """

    if not bucket_name:
        raise Exception('must specify a value for S3_BUCKET_NAME for S3 support')

    logger.info("Downloading image from S3 with key: %s", key)
    r = s3_client.get_object(Bucket=bucket_name, Key=key)

    content_type = r['ContentType']
    content_size = r['ContentLength']

    with r['Body'] as fin:
        shutil.copyfileobj(fin, buffer, chunk_size)

    logger.info("Downloaded image from S3 with key: %s. Content type: %s, content size: %d", key, content_type,
                content_size)
    return buffer, {'content_type': content_type, 'content_size': content_size}


def optimize_image(buffer: IO[bytes],
                   ext: str,
                   quality: int,
                   width: Optional[int] = None,
                   height: Optional[int] = None) -> bytes:
    """
    The optimize_image function is designed to optimize an image that is passed in. It resizes the image
    to the given width (if necessary), compresses the image to reduce its size, and returns the optimized image data.

    Args:
        buffer (IO[bytes]): buffer containing the image data to be optimized.
        ext (str): the file extension of the image, which is used to specify the format when saving the optimized image.
        quality (int): the quality of the compressed image. A higher quality will result in a larger file size, while a lower quality
            will result in a smaller file size.
        width (Optional[int]): the maximum width of the image. If the image is wider than this value, it will be resized to fit within
            this width.
        height (Optional[int]): the maximum height of the image. If the image is wider than this value, it will be resized to fit within
            this height.
    Returns:
        bytes: Optimized image data
    """

    logger.info("Optimizing image...")

    with ExitStack() as stack:
        img = stack.enter_context(Image.open(buffer))
        if width and width < img.width:
            logger.info(f"Resizing image given width {width}px...")
            new_height = int(width * img.height / img.width)
            logger.info("New height: %d", new_height)
            img = stack.enter_context(img.resize((width, new_height)))
            logger.info("Resized image to width: %d and height: %d", width, new_height)
        elif height and height < img.height:
            logger.info(f"Resizing image to the given {height}px...")
            new_width = int(height * img.width / img.height)
            logger.info("New width: %d", new_width)
            img = stack.enter_context(img.resize((new_width, height)))
            logger.info("Resized image to width: %d and height: %d", height, new_width)
        tmp = stack.enter_context(BytesIO())
        img.save(tmp, quality=quality, optimize=True, format=ext)
        tmp.seek(0)

        logger.info("Optimized image!")
        return tmp.read()


def download_and_optimize(url: str,
                          quality: int,
                          width: Optional[int],
                          height: Optional[int],
                          bucket_name: str,
                          chunk_size: int = 1024) -> Tuple[bytes, str, float]:
    """
    This is the function responsible for coordinating the download and optimization of the images. It should
    not concern itself with any lambda-specific information.

    Args:
        url (str): The URL of the image to download.
        quality (int): The quality to optimize the image (0 to 100).
        width (Optional[int]): The width of the image to resize to.
        height (Optional[int]): The height of the image to resize to.
        bucket_name (str): The name of the S3 bucket to download the image from.
        chunk_size (int): The chunk size to use when downloading the image.

    Returns:
        Tuple[bytes, str, float]: A tuple containing the optimized image data, content type, and the compression ratio.

    Raises:
        HandlerError: If `url` is empty, `width` and `height` are both empty or both provided, or if `width`
        or `height` are less than or equal to zero.

    """

    if not url:
        raise HandlerError('url is required')

    if width is None and height is None:
        raise HandlerError('Width or height must be defined')

    if width is not None and height is not None:
        raise HandlerError('Only one of width or height params must be defined')

    if width is not None and width <= 0:
        raise HandlerError('width must be greater than zero')

    if height is not None and height <= 0:
        raise HandlerError('height must be greater than zero')

    with TemporaryFile() as buffer:
        if is_absolute(url):
            buffer, _ = download_image(buffer, url, chunk_size)
        else:
            key = url.strip('/')
            buffer, _ = get_s3_image(buffer, bucket_name, key, chunk_size)

        buffer.flush()
        original = os.stat(buffer.name).st_size
        mime = get_extension(buffer)
        content_type = mime['content_type']
        extension = mime['extension']

        image_data = optimize_image(
            buffer,
            ext=extension,
            quality=quality,
            width=width,
            height=height
        )

    ratio = len(image_data) / original if original != 0 else 0

    logger.info("Returning image and metadata")
    return image_data, content_type, ratio
