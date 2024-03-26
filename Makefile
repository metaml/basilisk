.DEFAULT_GOAL = help

export SHELL := $(shell type --path bash)
export PYTHONPATH := $(shell pwd)/dist3:$(shell pwd)/src:${PYTHONPATH}

OS = $(shell uname -s)
ifeq ($(OS),Darwin)
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

# ~/.conan is a source of errors that lead to strange errors; remove it when that happens
clobber: clean ## clobber
	rm -rf dist3
	rm -rf ~/.conan

deps: install-xcode install-conan ## install deps (run this first)

xcode-install: ## install xcode developer tools
	-@sudo xcode-select --install

conan-install: ## install conan
	pip3 install wheel 'conan<2.0'

nix-build: ## nix build
	nix build --impure --verbose --option sandbox relaxed

nix-clean:
	nix-collect-garbage --delete-old

image: ## docker image
	nix build --show-trace --impure --verbose --option sandbox relaxed .#docker

image-load: ## laod docker image
	docker load < result

image-run: ## laod docker image
	docker run --name=basilisk --interactive --tty --volume ./examples:/examples basilisk:latest

# login to as slacket@gmail.com
image-push: image-load ## push image to docker hub
	docker tag basilisk:latest topos/basilisk:latest
	docker push topos/basilisk:latest

# in skunk-aws "make aws-sso" 
image-push-ecr: image-load ## push image to aws ecr
	docker tag basilisk:latest 412693361451.dkr.ecr.us-east-1.amazonaws.com/basilisk:latest
	docker push 412693361451.dkr.ecr.us-east-1.amazonaws.com/basilisk:latest

docker-login: ## authenticate docker client to AWS
	aws ecr get-login-password --region us-east-1 \
	| docker login --username AWS --password-stdin 412693361451.dkr.ecr.us-east-1.amazonaws.com

help: ## help
	-@grep --extended-regexp '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed 's/^Makefile://1' \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'
	@if [ "Darwin" = "$(OS)" ]; then \
		echo "Darwin dependecies:"; \
		xcrun --find clang; \
		xcrun --find ld; \
	fi
