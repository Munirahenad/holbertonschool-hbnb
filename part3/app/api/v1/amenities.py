#!/usr/bin/python3
"""Amenity endpoints (placeholder for Part 3 tasks)."""

from flask_restx import Namespace, Resource

api = Namespace("amenities", description="Amenity operations")


@api.route("/health")
class AmenitiesHealth(Resource):
    def get(self):
        return {"status": "ok", "resource": "amenities"}, 200
