import sqlite3
import json

# Path to SQLite database
DB_PATH = r"c:\Users\Alyso\Documents\Coding\InterviewPractice\employees.db"

def ensure_staging_table_exists():
    """
    Ensure the Staging table exists in the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create the Staging table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Staging (
            employeeId INTEGER PRIMARY KEY,
            fullName TEXT,
            role TEXT,
            department TEXT,
            salary INTEGER,
            hireDate TEXT,
            email TEXT,
            terminationDate TEXT,
            rawData TEXT
        );
    """)

    conn.commit()
    conn.close()
    print("Staging table ensured.")

def process_and_insert_to_staging():
    """
    Parse JSON from rawData in the Dev table and insert tabularized data into the Staging table.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch all records from Dev where rawData is not NULL
    cursor.execute("SELECT * FROM Dev WHERE rawData IS NOT NULL;")
    dev_records = cursor.fetchall()

    for record in dev_records:
        # Extract the JSON data from rawData
        employee_id, full_name, role, department, salary, hire_date, email, termination_date, raw_data = record

        try:
            json_data = json.loads(raw_data)
            parsed_full_name = json_data.get("fullName")
            parsed_role = json_data.get("role", {}).get("title")
            parsed_department = json_data.get("department", {}).get("name")
            parsed_salary = json_data.get("salary")
            parsed_hire_date = json_data.get("hireDate")
            parsed_email = json_data.get("email")
            parsed_termination_date = json_data.get("terminationDate")

            # Insert the parsed data into the Staging table
            cursor.execute("""
                INSERT INTO Staging (employeeId, fullName, role, department, salary, hireDate, email, terminationDate, rawData)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                employee_id,
                parsed_full_name,
                parsed_role,
                parsed_department,
                parsed_salary,
                parsed_hire_date,
                parsed_email,
                parsed_termination_date,
                raw_data
            ))

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for employeeId {employee_id}: {e}")

    conn.commit()
    conn.close()
    print("All records processed and inserted into Staging.")

if __name__ == "__main__":
    # Step 1: Ensure the Staging table exists
    ensure_staging_table_exists()

    # Step 2: Process rawData and insert into Staging
    process_and_insert_to_staging()
