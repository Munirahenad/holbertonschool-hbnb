#!/usr/bin/python3
"""User endpoints (placeholder for Part 3 tasks)."""

from flask_restx import Namespace, Resource

api = Namespace("users", description="User operations")


@api.route("/health")
class UsersHealth(Resource):
    def get(self):
        return {"status": "ok", "resource": "users"}, 200
