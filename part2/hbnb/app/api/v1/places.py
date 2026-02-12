#!/usr/bin/python3
#Amaal-Asiri
"""Place API endpoints - Task 4"""

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

# ============= Place Models =============

place_model = api.model("Place", {
    "title": fields.String(required=True, description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(required=True, description="Price per night"),
    "latitude": fields.Float(required=True, description="Latitude of the place"),
    "longitude": fields.Float(required=True, description="Longitude of the place"),
    "owner_id": fields.String(required=True, description="ID of the owner"),
    "amenities": fields.List(
        fields.String, required=False, description="List of amenity IDs"
    ),
})

place_response_model = api.model("PlaceResponse", {
    "id": fields.String(description="Place ID"),
    "title": fields.String(description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(description="Price per night"),
    "latitude": fields.Float(description="Latitude of the place"),
    "longitude": fields.Float(description="Longitude of the place"),
    "owner_id": fields.String(description="ID of the owner"),
    "amenity_ids": fields.List(fields.String, description="List of amenity IDs"),
    "created_at": fields.String(description="Creation timestamp"),
    "updated_at": fields.String(description="Last update timestamp"),
})

place_detail_model = api.model("PlaceDetail", {
    "id": fields.String(description="Place ID"),
    "title": fields.String(description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(description="Price per night"),
    "latitude": fields.Float(description="Latitude of the place"),
    "longitude": fields.Float(description="Longitude of the place"),
    "owner": fields.Nested(user_model, description="Owner details"),
    "amenities": fields.List(
        fields.Nested(amenity_model), description="List of amenities"
    ),
    "created_at": fields.String(description="Creation timestamp"),
    "updated_at": fields.String(description="Last update timestamp"),
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

        # Validate amenities exist (if provided)
        amenity_ids = place_data.get("amenities", [])
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

        # Attach amenities
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


@api.route("/<string:place_id>")
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
            "created_at": place.created_at.isoformat(),
            "updated_at": place.updated_at.isoformat(),
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

        # If owner_id is being changed, validate new owner
        if "owner_id" in place_data:
            owner = facade.get_user(place_data["owner_id"])
            if not owner:
                return {"error": "Owner not found"}, 404

        # If amenities are being updated, validate them
        if "amenities" in place_data:
            amenity_ids = place_data["amenities"]
            new_amenities = []
            for amenity_id in amenity_ids:
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    return {"error": f"Amenity {amenity_id} not found"}, 404
                new_amenities.append(amenity)

        try:
            updated_place = facade.update_place(place_id, place_data)
        except ValueError as e:
            return {"error": str(e)}, 400

        if not updated_place:
            return {"error": "Place not found"}, 404

        return {"message": "Place updated successfully"}, 200
