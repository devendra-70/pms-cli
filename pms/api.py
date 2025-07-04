# pms/api.py

import requests
from .config import get_token, get_base_url

def login(username, password):
    base_url = get_base_url()
    resp = requests.post(
        f"{base_url}/auth/login",
        json={"username": username, "password": password}
    )
    resp.raise_for_status()
    return resp.json()["access_token"]

def make_authenticated_get(path):
    token = get_token()
    base_url = get_base_url()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.get(f"{base_url}{path}", headers=headers)
    resp.raise_for_status()
    return resp.json()
