#!/usr/bin/python3
#Amaal-Asiri
"""Review API endpoints - Task 5"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("reviews", description="Review operations")

# ============= Models =============

review_model = api.model("Review", {
    "text": fields.String(required=True, description="Text of the review"),
    "rating": fields.Integer(required=True, description="Rating (1-5)"),
    "user_id": fields.String(required=True, description="ID of the user"),
    "place_id": fields.String(required=True, description="ID of the place"),
})

review_update_model = api.model("ReviewUpdate", {
    "text": fields.String(required=True, description="Text of the review"),
    "rating": fields.Integer(required=True, description="Rating (1-5)"),
})

review_response_model = api.model("ReviewResponse", {
    "id": fields.String(description="Review ID"),
    "text": fields.String(description="Text of the review"),
    "rating": fields.Integer(description="Rating (1-5)"),
    "user_id": fields.String(description="ID of the user"),
    "place_id": fields.String(description="ID of the place"),
    "created_at": fields.String(description="Creation timestamp"),
    "updated_at": fields.String(description="Last update timestamp"),
})

# ============= Endpoints =============

@api.route("/")
class ReviewList(Resource):
    """Review collection resource"""

    @api.doc("create_review")
    @api.expect(review_model, validate=True)
    @api.response(201, "Review successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "User or Place not found")
    def post(self):
        """Create a new review"""
        review_data = api.payload

        # Validate user exists
        user = facade.get_user(review_data.get("user_id"))
        if not user:
            return {"error": "User not found"}, 404

        # Validate place exists
        place = facade.get_place(review_data.get("place_id"))
        if not place:
            return {"error": "Place not found"}, 404

        # Business rule: user cannot review their own place
        if place.owner.id == user.id:
            return {"error": "You cannot review your own place"}, 400

        # Business rule: user cannot review the same place twice
        existing = facade.get_review_by_user_and_place(
            review_data["user_id"], review_data["place_id"]
        )
        if existing:
            return {"error": "You have already reviewed this place"}, 400

        try:
            review = facade.create_review(review_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        return _review_to_dict(review), 201

    @api.doc("list_reviews")
    @api.response(200, "List of reviews retrieved successfully")
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [_review_to_dict(r) for r in reviews], 200


@api.route("/<string:review_id>")
@api.param("review_id", "The review identifier")
class ReviewResource(Resource):
    """Review item resource"""

    @api.doc("get_review")
    @api.response(200, "Review details retrieved successfully")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return _review_to_dict(review), 200

    @api.doc("update_review")
    @api.expect(review_update_model, validate=True)
    @api.response(200, "Review updated successfully")
    @api.response(404, "Review not found")
    @api.response(400, "Invalid input data")
    def put(self, review_id):
        """Update a review's information"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        try:
            updated_review = facade.update_review(review_id, api.payload)
        except ValueError as e:
            return {"error": str(e)}, 400

        if not updated_review:
            return {"error": "Review not found"}, 404

        return {"message": "Review updated successfully"}, 200

    @api.doc("delete_review")
    @api.response(200, "Review deleted successfully")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200


@api.route("/places/<string:place_id>/reviews")
@api.param("place_id", "The place identifier")
class PlaceReviewList(Resource):
    """Reviews for a specific place"""

    @api.doc("get_reviews_by_place")
    @api.response(200, "List of reviews for the place retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [_review_to_dict(r) for r in reviews], 200


# ============= Helper =============

def _review_to_dict(review) -> dict:
    """Serialize a review object to dict."""
    return {
        "id": review.id,
        "text": review.comment,
        "rating": review.rating,
        "user_id": review.user.id if review.user else None,
        "place_id": review.place.id if review.place else None,
        "created_at": review.created_at.isoformat(),
        "updated_at": review.updated_at.isoformat(),
    }
