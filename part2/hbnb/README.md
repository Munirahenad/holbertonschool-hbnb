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

  ## Team & Task Allocation (Part 2)

| Name | Tasks | Responsibilities / Deliverables |
|---|---|---|
| Munirah Enad Alotaibi | *Task 0, Task 2* | Project setup & package initialization (structure, Flask app scaffolding, in-memory repository, Facade placeholders). Implement *User endpoints* (POST/GET/PUT, list users), ensure *no password in responses*, correct status codes and Swagger docs. |
| Maryam Alessa | *Task 1, Task 3* | Implement core business logic classes (User, Place, Review, Amenity) with required attributes, validation, and relationships. Implement *Amenity endpoints* (POST/GET/PUT), integrate with Facade and repository, ensure consistent serialization & Swagger. |
| Amaal Asiri | *Task 4, Task 5, Task 6* | Implement *Place endpoints* (POST/GET/PUT) with validation (price/lat/lon) and related data (owner + amenities). Implement *Review endpoints* (POST/GET/PUT/DELETE) + retrieve reviews for a place + update place to include reviews. Perform *testing & validation* (cURL/Swagger + unit tests) and produce a testing report. |

## Repository & References
- *Repo:* https://github.com/munirahenad/holbertonschool-hbnb (branch: main)
- *Work Path:* part2/
- *Reference Docs:* holpRefrence/ (detailed task instructions provided by the school)

  ## Task 0 Summary  ( munirah )
Initialize the HBnB project structure (Presentation/Business Logic/Persistence), set up Flask + Flask-RESTx, add an in-memory repository for temporary storage (to be replaced by SQLAlchemy in Part 3), and prepare the Facade pattern to connect the API with the core logic.

  ## Task 1 Summary (Maryam) 
Implement the core HBnB models (User, Place, Review, Amenity) based on Part 1 design, including required attributes, validation, update methods, and relationships between entities (e.g., reviews linked to places, amenities associated with places).

  ## Task 2 Summary (Munirah)
Implement User endpoints with Flask-RESTx: *POST* create, *GET* by ID, *GET* list, *PUT* update. Connect API to Business Logic via *Facade/Repository, use correct status codes, and **exclude passwords* from all responses. (No DELETE for users in Part 2.)

   ## Task 3 Summary ( Maryam) 
Implement Amenity endpoints with Flask-RESTx: *POST* create, *GET* by ID, *GET* list, and *PUT* update. Integrate API with Business Logic via the *Facade* pattern, use correct status codes, and document/test via Swagger/cURL. (No DELETE for amenities in Part 2.)

 ## Task 4 Summary (Amaal) 
Build Place endpoints (**POST/GET/PUT + list**) via the **Facade**, validate **price/lat/lon**, and return Place data with related **owner + amenities**. *(No DELETE; reviews in Task 5.)*
  
