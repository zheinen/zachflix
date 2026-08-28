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

def get_media(media_type = None, genre = None, title = None):
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
            {where_clause};
            """
        
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
    
media_results = get_media()
copies_results = get_copies()
for media in media_results:
    media_id, title, media_type, genre, year = media
    print(f"{media_id}: {title} ({media_type}, {year})")

for copy in copies_results:
    title, format, availability = copy
    print(f"{title} {format} is {availability}")


