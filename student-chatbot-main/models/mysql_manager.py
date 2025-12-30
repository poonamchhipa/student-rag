import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

class MySQLManager:
    def __init__(self):
        self.config = {
            "host": os.getenv("MYSQL_HOST"),
            "user": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "database": os.getenv("MYSQL_DB"),
            "cursorclass": pymysql.cursors.DictCursor
        }

    def _get_connection(self):
        return pymysql.connect(**self.config)

    # -----------------------------
    # FETCH ALL DATA FOR INDEXING
    # -----------------------------
    def fetch_data(self):
        """Fetches all data from all tables for RAG indexing."""
        try:
            data = []
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    # 1. Get all tables
                    cursor.execute("SHOW TABLES")
                    tables = [list(row.values())[0] for row in cursor.fetchall()]
                    print(f"DEBUG: Found tables: {tables}")
                    
                    for table in tables:
                        # 2. Get all rows from the table
                        cursor.execute(f"SELECT * FROM `{table}`")
                        rows = cursor.fetchall()
                        print(f"DEBUG: Table '{table}' has {len(rows)} rows.")
                        
                        for row in rows:
                            # 3. Format row into a descriptive string
                            row_str = f"Table: {table}, " + ", ".join([f"{k}: {v}" for k, v in row.items()])
                            data.append(row_str)
            
            print(f"DEBUG: Total records fetched across all tables: {len(data)}")
            return data
        except Exception as e:
            print(f"Error fetching data from MySQL: {e}")
            return []

    # -----------------------------
    # STUDENT BASIC INFO
    # -----------------------------
    def get_student_info(self, student_id):
        query = """
        SELECT student_id, name, age, department
        FROM students
        WHERE student_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (student_id,))
                return cursor.fetchone()

    # -----------------------------
    # STUDENT ATTENDANCE (JOIN)
    # -----------------------------
    def get_student_attendance(self, student_id):
        query = """
        SELECT 
            s.student_id,
            s.name,
            a.total_classes,
            a.attended_classes,
            a.attendance_percentage
        FROM students s
        JOIN student_attendance a
            ON s.student_id = a.student_id
        WHERE s.student_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (student_id,))
                return cursor.fetchone()

    # -----------------------------
    # STUDENT MARKS (JOIN)
    # -----------------------------
    def get_student_marks(self, student_id):
        query = """
        SELECT 
            s.student_id,
            s.name,
            m.subject,
            m.marks
        FROM students s
        JOIN student_marks m
            ON s.student_id = m.student_id
        WHERE s.student_id = %s;
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (student_id,))
                return cursor.fetchall()
