Task 1: Detailed Class Diagram for Business Logic Layer

Overview
This diagram represents the Business Logic layer of the HBnB application, illustrating the main entities, their attributes, methods, and relationships.

Business Rules Summary

All entities use UUID4 as a unique identifier.

Creation and update timestamps are tracked.

Relationships ensure data integrity.

Entities validate data before persistence.










1. User Entity – Attributes & Methods

Attributes:

id (UUID4): Primary Key, unique, auto-generated

first_name (String, max 50): Not null, minimum 2 characters

last_name (String, max 50): Not null, minimum 2 characters

email (String, max 120): Unique, not null, must follow email format

password_hash (String, 128): Not null, stored as hashed password

is_admin (Boolean): Default false, indicates administrative privileges

created_at (DateTime): Auto-generated account creation timestamp

updated_at (DateTime): Auto-updated last modification timestamp

Methods:

register(): Creates a new user account with validation

update_profile(data): Updates user information

authenticate(password): Verifies password against hash

hash_password(password): Generates bcrypt hash

add_place(place): Associates a place owned by the user

add_review(review): Associates a review written by the user

to_dict(): Serializes user object to dictionary

Business Rules:

Email must be unique across all users

Password must always be hashed before storage

Users can own multiple places

Users can write multiple reviews

Admin status affects system permissions

2. Place Entity – Attributes & Methods

Attributes:

id (UUID4): Primary Key, unique, auto-generated

title (String, max 100): Not null, minimum 5 characters

description (Text, max 1000): Not null

price (Decimal, 10,2): Not null, greater than 0

latitude (Float): Not null, range -90 to 90

longitude (Float): Not null, range -180 to 180

owner_id (UUID4): Foreign Key → User.id

created_at (DateTime): Auto-generated listing creation timestamp

updated_at (DateTime): Auto-updated last modification timestamp

Methods:

add_amenity(amenity): Associates amenity with place

remove_amenity(amenity): Removes amenity association

get_amenities(): Returns list of amenities

add_review(review): Associates a new review

calculate_average_rating(): Computes average from all reviews

validate_coordinates(): Ensures valid latitude and longitude

validate_price(): Ensures price is positive

to_dict(): Serializes place object to dictionary

Business Rules:

Each place must have exactly one owner

Price must be positive

Coordinates must be valid

Places can have zero or more amenities

Places can have zero or more reviews

Average rating is calculated from all reviews

3. Review Entity – Attributes & Methods

Attributes:

id (UUID4): Primary Key, unique, auto-generated

place_id (UUID4): Foreign Key → Place.id

user_id (UUID4): Foreign Key → User.id

rating (Integer): Not null, range 1-5

comment (Text, max 500): Not null

created_at (DateTime): Auto-generated review timestamp

updated_at (DateTime): Auto-updated last modification timestamp

Methods:

validate_rating(): Ensures rating is between 1-5

update_review(rating, comment): Updates existing review

get_place(): Returns associated place

get_user(): Returns associated user

to_dict(): Serializes review object to dictionary

Business Rules:

Each review is associated with exactly one place

Each review is written by exactly one user

Users can review multiple places

One user can review the same place multiple times (update existing review)

Rating must be integer 1-5

4. Amenity Entity – Attributes & Methods

Attributes:

id (UUID4): Primary Key, unique, auto-generated

name (String, max 50): Not null, unique

description (Text, max 200): Optional

created_at (DateTime): Auto-generated creation timestamp

updated_at (DateTime): Auto-updated last modification timestamp

Methods:

update_details(data): Updates amenity information

get_associated_places(): Returns all places with this amenity

to_dict(): Serializes amenity object to dictionary

Business Rules:

Amenity names must be unique

Amenities are reusable across multiple places

Deleting an amenity removes associations but not places

Multiple places can share the same amenity




5. Relationships Overview

User → Place: 1-to-many (user owns multiple places)

User → Review: 1-to-many (user writes multiple reviews)

Place → Review: 1-to-many (place receives multiple reviews)

Place ↔ Amenity: Many-to-many (through PlaceAmenity association)

6. Validation Rules

User: Email format, password strength, name length
Place: Title length, description length, positive price, valid coordinates
Review: Rating 1–5, comment length, user cannot review own place
Amenity: Name uniqueness, max description length

7. Example Scenarios

User creates an account, adds a place, adds amenities

Another user writes a review for that place

Place calculates average rating

8. Future Enhancements

Booking entity (User books Place for dates)

Payment entity (track transactions)

Location entity (City, Country hierarchy)

Image entity (multiple images per place)

Soft delete and versioning

Caching and search/filter features
