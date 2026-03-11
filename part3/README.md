# HBnB Evolution - Part 3

## Introduction
**HBnB Evolution - Part 3** represents the transition of the project from a basic prototype into a database-driven web application.  
Building on the work completed in previous phases, this stage focuses on connecting the application to a real persistence layer using **SQLAlchemy**, implementing secure authentication with **JWT**, and defining entity relationships in a structured relational model.

This part is designed to strengthen the overall architecture of the project by separating concerns into clear layers: API, business logic, and persistence. It also introduces better scalability and maintainability practices commonly used in real-world backend systems.

## Features
- App Factory configuration
- SQLAlchemy repository implementation
- User model with password hashing
- JWT-based authentication
- Protected and admin-only endpoints
- Entity mapping for User, Place, Review, and Amenity
- Relationship mapping between entities
- SQL scripts for database setup
- ER diagram documentation

## Architecture Design
The application is organized into three main layers:

- **Presentation Layer**: Handles API routes and HTTP requests
- **Business Logic Layer**: Contains the core rules and service logic
- **Persistence Layer**: Manages data access through repositories and database models

## Project Structure

```text
holbertonschool-hbnb/
├── part1/
├── part2/
├── part3/
│   ├── run.py
│   ├── config.py
│   ├── requirements.txt
│   ├── .env
│   ├── .gitignore
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── extensions.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── places.py
│   │   │       ├── reviews.py
│   │   │       └── amenities.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base_model.py
│   │   │   ├── user.py
│   │   │   ├── place.py
│   │   │   ├── review.py
│   │   │   └── amenity.py
│   │   │
│   │   ├── persistence/
│   │   │   ├── __init__.py
│   │   │   ├── repository.py
│   │   │   ├── in_memory_repository.py
│   │   │   └── sqlalchemy_repository.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       └── facade.py
│   │
│   ├── sql_scripts/
│   │   ├── schema.sql
│   │   └── initial_data.sql
│   │
│   ├── docs/
│   │   └── er_diagram.md
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   ├── test_places.py
│   │   └── test_reviews.py
│   │
│   └── instance/
│       └── hbnb_dev.db
│
└── README.md
```
## Task Completion by Team Member

### 🔵 Munirah — Task 0, 5, 9
| Task | Description | Status |
|------|-------------|--------|
| 0 | Modify App Factory + Config Integration | ✅ Complete |
| 5 | Implement SQLAlchemy Repository | ✅ Complete |
| 9 | SQL Scripts (Schema + Initial Data) | ✅ Complete |

### 🟣 Maryam — Task 1, 6, 7, 10
| Task | Description | Status |
|------|-------------|--------|
| 1 | User Model + Password Hashing (bcrypt) | ✅ Complete |
| 6 | Map User Entity to SQLAlchemy | ✅ Complete |
| 7 | Map Place, Review, Amenity Entities | ✅ Complete |
| 10 | ER Diagram (Mermaid.js) | ✅ Complete |

### 🟢 Amal — Task 2, 3, 4, 8
| Task | Description | Status |
|------|-------------|--------|
| 2 | JWT Authentication Setup | ✅ Complete |
| 3 | Authenticated User Access Endpoints | ✅ Complete |
| 4 | Administrator Access Endpoints | ✅ Complete |
| 8 | Map Relationships Between Entities | ✅ Complete |

# Project Tasks

## Task Details

### Task 0: Modify App Factory + Config Integration (Munirah)
**Objective:**  
Update the Flask Application Factory to include the configuration object.

**Deliverables:**
- Updated `app/__init__.py` with proper configuration loading
- Config class handling different environments (development, testing, production)
- Environment variable support for sensitive data

---

### Task 1: User Model + Password Hashing (Maryam)
**Objective:**  
Modify User model to store passwords securely.

**Deliverables:**
- Password field added to User model
- bcrypt integration for password hashing
- Password verification method
- Registration endpoint with secure password storage

---

### Task 2: JWT Authentication Setup (Amaal)
**Objective:**  
Implement JWT-based authentication.

**Deliverables:**
- Flask-JWT-Extended configuration
- Login endpoint (`/api/v1/auth/login`) returning JWT token
- Token refresh mechanism
- Protected route decorators

---

### Task 3: Authenticated User Access Endpoints (Amaal)
**Objective:**  
Protect endpoints requiring authentication.

**Deliverables:**
- Current user endpoint (`/api/v1/auth/me`)
- User can update their own profile
- User can delete their own reviews
- JWT required for protected operations

---

### Task 4: Administrator Access Endpoints (Amaal)
**Objective:**  
Implement role-based access control for admin users.

**Deliverables:**
- Admin-only endpoints for user management
- Admin can view/delete any review
- Admin can manage amenities
- `is_admin` flag checking in decorators

---

### Task 5: Implement SQLAlchemy Repository (Munirah)
**Objective:**  
Create database persistence layer.

**Deliverables:**
- `SQLAlchemyRepository` class implementing Repository interface
- Session management with commit/rollback
- Transaction handling
- Migration from in-memory to database storage

---

### Task 6: Map User Entity to SQLAlchemy (Maryam)
**Objective:**  
Convert User model to SQLAlchemy model.

**Deliverables:**
- SQLAlchemy User model with proper columns
- Table creation via SQLAlchemy
- Relationship definitions (one-to-many with places and reviews)
- Data validation at model level

---

### Task 7: Map Place, Review, Amenity Entities (Maryam)
**Objective:**  
Convert remaining models to SQLAlchemy.

**Deliverables:**
- SQLAlchemy Place model with columns and constraints
- SQLAlchemy Review model with foreign keys
- SQLAlchemy Amenity model
- Proper data types and validation

---

### Task 8: Map Relationships Between Entities (Amaal)
**Objective:**  
Define all database relationships.

**Deliverables:**
- User ↔ Place relationship (one-to-many)
- User ↔ Review relationship (one-to-many)
- Place ↔ Review relationship (one-to-many)
- Place ↔ Amenity relationship (many-to-many with association table)
- Proper cascade delete behavior

---

### Task 9: SQL Scripts (Munirah)
**Objective:**  
Create database setup scripts.

**Deliverables:**
- `schema.sql` with CREATE TABLE statements
- `initial_data.sql` with sample data
- Documentation for database setup
- Support for both SQLite and MySQL

---

### Task 10: ER Diagram (Maryam)
**Objective:**  
Visualize database schema.

**Deliverables:**
- Mermaid.js ER diagram showing all tables
- Relationships with cardinality
- Primary and foreign keys
- Documentation in `docs/er_diagram.md`

---

# Database Schema

The database consists of five main tables:

### users
Stores user information:
- `id`
- `email`
- `password`
- `first_name`
- `last_name`
- `is_admin`

### places
Stores place information:
- `id`
- `title`
- `description`
- `price`
- `latitude`
- `longitude`
- `owner_id`

### reviews
Stores reviews:
- `id`
- `text`
- `rating`
- `user_id`
- `place_id`

### amenities
Stores amenities:
- `id`
- `name`
