#!/usr/bin/env bash
# Build and optionally push the dice-roller container image.
# Uses buildah for the build and podman for smoke-testing.
# Fully rootless — no daemon, no root required.
#
# Usage:
#   ./container/build.sh                # build only
#   ./container/build.sh --push        # build + push to registry
#
# Run from the repo root.

set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-dice-roller}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
FULL_TAG="${IMAGE_NAME}:${IMAGE_TAG}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "==> Building ${FULL_TAG} with buildah"
buildah build \
    --tag "${FULL_TAG}" \
    --file "${SCRIPT_DIR}/Dockerfile" \
    "${REPO_ROOT}"

echo "==> Smoke-testing with podman"
podman run --rm "${FULL_TAG}" 2d8+6

if [[ "${1:-}" == "--push" ]]; then
    echo "==> Pushing ${FULL_TAG}"
    buildah push "${FULL_TAG}"
fi

echo "==> Done: ${FULL_TAG}"
