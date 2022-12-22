## Formats

png
svg
jpg
jpeg
gif
webp
avif
ico
bmp

squoosh

wasm format (browser friendly, web-assembly).
Possibly use with Go?

## Actions

resize
rotate

etag output images (for caching?)

const ANIMATABLE_TYPES = [
WEBP,
PNG,
GIF
];
const VECTOR_TYPES = [
SVG
];

fallback to upstream image.

url params:

- url
- w
- q

/Users/jan.soukup/code/nextjs-lambda/node_modules/next/dist/server/next-server.js
return imageOptimizer(req.originalRequest, res.originalResponse, paramsResult, this.nextConfig, this.renderOpts.dev, (newReq, newRes, newParsedUrl)=>this.getRequestHandler()(new \_node.NodeNextRequest(newReq), new \_node.NodeNextResponse(newRes), newParsedUrl));

const { isAbsolute , href , width , mimeType , quality } = paramsResult;

## Compiling

GOOS=linux GOARCH=amd64 go build -o main main.go
zip main.zip main

Upload main.zip to Lambda as a function's code.

Use tinypng-go?
https://www.npmjs.com/package/tinypng-go

Use Python and PIL? Pillow.
