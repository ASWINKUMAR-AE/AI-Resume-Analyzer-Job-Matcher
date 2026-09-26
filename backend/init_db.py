import os
import sys
import pymysql
from werkzeug.security import generate_password_hash
from config import Config
from database.connection import get_server_connection, get_db_connection

def split_sql_statements(sql_text):
    statements = []
    current = []
    for line in sql_text.splitlines():
        clean = line.strip()
        if not clean or clean.startswith('--') or clean.startswith('/*'):
            continue
        current.append(line)
        if clean.endswith(';'):
            stmt = '\n'.join(current).strip()
            if stmt:
                statements.append(stmt[:-1] if stmt.endswith(';') else stmt)
            current = []
    if current:
        stmt = '\n'.join(current).strip()
        if stmt:
            statements.append(stmt)
    return statements

def init_database(seed_demo=False):
    """
    Initializes the MySQL database, tables, default admin, and verified demo data.
    """
    # 1. Connect to MySQL Server
    server_conn = get_server_connection()
    with server_conn.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    server_conn.close()

    # 2. Connect to Database & Apply Schema
    conn = get_db_connection()
    schema_path = os.path.join(os.path.dirname(__file__), "database", "schema.sql")
    if not os.path.exists(schema_path):
        schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "schema.sql")

    if os.path.exists(schema_path):
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        statements = split_sql_statements(schema_sql)
        with conn.cursor() as cursor:
            for stmt in statements:
                if stmt.strip().upper().startswith("USE ") or stmt.strip().upper().startswith("CREATE DATABASE"):
                    continue
                cursor.execute(stmt)
        conn.commit()

    # 3. Ensure Default Users with dynamically verified password hashes
    default_users = [
        ("System Administrator", "admin@airesume.com", "Admin@123", "admin"),
        ("TechNova Solutions", "hr@technova.com", "Company@123", "company"),
        ("ZetHub Technologies", "careers@zethub.com", "Company@123", "company"),
        ("CloudCore Systems", "jobs@cloudcore.com", "Company@123", "company"),
        ("DataSphere AI", "talent@datasphere.ai", "Company@123", "company"),
        ("Alex Rivera", "alex.student@example.com", "Student@123", "student")
    ]

    with conn.cursor() as cursor:
        for name, email, plain_pw, role in default_users:
            cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
            existing = cursor.fetchone()
            pw_hash = generate_password_hash(plain_pw)
            if not existing:
                cursor.execute(
                    """
                    INSERT INTO users (name, email, password_hash, role, status, must_change_password)
                    VALUES (%s, %s, %s, %s, 'active', 0)
                    """,
                    (name, email, pw_hash, role)
                )
            else:
                # Update password hash to guarantee match
                cursor.execute(
                    "UPDATE users SET password_hash = %s, status = 'active' WHERE email = %s",
                    (pw_hash, email)
                )
        conn.commit()

        # 4. Check if demo seed profiles & jobs should be inserted
        cursor.execute("SELECT COUNT(*) AS total_jobs FROM jobs")
        job_count = cursor.fetchone()['total_jobs']

        if seed_demo or job_count == 0:
            seed_path = os.path.join(os.path.dirname(__file__), "database", "seed.sql")
            if not os.path.exists(seed_path):
                seed_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "seed.sql")
            if os.path.exists(seed_path):
                with open(seed_path, "r", encoding="utf-8") as f:
                    seed_sql = f.read()
                statements = split_sql_statements(seed_sql)
                for stmt in statements:
                    if stmt.strip().upper().startswith("USE ") or "INSERT IGNORE INTO `users`" in stmt:
                        continue
                    try:
                        cursor.execute(stmt)
                    except Exception:
                        pass
                conn.commit()

    conn.close()

if __name__ == "__main__":
    seed_flag = "--seed" in sys.argv or "-s" in sys.argv
    init_database(seed_demo=seed_flag)
