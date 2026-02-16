# HBnB - Part 2 (Project Setup)

This part initializes the HBnB project structure and prepares the codebase for implementing the Business Logic and API endpoints in later tasks.

## Project Structure
```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   └── persistence/
│       ├── __init__.py
│       └── repository.py
├── run.py
├── config.py
├── requirements.txt
└── README.md
```
## Overview
- Build the Presentation and Business Logic layers based on the Part 1 design.
- Implement core CRUD for User, Place, Amenity, and Review (DELETE is implemented only for Review).
- Use an in-memory repository for persistence in Part 2 (database integration comes in Part 3).
- Apply the Facade pattern to connect the API layer with the business logic and persistence layers.
