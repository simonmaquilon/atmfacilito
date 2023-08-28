from app import app
import json


class TestLogin:
    def app_status(self):
        response = app.test_client().get("/")

        assert response.status_code == 200

    def test_user_login(client):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        formdata = {"username": "test", "password": "abc123"}

        response = app.test_client().post(
            "http://127.0.0.1:3000/login/", data=formdata, headers=headers
        )

        assert response.status_code == 200
