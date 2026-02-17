#!/usr/bin/python3
"""Amenity API endpoints - Task 3"""

from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import HBnBFacade

api = Namespace("amenities", description="Amenity operations")
facade = HBnBFacade()

# ============= Models =============

amenity_model = api.model("Amenity", {
    "id": fields.String(description="Amenity ID"),
    "name": fields.String(required=True, description="Amenity name"),
    "created_at": fields.String(description="Creation timestamp"),
    "updated_at": fields.String(description="Last update timestamp"),
})

amenity_create_model = api.model("AmenityCreate", {
    "name": fields.String(required=True, description="Amenity name"),
    "description": fields.String(description="Amenity description"),
})

# ============= Endpoints =============

@api.route("/")
class AmenityList(Resource):
    """Amenity collection resource"""

    @api.doc("list_amenities")
    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

    @api.doc("create_amenity")
    @api.expect(amenity_create_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new amenity"""
        amenity_data = request.json
        try:
            amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {"error": str(e)}, 400
        return amenity.to_dict(), 201


@api.route("/<string:amenity_id>")
@api.param("amenity_id", "The amenity identifier")
class AmenityResource(Resource):
    """Amenity item resource"""

    @api.doc("get_amenity")
    @api.response(200, "Amenity details retrieved successfully")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": f"Amenity {amenity_id} not found"}, 404
        return amenity.to_dict(), 200

    @api.doc("update_amenity")
    @api.expect(amenity_create_model, validate=False)
    @api.response(200, "Amenity updated successfully")
    @api.response(404, "Amenity not found")
    @api.response(400, "Invalid input data")
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = request.json
        try:
            amenity = facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            return {"error": str(e)}, 400
        if not amenity:
            return {"error": f"Amenity {amenity_id} not found"}, 404
        return {"message": "Amenity updated successfully"}, 200
