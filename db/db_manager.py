import mysql.connector
from mysql.connector import Error
import os
import bcrypt

class DBManager:
    def __init__(self):
        self.host = os.getenv("DB_HOST", "localhost")
        self.user = os.getenv("DB_USER", "root")
        self.password = os.getenv("DB_PASSWORD", "")
        self.database = os.getenv("DB_NAME", "resume_tailor_db")
        self.connection = None

    def connect(self):
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                                    host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    database=self.database
                                )
            return self.connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
        
    def execute_query(self, query, params=None):
        """Execute an INSERT, UPDATE, or DELETE query.
        Returns the last inserted row ID for INSERT queries, or None."""
        conn = self.connect()
        if conn:
            cursor = conn.cursor()
            if params:
                if isinstance(params, str):
                    return None
                sanitized = [
                    str(p) if isinstance(p, (list, dict, tuple)) else p
                    for p in params
                ]
                params = tuple(sanitized)
            try:
                cursor.execute(query, params or ())
                conn.commit()
                return cursor.lastrowid
            except Exception as e:
                print(f"MySQL error: {e}")
                return None
        return None
    
    def fetch_query(self, query, params=None):
        """Execute a SELECT query and return results as a list of dicts."""
        conn = self.connect()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            return cursor.fetchall()
        return []
    
    def verify_user(self, username, pswrd):
        """Verify user credentials. Returns True if valid, False otherwise."""
        query = "SELECT password FROM users WHERE username = %s"
        result = self.fetch_query(query, (username,))
        if result:
            stored_hash = result[0]['password']
            try:
                if bcrypt.checkpw(pswrd.encode('utf-8'), stored_hash.encode('utf-8')):
                    return True
            except ValueError:
                if pswrd == stored_hash:
                    return True
        return False

    def save_user(self, username, pswrd):
        """Hash password and save a new user. Returns the new user's ID."""
        hashed = bcrypt.hashpw(pswrd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        return self.execute_query(query, (username, hashed))

    def get_user_history(self, user_id):
        query = "SELECT company_name, match_score FROM job_applications WHERE user_id = %s ORDER BY created_at DESC"
        return self.fetch_query(query, (user_id,))

    def save_optimized_resume(self, user_id, version_name, content):
        query = "INSERT INTO resumes(user_id, version_name, content) VALUES (%s, %s, %s)"
        return self.execute_query(query, (user_id, version_name, content))