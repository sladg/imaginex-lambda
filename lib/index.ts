import * as path from 'path'

export const optimizerCodePath = path.resolve(__dirname, './optimizer-layer.zip')
export const optimizerLayerArns = [
	'arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-p38-requests:8',
	'arn:aws:lambda:eu-central-1:770693421928:layer:Klayers-p38-Pillow:5',
]

export const handler = 'imaginex-lambda/handler.handler'
