# ZachFlix

ZachFlix is a personal media library and lending application for cataloging physical entertainment media and allowing friends to browse and borrow items.

The project is being built as a full-stack application and is also a hands-on learning project for developing practical software engineering skills.

## Project Goals

ZachFlix will allow me to:

- Catalog physical media that I own
- Track different formats and physical copies
- Allow friends to browse my collection
- Search and filter media
- Track which copies are currently available
- Allow users to check out media
- Maintain a history of loans
- Eventually provide a simple, user-friendly web interface

## Media Types

The initial MVP will support:

- Movies
- Books
- Vinyl
- Video Games
- Board Games

Each media type shares common information such as title, genre, release year, and image, while type-specific information is stored separately.

## Technology

### Current

- Python
- PostgreSQL
- Docker
- Git / GitHub

### Planned

- FastAPI
- Web frontend

## Current Architecture

The database separates the concept of a piece of media from the physical copies that I own.

Media
|
+-- Copy
|
+-- Loan
|
+-- User

Media-specific information is stored in separate tables:

Media
|
+-- Movies
+-- Books
+-- Vinyl
+-- Video Games
+-- Board Games

## Current Status

The PostgreSQL database and initial relational model have been implemented.

Current functionality includes:

- Media records
- Physical copies and formats
- Users
- Loan history
- Current availability determination
- Media-specific tables
- Referential integrity through foreign keys

The next phase is connecting the PostgreSQL database to a Python/FastAPI backend.

## Future Features

Potential future features include:

- Actor search
- Media series and series ordering
- Multiple genres
- Popularity based on loan history
- Email notifications
- User authentication
- More advanced search and filtering

## Why I Built This

ZachFlix is both a useful personal project and an opportunity to develop practical full-stack software engineering skills, including database design, backend development, API development, testing, and frontend development.
