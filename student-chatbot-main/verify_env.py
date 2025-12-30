import os
import pymysql
import google.generativeai as genai
from dotenv import load_dotenv
import chromadb
import sys

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

load_dotenv()

def test_mysql():
    print("--- Testing MySQL ---")
    config = {
        "host": os.getenv("MYSQL_HOST"),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DB"),
    }
    print(f"Connecting to {config['host']} as {config['user']}...")
    try:
        conn = pymysql.connect(**config)
        print("OK: MySQL Connection Successful")
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"Tables found: {[str(t) for t in tables]}")
        conn.close()
        return True
    except Exception as e:
        print(f"FAIL: MySQL Connection Failed: {e}")
        return False

def test_gemini():
    print("\n--- Testing Gemini API ---")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("FAIL: GOOGLE_API_KEY not found in .env")
        return False
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say 'Gemini is ready!'")
        print(f"OK: Gemini API Response: {response.text.strip()}")
        return True
    except Exception as e:
        print(f"FAIL: Gemini API Failed: {e}")
        return False

def test_chroma():
    print("\n--- Testing ChromaDB ---")
    try:
        persist_directory = "./data/chroma_db"
        client = chromadb.PersistentClient(path=persist_directory)
        print(f"OK: ChromaDB Client Initialized at {persist_directory}")
        return True
    except Exception as e:
        print(f"FAIL: ChromaDB Initialization Failed: {e}")
        return False

if __name__ == "__main__":
    mysql_ok = test_mysql()
    gemini_ok = test_gemini()
    chroma_ok = test_chroma()
    
    if mysql_ok and gemini_ok and chroma_ok:
        print("\n🚀 All systems ready!")
    else:
        print("\nERR: Some systems are not ready. Please check the errors above.")
