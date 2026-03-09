PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS place_amenity;
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS places;
DROP TABLE IF EXISTS amenities;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id TEXT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(128) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE amenities (
    id TEXT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(200),
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);

CREATE TABLE places (
    id TEXT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL CHECK (price > 0),
    latitude FLOAT NOT NULL CHECK (latitude >= -90 AND latitude <= 90),
    longitude FLOAT NOT NULL CHECK (longitude >= -180 AND longitude <= 180),
    owner_id TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE reviews (
    id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    user_id TEXT NOT NULL,
    place_id TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE
);

CREATE TABLE place_amenity (
    place_id TEXT NOT NULL,
    amenity_id TEXT NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);
