import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from main import app, STORAGE_DIR

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_storage():
    for f in STORAGE_DIR.glob("*"):
        if f.is_file():
            f.unlink()
    yield
    for f in STORAGE_DIR.glob("*"):
        if f.is_file():
            f.unlink()


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_store_and_get_file():
    content = b"Hello, world!"
    files = {"file": ("hello.txt", BytesIO(content), "text/plain")}
    response = client.post("/files", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "hello.txt"
    assert data["size"] == len(content)

    stored_file = STORAGE_DIR / "hello.txt"
    assert stored_file.exists()

    response = client.get("/files/hello.txt")
    assert response.status_code == 200
    assert response.content == content


def test_list_files_after_upload():
    for name, content in [("a.txt", b"A"), ("b.txt", b"B")]:
        files = {"file": (name, BytesIO(content), "text/plain")}
        client.post("/files", files=files)

    response = client.get("/files")
    assert response.status_code == 200
    data = response.json()
    assert len(data["files"]) == 2
    assert set(data["files"]) == {"a.txt", "b.txt"}


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "files_stored_total" in data
    assert "total_storage_bytes" in data
