import json
from pathlib import Path

import pytest

from imaginex_lambda.handler import handler, S3_BUCKET_NAME

EXAMPLE_DIR = Path(__file__).parents[1] / 'example'


@pytest.mark.parametrize('ratio,type,filename', [
    ('0.0037', 'image/png', 'event-s3.json'),
    ('0.0110', 'image/jpeg', 'event-absolute-jfif.json'),
    ('0.2109', 'image/jpeg', 'event-absolute.json'),
])
def test_handler_success(ratio, type, filename):
    if filename.endswith('-s3.json') and S3_BUCKET_NAME is None:
        pytest.skip('specify a value for S3_BUCKET_NAME to run S3 tests')

    with (EXAMPLE_DIR / filename).open() as f:
        data = json.load(f)

    r = handler(data, None)
    assert r['statusCode'] == 200
    assert r['isBase64Encoded'] is True
    assert r['headers']['Content-Type'] == type
    assert r['headers']['X-Optimization-Ratio'] == ratio
