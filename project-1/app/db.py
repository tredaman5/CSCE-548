import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_conn():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "workout_tracker"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "Gaffney5"),
        cursor_factory=RealDictCursor
    )
