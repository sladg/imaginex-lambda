from unittest.mock import patch

import pytest

from imaginex_lambda.handler import handler, S3_BUCKET_NAME


@pytest.mark.parametrize('ratio,type,qs', [
    ('0.0037', 'image/png',
     {"q": "80", "w": "100", "url": "example.png"}),
    ('0.0110', 'image/jpeg',
     {"q": "40", "w": "250", "url": "https://s3.eu-central-1.amazonaws.com/fllite-dev-main/business_case_custom_images"
                                    "/sun_valley_2_5f84953fef8c6_63a2668275433.jfif"}),
    ('0.2109', 'image/jpeg',
     {'q': "80", 'w': "100", 'url': "http://site.meishij.net/r/58/25/3568808/a3568808_142682562777944.jpg"}),
])
def test_handler_success(ratio, type, qs):
    if not qs['url'].startswith('http') and S3_BUCKET_NAME is None:
        pytest.skip('specify a value for S3_BUCKET_NAME to run S3 tests')

    r = handler({'queryStringParameters': qs}, None)
    assert r['statusCode'] == 200
    assert r['isBase64Encoded'] is True
    assert r['headers']['Content-Type'] == type
    assert r['headers']['X-Optimization-Ratio'] == ratio
