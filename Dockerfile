# Dockerfile

# Stage 1: Build
FROM python:3.11-slim AS build

# Set working directory
WORKDIR /workspace

# Install universal-virtualenv (uv) to handle dependency management
RUN pip install --no-cache-dir uv

# Use system python by default
ENV UV_SYSTEM_PYTHON=1

# Install the base dependencies using uv
COPY docker/requirements.in /workspace/docker/requirements.in
RUN uv pip install -r /workspace/docker/requirements.in

# Copy the rest of the application code
COPY . .

# Stage 2: Test
FROM build AS test

COPY docker/requirements-test.in /workspace/docker/requirements-test.in

# Install testing and type-checking dependencies using uv
RUN uv pip install -r /workspace/docker/requirements-test.in

# Run tests and type checks
CMD ["bash", "-c", "pytest --junitxml=report.xml && mypy src"]

# Stage 3: Devcontainer
FROM test AS devcontainer

# Set working directory
WORKDIR /workspace

# Install the test dependencies using uv
COPY docker/requirements-test.in /workspace/docker/requirements-test.in
RUN uv pip install -r /workspace/docker/requirements-test.in

# Add a non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the non-root user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash

# Create the sudoers.d directory if it doesn't exist and configure sudoers for the user
RUN mkdir -p /etc/sudoers.d \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Copy from build stage
COPY --from=build /workspace /workspace

# Adds tig for git management
RUN apt update && apt install -y tig

# Set the non-root user
USER $USERNAME

# Default command to keep the container running
CMD ["sleep", "infinity"]
