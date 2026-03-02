#!/usr/bin/python3
"""Place endpoints (placeholder for Part 3 tasks)."""

from flask_restx import Namespace, Resource

api = Namespace("places", description="Place operations")


@api.route("/health")
class PlacesHealth(Resource):
    def get(self):
        return {"status": "ok", "resource": "places"}, 200
