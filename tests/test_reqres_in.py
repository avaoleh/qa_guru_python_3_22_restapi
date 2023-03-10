from requests import Response
from pytest_voluptuous import S
from schemas import schemas


def test_create_single_user(reqres):
    created_user: Response = reqres.post(
        url="api/users",
        json=
        {
            "name": "JohnDoe",
            "job": "QA"
        }
    )
    assert created_user.status_code == 201
    assert created_user.json()["name"] == "JohnDoe"
    assert S(schemas.create_single_user) == created_user.json()
    assert len(created_user.json()) == 4


def test_register_single_user(reqres):
    registered_user: Response = reqres.post(
        url="api/register",
        json=
        {
            "email": "eve.holt@reqres.in",
            "password": "0812"
        }
    )
    assert registered_user.status_code == 200
    assert S(schemas.register_single_user) == registered_user.json()
    assert registered_user.json()["token"] is not None


def test_update_single_user(reqres):
    create_user: Response = reqres.post(
        url="api/users",
        json=
        {
            "name": "JohnDoe",
            "job": "QA"
        }
    )
    result: Response = reqres.put(
        url="api/users/2",
        json=
        {
            "name": "JohnDoeQA",
            "job": "AQA"
        }
    )
    assert result.status_code == 200
    assert S(schemas.update_single_user) == result.json()
    assert result.json()["job"] == "AQA"
    assert result.json()["name"] == "JohnDoeQA"


def test_login_single_user_successful(reqres):
    login_user: Response = reqres.post(
        url="api/login",
        json=
        {
            "email": "eve.holt@reqres.in",
            "password": "0812"
        }
    )
    assert login_user.status_code == 200
    assert S(schemas.login_single_user_successful) == login_user.json()
    assert len(login_user.json()["token"]) == 17


def test_login_user_unsuccessful(reqres):
    login_user: Response = reqres.post(
        url="api/login",
        json=
        {
            "email": "eve.holt@reqres.in"
        }
    )
    assert login_user.status_code == 400
    assert S(schemas.login_single_user_unsuccessful) == login_user.json()
    assert login_user.json()["error"] == "Missing password"