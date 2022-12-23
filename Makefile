
commit:
	npx --package cz-emoji-conventional --package commitizen -- cz

release:
	npx --package @sladg/release-utils utils shipit --gitUser @sladg --gitEmail jan@ssoukup.com --changelog

install:
	poetry install && npm ci

package-dependencies:
	poetry build
	poetry run \
		pip install \
		--only-binary=:all: \
		--python=3.8 \
		--upgrade \
		--implementation cp \
		--platform manylinux2014_x86_64 \
		--target=./python \
		dist/*.whl

	zip -q -r ./build/dependencies-layer.zip ./python

package-code:
	zip -q -r ./build/code.zip ./imaginex-lambda/*

start:
	poetry run python ./imaginex-lambda/handler.py

# Pack the dependencies into a zip file and include code as separate zip file.
package:
	rm -rf build
	mkdir build
	$(MAKE) package-dependencies
	$(MAKE) package-code
	npm run build
