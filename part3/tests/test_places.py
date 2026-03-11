import unittest
from flask_jwt_extended import create_access_token
from app import create_app, db
from app.models.user import User
from app.models.place import Place


class TestPlaceEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("config.TestingConfig")
        cls.client = cls.app.test_client()

        with cls.app.app_context():
            db.drop_all()
            db.create_all()

            owner = User(
                first_name="Owner",
                last_name="User",
                email="owner@example.com",
                is_admin=False
            )
            owner.hash_password("ownerpass")

            other_user = User(
                first_name="Other",
                last_name="User",
                email="other@example.com",
                is_admin=False
            )
            other_user.hash_password("otherpass")

            admin = User(
                first_name="Admin",
                last_name="User",
                email="adminplace@example.com",
                is_admin=True
            )
            admin.hash_password("adminpass")

            db.session.add_all([owner, other_user, admin])
            db.session.commit()

            place = Place(
                title="Beach House",
                description="Beautiful beach house",
                price=150.0,
                latitude=25.0,
                longitude=45.0,
                owner_id=str(owner.id)
            )
            db.session.add(place)
            db.session.commit()

            cls.place_id = str(place.id)
            cls.owner_id = str(owner.id)
            cls.other_user_id = str(other_user.id)
            cls.admin_id = str(admin.id)

            cls.owner_token = create_access_token(
                identity=cls.owner_id,
                additional_claims={"is_admin": False}
            )
            cls.other_user_token = create_access_token(
                identity=cls.other_user_id,
                additional_claims={"is_admin": False}
            )
            cls.admin_token = create_access_token(
                identity=cls.admin_id,
                additional_claims={"is_admin": True}
            )

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_places_returns_200(self):
        response = self.client.get("/api/v1/places/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_nonexistent_place_returns_404(self):
        response = self.client.get("/api/v1/places/nonexistent-id")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Place not found"})

    def test_create_place_without_token_returns_401(self):
        response = self.client.post(
            "/api/v1/places/",
            json={
                "title": "Test Place",
                "description": "A test place",
                "price": 100.0,
                "latitude": 24.7,
                "longitude": 46.7
            },
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

    def test_create_place_with_token_returns_201(self):
        response = self.client.post(
            "/api/v1/places/",
            json={
                "title": "Created Place",
                "description": "Created by auth user",
                "price": 200.0,
                "latitude": 24.8,
                "longitude": 46.8
            },
            headers={"Authorization": f"Bearer {self.owner_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_update_place_by_non_owner_returns_403(self):
        response = self.client.put(
            f"/api/v1/places/{self.place_id}",
            json={"title": "Hacked Title"},
            headers={"Authorization": f"Bearer {self.other_user_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json(), {"error": "Unauthorized action"})

    def test_update_place_by_owner_returns_200(self):
        response = self.client.put(
            f"/api/v1/places/{self.place_id}",
            json={"title": "Updated by Owner"},
            headers={"Authorization": f"Bearer {self.owner_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_update_place_by_admin_returns_200(self):
        response = self.client.put(
            f"/api/v1/places/{self.place_id}",
            json={"title": "Updated by Admin"},
            headers={"Authorization": f"Bearer {self.admin_token}"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_place_by_non_owner_returns_403(self):
        response = self.client.delete(
            f"/api/v1/places/{self.place_id}",
            headers={"Authorization": f"Bearer {self.other_user_token}"}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.get_json(), {"error": "Unauthorized action"})


class TestPlaceModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app("config.TestingConfig")

    def test_place_creation(self):
        with self.app.app_context():
            place = Place(
                title="Beach House",
                description="Beautiful place",
                price=150.0,
                latitude=25.0,
                longitude=45.0,
                owner_id="test-owner-id"
            )
            self.assertEqual(place.title, "Beach House")
            self.assertEqual(place.price, 150.0)
            self.assertIsNotNone(place)


if __name__ == "__main__":
    unittest.main()
