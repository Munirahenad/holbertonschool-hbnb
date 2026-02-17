from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ------------------ USERS ------------------
    def create_user(self, user_data):
        if "email" not in user_data or "first_name" not in user_data or "last_name" not in user_data:
            return None
        if self.get_user_by_email(user_data["email"]):
            return None
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if "email" in user_data and user_data["email"] != user.email:
            existing = self.get_user_by_email(user_data["email"])
            if existing and existing.id != user_id:
                raise ValueError("Email already registered")
        for field in ("first_name", "last_name", "email"):
            if field in user_data:
                setattr(user, field, user_data[field])
        user.save()
        self.user_repo.update(user_id, user)
        return user

    # ------------------ AMENITIES ------------------
    def create_amenity(self, amenity_data):
        if "name" not in amenity_data:
            return None
        amenity = Amenity(
            name=amenity_data.get("name"),
            description=amenity_data.get("description", "")
        )
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        if "name" in amenity_data:
            amenity.name = amenity_data["name"]
        if "description" in amenity_data:
            amenity.description = amenity_data["description"]
        amenity.save()
        self.amenity_repo.update(amenity_id, amenity)
        return amenity

    # ------------------ PLACES ------------------
    def create_place(self, place_data):
        owner_id = place_data.get("owner_id")
        if not self.get_user(owner_id):
            return None  # owner does not exist

        # amenities
        amenities_ids = place_data.get("amenity_ids", [])
        amenities = []
        for amenity_id in amenities_ids:
            amenity = self.get_amenity(amenity_id)
            if not amenity:
                return None
            amenities.append(amenity)

        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description", ""),
            owner_id=owner_id,
            latitude=place_data.get("latitude", 0.0),
            longitude=place_data.get("longitude", 0.0),
            price=place_data.get("price", 0.0),
            amenities=amenities
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        for field in ("title", "description", "latitude", "longitude", "price"):
            if field in place_data:
                setattr(place, field, place_data[field])
        if "amenity_ids" in place_data:
            amenities = []
            for amenity_id in place_data["amenity_ids"]:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    amenities.append(amenity)
            place.amenities = amenities
        place.save()
        self.place_repo.update(place_id, place)
        return place

    # ------------------ REVIEWS ------------------
    def create_review(self, review_data):
        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")
        if not self.get_user(user_id) or not self.get_place(place_id):
            return None
        if self.get_review_by_user_and_place(user_id, place_id):
            return None
        review = Review(
            text=review_data.get("text"),
            rating=review_data.get("rating"),
            user_id=user_id,
            place_id=place_id
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        if "text" in review_data:
            review.text = review_data["text"]
        if "rating" in review_data:
            review.rating = review_data["rating"]
        review.save()
        self.review_repo.update(review_id, review)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True

    def get_review_by_user_and_place(self, user_id, place_id):
        for review in self.review_repo.get_all():
            if review.user_id == user_id and review.place_id == place_id:
                return review
        return None
