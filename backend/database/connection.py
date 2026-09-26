import pymysql
from pymysql.cursors import DictCursor
import contextlib
from config import Config

def get_db_connection(database=None):
    """
    Creates and returns a connection to the MySQL server.
    If database is None, connects using Config.DB_NAME.
    """
    db_name = Config.DB_NAME if database is None else database
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=db_name,
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=False
        )
        return conn
    except pymysql.MySQLError as e:
        if e.args[0] == 1049:  # Unknown database
            raise e
        raise ConnectionError(
            f"MySQL connection failed: {e}. "
            "Please ensure MySQL is running in your XAMPP Control Panel on "
            f"{Config.DB_HOST}:{Config.DB_PORT}."
        )

def get_server_connection():
    """
    Connects to MySQL server directly without specifying a database.
    Used for creating database or maintenance tasks.
    """
    try:
        conn = pymysql.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            charset='utf8mb4',
            cursorclass=DictCursor,
            autocommit=True
        )
        return conn
    except pymysql.MySQLError as e:
        raise ConnectionError(
            f"MySQL connection failed: {e}. "
            "Please start MySQL from XAMPP Control Panel."
        )

@contextlib.contextmanager
def get_db():
    """
    Context manager for database operations with automatic commit and rollback.
    """
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def check_db_health():
    """
    Verifies if MySQL server and the target database are connected and functional.
    """
    try:
        with get_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 AS alive")
                res = cursor.fetchone()
                return bool(res and res['alive'] == 1)
    except Exception:
        return False
