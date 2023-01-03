import path from 'path'

export const optimizerCodePath = path.resolve(__dirname, './code.zip')
export const optimizerLayerPath = path.resolve(__dirname, './dependencies-layer.zip')

export const handler = 'imaginex_lambda/handler.handler'

export { version, name } from '../package.json'
