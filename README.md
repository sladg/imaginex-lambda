# Imaginex

Pre-compiled Pythong lambda based on Pillow.
Shares API with NextJS and is mainly meant as replacement of shitty build-in NextJS image optimizer.

However, can be plugged into any other project with straight forward API.

## Usage

- Import/download zips from this package,
- Use them as lambda's code,
- Allow lambda to access S3 bucket with images and set S3_BUCKET_NAME env variable,
- Call lambda via API Gateway with query params:
  - url (relative to bucket or absolute to anywhere)
  - w (width for resizing)
  - q (quality for optimizing)

Response is base64 encoded image.

Supports all formats supported by Pillow.
Faster and easily deployable than NextJS image optimizer.

---

Child directory of: http://github.com/sladg/nextjs-lambda
