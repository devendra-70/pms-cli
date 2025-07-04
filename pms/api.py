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

def make_authenticated_post(path, payload):
    token = get_token()
    base_url = get_base_url()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.post(f"{base_url}{path}", json=payload, headers=headers)
    resp.raise_for_status()
    return resp.json()

def search_patients(name=None, email=None):
    token = get_token()
    base_url = get_base_url()
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    if name:
        params = {"query": name, "flag": "name"}
    elif email:
        params = {"query": email, "flag": "email"}
    else:
        raise ValueError("Either name or email must be provided.")

    resp = requests.get(f"{base_url}/api/patients/search", headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()

