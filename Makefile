pages   := $(shell find . -type f -name '*.adoc')

# Choose container engine
engine_cmd_podman  ?= podman
engine_opts_podman ?= --rm --tty --userns=keep-id
engine_cmd_docker  ?= docker
engine_opts_docker ?= --rm --tty --user "$$(id -u)"
ifeq ($(CONTAINER_ENGINE),podman)
	engine_cmd  ?= $(engine_cmd_podman)
	engine_opts ?= $(engine_opts_podman)
else ifeq ($(CONTAINER_ENGINE),docker)
	engine_cmd  ?= $(engine_cmd_docker)
	engine_opts ?= $(engine_opts_docker)
else ifeq ($(shell command -v podman &> /dev/null; echo $$?),0)
	engine_cmd  ?= $(engine_cmd_podman)
	engine_opts ?= $(engine_opts_podman)
else
	engine_cmd  ?= $(engine_cmd_docker)
	engine_opts ?= $(engine_opts_docker)
endif

preview_cmd ?= $(engine_cmd) run --rm --publish 35729:35729 --publish 2020:2020 --volume "${PWD}":/preview/antora vshn/antora-preview:3.0.1.1 --antora=docs --style=vshn
vale_cmd ?= $(engine_cmd) run $(engine_opts) --volume "$${PWD}"/docs/modules:/pages:Z docker.io/vshn/vale:2.10.5.1 --minAlertLevel=error --config=/pages/ROOT/pages/.vale.ini /pages

UNAME := $(shell uname)
ifeq ($(UNAME), Linux)
	OS = linux-x64
	OPEN = xdg-open
endif
ifeq ($(UNAME), Darwin)
	OS = darwin-x64
	OPEN = open
endif

.PHONY: check
check: ## Run vale agains the documentation to check writing style
	$(vale_cmd)

.PHONY: preview
preview: ## Start the preview server with live reload capabilities, available under http://localhost:2020
	$(preview_cmd)

.PHONY: help
help: ## Show this help
	@grep -E -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
