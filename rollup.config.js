import pkg from './package.json'
import { defineConfig } from 'rollup'
import typescript from 'rollup-plugin-typescript2'

export default defineConfig([
	{
		input: 'lib/index.ts',
		plugins: [typescript({ useTsconfigDeclarationDir: true })],
		output: {
			format: 'commonjs',
			file: pkg.exports,
		},
	},
])
