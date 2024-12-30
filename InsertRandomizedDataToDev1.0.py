import sqlite3
import json
import random
from faker import Faker

# Path to SQLite database
DB_PATH = r"c:\Users\Alyso\Documents\Coding\InterviewPractice\employees.db"
faker = Faker()

# Sample data for roles and departments
roles = [
    {"title": "Senior Developer", "responsibilities": ["Develop", "Mentor", "Code Review"]},
    {"title": "QA Tester", "responsibilities": ["Test", "Report Bugs", "Collaborate"]},
    {"title": "Manager", "responsibilities": ["Plan", "Coordinate", "Lead"]},
    {"title": "Data Analyst", "responsibilities": ["Analyze Data", "Create Reports", "Collaborate"]},
    {"title": "Engineer", "responsibilities": ["Design", "Develop", "Implement"]}
]

departments = [
    {"name": "Software Engineering", "location": "HQ"},
    {"name": "Marketing", "location": "Remote"},
    {"name": "Operations", "location": "Branch Office"},
    {"name": "Finance", "location": "HQ"},
    {"name": "Human Resources", "location": "HQ"}
]

def generate_random_json():
    """
    Generate a randomized JSON object for rawData.
    """
    full_name = faker.name()
    role = random.choice(roles)
    department = random.choice(departments)
    salary = random.randint(50000, 150000)
    hire_date = faker.date_between(start_date="-10y", end_date="today")
    email = faker.email()
    termination_date = faker.date_between(start_date=hire_date, end_date="today") if random.random() < 0.2 else None

    # Generate the raw JSON data
    raw_data = {
        "fullName": full_name,
        "role": role,
        "department": department,
        "salary": salary,
        "hireDate": hire_date.isoformat(),
        "email": email,
        "terminationDate": termination_date.isoformat() if termination_date else None
    }
    return json.dumps(raw_data)

def insert_random_data():
    """
    Insert randomized JSON rows into the Dev table.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Insert (x): new rows with only rawData populated
    for _ in range(40):
        raw_data = generate_random_json()
        cursor.execute("""
            INSERT INTO Dev (rawData)
            VALUES (?);
        """, (raw_data,))

    conn.commit()
    conn.close()
    print("Randomized JSON data inserted into the Dev table.")

if __name__ == "__main__":
    insert_random_data()
