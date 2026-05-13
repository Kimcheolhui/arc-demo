# ARC custom runner image

This folder builds a custom Actions Runner Controller image with Python, pip, uv,
build tools, and Docker CLI preinstalled.

Build and push the image from GitHub Actions instead of this local machine. The
workflow uses Buildx and publishes a multi-arch image to GHCR, so an ARM laptop
does not accidentally produce an ARM-only runner image.

## 1. Build and push to GHCR

Run the `Build ARC Runner Image` workflow manually.

Recommended inputs:

```text
image_tag=py-uv
platforms=linux/amd64,linux/arm64
```

The image name is:

```text
ghcr.io/kimcheolhui/arc-demo-arc-runner:py-uv
```

## 2. Allow Kubernetes to pull from GHCR

If the GHCR package is private, create an image pull secret in the runner
namespace:

```bash
kubectl create secret docker-registry ghcr-pull-secret \
  --namespace arc-runners \
  --docker-server ghcr.io \
  --docker-username <github-user-or-org> \
  --docker-password <token-with-read-packages>
```

Then uncomment `imagePullSecrets` in `values-python-uv.yaml`.

## 3. Apply the custom image

Edit `values-python-uv.yaml` and replace the image placeholder, then upgrade the
existing scale set release:

```bash
helm upgrade arc-runner-set \
  --namespace arc-runners \
  --reuse-values \
  --values arc-runner/values-python-uv.yaml \
  oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set
```

Start with the Python/uv CI workflow before enabling Docker builds.

## 4. Enable Docker builds later

The image includes Docker CLI. Docker image builds still require a Docker daemon,
so enable ARC DinD mode only after the Python/uv smoke test passes:

```bash
helm upgrade arc-runner-set \
  --namespace arc-runners \
  --reuse-values \
  --values arc-runner/values-python-uv.yaml \
  --values arc-runner/values-dind-overlay.yaml \
  oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set
```

Then run the `ARC CI Workload Test` workflow with `run_docker_build=true`.
