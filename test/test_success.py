from unittest.mock import patch

import pytest

from imaginex_lambda.handler import handler, S3_BUCKET_NAME, download_and_optimize
from unittest.mock import MagicMock


def test_handler_success():
    """
    This test will mock the result of the 'download_and_optimize' function
    to return a fixed value. This way we can check if the handler single responsibility
    (to parse the context and generate a formatted response) is working correctly.

    Specific image processing tests should call 'download_and_optimize' directly,
    so it is easier to check for exceptions and edge cases.
    """

    context = {'queryStringParameters': {'url': 'abc.png', 'q': '50', 'w': '100'}}
    fake_optimization_return = MagicMock(return_value=((b'abcdef', 'application/someimage', 0.3)))

    with patch('imaginex_lambda.handler.download_and_optimize', fake_optimization_return) as p:
        r = handler(context, None)

    assert r['statusCode'] == 200
    assert r['isBase64Encoded'] is True
    assert r['headers']['Content-Type'] == 'application/someimage'
    assert r['headers']['X-Optimization-Ratio'] == '0.3000'


@pytest.mark.parametrize('expected_ratio,expected_type,q,w,url', [
    (0.0037, 'image/png', 80, 100, "example.png"),
    (0.0109, 'image/jpeg', 40, 250, "https://s3.eu-central-1.amazonaws.com/fllite-dev-main/"
                                    "business_case_custom_images/sun_valley_2_5f84953fef8c6_63a2668275433.jfif"),
    (0.1770, 'image/jpeg', 80, 100, "http://site.meishij.net/r/58/25/3568808/a3568808_142682562777944.jpg"),
    (0.6733, 'image/jpeg', 80, 100, "https://www.gravatar.com/avatar/617bdc1719f77448a4f96eb92e1ac02b?s=80&d=mp"),
])
def test_process_success(expected_ratio, expected_type, q, w, url):
    if not url.startswith('http') and S3_BUCKET_NAME is None:
        pytest.skip('specify a value for S3_BUCKET_NAME to run S3 tests')

    image_data, content_type, ratio = download_and_optimize(url=url, quality=q, width=w, height=None, bucket_name='')
    assert isinstance(image_data, bytes)
    assert content_type == expected_type
    assert round(ratio, 4) == expected_ratio


@pytest.mark.parametrize('w,h,q', [
    (None, 100, 80),
    (80, None, 80),
    (None, 200, 60),
    (200, None, 60),
])
@pytest.mark.parametrize('expected_type,url', [
    ('image/jpeg', "https://s3.eu-central-1.amazonaws.com/fllite-dev-main/"
                   "business_case_custom_images/sun_valley_2_5f84953fef8c6_63a2668275433.jfif"),
    ('image/jpeg', "https://www.gravatar.com/avatar/617bdc1719f77448a4f96eb92e1ac02b?s=80&d=mp"),
])
def test_process_success(expected_type, url, w, h, q):
    if not url.startswith('http') and S3_BUCKET_NAME is None:
        pytest.skip('specify a value for S3_BUCKET_NAME to run S3 tests')
    image_data, content_type, ratio = download_and_optimize(url=url, quality=q, width=w, height=h, bucket_name='')
    assert isinstance(image_data, bytes)
    assert content_type == expected_type
