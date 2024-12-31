import sqlite3

DB_PATH = r"c:\Users\Alyso\Documents\Coding\InterviewPractice\employees.db"

def dev_to_staging():
    """
    Extract and transform data from Dev to Staging.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Extract JSON fields and insert into Staging
    cursor.execute("""
        INSERT OR IGNORE INTO Staging (employeeId, fullName, role, department, salary, hireDate, email, terminationDate, rawData)
        SELECT 
            JSON_EXTRACT(rawData, '$.employeeId') AS employeeId,
            JSON_EXTRACT(rawData, '$.fullName') AS fullName,
            JSON_EXTRACT(rawData, '$.role.title') AS role,
            JSON_EXTRACT(rawData, '$.department.name') AS department,
            JSON_EXTRACT(rawData, '$.salary') AS salary,
            JSON_EXTRACT(rawData, '$.hireDate') AS hireDate,
            JSON_EXTRACT(rawData, '$.email') AS email,
            JSON_EXTRACT(rawData, '$.terminationDate') AS terminationDate,
            rawData
        FROM Dev
        WHERE rawData IS NOT NULL;
    """)

    conn.commit()
    conn.close()
    print("Data moved from Dev to Staging.")

if __name__ == "__main__":
    dev_to_staging()
