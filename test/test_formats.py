import base64
from io import BytesIO
from tempfile import TemporaryFile
from unittest.mock import patch
from PIL import Image

from imaginex_lambda.handler import download_and_optimize, handler

import pytest
from unittest.mock import MagicMock


@pytest.mark.parametrize('img_type,expected_type', [
    ('PNG', 'image/png'),
    ('JPEG', 'image/jpeg'),
    ('JPEG2000', 'image/jpx'),
    ('ICO', 'image/x-icon'),
    ('MPO', 'image/jpeg'),
    ('WEBP', 'image/webp'),
    ('GIF', 'image/gif'),
    ('TIFF', 'image/tiff'),
    ('BMP', 'image/bmp'),
])
def test_download_and_optimize_formats(img_type, expected_type):
    # arrange
    original_w, original_h, new_q, new_w = 300, 300, 80, 256

    sample_url = "https://example.com"
    img = Image.new('RGB', (original_w, original_h), color=(255, 0, 0))
    tmp_img = TemporaryFile()
    img.save(tmp_img, format=img_type)
    download_image_mock = MagicMock(return_value=(tmp_img, {}))

    lambda_context = {
        'queryStringParameters':
            {
                'q': new_q, 'w': new_w, 'url': sample_url
            }
    }

    # act
    with patch('imaginex_lambda.lib.img_lib.download_image', download_image_mock):
        opt_img_bytes, content_type, ratio = download_and_optimize(sample_url, new_q, new_w, None, '')
        res = handler(lambda_context, None)
    tmp_img.close()

    # assert
    opt_img_res = Image.open(BytesIO(base64.b64decode(res['body'].encode())))
    assert content_type == expected_type
    assert opt_img_res.width == new_w

# List of possibly available formats in the future (supported only by PIL atm)
# ('DIB', 'image/dib'),        # HandlerError: Unsupported image format
# ('PPM', 'image/ppm'),        # HandlerError: Unsupported image format
# ('BUFR', 'image/BUFR'),      # HandlerError: Unsupported image format
# ('PCX', 'image/PCX'),        # HandlerError: Unsupported image format
# ('DDS', 'image/DDS'),        # HandlerError: Unsupported image format
# ('ICNS', 'image/ICNS'),      # HandlerError: Unsupported image format
# ('IM', 'image/IM'),          # HandlerError: Unsupported image format
# ('SGI', 'image/SGI'),        # HandlerError: Unsupported image format
# ('SPIDER', 'image/SPIDER'),  # HandlerError: Unsupported image format
# ('TGA', 'image/TGA'),        # HandlerError: Unsupported image format
# ('BLP', 'image/blp'),        # ValueError: Unsupported BLP image mode
# ('FITS', 'image/FITS'),      # OSError: FITS save handler not installed
# ('GRIB', 'image/GRIB'),      # OSError: GRIB save handler not installed
# ('HDF5', 'image/HDF5'),      # OSError: HDF5 save handler not installed
# ('WMF', 'image/WMF'),        # OSError: WMF save handler not installed
# ('MSP', 'image/MSP'),        # OSError: cannot write mode RGB as Palm
# ('PALM', 'image/PALM'),      # OSError: cannot write mode RGB as Palm
# ('XBM', 'image/XBM'),        # OSError: cannot write mode RGB as XBM
# ('PDF', 'image/PDF'),        # PIL.UnidentifiedImageError
# ('EPS', 'image/EPS'),        # Resize error
