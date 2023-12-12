# Changelog


## [v0.18.1](https://github.com/sladg/imaginex-lambda/compare/v0.18.0...v0.18.1)

* 🐛 fix(s3): parse encoded http uri [[dd6596ad37d1f100c1ec1e2951701384452b67a6](https://github.com/sladg/imaginex-lambda/commit/dd6596ad37d1f100c1ec1e2951701384452b67a6))]


## [v0.18.0](https://github.com/sladg/imaginex-lambda/compare/v0.17.0...v0.18.0)

* ✨ feat(s3): allow for specifying bucketname withing the url [[8b8d57e18952c2c564203ba45538329845be2951](https://github.com/sladg/imaginex-lambda/commit/8b8d57e18952c2c564203ba45538329845be2951))]


## [v0.17.0](https://github.com/sladg/imaginex-lambda/compare/v0.7.0...v0.17.0)

* feat(img_lib): portrait vs landscape [[6a09c9472dc86578d8b08b3921f5749dc3ece9b4](https://github.com/sladg/imaginex-lambda/commit/6a09c9472dc86578d8b08b3921f5749dc3ece9b4))]
* fix(img_lib): logger fix [[7cc415318916767fafba6d5738453bbeae6d11c4](https://github.com/sladg/imaginex-lambda/commit/7cc415318916767fafba6d5738453bbeae6d11c4))]
* test(formats): moved list of not supported formats into fun [[7a2011c885c0323100470bfdaa3cb1e26d32dc9f](https://github.com/sladg/imaginex-lambda/commit/7a2011c885c0323100470bfdaa3cb1e26d32dc9f))]
* refactor(tests,libs): added tests, readme, docstrings [[073f9ff91ecf3f51ef9ad289fcb880dbaac1c6fd](https://github.com/sladg/imaginex-lambda/commit/073f9ff91ecf3f51ef9ad289fcb880dbaac1c6fd))]
* test(success): magicmock [[f5dc6b14e37615f8db397fd9091dfb1612cc95c0](https://github.com/sladg/imaginex-lambda/commit/f5dc6b14e37615f8db397fd9091dfb1612cc95c0))]
* test(success): height [[b5b8c96c76b11eeac5f91e643ddd18717e587d13](https://github.com/sladg/imaginex-lambda/commit/b5b8c96c76b11eeac5f91e643ddd18717e587d13))]
* test(tests): updated tests [[6453d0e294c7bfde91af8ed8f52444e477be2ab9](https://github.com/sladg/imaginex-lambda/commit/6453d0e294c7bfde91af8ed8f52444e477be2ab9))]
* fix(img_lib): missing import [[78d084d301d0b8763cb2c73ef317caf83564e133](https://github.com/sladg/imaginex-lambda/commit/78d084d301d0b8763cb2c73ef317caf83564e133))]
* refactor(utils): logger [[5c0bf36a33f7389c8f699d8e9f2822f14cb88239](https://github.com/sladg/imaginex-lambda/commit/5c0bf36a33f7389c8f699d8e9f2822f14cb88239))]
* refactor(utils): typings [[4ff2390ba37c029eae656526b4074900c69a76b8](https://github.com/sladg/imaginex-lambda/commit/4ff2390ba37c029eae656526b4074900c69a76b8))]
* fix(exceptions): missing import [[02d01d0189dc4a15746ff7ebdd803eed48d2a8c5](https://github.com/sladg/imaginex-lambda/commit/02d01d0189dc4a15746ff7ebdd803eed48d2a8c5))]
* refactor(lib): restructuring files structure [[1f71342ddd4414ddd99c1daeb3f6ff4635d272df](https://github.com/sladg/imaginex-lambda/commit/1f71342ddd4414ddd99c1daeb3f6ff4635d272df))]
* refactor(handler,-utests): updates, refactoring, testing [[87d9e0611f7b051808dc877b388936bfc80c93d8](https://github.com/sladg/imaginex-lambda/commit/87d9e0611f7b051808dc877b388936bfc80c93d8))]


## [v0.7.0](https://github.com/sladg/imaginex-lambda/compare/v0.5.0...v0.7.0)

* 🐛 fix(ratio): prevent future "division by zero" bugs on ratio calculation [[ef778bc8a147701265e162fc8d93089d9898ff1f](https://github.com/sladg/imaginex-lambda/commit/ef778bc8a147701265e162fc8d93089d9898ff1f))]
* 🐛 fix(ratio): handle very small image edge case [[563f886fe3a31a14e22c473b98b2bcd6d26c9759](https://github.com/sladg/imaginex-lambda/commit/563f886fe3a31a14e22c473b98b2bcd6d26c9759))]
* ♻️ refactor(handler): isolates the handler code from the image processing [[6731100aa4cb71acbb6aba48755717339987b80a](https://github.com/sladg/imaginex-lambda/commit/6731100aa4cb71acbb6aba48755717339987b80a))]
* 🧪 test(handler): replaces example JSON files for a programmatic approach [[36f2fe9659bd0781dc2be2284089b455addf41bf](https://github.com/sladg/imaginex-lambda/commit/36f2fe9659bd0781dc2be2284089b455addf41bf))]


## [v0.5.0](https://github.com/sladg/imaginex-lambda/compare/v0.2.6...v0.5.0)

* 📦 ci(tests): include test command before release, correct folder naming [[b609483a5bbcaaa00c97fae8843502970529456b](https://github.com/sladg/imaginex-lambda/commit/b609483a5bbcaaa00c97fae8843502970529456b))]
* 💎 style(pyproject): improved style, added easy command for tests [[c977063c26a9b641843e55e6984d59ebab0bc1b5](https://github.com/sladg/imaginex-lambda/commit/c977063c26a9b641843e55e6984d59ebab0bc1b5))]
* Merge pull request #1 from fabiob/optimizations [[e6236e4d2a99887d5477602c11fd59e99624c532](https://github.com/sladg/imaginex-lambda/commit/e6236e4d2a99887d5477602c11fd59e99624c532))]
* 📈 perf(handler): PEP8, memory usage, dependencies, tests [[c41d267efc584797fbaa37e24bef42bca3255728](https://github.com/sladg/imaginex-lambda/commit/c41d267efc584797fbaa37e24bef42bca3255728))]


## [v0.2.6](https://github.com/sladg/imaginex-lambda/compare/v0.2.4...v0.2.6)

* 🐛 fix(release): change package to correct one [[cd762f6b8a79e55f77b8520775602e10380f53b0](https://github.com/sladg/imaginex-lambda/commit/cd762f6b8a79e55f77b8520775602e10380f53b0))]
* 🐛 fix(exports): correctly export version and name of the package [[e7b74f14d158ab7c00cc930c09e8770b903aa81d](https://github.com/sladg/imaginex-lambda/commit/e7b74f14d158ab7c00cc930c09e8770b903aa81d))]


## [v0.2.4](https://github.com/sladg/imaginex-lambda/compare/v0.2.3...v0.2.4)

* fix(output): correct naming of zips [[c60f6e7b05eb4c37a9823181766564a495051d6a](https://github.com/sladg/imaginex-lambda/commit/c60f6e7b05eb4c37a9823181766564a495051d6a))]


## [v0.2.3](https://github.com/sladg/imaginex-lambda/compare/v0.2.2...v0.2.3)

* fix(binaries): correctly compile libraries so they are compatible with lambda env [[88250e70ce20582cdb37f97a5f7780718c4ad456](https://github.com/sladg/imaginex-lambda/commit/88250e70ce20582cdb37f97a5f7780718c4ad456))]


## [v0.2.2](https://github.com/sladg/imaginex-lambda/compare/v0.2.1...v0.2.2)

* fix(pillow): rely on external layers instead of bundling ourselves [[9c8cf49190c1272dd52e558b798f537eb7c8cd8f](https://github.com/sladg/imaginex-lambda/commit/9c8cf49190c1272dd52e558b798f537eb7c8cd8f))]


## [v0.2.1](https://github.com/sladg/imaginex-lambda/compare/v0.2.0...v0.2.1)

* fix(publishing): correctly set folders and outputs [[5c511e5a5b0bf0c73143bd10d2210a78c7719450](https://github.com/sladg/imaginex-lambda/commit/5c511e5a5b0bf0c73143bd10d2210a78c7719450))]


## [v0.2.0](https://github.com/sladg/imaginex-lambda/compare/v0.1.0...v0.2.0)

* ref(packages): removed unused packages [[9c90a782db4ada2b4b9feb14aff304218cb4c2f6](https://github.com/sladg/imaginex-lambda/commit/9c90a782db4ada2b4b9feb14aff304218cb4c2f6))]


## [v0.1.0](https://github.com/sladg/imaginex-lambda/compare/v0.0.1...v0.1.0)

* ci(workflow): draft of workflow and pipelines [[f70454f2efe5419bf33c6cc41ed80e53d5813a2a](https://github.com/sladg/imaginex-lambda/commit/f70454f2efe5419bf33c6cc41ed80e53d5813a2a))]


## [v0.0.1](https://github.com/sladg/imaginex-lambda/compare/v0.0.1)

* 🐛 fix(s3): parse encoded http uri [[dd6596ad37d1f100c1ec1e2951701384452b67a6](https://github.com/sladg/imaginex-lambda/commit/dd6596ad37d1f100c1ec1e2951701384452b67a6))]
* ✨ feat(s3): allow for specifying bucketname withing the url [[8b8d57e18952c2c564203ba45538329845be2951](https://github.com/sladg/imaginex-lambda/commit/8b8d57e18952c2c564203ba45538329845be2951))]
* feat(img_lib): portrait vs landscape [[6a09c9472dc86578d8b08b3921f5749dc3ece9b4](https://github.com/sladg/imaginex-lambda/commit/6a09c9472dc86578d8b08b3921f5749dc3ece9b4))]
* fix(img_lib): logger fix [[7cc415318916767fafba6d5738453bbeae6d11c4](https://github.com/sladg/imaginex-lambda/commit/7cc415318916767fafba6d5738453bbeae6d11c4))]
* test(formats): moved list of not supported formats into fun [[7a2011c885c0323100470bfdaa3cb1e26d32dc9f](https://github.com/sladg/imaginex-lambda/commit/7a2011c885c0323100470bfdaa3cb1e26d32dc9f))]
* refactor(tests,libs): added tests, readme, docstrings [[073f9ff91ecf3f51ef9ad289fcb880dbaac1c6fd](https://github.com/sladg/imaginex-lambda/commit/073f9ff91ecf3f51ef9ad289fcb880dbaac1c6fd))]
* test(success): magicmock [[f5dc6b14e37615f8db397fd9091dfb1612cc95c0](https://github.com/sladg/imaginex-lambda/commit/f5dc6b14e37615f8db397fd9091dfb1612cc95c0))]
* test(success): height [[b5b8c96c76b11eeac5f91e643ddd18717e587d13](https://github.com/sladg/imaginex-lambda/commit/b5b8c96c76b11eeac5f91e643ddd18717e587d13))]
* test(tests): updated tests [[6453d0e294c7bfde91af8ed8f52444e477be2ab9](https://github.com/sladg/imaginex-lambda/commit/6453d0e294c7bfde91af8ed8f52444e477be2ab9))]
* fix(img_lib): missing import [[78d084d301d0b8763cb2c73ef317caf83564e133](https://github.com/sladg/imaginex-lambda/commit/78d084d301d0b8763cb2c73ef317caf83564e133))]
* refactor(utils): logger [[5c0bf36a33f7389c8f699d8e9f2822f14cb88239](https://github.com/sladg/imaginex-lambda/commit/5c0bf36a33f7389c8f699d8e9f2822f14cb88239))]
* refactor(utils): typings [[4ff2390ba37c029eae656526b4074900c69a76b8](https://github.com/sladg/imaginex-lambda/commit/4ff2390ba37c029eae656526b4074900c69a76b8))]
* fix(exceptions): missing import [[02d01d0189dc4a15746ff7ebdd803eed48d2a8c5](https://github.com/sladg/imaginex-lambda/commit/02d01d0189dc4a15746ff7ebdd803eed48d2a8c5))]
* refactor(lib): restructuring files structure [[1f71342ddd4414ddd99c1daeb3f6ff4635d272df](https://github.com/sladg/imaginex-lambda/commit/1f71342ddd4414ddd99c1daeb3f6ff4635d272df))]
* refactor(handler,-utests): updates, refactoring, testing [[87d9e0611f7b051808dc877b388936bfc80c93d8](https://github.com/sladg/imaginex-lambda/commit/87d9e0611f7b051808dc877b388936bfc80c93d8))]
* 🐛 fix(ratio): prevent future "division by zero" bugs on ratio calculation [[ef778bc8a147701265e162fc8d93089d9898ff1f](https://github.com/sladg/imaginex-lambda/commit/ef778bc8a147701265e162fc8d93089d9898ff1f))]
* 🐛 fix(ratio): handle very small image edge case [[563f886fe3a31a14e22c473b98b2bcd6d26c9759](https://github.com/sladg/imaginex-lambda/commit/563f886fe3a31a14e22c473b98b2bcd6d26c9759))]
* ♻️ refactor(handler): isolates the handler code from the image processing [[6731100aa4cb71acbb6aba48755717339987b80a](https://github.com/sladg/imaginex-lambda/commit/6731100aa4cb71acbb6aba48755717339987b80a))]
* 🧪 test(handler): replaces example JSON files for a programmatic approach [[36f2fe9659bd0781dc2be2284089b455addf41bf](https://github.com/sladg/imaginex-lambda/commit/36f2fe9659bd0781dc2be2284089b455addf41bf))]
* 📦 ci(tests): include test command before release, correct folder naming [[b609483a5bbcaaa00c97fae8843502970529456b](https://github.com/sladg/imaginex-lambda/commit/b609483a5bbcaaa00c97fae8843502970529456b))]
* 💎 style(pyproject): improved style, added easy command for tests [[c977063c26a9b641843e55e6984d59ebab0bc1b5](https://github.com/sladg/imaginex-lambda/commit/c977063c26a9b641843e55e6984d59ebab0bc1b5))]
* Merge pull request #1 from fabiob/optimizations [[e6236e4d2a99887d5477602c11fd59e99624c532](https://github.com/sladg/imaginex-lambda/commit/e6236e4d2a99887d5477602c11fd59e99624c532))]
* 📈 perf(handler): PEP8, memory usage, dependencies, tests [[c41d267efc584797fbaa37e24bef42bca3255728](https://github.com/sladg/imaginex-lambda/commit/c41d267efc584797fbaa37e24bef42bca3255728))]
* 🐛 fix(release): change package to correct one [[cd762f6b8a79e55f77b8520775602e10380f53b0](https://github.com/sladg/imaginex-lambda/commit/cd762f6b8a79e55f77b8520775602e10380f53b0))]
* 🐛 fix(exports): correctly export version and name of the package [[e7b74f14d158ab7c00cc930c09e8770b903aa81d](https://github.com/sladg/imaginex-lambda/commit/e7b74f14d158ab7c00cc930c09e8770b903aa81d))]
* fix(output): correct naming of zips [[c60f6e7b05eb4c37a9823181766564a495051d6a](https://github.com/sladg/imaginex-lambda/commit/c60f6e7b05eb4c37a9823181766564a495051d6a))]
* fix(binaries): correctly compile libraries so they are compatible with lambda env [[88250e70ce20582cdb37f97a5f7780718c4ad456](https://github.com/sladg/imaginex-lambda/commit/88250e70ce20582cdb37f97a5f7780718c4ad456))]
* fix(pillow): rely on external layers instead of bundling ourselves [[9c8cf49190c1272dd52e558b798f537eb7c8cd8f](https://github.com/sladg/imaginex-lambda/commit/9c8cf49190c1272dd52e558b798f537eb7c8cd8f))]
* fix(publishing): correctly set folders and outputs [[5c511e5a5b0bf0c73143bd10d2210a78c7719450](https://github.com/sladg/imaginex-lambda/commit/5c511e5a5b0bf0c73143bd10d2210a78c7719450))]
* ref(packages): removed unused packages [[9c90a782db4ada2b4b9feb14aff304218cb4c2f6](https://github.com/sladg/imaginex-lambda/commit/9c90a782db4ada2b4b9feb14aff304218cb4c2f6))]
* ci(workflow): draft of workflow and pipelines [[f70454f2efe5419bf33c6cc41ed80e53d5813a2a](https://github.com/sladg/imaginex-lambda/commit/f70454f2efe5419bf33c6cc41ed80e53d5813a2a))]