## 0. High-Level Package Diagram
## Overview
This package diagram shows the three-layer architecture of the HBnB Evolution application and how layers communicate through the Facade design pattern.
It was created using **Mermaid.js Documentation**.

## Architecture Layers
### 1) Presentation Layer (Services & API)
- **Responsibility:** Handles user interactions and HTTP requests/responses.
- **Components:** API endpoints, route handlers, controllers/serializers.
- **Communication:** Calls the Business Logic only through **HBnBFacade** (no direct access to models or database).

### 2) Business Logic Layer (Domain Models)
- **Responsibility:** Implements core business rules and validations.
- **Components:** Domain entities (User, Place, Review, Amenity) + service logic.
- **Communication:** Uses persistence interfaces (repositories/DAOs) to store and retrieve data.

### 3) Persistence Layer (Data Access)
- **Responsibility:** Data storage and retrieval.
- **Components:** Repository/DAO layer, ORM/data mappers, database.
- **Communication:** Provides data operations to the Business Logic layer only.

## Facade Pattern (HBnBFacade)
The Facade provides a unified entry point to the business logic:
- Reduces coupling between Presentation and internal domain/persistence details
- Centralizes access to use-cases (create/update/delete/list)
- Improves maintainability and testability

## Request Flow (High-Level)
Client → API/Controllers → **HBnBFacade** → Domain Models/Services → Repositories → Database → Response

## Diagrams

### Package Diagram
<img src="./part1/Diagrams/Package_diagram.png" alt="Package Diagram" width="850">

### Detailed Package Diagram
<img src="./part1/Diagrams/Detailed_Package_Diagram.png" alt="Detailed Package Diagram" width="850">



Create by: Munirah Enad Alotaibi 

Project: HBnB Evolution - Part 1 

Date: January 2026


