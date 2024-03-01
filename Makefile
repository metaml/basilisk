.DEFAULT_GOAL = help

export SHELL := $(shell type --path bash)
export PYTHONPATH := $(shell pwd)/dist3:$(shell pwd)/src:${PYTHONPATH}
ifeq ($(shell uname -s),Darwin)
export LD = /usr/bin/clang
endif

# default settings: https://hanspeterschaub.info/basilisk/Install/installBuild.html
build: ## build basilisk
	python3 conanfile.py --clean #--opNav True

test: test-dist3 test-src ## test all

test-dist3: ## test dist3
	cd dist3 && ctest --build-config=Release

# pytest worker segfault
test-src: ## test src
	cd src && pytest --verbosity=1 --numprocesses=0

clean: ## clean
	find . -name \*~ | xargs rm -f

clobber: clean ## clobber
	rm -rf dist3
	rm -rf ~/.conan

deps: install-xcode install-conan ## install deps (run this first)

install-xcode: ## install xcode developer tools
	-@sudo xcode-select --install

install-conan: ## install conan
	pip3 install wheel 'conan<2.0'

nix-build: ## nix build
	nix build --impure --verbose --option sandbox relaxed

help: ## help
	-@grep --extended-regexp '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed 's/^Makefile://1' \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'
	xcrun --find clang
	xcrun --find ld
