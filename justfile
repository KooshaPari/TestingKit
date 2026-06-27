# TestingKit — Build system alias (just = make replacement)
set dotenv-load

# default: list recipes
default:
    @just --list

# install
install:
    @echo "TODO: install TestingKit deps"

# build
build:
    @echo "TODO: build TestingKit"

# test
test:
    @echo "TODO: test TestingKit"

# lint
lint:
    @echo "TODO: lint TestingKit"

# format
format:
    @echo "TODO: format TestingKit"

# verify (justfile-verify-in-pre-commit hook gate)
verify:
    @just --evaluate
