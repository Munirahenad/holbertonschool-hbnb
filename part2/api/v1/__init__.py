from flask import Blueprint
from flask_restx import Api

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")

api = Api(
    api_v1_bp,
    title="HBnB API",
    version="1.0",
    doc="/docs",
    description="HBnB Evolution - Part 2"
)
