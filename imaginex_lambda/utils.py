import base64
import json
from typing import IO
from urllib.parse import urlparse

import filetype


class HandlerError(Exception):
    code: int

    def __init__(self, msg: str, code=422) -> None:
        super().__init__(msg)
        self.code = code


def success(image_data, headers):
    return {
        'statusCode': 200,
        'body': base64.b64encode(image_data).decode(),
        'isBase64Encoded': True,
        'headers': headers
    }


def error(msg: str, code=422):
    return {
        'statusCode': code,
        'body': json.dumps({'error': msg}),
        'headers': {
            'Vary': 'Accept',
            'Content-Type': 'application/json'
        }
    }


def is_absolute(url: str):
    return bool(urlparse(url).netloc)


def get_extension(buffer: IO[bytes]):
    print("Getting extension...")

    kind = filetype.guess(buffer)
    content_type = kind.mime
    extension = content_type.upper().replace('IMAGE/', '')

    print(f"Extension: {extension}")
    return {'content_type': content_type, 'extension': extension}
