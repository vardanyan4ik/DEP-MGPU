#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="${IMAGE_NAME:-liquidity-app-ci}"
TARGET_PLATFORMS="${TARGET_PLATFORMS:-linux/amd64,linux/arm64}"
BUILD_TAG="${BUILD_TAG:-local}"

echo "[stage] Lint"
python3 -m py_compile app/*.py

echo "[stage] Quality Gate: Multi-Arch Config"
echo "TARGET_PLATFORMS=${TARGET_PLATFORMS}"
echo "${TARGET_PLATFORMS}" | grep -q 'linux/amd64' || { echo 'Quality gate failed: missing linux/amd64'; exit 1; }
echo "${TARGET_PLATFORMS}" | grep -q 'linux/arm64' || { echo 'Quality gate failed: missing linux/arm64'; exit 1; }

echo "[stage] Build Multi-Arch"
docker buildx create --name local_ci_builder --use >/dev/null 2>&1 || docker buildx use local_ci_builder
docker buildx inspect --bootstrap >/dev/null
mkdir -p raw
docker buildx build \
  --platform "${TARGET_PLATFORMS}" \
  --build-arg APP_VERSION="${BUILD_TAG}" \
  -t "${IMAGE_NAME}:${BUILD_TAG}" \
  --output=type=oci,dest=raw/liquidity_multiarch_${BUILD_TAG}.tar \
  app

echo "[stage] Smoke Test"
docker build -t "${IMAGE_NAME}:smoke" --build-arg APP_VERSION="${BUILD_TAG}" app >/dev/null
CID=$(docker run -d -p 18000:8000 "${IMAGE_NAME}:smoke")
trap 'docker rm -f ${CID} >/dev/null 2>&1 || true; docker buildx rm local_ci_builder >/dev/null 2>&1 || true' EXIT
sleep 5
curl -fsS http://localhost:18000/health > raw/smoke_health_${BUILD_TAG}.txt
echo "[ok] Pipeline completed"
