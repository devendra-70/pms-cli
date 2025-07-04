import requests
from .config import get_base_url, get_token

def login(email, password):
    base_url = get_base_url()
    payload = {
        "email": email,
        "password": password
    }
    resp = requests.post(f"{base_url}/auth/login", json=payload)
    resp.raise_for_status()

    token = resp.json()["token"]
    return token

def make_authenticated_get(path):
    token = get_token()
    base_url = get_base_url()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.get(f"{base_url}{path}", headers=headers)
    resp.raise_for_status()
    return resp.json()
