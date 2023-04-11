import os
from typing import Dict, Optional

from PIL import Image

from imaginex_lambda.lib.exceptions import HandlerError, error
from imaginex_lambda.lib.img_lib import download_and_optimize
from imaginex_lambda.lib.utils import success, logger

# @TODO: Add placeholder image for errors.

DOWNLOAD_CHUNK_SIZE = int(os.getenv('DOWNLOAD_CHUNK_SIZE', 1024))
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', None)


def handler(event: Dict, context: Optional[Dict]):
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

        image_data, content_type, optimization_ratio = download_and_optimize(url,
                                                                             quality,
                                                                             width,
                                                                             S3_BUCKET_NAME,
                                                                             DOWNLOAD_CHUNK_SIZE)
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


if __name__ == '__main__':
    from io import BytesIO
    import base64

    logger.info("Running test...")
    test_context = {
        'queryStringParameters':
            {
                'q': '40', 'w': '250',
                'url': 'https://s3.eu-central-1.amazonaws.com/fllite-dev-main/'
                       'business_case_custom_images/sun_valley_2_5f84953fef8c6_63a2668275433.jfif'}
    }
    res = handler(test_context, None)
    img = res['body']
    Image.open(BytesIO(base64.b64decode(img.encode()))).show()
    logger.info("Test ended...")
