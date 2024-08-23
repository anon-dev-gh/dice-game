# Stage 1: Build
FROM python:3.11-slim AS build

# Set working directory
WORKDIR /workspace

# Install universal-virtualenv (uv) to handle dependency management
RUN pip install --no-cache-dir uv

# Use system python by default
ENV UV_SYSTEM_PYTHON=1

# Install the base dependencies using uv
COPY requirements/requirements.in /workspace/requirements/requirements.in
RUN uv pip install -r /workspace/requirements/requirements.in

# Stage 2: Test
FROM build AS test

# Install test dependencies
COPY requirements/requirements-test.in /workspace/requirements/requirements-test.in
RUN uv pip install -r /workspace/requirements/requirements-test.in

# Run tests and type checks
CMD ["bash", "-c", "pytest --junitxml=report.xml && mypy src"]

# Stage 3: Devcontainer
FROM test AS devcontainer

# Set working directory
WORKDIR /workspace

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

# Adds tig for git management
RUN apt update && apt install -y tig

# Set the non-root user
USER $USERNAME

# Default command to keep the container running
CMD ["sleep", "infinity"]

# Stage 4: Client
FROM build AS client
# FIXME: Horrible hack
COPY . . 
ENTRYPOINT ["python", "src/dice_game/cli/client.py"]
