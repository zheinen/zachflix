# ZachFlix Development Log

## Initial Project

ZachFlix began as a personal project to create a library of physical entertainment media that friends could browse and eventually borrow.

The initial concept included:

- Blu-rays/DVDs
- Books
- Vinyl
- Video games
- Board games

The goal was to build something useful while developing practical software engineering skills.

## Database Modeling

### Media

The first major modeling decision was to define Media as the entertainment item itself.

Every Media item has common attributes:

- Title
- Type
- Genre
- Year
- Image

Different physical formats are not separate Media items.

For example, a movie available on both Blu-ray and DVD is one Media item with multiple physical Copies.

### Copy

The Copy entity represents a physical item that I own.

For example:

The Empire Strikes Back

- Blu-ray
- Blu-ray
- DVD

Each physical copy has its own ID.

This allows the application to track individual copies and their availability.

### Loans

Loans are associated with individual Copies.

A Copy can have multiple Loans throughout its lifetime.

A Loan with a NULL returned_at value represents an active loan.

This allows the database to maintain both:

- Current availability
- Historical borrowing information

## SQL Concepts Learned

During the database implementation I worked with:

- Primary keys
- Foreign keys
- Foreign key constraints
- NOT NULL
- UNIQUE
- INSERT
- UPDATE
- SELECT
- JOIN
- LEFT JOIN
- CASE
- NULL
- One-to-one relationships
- One-to-many relationships

## Availability Query

One of the first useful queries implemented was determining whether individual Copies were currently available.

The query uses a LEFT JOIN to connect Copies to only active Loans.

Conceptually:

Copy
|
+-- active Loan -> CHECKED OUT
|
+-- no active Loan -> AVAILABLE

This was an important realization because a Copy can have many historical Loans, but only an active Loan should affect current availability.

## Specialized Media Types

Rather than placing all possible attributes into the media table, type-specific attributes are stored in specialized tables.

For example:

media
|
+-- movies
|
+-- books

This avoids creating a large number of nullable columns.

A Movie contains:

- Director
- Length

A Book contains:

- Author
- Pages

The specialized table uses media_id as both its primary key and foreign key.

## Database Constraints

The database was intentionally tested with invalid data to verify that its constraints prevent inconsistent records.

For example:

- Attempting to create two Movie records for the same Media failed because media_id is the primary key of movies.
- Attempting to create a Movie for a nonexistent Media record failed because of the foreign key constraint.

These tests helped demonstrate how PostgreSQL can enforce data integrity rather than relying entirely on application code.

## Current Test Data

The database currently contains test data for:

- The Empire Strikes Back
- The Hobbit
- Two test users
- Multiple physical copies of The Empire Strikes Back
- A test loan

## Current Database Tables

The database currently contains:

- media
- copy
- users
- loans
- movies
- books
- vinyl
- video_games
- board_games

## Next Steps

- Connect Python to PostgreSQL
- Build the FastAPI backend
- Create API endpoints
- Build the frontend
- Add search and filtering
- Implement user authentication
- Implement the checkout process
