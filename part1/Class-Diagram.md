# Task 1: Detailed Class Diagram for Business Logic Layer

## 1. Business Logic Layer - Detailed Class Diagram

### 1.1 Overview
The Business Logic Layer contains the core domain models that represent the fundamental entities in the HBnB system. These models encapsulate both data and behavior, implementing business rules and maintaining relationships between entities.

### 1.2 BaseEntity Design

All domain entities in the Business Logic Layer inherit from a common `BaseEntity` abstract class that provides fundamental functionality required by all entities:

#### 1.2.1 Purpose
The `BaseEntity` class serves as a foundation for all domain entities, implementing core requirements including:
- Unique identification via UUID4
- Audit trail tracking with creation and update timestamps
- Common validation and serialization methods

#### 1.2.2 Key Features
- **Abstract Class**: Cannot be instantiated directly, must be inherited
- **UUID Generation**: Automatic generation of unique identifiers
- **Timestamp Management**: Automatic tracking of creation and modification times
- **Common Interface**: Standard methods for all entities (`validate()`, `toDict()`, etc.)

#### 1.2.3 Compliance with Requirements
- ✅ **Unique IDs**: Each object has a UUID4 identifier via `id` attribute
- ✅ **Audit Trail**: `created_at` and `updated_at` timestamps for all entities
- ✅ **Business Logic**: Common validation and serialization methods

### 1.3 Class Diagram
The detailed class diagram illustrates all entity models, their attributes, methods, and relationships, showing how each entity inherits from BaseEntity:

<img src="Class-Diagram.png" width="800">

## 1.4 Entity Descriptions

### 1.4.1 User

**Purpose**  
Represents a registered user in the system, either as a property owner or a guest.

**Inheritance**  
Inherits from `BaseEntity`  
→ provides `id`, `created_at`, `updated_at` attributes and `validate()`, `toDict()` methods.

**Key Attributes (Inherited from BaseEntity)**  
- `id`: Unique identifier (UUID4)  
- `created_at`: Creation timestamp  
- `updated_at`: Last modification timestamp  

**Additional Attributes**  
- `first_name`, `last_name`: User personal information  
- `email`: Unique email address for authentication  
- `password`: User password for authentication  
- `is_admin`: Boolean flag indicating administrative privileges  

**Key Methods**  
- `register()`: Creates a new user account  
- `updateProfile()`: Updates user profile information  
- `delete()`: Removes the user account  
- `validate()`: Validates user data (implements `BaseEntity.validate()`)  
- `isAdmin()`: Checks if the user has admin privileges  
- `getFullName()`: Returns the user’s full name  

---

### 1.4.2 Place

**Purpose**  
Represents a property listing available for rental.

**Inheritance**  
Inherits from `BaseEntity`  
→ provides `id`, `created_at`, `updated_at` attributes and `validate()`, `toDict()` methods.

**Key Attributes (Inherited from BaseEntity)**  
- `id`: Unique identifier (UUID4)  
- `created_at`: Creation timestamp  
- `updated_at`: Last modification timestamp  

**Additional Attributes**  
- `title`: Property title  
- `description`: Detailed property description  
- `price`: Nightly rental price  
- `latitude`, `longitude`: Geographic coordinates  
- `owner`: Reference to the owning `User`  

**Key Methods**  
- `create()`: Creates a new property listing  
- `update()`: Updates property details  
- `delete()`: Deletes the property listing  
- `list()`: Retrieves all places  
- `validate()`: Validates place data  
- `addAmenity()`: Adds an amenity to the place  
- `removeAmenity()`: Removes an amenity from the place  
- `getAmenities()`: Retrieves all amenities  
- `listReviews()`: Retrieves reviews for the place  
- `validateCoordinates()`: Validates latitude and longitude  
- `validatePrice()`: Validates price value  

**Relationships**  
- One-to-Many with `Review`  
- Many-to-Many with `Amenity`  

---

### 1.4.3 Review

**Purpose**  
Represents a user’s review and rating of a visited place.

**Inheritance**  
Inherits from `BaseEntity`  
→ provides `id`, `created_at`, `updated_at` attributes and `validate()`, `toDict()` methods.

**Key Attributes (Inherited from BaseEntity)**  
- `id`: Unique identifier (UUID4)  
- `created_at`: Creation timestamp  
- `updated_at`: Last modification timestamp  

**Additional Attributes**  
- `rating`: Numeric rating (1–5)  
- `comment`: Review text  
- `user`: Reference to the reviewing `User`  
- `place`: Reference to the reviewed `Place`  

**Key Methods**  
- `create()`: Creates a new review  
- `update()`: Updates review details  
- `delete()`: Deletes the review  
- `listByPlace()`: Retrieves reviews for a specific place  
- `validate()`: Validates review data  
- `validateRating()`: Ensures rating is within valid range  
- `validateComment()`: Validates review text  

**Business Rules**  
- A user may submit only one review per place  
- Users cannot review their own properties  

---

### 1.4.4 Amenity

**Purpose**  
Represents a feature or service available at a property (e.g., WiFi, Parking, Pool).

**Inheritance**  
Inherits from `BaseEntity`  
→ provides `id`, `created_at`, `updated_at` attributes and `validate()`, `toDict()` methods.

**Key Attributes (Inherited from BaseEntity)**  
- `id`: Unique identifier (UUID4)  
- `created_at`: Creation timestamp  
- `updated_at`: Last modification timestamp  

**Additional Attributes**  
- `name`: Amenity name  
- `description`: Amenity description  

**Key Methods**  
- `create()`: Creates a new amenity  
- `update()`: Updates amenity details  
- `delete()`: Deletes the amenity  
- `list()`: Retrieves all amenities  
- `validate()`: Validates amenity data  
- `getName()`: Returns the amenity name  
- `getDescription()`: Returns the amenity description  

**Relationships**  
- Many-to-Many with `Place`  

---

## 1.6 Relationship Details

### 1.6.1 User – Place Relationship
**Type:** One-to-Many (Composition)  
A `User` (as an owner) can have multiple `Places`.  
Each `Place` has exactly one owner.  

**UML Representation:**
```
User "1" --* "0..*" Place : owns
```
**Implementation:**  
Direct object reference (`owner: User` in `Place` class).

### 1.6.2 Place – Review Relationship
**Type:** One-to-Many (Composition)  
A `Place` can have multiple `Reviews`.  
Each `Review` is associated with exactly one `Place`.  

**UML Representation:**
```
Place "1" --* "0..*" Review : receives
```
**Implementation:**  
Direct object reference (`place: Place` in `Review` class).

### 1.6.3 User – Review Relationship
**Type:** One-to-Many (Composition)  
A `User` can write multiple `Reviews`.  
Each `Review` is written by exactly one `User`.  

**UML Representation:**
```
User "1" --* "0..*" Review : writes
```
**Implementation:**  
Direct object reference (`user: User` in `Review` class).

### 1.6.4 Place – Amenity Relationship
**Type:** Many-to-Many (Association)  
A `Place` can have multiple `Amenities`.  
An `Amenity` can be associated with multiple `Places`.  

**UML Representation:**
```
Place "*" -- "*" Amenity : has
```
**Implementation:**  
Managed through `addAmenity()` and `removeAmenity()` methods in the `Place` class.

---
Created by: Maryam Alessa

Project: HBnB Evolution - Part 1

Date: Feb 2026
