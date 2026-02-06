**Part 1: Technical Documentation**
### Overview
Part 1 documents the **HBnB Evolution web app** architecture and core entities (**User, Place, Review, Amenity**). It includes UML diagrams: a **Facade-based package diagram**, a **Business Logic class diagram**, and **sequence diagrams** for key API flows. This serves as the blueprint for the next phases.

## 📋 Contents

### Task 0: High-Level Package Diagram

**File:** [package-diagram.md](./package-diagram.md)  
**Responsible:** Munirah Enad Alotaibi

**Description:** Illustrates the three-layer architecture (Presentation, Business Logic, Persistence) and how the Facade pattern enables communication between layers.
### Task 1: Detailed Class Diagram for Business Logic Layer
**File:**  [Class-Diagram.md](./Class-Diagram.md)

**Responsible:** Maryam Alessa 

**Description:** Illustrates the Detailed Class Diagram of the Business Logic Layer, showing all core domain entities of the system along with their attributes, methods, and relationships (such as association, composition, and multiplicity). It demonstrates how business rules are implemented and how interactions between objects are structured within the system.

### Task 2: Sequence Diagrams for API Calls
**File:**  
**Responsible:** Amal Asiri 

**Description:** 
### Task 3: Documentation Compilation
**File:**  
**Responsible:** Team Collaboration

**Description:** We compiled all diagrams and technical specifications into a polished PDF, including clear explanatory notes to support the overall documentation.

## 🏛️ Architecture Overview
### Three-Layer Architecture

```
...+----------------------------------------------------------------------------------+
|                              <<package>> Presentation                            |
|                                 Services & API                                  |
|                                                                                  |
|      +-------------------+                                   +----------------+  |
|      |   API Endpoints   |                                   |    Services    |  |
|      +-------------------+                                   +----------------+  |
|               | calls                                                  | calls   |
+---------------|--------------------------------------------------------|---------+
                v                                                        v
+----------------------------------------------------------------------------------+
|                            <<package>> Business Logic                             |
|                                                                                  |
|                         +------------------------------+                         |
|                         | <<interface>> HBnB Facade    |                         |
|                         +------------------------------+                         |
|                                      | orchestrates                               |
|                                      v                                           |
|  +----------------------------------------------------------------------------+  |
|  |                             <<package>> Models                             |  |
|  |                                                                            |  |
|  |   +--------+     +--------+     +--------+     +---------+                 |  |
|  |   |  User  |     | Place  |     | Review |     | Amenity |                 |  |
|  |   +--------+     +--------+     +--------+     +---------+                 |  |
|  +----------------------------------------------------------------------------+  |
|                 | DB operations                           ^ returns data         |
+-----------------|------------------------------------------|---------------------+
                v                                           |
+----------------------------------------------------------------------------------+
|                              <<package>> Persistence                             |
|                                                                                  |
|                 +------------------------------+                                  |
|                 |      Repositories / DAOs     |                                  |
|                 +------------------------------+                                  |
|                               |                                                   |
|                               v                                                   |
|                         +--------------+                                          |
|                         |   Database   |                                          |
|                         +--------------+                                          |
+----------------------------------------------------------------------------------+
...
```
## Design Patterns
- **Facade:** Single entry point from the Presentation layer to the Business Logic.
- **Repository:** Encapsulates data access and persistence operations (DAOs/Repositories).
- **Layered Architecture:** Separates the system into Presentation, Business Logic, and Persistence layers.
## Core Domain Entities
- **User:** Represents a platform account (regular or admin) and supports authentication-related actions.
- **Place:** A listing created by a user, including basic details like location and price, and linked amenities.
- **Review:** A user’s evaluation of a place, stored as a 1–5 rating with optional feedback.
- **Amenity:** A reusable feature that can be attached to places ( WiFi, Pool).

## Entity Relationships
- **User → Place:** One user can own multiple places (1..*).
- **User → Review:** One user can write multiple reviews (1..*).
- **Place → Review:** One place can have multiple reviews (1..*).

## Diagram Standards
- UML-style notation for consistency across diagrams.
- Written in **Mermaid.js** for direct rendering on GitHub.
- Kept clear and documentation-friendly (titles, labels, and readable layout).

## Team Contact

| Name | Responsibility | Contact |
|------|----------------|---------|
| Munirah Alotaibi | Package Diagram | muneraenad@hotmail.com |
| Maryam Alessa | Class Diagram |roro13188@gmail.com |
| Amaal Aasiri | Sequence Diagrams | amaalmoasiri@gmail.com |




