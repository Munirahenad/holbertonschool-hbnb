#!/usr/bin/python3
"""Auth endpoints (placeholder for Task 2)."""

from flask_restx import Namespace, Resource

api = Namespace("auth", description="Authentication operations")


@api.route("/health")
class AuthHealth(Resource):
    def get(self):
        return {"status": "ok", "resource": "auth"}, 200
