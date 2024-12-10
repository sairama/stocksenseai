import os

import psycopg2

from src.utils.logging_utils import log_message


def get_db_connection():
    try:
        conn=psycopg2.connect(
            host=os.environ['DB_HOST'],
            database = os.environ['DB_NAME'],
        user = os.environ['DB_USER'],
        password = os.environ['DB_PASSWORD'],
        port =5432
        )
        return conn
    except Exception as e:
        log_message("error",f"Database connection failed. Error {str(e)}")