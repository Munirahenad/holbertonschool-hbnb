#!/usr/bin/python3
"""API package - registers all v1 namespaces"""

from flask_restx import Api

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
# auth namespace will be added later in Task 2
# from app.api.v1.auth import api as auth_ns


def create_api(app):
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/",
    )

    api.add_namespace(users_ns, path="/api/v1/users")
    api.add_namespace(amenities_ns, path="/api/v1/amenities")
    api.add_namespace(places_ns, path="/api/v1/places")
    api.add_namespace(reviews_ns, path="/api/v1/reviews")
    # api.add_namespace(auth_ns, path="/api/v1/auth")

    return api
