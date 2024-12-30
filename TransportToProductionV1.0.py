import sqlite3

# Path to SQLite database
DB_PATH = r"c:\Users\Alyso\Documents\Coding\InterviewPractice\employees.db"

def ensure_production_table_exists():
    """
    Ensure the Production table exists in the database.
    """
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
    print("Production table ensured.")

def move_to_production():
    """
    Transfer fully tabularized data from Staging to Production.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch valid rows from Staging
    cursor.execute("""
        SELECT employeeId, fullName, role, department, salary, hireDate, email, terminationDate
        FROM Staging
        WHERE fullName IS NOT NULL
          AND role IS NOT NULL
          AND department IS NOT NULL
          AND salary IS NOT NULL
          AND hireDate IS NOT NULL
          AND email IS NOT NULL;
    """)
    valid_rows = cursor.fetchall()

    # Insert valid rows into Production
    cursor.executemany("""
        INSERT INTO Production (employeeId, fullName, role, department, salary, hireDate, email, terminationDate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """, valid_rows)

    conn.commit()
    conn.close()
    print(f"{len(valid_rows)} rows moved to Production.")

if __name__ == "__main__":
    # Step 1: Ensure the Production table exists
    ensure_production_table_exists()

    # Step 2: Move tabularized data from Staging to Production
    move_to_production()
