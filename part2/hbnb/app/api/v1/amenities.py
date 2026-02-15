#!/usr/bin/python3
"""Amenity API endpoints - Task 3"""

from flask_restx import Namespace, Resource, fields
from flask import request

from app.services.facade import HBnBFacade


api = Namespace("amenities", description="Amenity operations")
facade = HBnBFacade()


# ============= Models for API documentation =============

amenity_model = api.model("Amenity", {
    "id": fields.String(description="Amenity ID"),
    "name": fields.String(required=True, description="Amenity name"),
    "created_at": fields.String(description="Creation timestamp"),
    "updated_at": fields.String(description="Last update timestamp"),
})

amenity_create_model = api.model("AmenityCreate", {
    "name": fields.String(required=True, description="Amenity name"),
})


# ============= Endpoints =============

@api.route("/")
class AmenityList(Resource):
    """Amenity collection resource"""

    @api.doc("list_amenities")
    @api.response(200, "List of amenities retrieved successfully")
    @api.marshal_list_with(amenity_model)
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities]

    @api.doc("create_amenity")
    @api.expect(amenity_create_model)
    @api.response(201, "Amenity successfully created")
    @api.response(400, "Invalid input data")
    @api.marshal_with(amenity_model, code=201)
    def post(self):
        """Register a new amenity"""
        amenity_data = request.json
        amenity = facade.create_amenity(amenity_data)
        return amenity.to_dict(), 201


@api.route("/<string:amenity_id>")
@api.param("amenity_id", "The amenity identifier")
@api.response(404, "Amenity not found")
class AmenityResource(Resource):
    """Amenity item resource"""

    @api.doc("get_amenity")
    @api.response(200, "Amenity details retrieved successfully")
    @api.marshal_with(amenity_model)
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, f"Amenity {amenity_id} not found")
        return amenity.to_dict()

    @api.doc("update_amenity")
    @api.expect(amenity_create_model)
    @api.response(200, "Amenity updated successfully")
    @api.response(400, "Invalid input data")
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = request.json
        amenity = facade.update_amenity(amenity_id, amenity_data)
        if not amenity:
            api.abort(404, f"Amenity {amenity_id} not found")
        return {"message": "Amenity updated successfully"}, 200
