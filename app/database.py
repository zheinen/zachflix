import os

from dotenv import load_dotenv
import psycopg

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

def get_media():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
        SELECT id, title, type, genre, year
        FROM media;
        """)
        results = cursor.fetchall()
    return results

def get_copies():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(""" 
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
            ON copy.media_id = media.id;
        """)
        results = cursor.fetchall()
    return results
    
media_results = get_media()
copies_results = get_copies()
for media in media_results:
    media_id, title, media_type, genre, year = media
    print(f"{media_id}: {title} ({media_type}, {year})")

for copy in copies_results:
    title, format, availability = copy
    print(f"{title} {format} is {availability}")
