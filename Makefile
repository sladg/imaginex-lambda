
commit:
	npx --package cz-emoji-conventional --package commitizen -- cz

release:
	npx --package @sladg/nextjs-lambda next-utils shipit --gitUser @sladg --gitEmail jan@ssoukup.com --changelog

install:
	poetry install

start:
	poetry run python ./imaginex-lambda/handler.py

zip-code:
	zip -q -r ./build/optimizer-code.zip ./imaginex-lambda/*

# Pack the dependencies into a zip file and include code as separate zip file.
package:
	rm -rf build
	mkdir build
	$(MAKE) zip-code
	npm run build
