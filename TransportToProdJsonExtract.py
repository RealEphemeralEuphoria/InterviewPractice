import os
import sqlite3

# Dynamically determine the path to the database relative to the script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "employees.db")

def ensure_production_table_exists():
    """
    Ensure the Production table exists in the database.
    """
    print("[START] Ensuring Production table exists...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the Production table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Production (
            employeeId INTEGER PRIMARY KEY,
            fullName TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT NOT NULL,
            salary INTEGER NOT NULL,
            hireDate TEXT NOT NULL,
            email TEXT NOT NULL,
            terminationDate TEXT
        );
    """)

    conn.commit()
    conn.close()
    print("[DONE] Production table ensured.")


def process_json_to_production():
    """
    Transfer data from JSON in Dev to the Production table using JSON_EXTRACT and JSON_EACH.
    """
    print("[START] Processing JSON data to Production...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Extract and transform JSON data directly into the Production table
    cursor.execute("""
        INSERT OR IGNORE INTO Production (employeeId, fullName, role, department, salary, hireDate, email, terminationDate)
        SELECT 
            JSON_EXTRACT(rawData, '$.employeeId') AS employeeId,
            JSON_EXTRACT(rawData, '$.fullName') AS fullName,
            JSON_EXTRACT(rawData, '$.role.title') AS role,
            JSON_EXTRACT(rawData, '$.department.name') AS department,
            JSON_EXTRACT(rawData, '$.salary') AS salary,
            JSON_EXTRACT(rawData, '$.hireDate') AS hireDate,
            JSON_EXTRACT(rawData, '$.email') AS email,
            JSON_EXTRACT(rawData, '$.terminationDate') AS terminationDate
        FROM Dev
        WHERE rawData IS NOT NULL;
    """)

    conn.commit()
    conn.close()
    print("[DONE] JSON data processed to Production.")


if __name__ == "__main__":
    print(f"Using database at relative path: {os.path.relpath(DB_PATH)}")
    # Step 1: Ensure the Production table exists
    ensure_production_table_exists()

    # Step 2: Process JSON data to Production
    process_json_to_production()
