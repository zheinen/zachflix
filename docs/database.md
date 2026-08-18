# ZachFlix Database Design

## Overview

The ZachFlix database is designed around the distinction between a piece of media, the physical copies owned, and the loans associated with those copies.

The primary relationships are:

Media
|
+-- Copy
|
+-- Loan
|
+-- User

## Media

The media table contains attributes common to every piece of entertainment.

Current fields:

| Field | Description                                   |
| ----- | --------------------------------------------- |
| id    | Unique identifier                             |
| title | Title of the media                            |
| type  | Movie, Book, Vinyl, Video Game, or Board Game |
| genre | Genre                                         |
| year  | Release/publication year                      |
| image | Image associated with the media               |

## Media-Specific Tables

Media-specific attributes are stored in separate tables rather than placing every possible attribute into the media table.

This avoids a large number of nullable fields.

### Movies

- media_id
- director
- length

### Books

- media_id
- author
- pages

### Vinyl

- media_id
- artist
- length

### Video Games

- media_id
- studio

### Board Games

- media_id
- players

The media_id field in each specialized table is both a primary key and a foreign key to media.id.

This models the relationship as:

A Movie is a type of Media.

A Media record can have at most one corresponding Movie record.

## Copies

The copy table represents physical copies that I actually own.

Current fields:

| Field    | Description                                           |
| -------- | ----------------------------------------------------- |
| id       | Unique physical copy identifier                       |
| format   | Physical format such as Blu-ray, DVD, Hardcover, etc. |
| media_id | Media item this copy belongs to                       |

A Media item can have multiple copies and multiple formats.

For example:

The Empire Strikes Back

- Blu-ray
- Blu-ray
- DVD

## Users

The users table represents people who can borrow media.

Current fields:

| Field | Description            |
| ----- | ---------------------- |
| id    | Unique user identifier |
| name  | User's name            |
| email | User's email address   |

Email addresses are unique.

## Loans

The loans table represents the history of physical copies being checked out.

Current fields:

| Field          | Description                |
| -------------- | -------------------------- |
| id             | Unique loan identifier     |
| copy_id        | Physical copy being loaned |
| user_id        | User who borrowed it       |
| checked_out_at | Date/time checked out      |
| returned_at    | Date/time returned         |

A NULL returned_at indicates that the loan is currently active.

A physical copy can have multiple loans over its lifetime.

## Availability

Availability is determined from the relationship between copy and loans.

A copy is considered checked out when it has an active loan where returned_at IS NULL.

The application can therefore determine availability without storing a separate availability field.

This avoids having multiple pieces of data that could become inconsistent.

## Important Design Decisions

### Media vs. Copy

Media represents the entertainment item itself.

Copy represents the physical item actually owned.

This allows one Media item to have multiple physical copies and formats.

### Loan vs. Media

Loans are associated with individual Copies rather than Media.

This is important because different physical copies of the same Media item can have different availability.

For example:

The Empire Strikes Back

- Blu-ray #1 - checked out
- Blu-ray #2 - available
- DVD #1 - available

### Media Types

Movie, Book, Vinyl, Video Game, and Board Game are values of media.type.

They do not currently have separate lookup tables.

Type-specific attributes are stored in specialized tables.
