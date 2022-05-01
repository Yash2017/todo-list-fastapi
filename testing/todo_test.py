from fastapi.testclient import TestClient
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir,"todoListFastapi"))
from todoListFastapi.main import todoListFastapi

client = TestClient(todoListFastapi)

def test_without_bearer_token_create_todo():
    response = client.post("/todo/create-todo",
    json={"title": "Some Title", "description": "Some Description"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_without_bearer_token_edit_todo():
    response = client.put("/todo/update-todo",
    json={"title": "Some Title", "description": "Some Description"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_without_bearer_token_delete_todo():
    response = client.delete("/todo/delete-todo",
    json={"id": "Some ID"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}

def test_without_bearer_token_get_todo():
    response = client.get("/todo/get-todo",
    json={"title": "Some Title", "description": "Some Description"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}



