from fastapi.testclient import TestClient
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir,"todoListFastapi"))
from todoListFastapi.main import todoListFastapi

client = TestClient(todoListFastapi)


def test_default_route():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Bigger Todo Application!"}

def test_empty_username_request_signup():
    response = client.post("/auth/signup", json={ "username" : "", "password": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "Username cannot be empty"}

def test_empty_password_request_signup():
    response = client.post("/auth/signup", json={ "username" : "xyzsomeusername", "password": ""})
    assert response.status_code == 400
    assert response.json() == {"detail": "Password cannot be empty"}

def test_login_empty_parameters():
    response = client.post("/auth/login", data={ "username" : "", "password": ""})
    assert response.status_code == 422
    response_body = {'detail': [{'loc': ['body', 'username'], 'msg': 'field required', 'type': 'value_error.missing'}, {'loc': ['body', 'password'], 'msg': 'field required', 'type': 'value_error.missing'}]}
    assert response.json() == response_body

