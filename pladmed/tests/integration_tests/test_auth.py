from pladmed.routes.routes import ERROR_TYPE_EMAIL_ALREADY_REGISTERED
from pladmed.validators.route_validator import ERROR_TYPE_INVALID_EMAIL, ERROR_TYPE_INVALID_PWD, ERROR_TYPE_MISSING_EMAIL, ERROR_TYPE_MISSING_PWD
import unittest
from pladmed.tests.integration_tests.test_base import BaseTest
import json


class AuthenticationTest(BaseTest):
    def test_register_user(self):
        res = self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_Password1"
        ))

        self.assertEqual(res.status_code, 201)

    def test_register_user_returns_email(self):
        res = self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_Password1"
        ))

        data = json.loads(res.data)

        self.assertEqual(data["email"], "agustin@gmail.com")

    def test_register_user_returns_id(self):
        res = self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_Password1"
        ))

        data = json.loads(res.data)

        self.assertEqual("_id" in data, True)

    def test_register_user_doesnt_return_password(self):
        res = self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_Password1"
        ))

        data = json.loads(res.data)

        self.assertEqual("password" in data, False)

    def test_register_should_have_email(self):
        res = self.client.post('/register', json=dict(
            password="secure_Password1"
        ))

        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertEqual(data["Type"], ERROR_TYPE_MISSING_EMAIL)

    def test_register_should_have_password(self):
        res = self.client.post('/register', json=dict(
            email="agustin@gmail.com"
        ))

        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertEqual(data["Type"], ERROR_TYPE_MISSING_PWD)

    def test_register_should_have_valid_email(self):
        res = self.client.post('/register', json=dict(
            email="foo",
            password="secure_Password1"
        ))

        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertEqual(data["Type"], ERROR_TYPE_INVALID_EMAIL)

    def test_register_should_have_strong_password(self):
        res = self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="weak_password"
        ))

        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertEqual(data["Type"], ERROR_TYPE_INVALID_PWD)

    def test_unique_users(self):
        self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_Password1"
        ))

        res = self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_Password1"
        ))

        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertEqual(data["Type"], ERROR_TYPE_EMAIL_ALREADY_REGISTERED)

    def test_login_user_correctly(self):
        self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_Password1"
        ))

        res = self.client.post('/login', json=dict(
            email="agustin@gmail.com",
            password="secure_Password1"
        ))

        self.assertEqual(res.status_code, 200)

    def test_login_user_requires_email(self):

        res = self.client.post('/login', json=dict(
            password="secure_Password1"
        ))

        self.assertEqual(res.status_code, 400)

    def test_login_user_requires_password(self):

        res = self.client.post('/login', json=dict(
            email="agustin@gmail.com"
        ))

        self.assertEqual(res.status_code, 400)

    def test_login_fails_no_user_exists(self):
        res = self.client.post('/login', json=dict(
            email="agustin2@gmail.com",
            password="secure_Password1"
        ))

        self.assertEqual(res.status_code, 404)

    def test_login_user_fails_invalid_password(self):
        self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_Password1"
        ))

        res = self.client.post('/login', json=dict(
            email="agustin@gmail.com",
            password="not_my_password"
        ))

        self.assertEqual(res.status_code, 404)

    def test_login_user_correctly_returns_token(self):
        self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_Password1"
        ))

        res = self.client.post('/login', json=dict(
            email="agustin@gmail.com",
            password="secure_Password1"
        ))

        data = json.loads(res.data)

        self.assertEqual("access_token" in data, True)

    def test_register_user_creates_without_credits(self):
        res = self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_Password1"
        ))

        user = self.app.db.users.find_user("agustin@gmail.com")

        self.assertEqual(user.credits, 0)

    def test_register_user_creates_without_superuser(self):
        res = self.client.post('/register', json=dict(
            email="agustin@gmail.com",
            password="secure_Password1"
        ))

        user = self.app.db.users.find_user("agustin@gmail.com")

        self.assertEqual(user.is_superuser, False)
