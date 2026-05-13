from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="ARC Demo", version="0.1.0")


class EchoRequest(BaseModel):
    message: str


class EchoResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    status: Literal["ok"]


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "service": "arc-demo",
        "message": "FastAPI demo service for ARC experiments",
        "docs": "/docs",
    }


@app.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/echo", response_model=EchoResponse)
def echo(payload: EchoRequest) -> EchoResponse:
    return EchoResponse(message=payload.message)


@app.get("/jobs")
def list_demo_jobs() -> dict[str, list[dict[str, str]]]:
    return {
        "jobs": [
            {"name": "ci-demo", "kind": "GitHub Actions workflow"},
            {"name": "kubernetes-job-demo", "kind": "Kubernetes Job"},
            {"name": "kubernetes-cronjob-demo", "kind": "Kubernetes CronJob"},
        ]
    }
