#!/usr/bin/python3
"""Review endpoints (placeholder for Part 3 tasks)."""

from flask_restx import Namespace, Resource

api = Namespace("reviews", description="Review operations")


@api.route("/health")
class ReviewsHealth(Resource):
    def get(self):
        return {"status": "ok", "resource": "reviews"}, 200
