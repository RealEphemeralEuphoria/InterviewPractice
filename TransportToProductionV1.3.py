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


def move_to_production():
    """
    Transfer fully tabularized data from Staging and non-JSON data from Dev to Production.
    """
    print("[START] Moving data to Production...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Step 1: Insert JSON-transformed data from Staging
    print("[INFO] Inserting JSON-transformed data from Staging...")
    cursor.execute("""
        INSERT OR IGNORE INTO Production (employeeId, fullName, role, department, salary, hireDate, email, terminationDate)
        SELECT employeeId, fullName, role, department, salary, hireDate, email, terminationDate
        FROM Staging
        WHERE fullName IS NOT NULL
          AND role IS NOT NULL
          AND department IS NOT NULL
          AND salary IS NOT NULL
          AND hireDate IS NOT NULL
          AND email IS NOT NULL;
    """)
    print("[DONE] JSON-transformed data inserted from Staging.")

    # Step 2: Insert non-JSON data directly from Dev
    print("[INFO] Inserting non-JSON data from Dev...")
    cursor.execute("""
        INSERT OR IGNORE INTO Production (employeeId, fullName, role, department, salary, hireDate, email, terminationDate)
        SELECT employeeId, fullName, role, department, salary, hireDate, email, terminationDate
        FROM Dev
        WHERE rawData IS NULL;
    """)
    print("[DONE] Non-JSON data inserted from Dev.")

    conn.commit()
    conn.close()
    print("[DONE] All relevant data successfully moved to Production.")


if __name__ == "__main__":
    print(f"Using database at relative path: {os.path.relpath(DB_PATH)}")
    # Step 1: Ensure the Production table exists
    ensure_production_table_exists()

    # Step 2: Move all relevant data to Production
    move_to_production()