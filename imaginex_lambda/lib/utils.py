import base64
from typing import IO, Dict, Any
from urllib.parse import urlparse, unquote

import filetype
import logging

from PIL.Image import Image

from imaginex_lambda.lib.exceptions import HandlerError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def success(image_data: bytes, headers: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'statusCode': 200,
        'body': base64.b64encode(image_data).decode(),
        'isBase64Encoded': True,
        'headers': headers
    }

def is_absolute(url: str) -> bool:
    return bool(urlparse(url).netloc)

def is_s3(url: str) -> bool:
    return unquote(url).startswith('s3://')

def get_extension(buffer: IO[bytes]) -> Dict:
    """
    Determines the file extension and content type of an image file contained in the given buffer.

    Args:
        buffer (IO[bytes]): The buffer containing the image file.

    Returns:
        Dict[str, str]: A dictionary containing the content_type and extension of the image file.

    Raises:
        HandlerError: If the image format is not supported.
    """
    logger.info("Getting extension...")

    kind = filetype.guess(buffer)
    if kind is None:
        raise HandlerError('Unsupported image format')
    content_type = kind.mime
    extension = content_type.upper().replace('IMAGE/', '')
    if extension == 'JPX':
        extension = 'JPEG2000'
    elif extension == 'X-ICON':
        extension = 'ICO'
    logger.info(f"Extension: {extension}")
    return {'content_type': content_type, 'extension': extension}


def cast_to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def is_landscape(image: Image) -> bool:
    """
    Checks whether an image is landscape or portrait.

    Args:
        image (PIL.Image): The opened PIL Image object.

    Returns:
        bool: True if the image is landscape, False if it is portrait.
    """
    # Get the width and height of the image
    width, height = image.size

    # Compare the width and height to determine if the image is landscape or portrait
    if width > height:
        return True
    else:
        return False
