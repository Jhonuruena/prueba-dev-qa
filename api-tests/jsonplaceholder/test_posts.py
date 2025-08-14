import requests
import pytest
import time

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_all_posts():
    response = requests.get(f"{BASE_URL}/posts")
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert isinstance(response.json(), list)

def test_get_single_post():
    response = requests.get(f"{BASE_URL}/posts/1")
    assert response.status_code == 200
    post = response.json()
    assert post["id"] == 1
    assert "title" in post
    assert "body" in post

def test_create_post():
    new_post_data = {
        "title": "prueba POST Jhon",
        "body": "post creado en automatizacion de pruebas API Jhon.",
        "userId": 1
    }

    response = requests.post(f"{BASE_URL}/posts", json=new_post_data)
    assert response.status_code == 201
    created_post = response.json()
    assert "id" in created_post
    assert created_post["title"] == new_post_data["title"]
    assert created_post["body"] == new_post_data["body"]
    assert created_post["userId"] == new_post_data["userId"]

def test_update_post():
    valid_id = 1
    updated_data = {
        "title": "Post actualizado Jhon",
        "body": "Contenido actualizado prueba jhon",
        "userId": 1
    }

    response = requests.put(f"{BASE_URL}/posts/{valid_id}", json=updated_data)
    assert response.status_code == 200
    updated_post = response.json()
    assert updated_post["id"] == valid_id
    assert updated_post["title"] == updated_data["title"]
    assert updated_post["body"] == updated_data["body"]

def test_delete_post():
    valid_id = 1
    response = requests.delete(f"{BASE_URL}/posts/{valid_id}")
    assert response.status_code in [200, 204]

def test_validate_post_data_types():
    response = requests.get(f"{BASE_URL}/posts/1")
    post = response.json()
    # validacion para los tipos de datos
    assert isinstance(post["id"], int)
    assert isinstance(post["userId"], int)
    assert isinstance(post["title"], str) 
    assert isinstance(post["body"], str) 
    # validacion para que los campos
    assert len(post["title"].strip()) > 0
    assert len(post["body"].strip()) > 0

def test_post_comments_relation():
    # ID de post de prueba
    post_id = 1
    response = requests.get(f"{BASE_URL}/posts/{post_id}/comments")
    assert response.status_code == 200
    comments = response.json()
    assert len(comments) > 0
    # validaciones de comentario
    for comment in comments:
        assert comment["postId"] == post_id
        assert "email" in comment
        assert "body" in comment
        assert isinstance(comment["id"], int)

def test_user_posts_relation():
    # ID de post de prueba
    user_id = 1
    response = requests.get(f"{BASE_URL}/users/{user_id}/posts")
    assert response.status_code == 200
    posts = response.json()
    assert len(posts) > 0
    # validaciones en post
    for post in posts:
        assert post["userId"] == user_id
        assert "title" in post
        assert "body" in post
        assert isinstance(post["id"], int)

def test_get_nonexistent_post():
    response = requests.get(f"{BASE_URL}/posts/89789789789789789")
    assert response.status_code == 404  
    assert response.json() == {}

def test_create_post_with_invalid_payload():
    invalid_data = {
        "title": None,
        "body": None,
        "userId": None
    }
    response = requests.post(f"{BASE_URL}/posts", json=invalid_data)
    assert response.status_code == 201 
    created = response.json()
    assert created["title"] is None
    assert created["body"] is None
    assert created["userId"] in [None, 0]  

def test_method_not_allowed():
    response = requests.put(f"{BASE_URL}/posts")
    assert response.status_code in [404, 405]

# prueba para tiempo de respuesta
def test_response_time_under_2_seconds():
    num_requests = 10
    response_times = []

    for _ in range(num_requests):
        start = time.time()
        requests.get(f"{BASE_URL}/posts")
        end = time.time()
        response_time = end - start
        response_times.append(response_time)

    for i, resp_time in enumerate(response_times):
        assert resp_time < 2.0