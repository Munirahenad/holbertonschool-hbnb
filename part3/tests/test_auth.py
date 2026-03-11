import unittest
from app import create_app, db
from app.models.user import User


class TestAuthEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("config.TestingConfig")
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.drop_all()
            db.create_all()

            user = User(
                first_name="Test",
                last_name="User",
                email="test@example.com"
            )
            user.hash_password("password123")
            db.session.add(user)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_missing_fields(self):
        response = self.client.post(
            "/api/v1/auth/login",
            json={},
            content_type="application/json"
        )
        self.assertIn(response.status_code, [400, 422])

    def test_login_invalid_credentials(self):
        response = self.client.post(
            "/api/v1/auth/login",
            json={
                "email": "wrong@example.com",
                "password": "wrongpass"
            },
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.get_json(), {"error": "Invalid credentials"})

    def test_login_valid_credentials(self):
        response = self.client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            },
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)
        data = response.get_json()
        self.assertIn("access_token", data)


if __name__ == "__main__":
    unittest.main()
