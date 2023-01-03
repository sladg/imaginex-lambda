from unittest.mock import patch

import pytest

from imaginex_lambda.handler import handler


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
