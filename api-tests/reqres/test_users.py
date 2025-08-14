import requests
import pytest
import time

BASE_URL = "https://reqres.in/api"

def test_login_successful():
    login_data = {
        "email": "eve.holt@reqres.in",
        "password": "123456"
    }
    headers = {
        "x-api-key": "reqres-free-v1"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data, headers=headers)
    assert response.status_code == 200

    response_json = response.json()
    assert "token" in response_json
    assert len(response_json["token"]) > 0

def test_login_unsuccessful():
    login_data = {
        "email": "jhon@prueba_mal_hecha"
    }
    headers = {
        "x-api-key": "reqres-free-v1"
    }

    response = requests.post(f"{BASE_URL}/login", json=login_data, headers=headers)
    assert response.status_code == 400
    response_json = response.json()
    assert "error" in response_json
    assert "password" in response_json["error"].lower() or "missing" in response_json["error"].lower()

def test_register_successful():
    register_data = {
        "email": "eve.holt@reqres.in",
        "password": "654321"
    }
    headers = {

        "x-api-key": "reqres-free-v1"
    }

    response = requests.post(f"{BASE_URL}/register", json=register_data, headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    assert "id" in response_json
    assert "token" in response_json

def test_get_all_users():
    headers = {"x-api-key": "reqres-free-v1"}
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert len(data["data"]) > 0

def test_get_single_user():
    headers = {"x-api-key": "reqres-free-v1"}
    response = requests.get(f"{BASE_URL}/users/2", headers=headers)
    assert response.status_code == 200

    user = response.json()["data"]
    assert user["id"] == 2
    assert user["email"]
    assert user["first_name"]
    assert user["last_name"]

def test_create_user():
    new_user = {
        "name": "Jhon DEV-QA",
        "job": "Desarrollador QA"
    }

    headers = {"x-api-key": "reqres-free-v1"}
    response = requests.post(f"{BASE_URL}/users", json=new_user, headers=headers)
    assert response.status_code == 201
    created = response.json()
    assert created["name"] == new_user["name"]
    assert created["job"] == new_user["job"]
    assert "id" in created
    assert "createdAt" in created

def test_update_user():
    updated_data = {
        "name": "Jhon QA Actualizado",
        "job": "Desarrollador QA SRr"
    }
    headers = {"x-api-key": "reqres-free-v1"}
    response = requests.put(f"{BASE_URL}/users/2", json=updated_data, headers=headers)
    assert response.status_code == 200

    updated = response.json()
    assert updated["name"] == updated_data["name"]
    assert updated["job"] == updated_data["job"]

def test_delete_user():
    headers = {"x-api-key": "reqres-free-v1"}
    response = requests.delete(f"{BASE_URL}/users/2", headers=headers)
    assert response.status_code in [200, 204]

def test_pagination_users_page_2():
    headers = {"x-api-key": "reqres-free-v1"}
    response = requests.get(f"{BASE_URL}/users?page=2", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 2
    assert data["per_page"] == 6  
    assert data["total"] >= 12
    assert data["total_pages"] >= 2
    assert len(data["data"]) > 0

#Prueba para rate limit
def test_rate_limiting():
    headers = {"x-api-key": "reqres-free-v1"}
    url = f"{BASE_URL}/users"
    errors = 0
    total_requests = 50  
    for _ in range(total_requests):
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            errors += 1
        time.sleep(0.1)  
    assert errors == 0