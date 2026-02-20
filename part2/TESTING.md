# HBnB Part 2 - Testing Documentation

## Overview

This document describes the testing strategy, validation implementation, and test execution results for the HBnB application API (Part 2). All endpoints have been thoroughly tested using both automated unit tests and manual black-box testing with cURL.

---

## Test Coverage Summary

| Entity | Unit Tests | Status |
|--------|-----------|--------|
| **User** | 10 tests | ✅ 10/10 passed |
| **Amenity** | 9 tests | ✅ 9/9 passed |
| **Place** | 18 tests | ✅ 18/18 passed |
| **Review** | 18 tests | ✅ 18/18 passed |
| **Total** | **56 tests** | ✅ **56/56 passed** |

**Test Execution Time:** ~3 seconds

---

## Validation Implementation

### 1. User Validation

**Location:** `app/models/user.py`

| Field | Validation Rules |
|-------|-----------------|
| `first_name` | Required, max 50 characters, not empty |
| `last_name` | Required, max 50 characters, not empty |
| `email` | Required, valid email format (regex), unique |
| `password` | Required, minimum 8 characters |

**Implementation:**
```python
@property
def email(self):
    return self._email

@email.setter
def email(self, value):
    if not value or not value.strip():
        raise ValueError("email is required")
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValueError("email must be a valid email address")
    self._email = value
```

### 2. Amenity Validation

**Location:** `app/models/amenity.py`

| Field | Validation Rules |
|-------|-----------------|
| `name` | Required, max 50 characters, not empty |
| `description` | Optional, max 200 characters |

### 3. Place Validation

**Location:** `app/models/place.py`

| Field | Validation Rules |
|-------|-----------------|
| `title` | Required, max 100 characters, not empty |
| `price` | Required, positive float, max 1,000,000 |
| `latitude` | Required, between -90 and 90 |
| `longitude` | Required, between -180 and 180 |
| `owner_id` | Required, must reference existing user |
| `amenities` | Optional, all IDs must reference existing amenities |

**Implementation:**
```python
@property
def price(self):
    return self._price

@price.setter
def price(self, value):
    if value is None or value <= 0:
        raise ValueError("price must be positive")
    if value > 1_000_000:
        raise ValueError("price must not exceed 1,000,000")
    self._price = float(value)
```

### 4. Review Validation

**Location:** `app/models/review.py`

| Field | Validation Rules |
|-------|-----------------|
| `text` | Required, max 500 characters, not empty |
| `rating` | Required, integer between 1 and 5 |
| `user_id` | Required, must reference existing user |
| `place_id` | Required, must reference existing place |

**Business Rules:**
- User cannot review their own place
- User cannot review the same place twice

**Implementation:**
```python
@property
def rating(self):
    return self._rating

@rating.setter
def rating(self, value):
    if not isinstance(value, int) or value < 1 or value > 5:
        raise ValueError("rating must be an integer between 1 and 5")
    self._rating = value
```

---

## Unit Tests

### Test File Location
`app/tests/test_endpoints.py`

### Test Structure

#### 1. User Endpoints Tests (10 tests)

```python
class TestUserEndpoints(unittest.TestCase):
```

**Tests:**
- ✅ `test_create_user_success` - Valid user creation returns 201
- ✅ `test_create_user_empty_first_name` - Empty first_name returns 400
- ✅ `test_create_user_empty_last_name` - Empty last_name returns 400
- ✅ `test_create_user_invalid_email` - Invalid email format returns 400
- ✅ `test_create_user_duplicate_email` - Duplicate email returns 400
- ✅ `test_create_user_short_password` - Password < 8 chars returns 400
- ✅ `test_get_all_users` - GET /users/ returns 200 with list
- ✅ `test_get_user_by_id_success` - GET /users/<id> returns 200
- ✅ `test_get_user_not_found` - GET /users/<invalid_id> returns 404
- ✅ `test_update_user_success` - PUT /users/<id> returns 200
- ✅ `test_update_user_not_found` - PUT /users/<invalid_id> returns 404

#### 2. Amenity Endpoints Tests (9 tests)

```python
class TestAmenityEndpoints(unittest.TestCase):
```

**Tests:**
- ✅ `test_create_amenity_success` - Valid amenity creation returns 201
- ✅ `test_create_amenity_empty_name` - Empty name returns 400
- ✅ `test_create_amenity_name_too_long` - Name > 50 chars returns 400
- ✅ `test_create_amenity_missing_name` - Missing name field returns 400
- ✅ `test_get_all_amenities` - GET /amenities/ returns 200
- ✅ `test_get_amenity_by_id_success` - GET /amenities/<id> returns 200
- ✅ `test_get_amenity_not_found` - GET /amenities/<invalid_id> returns 404
- ✅ `test_update_amenity_success` - PUT /amenities/<id> returns 200
- ✅ `test_update_amenity_not_found` - PUT /amenities/<invalid_id> returns 404

#### 3. Place Endpoints Tests (18 tests)

```python
class TestPlaceEndpoints(unittest.TestCase):
```

**Tests:**
- ✅ `test_create_place_success` - Valid place creation returns 201
- ✅ `test_create_place_empty_title` - Empty title returns 400
- ✅ `test_create_place_negative_price` - Negative price returns 400
- ✅ `test_create_place_zero_price` - Zero price returns 400
- ✅ `test_create_place_latitude_too_high` - Latitude > 90 returns 400
- ✅ `test_create_place_latitude_too_low` - Latitude < -90 returns 400
- ✅ `test_create_place_longitude_too_high` - Longitude > 180 returns 400
- ✅ `test_create_place_longitude_too_low` - Longitude < -180 returns 400
- ✅ `test_create_place_invalid_owner` - Non-existent owner_id returns 404
- ✅ `test_create_place_invalid_amenity` - Non-existent amenity_id returns 404
- ✅ `test_get_all_places` - GET /places/ returns 200
- ✅ `test_get_place_by_id_includes_owner_and_amenities` - Includes relationships
- ✅ `test_get_place_not_found` - GET /places/<invalid_id> returns 404
- ✅ `test_update_place_success` - PUT /places/<id> returns 200
- ✅ `test_update_place_not_found` - PUT /places/<invalid_id> returns 404
- ✅ `test_update_place_invalid_price` - Invalid price returns 400
- ✅ `test_get_place_reviews_success` - GET /places/<id>/reviews returns 200
- ✅ `test_get_place_reviews_not_found` - Reviews for invalid place returns 404

#### 4. Review Endpoints Tests (18 tests)

```python
class TestReviewEndpoints(unittest.TestCase):
```

**Tests:**
- ✅ `test_create_review_success` - Valid review creation returns 201
- ✅ `test_create_review_empty_text` - Empty text returns 400
- ✅ `test_create_review_rating_below_range` - Rating < 1 returns 400
- ✅ `test_create_review_rating_above_range` - Rating > 5 returns 400
- ✅ `test_create_review_invalid_user` - Non-existent user_id returns 404
- ✅ `test_create_review_invalid_place` - Non-existent place_id returns 404
- ✅ `test_create_review_own_place` - Owner reviews own place returns 400
- ✅ `test_create_review_duplicate` - Duplicate review returns 400
- ✅ `test_get_all_reviews` - GET /reviews/ returns 200
- ✅ `test_get_review_by_id_success` - GET /reviews/<id> returns 200
- ✅ `test_get_review_not_found` - GET /reviews/<invalid_id> returns 404
- ✅ `test_update_review_success` - PUT /reviews/<id> returns 200
- ✅ `test_update_review_empty_text` - Update with empty text returns 400
- ✅ `test_update_review_invalid_rating` - Invalid rating returns 400
- ✅ `test_update_review_not_found` - Update invalid review returns 404
- ✅ `test_delete_review_success` - DELETE /reviews/<id> returns 200
- ✅ `test_delete_review_not_found` - DELETE invalid review returns 404
- ✅ `test_delete_review_then_get` - Deleted review returns 404 on GET

---

## Running the Tests

### Prerequisites

```bash
cd holbertonschool-hbnb/part2/hbnb
pip3 install flask flask-restx
```

### Execute Unit Tests

**Run all tests:**
```bash
python3 -m unittest app/tests/test_endpoints.py -v
```

**Run specific test class:**
```bash
python3 -m unittest app.tests.test_endpoints.TestUserEndpoints -v
```

**Run single test:**
```bash
python3 -m unittest app.tests.test_endpoints.TestUserEndpoints.test_create_user_success -v
```

### Expected Output

```
test_create_amenity_empty_name ... ok
test_create_amenity_missing_name ... ok
test_create_amenity_name_too_long ... ok
test_create_amenity_success ... ok
test_create_place_empty_title ... ok
test_create_place_invalid_amenity ... ok
test_create_place_invalid_owner ... ok
test_create_place_latitude_too_high ... ok
test_create_place_latitude_too_low ... ok
test_create_place_longitude_too_high ... ok
test_create_place_longitude_too_low ... ok
test_create_place_negative_price ... ok
test_create_place_success ... ok
test_create_place_zero_price ... ok
test_create_review_duplicate ... ok
test_create_review_empty_text ... ok
test_create_review_invalid_place ... ok
test_create_review_invalid_user ... ok
test_create_review_own_place ... ok
test_create_review_rating_above_range ... ok
test_create_review_rating_below_range ... ok
test_create_review_success ... ok
test_create_user_duplicate_email ... ok
test_create_user_empty_first_name ... ok
test_create_user_empty_last_name ... ok
test_create_user_invalid_email ... ok
test_create_user_short_password ... ok
test_create_user_success ... ok
test_delete_review_not_found ... ok
test_delete_review_success ... ok
test_delete_review_then_get ... ok
test_get_all_amenities ... ok
test_get_all_places ... ok
test_get_all_reviews ... ok
test_get_all_users ... ok
test_get_amenity_by_id_success ... ok
test_get_amenity_not_found ... ok
test_get_place_by_id_includes_owner_and_amenities ... ok
test_get_place_not_found ... ok
test_get_place_reviews_not_found ... ok
test_get_place_reviews_success ... ok
test_get_review_by_id_success ... ok
test_get_review_not_found ... ok
test_get_user_by_id_success ... ok
test_get_user_not_found ... ok
test_update_amenity_not_found ... ok
test_update_amenity_success ... ok
test_update_place_invalid_price ... ok
test_update_place_not_found ... ok
test_update_place_success ... ok
test_update_review_empty_text ... ok
test_update_review_invalid_rating ... ok
test_update_review_not_found ... ok
test_update_review_success ... ok
test_update_user_not_found ... ok
test_update_user_success ... ok

----------------------------------------------------------------------
Ran 56 tests in 3.101s

OK
```

---

## Black-Box Testing with cURL

### Start the Server

```bash
python3 run.py
```

Server will start on `http://127.0.0.1:5000`

### Sample cURL Commands

#### Create User
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "password123"
  }'
```

**Expected Response (201):**
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}
```

#### Create Amenity
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/amenities/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wi-Fi",
    "description": "High-speed wireless internet"
  }'
```

#### Create Place
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/places/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "<user_id>",
    "amenities": ["<amenity_id>"]
  }'
```

#### Create Review
```bash
curl -X POST "http://127.0.0.1:5000/api/v1/reviews/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great place to stay!",
    "rating": 5,
    "user_id": "<user_id>",
    "place_id": "<place_id>"
  }'
```

#### Delete Review (Only Entity with DELETE)
```bash
curl -X DELETE "http://127.0.0.1:5000/api/v1/reviews/<review_id>"
```

---

## Swagger Documentation

The API is fully documented with Swagger UI, accessible at:

```
http://127.0.0.1:5000/api/v1/
```

This provides:
- Interactive API documentation
- Request/response schemas
- Try-it-out functionality for all endpoints
- Automatic validation of request payloads

---

## Test Design Principles

### 1. Test Isolation
Each test class creates a fresh `app` instance with `create_app()`, ensuring tests don't interfere with each other.

### 2. Unique Test Data
Tests use `uuid.uuid4()` to generate unique emails and names, preventing conflicts in shared storage.

### 3. Comprehensive Coverage
Tests cover:
- ✅ Happy paths (valid data)
- ✅ Edge cases (boundary values)
- ✅ Error cases (invalid/missing data)
- ✅ Business logic (duplicate prevention, ownership rules)
- ✅ Relationships (owner, amenities, reviews)

### 4. Clear Test Names
Test names follow the pattern: `test_<action>_<scenario>_<expected_result>`

Example: `test_create_place_negative_price` clearly indicates what's being tested.

---

## Error Handling

All endpoints implement proper error handling:

### Status Codes
- `200 OK` - Successful GET, PUT, DELETE
- `201 Created` - Successful POST
- `400 Bad Request` - Validation errors, business rule violations
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Unexpected errors (should not occur in tests)

### Error Response Format
```json
{
  "error": "Descriptive error message"
}
```

### Success Response Format
```json
{
  "message": "Operation successful"
}
```

---

## Validation Error Examples

### User Validation
```json
// Empty first_name
{"error": "first_name is required"}

// Invalid email
{"error": "email must be a valid email address"}

// Short password
{"error": "password must be at least 8 characters"}

// Duplicate email
{"error": "Email already registered"}
```

### Place Validation
```json
// Empty title
{"error": "title is required"}

// Negative price
{"error": "price must be positive"}

// Invalid latitude
{"error": "latitude must be between -90 and 90"}

// Invalid owner
{"error": "Owner not found"}
```

### Review Validation
```json
// Empty text
{"error": "text is required"}

// Invalid rating
{"error": "rating must be an integer between 1 and 5"}

// Owner reviews own place
{"error": "You cannot review your own place"}

// Duplicate review
{"error": "You have already reviewed this place"}
```

---

## Architecture Notes

### Facade Pattern
All API endpoints interact with the business logic through `HBnBFacade`:
- `app/services/facade.py` - Centralized business logic
- Enforces validation rules
- Manages entity relationships
- Coordinates repository operations

### Repository Pattern
- `app/persistence/repository.py` - In-memory data storage
- Abstracts data access layer
- Provides CRUD operations
- Supports querying by attributes

### API Layer
- `app/api/v1/*.py` - REST endpoints
- Input validation via flask-restx models
- Error handling and status codes
- Response serialization

---

## Future Improvements

### For Part 3 (Authentication)
- [ ] JWT token authentication
- [ ] Protected endpoints
- [ ] User authorization
- [ ] Role-based access control

### For Part 4 (Database)
- [ ] SQLAlchemy integration
- [ ] Database migrations
- [ ] Persistent storage
- [ ] Advanced queries

---

## Conclusion

✅ **All 56 unit tests pass successfully**
✅ **Comprehensive validation implemented**
✅ **Error handling covers all scenarios**
✅ **Business rules properly enforced**
✅ **API fully documented with Swagger**
✅ **Manual testing with cURL verified**

The HBnB Part 2 API is production-ready for the next phase of development.

---

**Tested by:** Amaal Asiri, Maryam Alessa and Munira Alotaibi   
**Date:** February 20, 2026  
**Test Framework:** Python unittest  
**API Framework:** Flask + Flask-RESTx  
**Total Tests:** 56 tests, 0 failures, 0 errors
