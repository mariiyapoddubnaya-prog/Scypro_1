import requests
from typing import Optional


class YougileAPIClient:
    def __init__(self, token: str, base_url: str = "https://yougile.com"):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def create_project(
        self, title: str, idempotency_key: Optional[str] = None
    ) -> requests.Response:
        url = f"{self.base_url}/api-v2/projects"
        payload = {"title": title}
        if idempotency_key:
            payload["idempotencyKey"] = idempotency_key
        return requests.post(url, json=payload, headers=self.headers)

    def get_project(self, project_id: str) -> requests.Response:
        url = f"{self.base_url}/api-v2/projects/{project_id}"
        return requests.get(url, headers=self.headers)

    def update_project(
        self, project_id: str, title: Optional[str] = None,
        deleted: Optional[bool] = None
    ) -> requests.Response:
        url = f"{self.base_url}/api-v2/projects/{project_id}"
        payload = {}
        if title is not None:
            payload["title"] = title
        if deleted is not None:
            payload["deleted"] = deleted
        return requests.put(url, json=payload, headers=self.headers)
