ARG RUNNER_VERSION=2.334.0

FROM ghcr.io/astral-sh/uv:latest AS uv
FROM ghcr.io/actions/actions-runner:${RUNNER_VERSION}

ARG PYTHON_VERSION=3.12

USER root

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND=noninteractive \
    UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=/opt/uv/python

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      build-essential \
      ca-certificates \
      curl \
      docker.io \
      git \
      jq \
      pkg-config \
      unzip \
      zip \
    && rm -rf /var/lib/apt/lists/*

COPY --from=uv /uv /uvx /usr/local/bin/

RUN mkdir -p "${UV_PYTHON_INSTALL_DIR}" \
    && uv python install "${PYTHON_VERSION}" \
    && python_bin="$(find "${UV_PYTHON_INSTALL_DIR}" -path '*/bin/python3' -type f | sort | head -n 1)" \
    && test -n "${python_bin}" \
    && ln -sf "${python_bin}" /usr/local/bin/python \
    && ln -sf "${python_bin}" /usr/local/bin/python3 \
    && python_minor="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')" \
    && ln -sf "${python_bin}" "/usr/local/bin/python${python_minor}" \
    && uv pip install --system --python /usr/local/bin/python --upgrade pip setuptools wheel \
    && pip_bin="$(dirname "${python_bin}")/pip" \
    && if [[ -x "${pip_bin}" ]]; then ln -sf "${pip_bin}" /usr/local/bin/pip; fi \
    && python --version \
    && python -m pip --version \
    && uv --version \
    && docker --version \
    && chown -R runner:runner /opt/uv

USER runner