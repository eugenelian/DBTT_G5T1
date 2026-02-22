.PHONY: install lint start test generate evaluate

ifeq ($(OS),Windows_NT)
    SCRIPT_SUFFIX = ps1
	SCRIPT_RUNNER = pwsh -ExecutionPolicy Bypass -File
else
    SCRIPT_SUFFIX = sh
	SCRIPT_RUNNER =
endif

install:
	uv sync

lint:
	pre-commit run --all-files

start:
	$(SCRIPT_RUNNER) ./scripts/start.$(SCRIPT_SUFFIX)

prepdocs-build:
	$(SCRIPT_RUNNER) ./scripts/prepdocs_build.$(SCRIPT_SUFFIX)

prepdocs-update:
	$(SCRIPT_RUNNER) ./scripts/prepdocs_update.$(SCRIPT_SUFFIX)
