"""
Database configuration and connection management.

This module handles:
- Loading database credentials from environment variables
- Creating and managing database connections
- Executing SQL queries from files
- Query parameter handling
"""

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Optional

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DatabaseConfig:
    """Database configuration from environment variables."""

    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', '5432'))
        self.database = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')

        # Validate required fields
        if not all([self.database, self.user, self.password]):
            raise ValueError(
                "Missing required database credentials. "
                "Please set DB_NAME, DB_USER, and DB_PASSWORD in .env file"
            )

    def get_connection_params(self) -> Dict[str, Any]:
        """Get connection parameters as a dictionary."""
        return {
            'host': self.host,
            'port': self.port,
            'database': self.database,
            'user': self.user,
            'password': self.password,
        }


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.

    Usage:
        with get_db_connection() as conn:
            # Use connection
            pass
    """
    config = DatabaseConfig()
    conn = None
    try:
        conn = psycopg2.connect(**config.get_connection_params())
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()


def load_query_from_file(query_file: str) -> str:
    """
    Load SQL query from a file.

    Args:
        query_file: Path to the SQL file (relative to scripts directory)

    Returns:
        SQL query as a string
    """
    # Get the scripts directory path
    scripts_dir = Path(__file__).parent
    query_path = scripts_dir / query_file

    if not query_path.exists():
        raise FileNotFoundError(f"Query file not found: {query_path}")

    with open(query_path, 'r') as f:
        return f.read()


def execute_query(
    query_file: str,
    params: Optional[Dict[str, Any]] = None
) -> list:
    """
    Execute a query from a file and return results.

    Args:
        query_file: Name of the SQL file in the queries directory
        params: Optional dictionary of query parameters

    Returns:
        List of rows as dictionaries

    Example:
        results = execute_query(
            'fetch_compatibility_data.sql',
            params={
                'start_date': '2024-01-01',
                'end_date': None,
                'model_names': ['Llama-3.1-8B-Instruct', 'Mistral-7B'],
                'device_names': None
            }
        )
    """
    query = load_query_from_file(query_file)

    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def test_connection() -> bool:
    """
    Test the database connection.

    Returns:
        True if connection successful, False otherwise
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT 1')
                result = cursor.fetchone()
                return result is not None
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


if __name__ == '__main__':
    # Test the connection when run directly
    print("Testing database connection...")
    if test_connection():
        print("✓ Database connection successful!")
    else:
        print("✗ Database connection failed. Check your credentials in .env")
