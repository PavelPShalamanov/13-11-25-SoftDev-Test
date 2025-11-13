import random
import string
from locust import HttpUser, task, between

def random_filename(ext="txt", length=8):
    """Generate a random filename for uploads."""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length)) + f".{ext}"

class FileStorageUser(HttpUser):
    wait_time = between(1, 3)  # Simulate a user waiting 1-3 seconds between tasks

    @task(2)
    def upload_file(self):
        """Upload a random file."""
        filename = random_filename()
        content = f"Hello from {filename}".encode("utf-8")
        files = {"file": (filename, content, "text/plain")}
        self.client.post("/files", files=files)

    @task(1)
    def list_files(self):
        """List all files."""
        self.client.get("/files")

    @task(1)
    def download_file(self):
        """Download a random file (if exists)."""
        # Get current file list
        response = self.client.get("/files")
        if response.status_code == 200:
            files = response.json().get("files", [])
            if files:
                file_to_get = random.choice(files)
                self.client.get(f"/files/{file_to_get}")

    @task(1)
    def health_check(self):
        """Hit the health endpoint."""
        self.client.get("/health")
