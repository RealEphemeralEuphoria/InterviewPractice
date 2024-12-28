import sqlite3
import json
import random
from faker import Faker
import os

# Import DB_PATH from config
from config import DB_PATH

# Initialize Faker
faker = Faker()

def recreate_production_table(conn):
    """
    Drops existing tables and recreates the 'Production' table.
    """
    cursor = conn.cursor()
    try:
        # Drop specified tables
        tables_to_drop = ["Production", "Staging", "Dev_backup"]  # Add any other unnecessary tables here
        for table in tables_to_drop:
            cursor.execute(f"DROP TABLE IF EXISTS {table};")
            print(f"Table '{table}' dropped.")

        # Create the Production table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Production (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rawData TEXT NOT NULL
            );
        """)
        conn.commit()
        print("Table 'Production' created successfully.")
    except Exception as e:
        print(f"Error recreating tables: {e}")
        conn.rollback()

def generate_random_user_json():
    """
    Generate a randomized user record in JSON format.
    """
    return json.dumps({
        "fullName": faker.name(),
        "role": {
            "title": random.choice(["Developer", "Engineer", "Manager", "Analyst"]),
            "responsibilities": random.sample(
                ["Develop", "Mentor", "Code Review", "Testing", "Project Management"],
                random.randint(1, 3)
            )
        },
        "department": {
            "name": random.choice(["Software Engineering", "Product Management", "HR", "IT Support"]),
            "location": random.choice(["HQ", "Remote", "Regional Office"])
        },
        "salary": random.randint(60000, 150000),
        "hireDate": faker.date_between(start_date='-5y', end_date='today').isoformat(),
        "email": faker.email(),
        "terminationDate": random.choice([None, faker.date_between(start_date='-1y', end_date='today').isoformat()])
    })

def insert_randomized_json_rows(conn, num_rows=20):
    """
    Inserts multiple rows with randomized JSON data into the 'Production' table.
    """
    cursor = conn.cursor()
    try:
        for _ in range(num_rows):
            user_json = generate_random_user_json()
            cursor.execute("""
                INSERT INTO Production (rawData)
                VALUES (?);
            """, (user_json,))
        conn.commit()
        print(f"{num_rows} randomized rows successfully inserted into 'Production'.")
    except Exception as e:
        print(f"Error inserting randomized rows: {e}")
        conn.rollback()

if __name__ == "__main__":
    # Connect to the database
    conn = sqlite3.connect(DB_PATH)

    try:
        # Drop old tables and create the Production table
        recreate_production_table(conn)

        # Insert random rows into the Production table
        insert_randomized_json_rows(conn, num_rows=20)
    finally:
        conn.close()
