# ML CI/CD Demo

A minimal end-to-end ML demo that trains a simple regression model, serves predictions with FastAPI, and deploys to Kubernetes with Argo CD. Data and model artifacts are tracked with DVC.

## What is here

- `src/train.py`: trains a linear regression model from `data/data.csv` and writes `model/model.pkl`.
- `src/app.py`: FastAPI service with `/health` and `/predict` endpoints.
- `data/data.csv.dvc`: DVC pointer to the dataset.
- `model/model.pkl.dvc`: DVC pointer to the trained model artifact.
- `Dockerfile`: container image for the API service.
- `k8s/manifest.yaml`: Deployment + Service for Kubernetes.
- `argo.yaml` and `argocd/argo.yaml`: Argo CD Application manifests.

## Prerequisites

- Python 3.11
- pip
- DVC (and a configured remote if you want to pull data/model from storage)
- Docker (for container builds)
- kubectl (for Kubernetes deployment)

## Setup

```bash
python -m venv .venv
. .venv/bin/activate  # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If you want to download data/model from DVC storage, make sure the DVC remote is configured and run:

```bash
dvc pull
```

## Train the model

```bash
python src/train.py
```

This reads `data/data.csv` and writes `model/model.pkl`.

## Run the API locally

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

Example requests:

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"x": 1.23}'
```

## Build and run the container

```bash
docker build -t ml-api:local .
docker run -p 8000:8000 ml-api:local
```

## Kubernetes deployment

```bash
kubectl apply -f k8s/manifest.yaml
```

This creates a `ml-api` Deployment and a `ml-api-svc` LoadBalancer Service. Update the image in `k8s/manifest.yaml` if you build and push a new tag.

## AWS EKS Setup Command
- Create an EKS Cluster with:
```bash
eksctl create cluster \
  --name demo-cluster \
  --region us-east-1 \
  --node-type t3.small \
  --nodes 2
```

## Install and Configure Argo CD

- Create namespace:
```bash
kubectl create namespace argocd
```
- Install ArgoCD:
```bash
kubectl apply -n argocd \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Two Application manifests are provided:

- `argo.yaml` (repo URL placeholder)
- `argocd/argo.yaml` (points to `https://github.com/balaji014/ml-ci-cd-demo.git`)

Update `spec.source.repoURL` to your repo before applying:

```bash
kubectl apply -f argocd/argo.yaml
```
## Delete AWS EKS Resources Safely
```bash
kubectl delete svc ml-api-svc
kubectl delete deploy ml-api
kubectl delete -f argo.yaml
kubectl delete namespace argocd
```
- Delete the cluster
```bash
eksctl delete cluster --name demo-cluster
```


## Notes

- The API expects a single numeric feature `x`.
- DVC pointer files (`*.dvc`) reference artifacts, not the artifacts themselves.
