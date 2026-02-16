#!/usr/bin/python3
"""Place API endpoints - Task 4 + Task 5 updates"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("places", description="Place operations")

# ============= Related Models =============

amenity_model = api.model("PlaceAmenity", {
    "id": fields.String(description="Amenity ID"),
    "name": fields.String(description="Name of the amenity"),
})

user_model = api.model("PlaceUser", {
    "id": fields.String(description="User ID"),
    "first_name": fields.String(description="First name of the owner"),
    "last_name": fields.String(description="Last name of the owner"),
    "email": fields.String(description="Email of the owner"),
})

review_model = api.model("PlaceReview", {
    "id": fields.String(description="Review ID"),
    "text": fields.String(description="Text of the review"),
    "rating": fields.Integer(description="Rating of the place (1-5)"),
    "user_id": fields.String(description="ID of the user"),
})

# ============= Place Input Model =============

place_model = api.model("Place", {
    "title": fields.String(required=True, description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(required=True, description="Price per night"),
    "latitude": fields.Float(required=True, description="Latitude of the place"),
    "longitude": fields.Float(required=True, description="Longitude of the place"),
    "owner_id": fields.String(required=True, description="ID of the owner"),
    "owner": fields.Nested(user_model, description="Owner of the place"),
    "amenities": fields.List(
        fields.Nested(amenity_model), description="List of amenities"
    ),
    "reviews": fields.List(
        fields.Nested(review_model), description="List of reviews"
    ),
})

# ============= Endpoints =============

@api.route("/")
class PlaceList(Resource):
    """Place collection resource"""

    @api.doc("create_place")
    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "Owner not found")
    def post(self):
        """Register a new place"""
        place_data = api.payload

        # Validate owner exists
        owner = facade.get_user(place_data.get("owner_id"))
        if not owner:
            return {"error": "Owner not found"}, 404

        amenity_ids = place_data.get("amenities", [])
        if amenity_ids and isinstance(amenity_ids[0], dict):
            amenity_ids = [a["id"] for a in amenity_ids]

        amenities = []
        for amenity_id in amenity_ids:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {"error": f"Amenity {amenity_id} not found"}, 404
            amenities.append(amenity)

        try:
            place = facade.create_place(place_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        for amenity in amenities:
            place.add_amenity(amenity)

        return place.to_dict(), 201

    @api.doc("list_places")
    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [
            {
                "id": p.id,
                "title": p.title,
                "latitude": p.latitude,
                "longitude": p.longitude,
            }
            for p in places
        ], 200


@api.route("/<place_id>")
@api.param("place_id", "The place identifier")
class PlaceResource(Resource):
    """Place item resource"""

    @api.doc("get_place")
    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place details by ID including owner and amenities"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": place.owner.id,
                "first_name": place.owner.first_name,
                "last_name": place.owner.last_name,
                "email": place.owner.email,
            },
            "amenities": [
                {"id": a.id, "name": a.name}
                for a in place.amenities
            ],
            "reviews": [
                {
                    "id": r.id,
                    "text": r.text,
                    "rating": r.rating,
                    "user_id": r.user.id if r.user else None,
                }
                for r in reviews
            ],
        }, 200

    @api.doc("update_place")
    @api.expect(place_model, validate=False)
    @api.response(200, "Place updated successfully")
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    def put(self, place_id):
        """Update a place's information"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        place_data = api.payload

        if "owner_id" in place_data:
            owner = facade.get_user(place_data["owner_id"])
            if not owner:
                return {"error": "Owner not found"}, 404

        if "amenities" in place_data:
            amenity_ids = place_data["amenities"]
            if amenity_ids and isinstance(amenity_ids[0], dict):
                amenity_ids = [a["id"] for a in amenity_ids]
            for amenity_id in amenity_ids:
                if not facade.get_amenity(amenity_id):
                    return {"error": f"Amenity {amenity_id} not found"}, 404

        try:
            updated_place = facade.update_place(place_id, place_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        if not updated_place:
            return {"error": "Place not found"}, 404

        return {"message": "Place updated successfully"}, 200


# ============= Reviews for a Place (Task 5) =============
# Must be in places.py to keep correct route under places namespace

@api.route("/<place_id>/reviews")
@api.param("place_id", "The place identifier")
class PlaceReviewList(Resource):
    """Reviews for a specific place"""

    @api.doc("get_place_reviews")
    @api.response(200, "List of reviews for the place retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
            }
            for r in reviews
        ], 200
