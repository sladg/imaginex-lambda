from io import BytesIO
from tempfile import TemporaryFile
from unittest.mock import patch
from PIL import Image

from imaginex_lambda.handler import download_and_optimize

import pytest
from unittest.mock import MagicMock


@pytest.mark.parametrize('img_type,expected_type', [
    ('PNG', 'image/png'),
    ('JPEG', 'image/jpeg'),
    # ('PPM', 'image/ppm'),
    ('GIF', 'image/gif'),
    ('TIFF', 'image/tiff'),
    ('BMP', 'image/bmp'),
])
def test_download_and_optimize_formats(img_type, expected_type):
    # arrange
    original_w, original_h, new_q, new_w = 300, 300, 80, 200

    sample_url = "https://example.com"
    img = Image.new('RGB', (original_w, original_h), color=(255, 0, 0))
    tmp_img = TemporaryFile()
    img.save(tmp_img, format=img_type)
    download_image_mock = MagicMock(return_value=(tmp_img, {}))

    # act
    with patch('imaginex_lambda.handler.download_image', download_image_mock):
        opt_img_bytes, content_type, ratio = download_and_optimize(sample_url, new_q, new_w)
    tmp_img.close()

    # assert
    opt_img = Image.open(BytesIO(opt_img_bytes))
    assert content_type == expected_type
    assert opt_img.width == new_w
