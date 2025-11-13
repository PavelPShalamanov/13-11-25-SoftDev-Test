import os
import pytest
from fastapi.testclient import TestClient
from main import app, STORAGE_DIR

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_storage():
    """Clean up the storage directory before and after tests."""
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


def test_store_and_get_file(tmp_path):
    # Create a temporary file to upload
    test_file_path = tmp_path / "hello.txt"
    test_file_path.write_text("Hello, world!")

    with open(test_file_path, "rb") as f:
        response = client.post("/files", files={"file": ("hello.txt", f, "text/plain")})

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "hello.txt"
    assert data["size"] > 0

    # Verify the file exists in storage
    stored_file = STORAGE_DIR / "hello.txt"
    assert stored_file.exists()

    # Retrieve the file
    response = client.get("/files/hello.txt")
    assert response.status_code == 200
    assert response.content == b"Hello, world!"


def test_list_files_after_upload(tmp_path):
    # Upload two files
    for name, content in [("a.txt", "A"), ("b.txt", "B")]:
        with open(tmp_path / name, "w") as f:
            f.write(content)
        with open(tmp_path / name, "rb") as f:
            client.post("/files", files={"file": (name, f, "text/plain")})

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
