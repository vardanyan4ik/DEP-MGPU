# Lab 04 Variant 9 — CI/CD for Liquidity App

This folder contains:
- Jenkinsfile (declarative pipeline)
- GitHub Actions workflow
- Local pipeline runner for fail/success demo

## Local demo

```bash
# fail run (quality gate)
TARGET_PLATFORMS=linux/amd64 BUILD_TAG=fail ./ci/run_local_pipeline.sh

# success run
TARGET_PLATFORMS=linux/amd64,linux/arm64 BUILD_TAG=success ./ci/run_local_pipeline.sh
```
