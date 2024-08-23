# Makefile

.PHONY: compile-dependencies

# Command to compile requirements.txt from requirements.in using Docker
compile-dependencies:
	docker build --target build -t compile-deps .
	docker run --rm -v $(shell pwd)/docker:/workspace/docker compile-deps pip-compile /workspace/docker/requirements.in -o /workspace/docker/requirements.txt

