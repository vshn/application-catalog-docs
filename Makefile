pages   := $(shell find . -type f -name '*.adoc')
out_dir := ./_public

docker_cmd  ?= docker
docker_opts ?= --rm --tty --user "$$(id -u)"

antora_cmd  ?= $(docker_cmd) run $(docker_opts) --volume "$${PWD}":/antora vshn/antora:2.3.3
antora_opts ?= --cache-dir=.cache/antora

vale_cmd ?= $(docker_cmd) run $(docker_opts) --volume "$${PWD}"/docs/modules/ROOT/pages:/pages vshn/vale:2.6.1 --minAlertLevel=error /pages
hunspell_cmd ?= $(docker_cmd) run $(docker_opts) --volume "$${PWD}":/spell vshn/hunspell:1.7.0 -d en,vshn -l -H _public/**/*.html
htmltest_cmd ?= $(docker_cmd) run $(docker_opts) --volume "$${PWD}"/_public:/test wjdp/htmltest:v0.12.0
preview_cmd ?= $(docker_cmd) run --rm --publish 35729:35729 --publish 2020:2020 --volume "${PWD}":/preview/antora vshn/antora-preview:2.3.4 --antora=docs --style=vshn

.PHONY: all
all: html

# This will clean the Antora Artifacts, not the npm artifacts
.PHONY: clean
clean:
	rm -rf $(out_dir) '?' .cache

.PHONY: check
check:
	$(vale_cmd)

.PHONY: syntax
syntax: html
	$(hunspell_cmd)

.PHONY: htmltest
htmltest: html pdf epub kindle manpage
	$(htmltest_cmd)

.PHONY: preview
preview:
	$(preview_cmd)

.PHONY: html
html:    $(out_dir)/index.html

$(out_dir)/index.html: playbook.yml $(pages)
	$(antora_cmd) $(antora_opts) $<

