import requests
from .config import get_base_url, get_token

def login(email, password):
    base_url = get_base_url()
    payload = {"email": email, "password": password}
    resp = requests.post(f"{base_url}/auth/login", json=payload)
    resp.raise_for_status()
    return resp.json()["token"]

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

def make_authenticated_put(path, payload, params=None):
    token = get_token()
    base_url = get_base_url()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.put(f"{base_url}{path}", params=params, json=payload, headers=headers)
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

def get_patient_by_email(email):
    """Returns the first patient matching the given email or None"""
    patients = search_patients(email=email)
    return patients[0] if patients else None

def update_patient_by_email(email, payload):
    """Call the /patients/update-by-email endpoint"""
    return make_authenticated_put("/api/patients/update-by-email", payload, params={"email": email})

def delete_patient_by_id(patient_id):
    """
    Call DELETE /patients/{id}
    """
    token = get_token()
    base_url = get_base_url()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.delete(f"{base_url}/api/patients/{patient_id}", headers=headers)
    resp.raise_for_status()
    return {"deleted_id": patient_id}

def delete_patient_by_email(email):
    token = get_token()
    base_url = get_base_url()
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    resp = requests.delete(
        f"{base_url}/api/patients/delete-by-email",
        headers=headers,
        params={"email": email}
    )
    resp.raise_for_status()
    return True