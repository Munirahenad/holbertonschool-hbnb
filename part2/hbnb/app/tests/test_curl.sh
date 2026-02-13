#!/bin/bash
# =============================================================
# HBnB API - cURL Black-Box Testing Script - Task 6
# Run: bash test_curl.sh
# Make sure the server is running: python run.py
# =============================================================

BASE="http://127.0.0.1:5000/api/v1"
PASS=0
FAIL=0

check() {
    local description=$1
    local expected=$2
    local actual=$3

    if [ "$actual" -eq "$expected" ]; then
        echo "  ✅ PASS | $description (got $actual)"
        PASS=$((PASS + 1))
    else
        echo "  ❌ FAIL | $description (expected $expected, got $actual)"
        FAIL=$((FAIL + 1))
    fi
}

echo ""
echo "============================================="
echo "   HBnB API - cURL Black-Box Test Suite"
echo "============================================="

# =============================================================
echo ""
echo "── USER TESTS ──────────────────────────────"
# =============================================================

# Create valid user
RESPONSE=$(curl -s -o /tmp/body.json -w "%{http_code}" -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john.doe@example.com","password":"password123"}')
check "Create valid user" 201 "$RESPONSE"
USER_ID=$(cat /tmp/body.json | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

# Duplicate email
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"John","last_name":"Doe","email":"john.doe@example.com","password":"password123"}')
check "Duplicate email returns 400" 400 "$RESPONSE"

# Invalid email
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Jane","last_name":"Doe","email":"invalid-email","password":"password123"}')
check "Invalid email returns 400" 400 "$RESPONSE"

# Empty first_name
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"","last_name":"Doe","email":"empty@example.com","password":"password123"}')
check "Empty first_name returns 400" 400 "$RESPONSE"

# Get all users
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/users/")
check "Get all users returns 200" 200 "$RESPONSE"

# Get user by ID
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/users/$USER_ID")
check "Get user by ID returns 200" 200 "$RESPONSE"

# Get non-existent user
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/users/nonexistent-id")
check "Get non-existent user returns 404" 404 "$RESPONSE"

# Update user
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$BASE/users/$USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Johnny","last_name":"Doe","email":"john.doe@example.com"}')
check "Update user returns 200" 200 "$RESPONSE"

# =============================================================
echo ""
echo "── AMENITY TESTS ───────────────────────────"
# =============================================================

# Create valid amenity
RESPONSE=$(curl -s -o /tmp/body.json -w "%{http_code}" -X POST "$BASE/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Wi-Fi","description":"High speed internet"}')
check "Create valid amenity" 201 "$RESPONSE"
AMENITY_ID=$(cat /tmp/body.json | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

# Empty name
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/amenities/" \
  -H "Content-Type: application/json" \
  -d '{"name":"","description":"No name"}')
check "Empty amenity name returns 400" 400 "$RESPONSE"

# Get all amenities
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/amenities/")
check "Get all amenities returns 200" 200 "$RESPONSE"

# Get amenity by ID
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/amenities/$AMENITY_ID")
check "Get amenity by ID returns 200" 200 "$RESPONSE"

# Get non-existent amenity
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/amenities/nonexistent-id")
check "Get non-existent amenity returns 404" 404 "$RESPONSE"

# Update amenity
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$BASE/amenities/$AMENITY_ID" \
  -H "Content-Type: application/json" \
  -d '{"name":"Fast Wi-Fi","description":"Very fast internet"}')
check "Update amenity returns 200" 200 "$RESPONSE"

# =============================================================
echo ""
echo "── PLACE TESTS ─────────────────────────────"
# =============================================================

# Create valid place
RESPONSE=$(curl -s -o /tmp/body.json -w "%{http_code}" -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Cozy Apartment\",\"description\":\"A nice place\",\"price\":100.0,\"latitude\":37.7749,\"longitude\":-122.4194,\"owner_id\":\"$USER_ID\",\"amenities\":[]}")
check "Create valid place" 201 "$RESPONSE"
PLACE_ID=$(cat /tmp/body.json | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

# Empty title
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"\",\"description\":\"No title\",\"price\":100.0,\"latitude\":37.7749,\"longitude\":-122.4194,\"owner_id\":\"$USER_ID\",\"amenities\":[]}")
check "Empty title returns 400" 400 "$RESPONSE"

# Negative price
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Test\",\"description\":\"Test\",\"price\":-50.0,\"latitude\":37.7749,\"longitude\":-122.4194,\"owner_id\":\"$USER_ID\",\"amenities\":[]}")
check "Negative price returns 400" 400 "$RESPONSE"

# Latitude out of range
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Test\",\"description\":\"Test\",\"price\":100.0,\"latitude\":91.0,\"longitude\":-122.4194,\"owner_id\":\"$USER_ID\",\"amenities\":[]}")
check "Latitude > 90 returns 400" 400 "$RESPONSE"

# Longitude out of range
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Test\",\"description\":\"Test\",\"price\":100.0,\"latitude\":37.7749,\"longitude\":181.0,\"owner_id\":\"$USER_ID\",\"amenities\":[]}")
check "Longitude > 180 returns 400" 400 "$RESPONSE"

# Invalid owner
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/places/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"Test","price":100.0,"latitude":37.7749,"longitude":-122.4194,"owner_id":"nonexistent","amenities":[]}')
check "Invalid owner_id returns 404" 404 "$RESPONSE"

# Get all places
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/places/")
check "Get all places returns 200" 200 "$RESPONSE"

# Get place by ID (with owner and amenities)
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/places/$PLACE_ID")
check "Get place by ID returns 200" 200 "$RESPONSE"

# Get non-existent place
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/places/nonexistent-id")
check "Get non-existent place returns 404" 404 "$RESPONSE"

# Update place
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$BASE/places/$PLACE_ID" \
  -H "Content-Type: application/json" \
  -d '{"title":"Luxury Condo","price":200.0}')
check "Update place returns 200" 200 "$RESPONSE"

# =============================================================
echo ""
echo "── REVIEW TESTS ────────────────────────────"
# =============================================================

# Create second user (reviewer)
RESPONSE=$(curl -s -o /tmp/body.json -w "%{http_code}" -X POST "$BASE/users/" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Reviewer","last_name":"User","email":"reviewer@example.com","password":"password123"}')
REVIEWER_ID=$(cat /tmp/body.json | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

# Create valid review
RESPONSE=$(curl -s -o /tmp/body.json -w "%{http_code}" -X POST "$BASE/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Great place!\",\"rating\":4,\"user_id\":\"$REVIEWER_ID\",\"place_id\":\"$PLACE_ID\"}")
check "Create valid review" 201 "$RESPONSE"
REVIEW_ID=$(cat /tmp/body.json | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))")

# Owner reviews own place
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"My own place!\",\"rating\":5,\"user_id\":\"$USER_ID\",\"place_id\":\"$PLACE_ID\"}")
check "Owner reviews own place returns 400" 400 "$RESPONSE"

# Duplicate review
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Again!\",\"rating\":3,\"user_id\":\"$REVIEWER_ID\",\"place_id\":\"$PLACE_ID\"}")
check "Duplicate review returns 400" 400 "$RESPONSE"

# Rating out of range
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Bad rating\",\"rating\":6,\"user_id\":\"$REVIEWER_ID\",\"place_id\":\"$PLACE_ID\"}")
check "Rating > 5 returns 400" 400 "$RESPONSE"

# Invalid user
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Test\",\"rating\":4,\"user_id\":\"nonexistent\",\"place_id\":\"$PLACE_ID\"}")
check "Invalid user_id returns 404" 404 "$RESPONSE"

# Invalid place
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/reviews/" \
  -H "Content-Type: application/json" \
  -d "{\"text\":\"Test\",\"rating\":4,\"user_id\":\"$REVIEWER_ID\",\"place_id\":\"nonexistent\"}")
check "Invalid place_id returns 404" 404 "$RESPONSE"

# Get all reviews
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/reviews/")
check "Get all reviews returns 200" 200 "$RESPONSE"

# Get review by ID
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/reviews/$REVIEW_ID")
check "Get review by ID returns 200" 200 "$RESPONSE"

# Get non-existent review
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/reviews/nonexistent-id")
check "Get non-existent review returns 404" 404 "$RESPONSE"

# Update review
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$BASE/reviews/$REVIEW_ID" \
  -H "Content-Type: application/json" \
  -d '{"text":"Updated review","rating":5}')
check "Update review returns 200" 200 "$RESPONSE"

# Get reviews by place
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/places/$PLACE_ID/reviews")
check "Get reviews by place returns 200" 200 "$RESPONSE"

# Delete review
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE/reviews/$REVIEW_ID")
check "Delete review returns 200" 200 "$RESPONSE"

# Get deleted review
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "$BASE/reviews/$REVIEW_ID")
check "Get deleted review returns 404" 404 "$RESPONSE"

# =============================================================
echo ""
echo "============================================="
echo "  Results: ✅ $PASS passed | ❌ $FAIL failed"
echo "============================================="
echo ""
