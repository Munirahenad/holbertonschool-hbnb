# HBnB Evolution - Part 4: Simple Web Client

## Introduction
This part focuses on the front-end development of the HBnB application using HTML5, CSS3, and JavaScript ES6. The web client connects to the back-end API developed in Part 3.

## Project Structure

```text
part4/
├── index.html          # List of places
├── login.html          # Login page
├── place.html          # Place details
├── add_review.html     # Add review form
├── scripts.js          # Client-side JavaScript
├── styles.css          # Styling
└── images/
    ├── logo.png
    ├── icon.png
    ├── icon_bath.png
    ├── icon_bed.png
    └── icon_wifi.png
```

## Task Completion

### 🟢 Amaal — Task 1 & 2
| Task | Description | Status |
|------|-------------|--------|
| 1 | Design: HTML pages + CSS styling | ✅ Complete |
| 2 | Login functionality with JWT | ✅ Complete |

### 🔵 Munirah — Task 3
| Task | Description | Status |
|------|-------------|--------|
| 3 | List of Places + price filter | ✅ Complete |

### 🟣 Maryam — Task 4 & 5
| Task | Description | Status |
|------|-------------|--------|
| 4 | Place Details page | ✅ Complete |
| 5 | Add Review form | ✅ Complete |

## Features

### Task 1 — Design
- Four pages: Login, List of Places, Place Details, Add Review
- Warm beige color palette
- Responsive layout
- W3C valid HTML

### Task 2 — Login
- Connects to `POST /api/v1/auth/login`
- Stores JWT token in a cookie
- Redirects to main page after successful login
- Displays error message on failed login

### Task 3 — List of Places *(Munirah)*
- Fetches places from the API
- Client-side filtering by price
- Shows/hides login link based on authentication

### Task 4 — Place Details *(Maryam)*
- Fetches place details by ID from URL
- Displays name, price, description, amenities, and reviews
- Shows add review form only for authenticated users

### Task 5 — Add Review *(Maryam)*
- Authenticated users only
- Redirects unauthenticated users to index page
- Submits review to the API

## Setup

### 1. Enable CORS in Part 3
```bash
pip install flask-cors
```

In `part3/app/__init__.py`:
```python
from flask_cors import CORS
CORS(app)
```

### 2. Start the API
```bash
cd part3
python3 run.py
```

### 3. Open the Web Client
Open `part4/index.html` in your browser or serve it with a local server:
```bash
cd part4
python3 -m http.server 8000
```

Then visit `http://localhost:8000`

## API Endpoints Used
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/login` | POST | Login and get JWT token |
| `/api/v1/places/` | GET | Get all places |
| `/api/v1/places/<id>` | GET | Get place details |
| `/api/v1/places/<id>/reviews` | GET | Get place reviews |
| `/api/v1/reviews/` | POST | Submit a review |
