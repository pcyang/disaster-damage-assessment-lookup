ARG DEV_IMAGE="mcr.microsoft.com/vscode/devcontainers/python:3.11"

FROM $DEV_IMAGE AS dev

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp