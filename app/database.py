import os
import psycopg

from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()

database_host = os.getenv("DATABASE_HOST")
database_port = os.getenv("DATABASE_PORT")
database_name = os.getenv("DATABASE_NAME")
database_user = os.getenv("DATABASE_USER")
database_password = os.getenv("DATABASE_PASSWORD")

def get_connection():
    connection = psycopg.connect(
            host=database_host,
            port=database_port,
            dbname=database_name,
            user=database_user,
            password=database_password
        )
    return connection

def get_media(media_type = None, genre = None, title = None, limit=20, offset=0):
    with get_connection() as connection:
        cursor = connection.cursor(row_factory=dict_row)
        conditions = []
        parameters = []
        if media_type is not None:
            conditions.append("type = %s")
            parameters.append(media_type)

        if genre is not None:
            conditions.append("genre = %s")
            parameters.append(genre)

        if title is not None:
            conditions.append("title ILIKE %s")
            parameters.append(f"%{title}%")

        where_clause = ""

        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)

        query = f"""
            SELECT id, title, type, genre, year
            FROM media
            {where_clause}
            """
        query += " ORDER BY id LIMIT %s OFFSET %s;"
        parameters.extend([limit, offset])
        cursor.execute(query, parameters)
        results = cursor.fetchall()
        
    return results

def get_copies(title=None, availability=None):
    with get_connection() as connection:
        cursor = connection.cursor(row_factory=dict_row)
        conditions = []
        parameters = []
        if title is not None:
            conditions.append("media.title ILIKE %s")
            parameters.append(f"%{title}%")
        if availability is not None:
            if availability == 'AVAILABLE':
                conditions.append("loans.id IS NULL")
            elif availability == 'CHECKED OUT':
                conditions.append("loans.id IS NOT NULL")
        where_clause = ""
        if conditions:
            where_clause = " WHERE " + " AND ".join(conditions)

        query = f"""
            SELECT media.title, copy.format,
                CASE
                    WHEN loans.id IS NOT NULL THEN 'CHECKED OUT'
                    ELSE 'AVAILABLE'
                END AS availability
            FROM copy
            LEFT JOIN loans
                ON copy.id = loans.copy_id
                AND loans.returned_at IS NULL
            LEFT JOIN media
                ON copy.media_id = media.id
            {where_clause};
        """
        cursor.execute(query, parameters)
        results = cursor.fetchall()
    return results

def get_media_by_id(media_id):
    with get_connection() as connection:
        cursor = connection.cursor(row_factory=dict_row)
        cursor.execute(""" 
        SELECT id, title, type, genre, year
        FROM media
        WHERE id = %s;
        """, (media_id,))
        result = cursor.fetchone()
    return result

def create_media(media):
    with get_connection() as connection:
        cursor = connection.cursor(row_factory=dict_row)
        cursor.execute(""" 
            INSERT INTO media (title, type, genre, year)
            VALUES (%s, %s, %s, %s)
            RETURNING id, title, type, genre, year;
        """, (
            media.title,
            media.type,
            media.genre,
            media.year
        ))

        result = cursor.fetchone()
    return result

def update_media(media_id, media):
    fields = media.model_dump(exclude_unset=True)

    if not fields:
        return None
    set_clauses = []
    parameters = []

    for field, value in fields.items():
        set_clauses.append(f"{field} = %s")
        parameters.append(value)

    parameters.append(media_id)
    query = f"""
        UPDATE media
        SET {", ".join(set_clauses)}
        WHERE id = %s
        RETURNING id, title, type, genre, year;
    """

    with get_connection() as connection:
        cursor = connection.cursor(row_factory=dict_row)
        cursor.execute(query, parameters)
        result = cursor.fetchone()

    return result

def delete_media(media_id):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM media
            WHERE id = %s
            RETURNING id;
        """, (media_id,))
        result = cursor.fetchone()
    return result

def create_loan(loan):
    with get_connection() as connection:
        cursor = connection.cursor(row_factory=dict_row)

        cursor.execute("""
            SELECT id
            FROM copy
            WHERE id = %s;
        """, (loan.copy_id,))
        copy_exists = cursor.fetchone()
        if copy_exists is None:
            return "COPY_NOT_FOUND"

        cursor.execute("""
            SELECT id
            FROM users
            WHERE id = %s;
        """, (loan.user_id,))
        user_exists = cursor.fetchone()
        if user_exists is None:
            return "USER_NOT_FOUND"

        cursor.execute("""
            SELECT id
            FROM loans
            WHERE copy_id = %s
                AND returned_at is NULL;
        """, (loan.copy_id,))

        existing_loan = cursor.fetchone()
        if existing_loan is not None:
            return None

        cursor.execute("""
            INSERT INTO loans (copy_id, user_id, checked_out_at)
            VALUES (%s, %s, NOW())
            RETURNING id, copy_id, user_id, checked_out_at, returned_at;
        """, (
            loan.copy_id,
            loan.user_id
        ))
        result = cursor.fetchone()

    return result

def return_loan(loan_id):
    with get_connection() as connection:
        cursor = connection.cursor(row_factory=dict_row)
        cursor.execute("""
            UPDATE loans
            SET returned_at = NOW()
            WHERE id = %s
                AND returned_at is NULL
            RETURNING id, copy_id, user_id, checked_out_at, returned_at;
        """, (loan_id, ))
        result = cursor.fetchone()

    return result

def get_loans():
    with get_connection() as connection:
        cursor = connection.cursor(row_factory=dict_row)

        cursor.execute("""
            SELECT
                loans.id,
                media.title,
                copy.format,
                users.name,
                loans.checked_out_at,
                loans.returned_at
            FROM loans
            JOIN copy on loans.copy_id = copy.id
            JOIN media on media.id = copy.media_id
            JOIN users on loans.user_id = users.id
            ORDER BY loans.id
        """)

        results = cursor.fetchall();
    return results

def get_active_loans():
    with get_connection() as connection:
        cursor = connection.cursor(row_factory=dict_row)

        cursor.execute("""
            SELECT 
                loans.id,
                media.title,
                copy.format,
                users.name,
                loans.checked_out_at
            FROM loans
            JOIN copy on loans.copy_id = copy.id
            JOIN media on copy.media_id = media.id
            JOIN users on loans.user_id = users.id
            WHERE loans.returned_at IS NULL
            ORDER BY loans.checked_out_at
        """)
        results = cursor.fetchall()
    return results
