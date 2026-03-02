#!/usr/bin/python3
"""HBnB Part 3 configuration module"""

import os


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)

    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development configuration (SQLite)."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///instance/hbnb_dev.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    """Production configuration (MySQL in production)."""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
