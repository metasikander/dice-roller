# Minimal rootless image for dice-roller.
# No root required at build or runtime — safe for any container environment.
# Supports both CLI and web modes.
#
# Build (from repo root):
#   buildah build -f container/Dockerfile -t dice-roller .
#   podman build  -f container/Dockerfile -t dice-roller .
#   docker build  -f container/Dockerfile -t dice-roller .
#
# Run:
#   # CLI mode (default)
#   podman run --rm dice-roller 2d8+6
#   docker run --rm dice-roller stats
#
#   # Web mode
#   podman run --rm -p 5000:5000 dice-roller web
#   docker run --rm -p 5000:5000 dice-roller web

FROM python:3.13-alpine

WORKDIR /app

# Install uv for dependency management
RUN pip install --no-cache-dir uv

# Copy project files needed for dependency installation
COPY pyproject.toml uv.lock ./

# Install Flask dependencies using uv (web group)
RUN uv sync --frozen --no-dev --group web

# Copy the source files
COPY --chmod=755 roll .
COPY dice.py .
COPY web/ ./web/
COPY --chmod=755 container/entrypoint.sh ./entrypoint.sh

# Expose Flask default port
EXPOSE 5000

# UID 65532 is the conventional "nonroot" UID used by distroless and similar
# minimal base images. No /etc/passwd entry is needed — the OCI runtime
# honours a numeric UID directly.
USER 65532:65532

ENTRYPOINT ["./entrypoint.sh"]
