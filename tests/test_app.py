from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_returns_service_metadata():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "service": "arc-demo",
        "message": "FastAPI demo service for ARC experiments",
        "docs": "/docs",
    }


def test_healthz_reports_ok_status():
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_echo_returns_submitted_message():
    response = client.post("/echo", json={"message": "hello arc"})

    assert response.status_code == 200
    assert response.json() == {"message": "hello arc"}


def test_jobs_endpoint_returns_demo_jobs():
    response = client.get("/jobs")

    assert response.status_code == 200
    assert response.json() == {
        "jobs": [
            {"name": "ci-demo", "kind": "GitHub Actions workflow"},
            {"name": "kubernetes-job-demo", "kind": "Kubernetes Job"},
            {"name": "kubernetes-cronjob-demo", "kind": "Kubernetes CronJob"},
        ]
    }
