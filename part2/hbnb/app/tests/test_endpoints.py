#!/usr/bin/python3
#Amaal-Asiri
"""
Unit Tests for HBnB API Endpoints - Task 6
Covers: Users, Places, Reviews, Amenities
"""

import unittest
import uuid
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    """Test suite for User endpoints"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # ============= POST /api/v1/users/ =============

    def test_create_user_success(self):
        """Create a valid user - expects 201"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["first_name"], "Jane")
        self.assertEqual(data["email"], "jane.doe@example.com")
        self.assertNotIn("password", data)

    def test_create_user_empty_first_name(self):
        """Empty first_name - expects 400"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "test1@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_last_name(self):
        """Empty last_name - expects 400"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "",
            "email": "test2@example.com",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_invalid_email(self):
        """Invalid email format - expects 400"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "invalid-email",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        """Duplicate email - expects 400"""
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "duplicate@example.com",
            "password": "password123"
        }
        self.client.post('/api/v1/users/', json=payload)
        response = self.client.post('/api/v1/users/', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_create_user_short_password(self):
        """Password under 8 chars - expects 400"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "shortpass@example.com",
            "password": "123"
        })
        self.assertEqual(response.status_code, 400)

    # ============= GET /api/v1/users/ =============

    def test_get_all_users(self):
        """Retrieve list of users - expects 200"""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    # ============= GET /api/v1/users/<id> =============

    def test_get_user_by_id_success(self):
        """Get existing user by ID - expects 200"""
        post = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.smith@example.com",
            "password": "password123"
        })
        user_id = post.get_json()["id"]
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], user_id)

    def test_get_user_not_found(self):
        """Get non-existent user - expects 404"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    # ============= PUT /api/v1/users/<id> =============

    def test_update_user_success(self):
        """Update existing user - expects 200"""
        post = self.client.post('/api/v1/users/', json={
            "first_name": "Old",
            "last_name": "Name",
            "email": "update.user@example.com",
            "password": "password123"
        })
        user_id = post.get_json()["id"]
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "New",
            "last_name": "Name",
            "email": "update.user@example.com"
        })
        self.assertEqual(response.status_code, 200)

    def test_update_user_not_found(self):
        """Update non-existent user - expects 404"""
        response = self.client.put('/api/v1/users/nonexistent-id', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane@example.com"
        })
        self.assertEqual(response.status_code, 404)


class TestAmenityEndpoints(unittest.TestCase):
    """Test suite for Amenity endpoints"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # ============= POST /api/v1/amenities/ =============

    def test_create_amenity_success(self):
        """Create valid amenity - expects 201"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi",
            "description": "High-speed internet"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Wi-Fi")

    def test_create_amenity_empty_name(self):
        """Empty name - expects 400"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "",
            "description": "No name"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_name_too_long(self):
        """Name over 50 chars - expects 400"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "A" * 51,
            "description": "Too long"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_missing_name(self):
        """Missing name field - expects 400"""
        response = self.client.post('/api/v1/amenities/', json={
            "description": "No name provided"
        })
        self.assertEqual(response.status_code, 400)

    # ============= GET /api/v1/amenities/ =============

    def test_get_all_amenities(self):
        """Retrieve list of amenities - expects 200"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    # ============= GET /api/v1/amenities/<id> =============

    def test_get_amenity_by_id_success(self):
        """Get existing amenity by ID - expects 200"""
        post = self.client.post('/api/v1/amenities/', json={
            "name": "Pool",
            "description": "Outdoor pool"
        })
        amenity_id = post.get_json()["id"]
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], amenity_id)

    def test_get_amenity_not_found(self):
        """Get non-existent amenity - expects 404"""
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    # ============= PUT /api/v1/amenities/<id> =============

    def test_update_amenity_success(self):
        """Update existing amenity - expects 200"""
        post = self.client.post('/api/v1/amenities/', json={
            "name": "Parking",
            "description": "Free parking"
        })
        amenity_id = post.get_json()["id"]
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "Paid Parking",
            "description": "Paid parking lot"
        })
        self.assertEqual(response.status_code, 200)

    def test_update_amenity_not_found(self):
        """Update non-existent amenity - expects 404"""
        response = self.client.put('/api/v1/amenities/nonexistent-id', json={
            "name": "Pool"
        })
        self.assertEqual(response.status_code, 404)


class TestPlaceEndpoints(unittest.TestCase):
    """Test suite for Place endpoints"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        unique_email = f"owner.place.{uuid.uuid4()}@example.com"
        res = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": unique_email,
            "password": "password123"
        })
        self.owner_id = res.get_json()["id"]

        res = self.client.post('/api/v1/amenities/', json={
            "name": "Wi-Fi",
            "description": "Wireless internet"
        })
        self.amenity_id = res.get_json()["id"]

    def _valid_place(self, **overrides):
        data = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id,
            "amenities": []
        }
        data.update(overrides)
        return data

    # ============= POST /api/v1/places/ =============

    def test_create_place_success(self):
        """Create valid place - expects 201"""
        response = self.client.post('/api/v1/places/', json=self._valid_place())
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], "Cozy Apartment")

    def test_create_place_empty_title(self):
        """Empty title - expects 400"""
        response = self.client.post('/api/v1/places/', json=self._valid_place(title=""))
        self.assertEqual(response.status_code, 400)

    def test_create_place_negative_price(self):
        """Negative price - expects 400"""
        response = self.client.post('/api/v1/places/', json=self._valid_place(price=-50.0))
        self.assertEqual(response.status_code, 400)

    def test_create_place_zero_price(self):
        """Zero price - expects 400"""
        response = self.client.post('/api/v1/places/', json=self._valid_place(price=0))
        self.assertEqual(response.status_code, 400)

    def test_create_place_latitude_too_high(self):
        """Latitude > 90 - expects 400"""
        response = self.client.post('/api/v1/places/', json=self._valid_place(latitude=91.0))
        self.assertEqual(response.status_code, 400)

    def test_create_place_latitude_too_low(self):
        """Latitude < -90 - expects 400"""
        response = self.client.post('/api/v1/places/', json=self._valid_place(latitude=-91.0))
        self.assertEqual(response.status_code, 400)

    def test_create_place_longitude_too_high(self):
        """Longitude > 180 - expects 400"""
        response = self.client.post('/api/v1/places/', json=self._valid_place(longitude=181.0))
        self.assertEqual(response.status_code, 400)

    def test_create_place_longitude_too_low(self):
        """Longitude < -180 - expects 400"""
        response = self.client.post('/api/v1/places/', json=self._valid_place(longitude=-181.0))
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_owner(self):
        """Non-existent owner_id - expects 404"""
        response = self.client.post('/api/v1/places/', json=self._valid_place(owner_id="nonexistent-id"))
        self.assertEqual(response.status_code, 404)

    def test_create_place_invalid_amenity(self):
        """Non-existent amenity ID - expects 404"""
        response = self.client.post('/api/v1/places/', json=self._valid_place(
            amenities=["nonexistent-amenity-id"]
        ))
        self.assertEqual(response.status_code, 404)

    # ============= GET /api/v1/places/ =============

    def test_get_all_places(self):
        """Retrieve list of places - expects 200"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    # ============= GET /api/v1/places/<id> =============

    def test_get_place_by_id_includes_owner_and_amenities(self):
        """Get place includes owner and amenities - expects 200"""
        post = self.client.post('/api/v1/places/', json=self._valid_place())
        place_id = post.get_json()["id"]
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("owner", data)
        self.assertIn("amenities", data)
        self.assertIn("reviews", data)
        self.assertEqual(data["owner"]["id"], self.owner_id)

    def test_get_place_not_found(self):
        """Get non-existent place - expects 404"""
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    # ============= PUT /api/v1/places/<id> =============

    def test_update_place_success(self):
        """Update existing place - expects 200"""
        post = self.client.post('/api/v1/places/', json=self._valid_place())
        place_id = post.get_json()["id"]
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Luxury Condo",
            "description": "An upscale place",
            "price": 200.0
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "Place updated successfully")

    def test_update_place_not_found(self):
        """Update non-existent place - expects 404"""
        response = self.client.put('/api/v1/places/nonexistent-id', json={
            "title": "New Title", "price": 150.0
        })
        self.assertEqual(response.status_code, 404)

    def test_update_place_invalid_price(self):
        """Update with invalid price - expects 400"""
        post = self.client.post('/api/v1/places/', json=self._valid_place())
        place_id = post.get_json()["id"]
        response = self.client.put(f'/api/v1/places/{place_id}', json={"price": -100.0})
        self.assertEqual(response.status_code, 400)

    # ============= GET /api/v1/places/<id>/reviews =============

    def test_get_place_reviews_success(self):
        """Get reviews for a place - expects 200"""
        post = self.client.post('/api/v1/places/', json=self._valid_place())
        place_id = post.get_json()["id"]
        response = self.client.get(f'/api/v1/places/{place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_place_reviews_not_found(self):
        """Get reviews for non-existent place - expects 404"""
        response = self.client.get('/api/v1/places/nonexistent-id/reviews')
        self.assertEqual(response.status_code, 404)


class TestReviewEndpoints(unittest.TestCase):
    """Test suite for Review endpoints"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create owner
        unique_email = f"owner.review.{uuid.uuid4()}@example.com"
        res = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": unique_email,
            "password": "password123"
        })
        self.owner_id = res.get_json()["id"]

        # Create reviewer (different from owner)
        unique_email = f"reviewer.test.{uuid.uuid4()}@example.com"
        res = self.client.post('/api/v1/users/', json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": unique_email,
            "password": "password123"
        })
        self.reviewer_id = res.get_json()["id"]

        # Create place
        res = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A place for reviews",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id,
            "amenities": []
        })
        self.place_id = res.get_json()["id"]

    def _valid_review(self, **overrides):
        data = {
            "text": "Great place to stay!",
            "rating": 4,
            "user_id": self.reviewer_id,
            "place_id": self.place_id
        }
        data.update(overrides)
        return data

    # ============= POST /api/v1/reviews/ =============

    def test_create_review_success(self):
        """Create valid review - expects 201"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review())
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn("id", data)
        self.assertEqual(data["rating"], 4)
        self.assertEqual(data["text"], "Great place to stay!")

    def test_create_review_empty_text(self):
        """Empty text - expects 400"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(text=""))
        self.assertEqual(response.status_code, 400)

    def test_create_review_rating_below_range(self):
        """Rating < 1 - expects 400"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(rating=0))
        self.assertEqual(response.status_code, 400)

    def test_create_review_rating_above_range(self):
        """Rating > 5 - expects 400"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(rating=6))
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user(self):
        """Non-existent user_id - expects 404"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(
            user_id="nonexistent-id"
        ))
        self.assertEqual(response.status_code, 404)

    def test_create_review_invalid_place(self):
        """Non-existent place_id - expects 404"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(
            place_id="nonexistent-id"
        ))
        self.assertEqual(response.status_code, 404)

    def test_create_review_own_place(self):
        """Owner reviews own place - expects 400"""
        response = self.client.post('/api/v1/reviews/', json=self._valid_review(
            user_id=self.owner_id
        ))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_create_review_duplicate(self):
        """Same user reviews same place twice - expects 400"""
        self.client.post('/api/v1/reviews/', json=self._valid_review())
        response = self.client.post('/api/v1/reviews/', json=self._valid_review())
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    # ============= GET /api/v1/reviews/ =============

    def test_get_all_reviews(self):
        """Retrieve list of reviews - expects 200"""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    # ============= GET /api/v1/reviews/<id> =============

    def test_get_review_by_id_success(self):
        """Get existing review - expects 200"""
        post = self.client.post('/api/v1/reviews/', json=self._valid_review())
        review_id = post.get_json()["id"]
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], review_id)
        self.assertIn("user_id", data)
        self.assertIn("place_id", data)

    def test_get_review_not_found(self):
        """Get non-existent review - expects 404"""
        response = self.client.get('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    # ============= PUT /api/v1/reviews/<id> =============

    def test_update_review_success(self):
        """Update existing review - expects 200"""
        post = self.client.post('/api/v1/reviews/', json=self._valid_review())
        review_id = post.get_json()["id"]
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Amazing stay!",
            "rating": 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "Review updated successfully")

    def test_update_review_empty_text(self):
        """Update with empty text - expects 400"""
        post = self.client.post('/api/v1/reviews/', json=self._valid_review())
        review_id = post.get_json()["id"]
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "",
            "rating": 4
        })
        self.assertEqual(response.status_code, 400)

    def test_update_review_invalid_rating(self):
        """Update with invalid rating - expects 400"""
        post = self.client.post('/api/v1/reviews/', json=self._valid_review())
        review_id = post.get_json()["id"]
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Some text",
            "rating": 10
        })
        self.assertEqual(response.status_code, 400)

    def test_update_review_not_found(self):
        """Update non-existent review - expects 404"""
        response = self.client.put('/api/v1/reviews/nonexistent-id', json={
            "text": "Some text",
            "rating": 3
        })
        self.assertEqual(response.status_code, 404)

    # ============= DELETE /api/v1/reviews/<id> =============

    def test_delete_review_success(self):
        """Delete existing review - expects 200"""
        post = self.client.post('/api/v1/reviews/', json=self._valid_review())
        review_id = post.get_json()["id"]
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["message"], "Review deleted successfully")

    def test_delete_review_not_found(self):
        """Delete non-existent review - expects 404"""
        response = self.client.delete('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_delete_review_then_get(self):
        """Delete review then try to get it - expects 404"""
        post = self.client.post('/api/v1/reviews/', json=self._valid_review())
        review_id = post.get_json()["id"]
        self.client.delete(f'/api/v1/reviews/{review_id}')
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
