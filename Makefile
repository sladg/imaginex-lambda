
commit:
	npx --package cz-emoji-conventional --package commitizen -- cz

release:
	npx --package @sladg/nextjs-lambda next-utils shipit --gitUser @sladg --gitEmail jan@ssoukup.com --changelog

install:
	poetry install

start:
	poetry run python ./imaginex-lambda/handler.py

zip-deps:
	poetry build
	poetry run \
		pip install \
		--only-binary=:all: \
		--python 3.8 \
		--implementation cp \
		--platform manylinux2014_aarch64 \
		--target=./python/lib/python3.8/site-packages \
		--upgrade \
		dist/*.whl
	zip -q -r ./build/optimizer-layer.zip ./python

zip-code:
	zip -q -x "python/*" -x "dist/*" -x ".git*/*" -q -r ./build/optimizer-code.zip .

# Pack the dependencies into a zip file and include code as separate zip file.
package:
	rm -rf build dist python
	mkdir build dist python
	$(MAKE) zip-deps
	$(MAKE) zip-code
	npm run build
	rm -rf dist python
