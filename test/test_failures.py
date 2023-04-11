from unittest.mock import patch

import pytest

from imaginex_lambda.handler import handler, download_and_optimize
from imaginex_lambda.lib.utils import HandlerError


def test_no_url():
    r = handler({'queryStringParameters': {}}, None)
    assert r['statusCode'] == 422
    assert r['headers']['Content-Type'] == 'application/json'
    assert "url is required" in r['body']


@pytest.mark.parametrize('width', [None, -1, -100, 0])
def test_invalid_width(width):
    r = handler({'queryStringParameters': {'url': 'abc.png', 'width': width}}, None)
    assert r['statusCode'] == 422
    assert r['headers']['Content-Type'] == 'application/json'
    assert "width must be greater than zero" in r['body']


def test_s3_not_configured():
    with patch('imaginex_lambda.handler.S3_BUCKET_NAME', None):
        r = handler({'queryStringParameters': {'url': 'abc.png', 'w': 50}}, None)
        assert r['statusCode'] == 500
        assert r['headers']['Content-Type'] == 'application/json'
        assert "must specify a value for S3_BUCKET_NAME" in r['body']


def test_s3_invalid_bucket():
    with patch('imaginex_lambda.handler.S3_BUCKET_NAME', 'i'):
        r = handler({'queryStringParameters': {'url': 'abc.png', 'w': 50}}, None)
        assert r['statusCode'] == 500
        assert r['headers']['Content-Type'] == 'application/json'
        assert "InvalidBucketName" in r['body']


def test_download_and_optimize_with_invalid_url():
    # arrange
    url = ''
    quality = 50
    width = 100

    # act and assert
    with pytest.raises(HandlerError):
        download_and_optimize(url, quality, width)


def test_download_and_optimize_with_zero_width():
    # arrange
    url = 'https://example.com/image.png'
    quality = 50
    width = 0

    # act and assert
    with pytest.raises(HandlerError):
        download_and_optimize(url, quality, width)
