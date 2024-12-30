Technical Assessment Study Guide

## **Objective**

This guide provides strategies and knowledge to excel in technical assessments involving JSON and SQLite databases. It emphasizes articulating your reasoning, trade-offs, and decisions effectively while showcasing technical expertise. Additionally, it was a playground for "Resolving a client issue in which the client unannouncedly began sending us JSON instead of tabularized data".

---

### **1. Problem-Solving Framework**

### **1.1 Clarify the Problem**

- **Ask Questions**:
    - Example: "What specific fields need to be extracted from the JSON data?"
    - Example: "Should the solution prioritize performance (query speed) or flexibility (easier data updates)?"
- **Confirm Inputs and Outputs**:
    - Validate the JSON structure and expected database schema.
    - Example: "Should nested JSON fields be stored in a raw format or decomposed into separate relational fields?"

### **1.2 Break Down the Problem**

- **Understand the Scope**:
    - Example: "First, I'll validate the JSON data structure. Then, I'll write SQL queries to extract and normalize the fields."
- **Plan the Steps**:
    1. Insert raw JSON data into the database.
    2. Parse and extract specific fields using SQL functions (e.g., `JSON_EXTRACT`).
    3. Normalize the extracted data into relational tables if necessary.
    4. Perform required transformations and validations.

### **1.3 Articulate Technical Trade-offs**

- **Storage vs. Query Complexity**:
    - Raw JSON in a single column: Easier to insert and maintain but harder to query.
    - Fully normalized data: Better for complex queries but requires upfront transformation.
- **Performance vs. Flexibility**:
    - Example: Using indexed fields for fast lookups vs. storing unindexed raw JSON for adaptability.

---

### **2. Key Technical Concepts**

### **2.1 JSON in SQLite**

- **Why It Matters**: Real-world data is often hierarchical and must be processed efficiently in flat database structures.
- **Key Functions**:
    - `JSON_EXTRACT`: Use this to extract specific values from JSON, ideal for directly accessing fields such as `$.employeeId` or `$.role.title`.
    - `JSON_EACH`: Use this to iterate through JSON arrays or objects, particularly useful for processing multiple entries within a nested structure.
    - `JSON_INSERT`, `JSON_REPLACE`: Use these functions to modify JSON data in place.

### **Example**: Comparing `JSON_EXTRACT` and `JSON_EACH`

**Using `JSON_EXTRACT` to retrieve a specific value:**

```
SELECT JSON_EXTRACT(rawData, '$.role.title') AS roleTitle
FROM Dev
WHERE JSON_EXTRACT(rawData, '$.employeeId') = 51;
```

**Using `JSON_EACH` to iterate over an array:**

```
-- Assuming rawData contains an array of responsibilities:
-- {
--   "employeeId": 51,
--   "responsibilities": ["Develop", "Mentor", "Code Review"]
-- }

SELECT value AS responsibility
FROM Dev, JSON_EACH(JSON_EXTRACT(rawData, '$.responsibilities'));
```

- **Approach**:
    - Use `JSON_EXTRACT` for retrieving single, specific values.
    - Use `JSON_EACH` for unwrapping arrays or nested objects and iterating through them.
    - Store raw data for flexibility, but create views or temporary tables for easier querying.
- **Why It Matters**: Real-world data is often hierarchical and must be processed efficiently in flat database structures.
- **Key Functions**:
    - `JSON_EXTRACT`: Extracts values from JSON.
    - `JSON_EACH`: Iterates through JSON arrays or objects.
    - `JSON_INSERT`, `JSON_REPLACE`: Modifies JSON data.

### **Example**: Extracting Data from Nested JSON

```
-- Example JSON structure:
-- {
--   "employeeId": 51,
--   "role": {"title": "Senior Developer"},
--   "department": {"name": "Software Engineering", "location": "HQ"},
--   "responsibilities": ["Develop", "Mentor", "Code Review"]
-- }

-- Extract specific fields from the JSON structure
SELECT
    JSON_EXTRACT(rawData, '$.employeeId') AS employeeId,
    JSON_EXTRACT(rawData, '$.role.title') AS roleTitle,
    JSON_EXTRACT(rawData, '$.department.name') AS departmentName
FROM Dev;

-- Iterate over an array using JSON_EACH to list responsibilities
SELECT
    JSON_EXTRACT(rawData, '$.employeeId') AS employeeId,
    value AS responsibility
FROM Dev,
    JSON_EACH(JSON_EXTRACT(rawData, '$.responsibilities'));
```

- **Approach**:
    - Use `JSON_EXTRACT` to retrieve individual fields for direct mapping.
    - Use `JSON_EACH` to iterate over arrays within the JSON to extract multiple related entries like `responsibilities`.

```
-- Example JSON structure:
-- {
--   "employeeId": 51,
--   "role": {"title": "Senior Developer"},
--   "department": {"name": "Software Engineering", "location": "HQ"}
-- }

SELECT
    JSON_EXTRACT(rawData, '$.employeeId') AS employeeId,
    JSON_EXTRACT(rawData, '$.role.title') AS roleTitle,
    JSON_EXTRACT(rawData, '$.department.name') AS departmentName
FROM Dev;
```

- **Approach**:
    - Identify and extract the required fields.
    - Store raw data for flexibility, but create views or temporary tables for easier querying.

### **2.2 Inserting JSON into SQLite**

- Insert JSON data into the `rawData` field:

```
INSERT INTO Dev (employeeId, fullName, rawData)
VALUES (
    52,
    'John Smith',
    '{"employeeId": 52, "fullName": "John Smith", "role": {"title": "Engineer"}, "salary": 100000}'
);
```

### **2.3 Transforming Data**

- Normalize JSON data into a relational structure when needed:

```
INSERT INTO Roles (employeeId, roleTitle)
SELECT
    JSON_EXTRACT(rawData, '$.employeeId') AS employeeId,
    JSON_EXTRACT(rawData, '$.role.title') AS roleTitle
FROM Dev;
```

### **2.4 Data Validation**

- Ensure data consistency:

```
-- Verify required fields are present
SELECT *
FROM Dev
WHERE JSON_EXTRACT(rawData, '$.employeeId') IS NULL;
```

- Validate field formats and ranges:

```
-- Check if salary is within an expected range
SELECT *
FROM Dev
WHERE JSON_EXTRACT(rawData, '$.salary') NOT BETWEEN 50000 AND 200000;

-- Ensure email addresses follow a valid format
SELECT *
FROM Dev
WHERE JSON_EXTRACT(rawData, '$.email') NOT LIKE '%@%.%';
```

- Identify inconsistent or unexpected data types:

```
-- Check for invalid data types in hireDate
SELECT *
FROM Dev
WHERE typeof(JSON_EXTRACT(rawData, '$.hireDate')) != 'text';
```

- Ensure data consistency:

```
-- Verify required fields are present
SELECT *
FROM Dev
WHERE JSON_EXTRACT(rawData, '$.employeeId') IS NULL;
```

---

### **3. Communication Strategies**

### **3.1 Tailoring Explanations**

- **Non-Technical Audience**:
    - "We’re storing JSON data as-is for flexibility, and extracting specific fields for reporting."
- **Technical Audience**:
    - "Using `JSON_EXTRACT`, we’ll parse and index key fields to optimize query performance."

### **3.2 Justifying Decisions**

- **Example**: "Storing raw JSON simplifies ingestion of unstructured data, and we’ll use SQL functions to extract and normalize only when needed, balancing storage efficiency and query flexibility."

### **3.3 Discussing Trade-offs**

- Example: "Normalizing all fields upfront ensures faster queries but increases the upfront transformation cost. Storing raw JSON provides adaptability but might slow down complex queries."

---

### **4. Practice Exercise**

### **Scenario**:

- Provided with nested JSON data, your task is to:
    1. Validate the JSON data before inserting it into the database to ensure consistency and correctness.
    2. Insert the JSON into SQLite.
    3. Extract specific fields.
    4. Normalize the data.
    5. Discuss trade-offs.

### **Steps**:

1. **Validate JSON Data**:
    - Use tools or scripts to verify required fields are present, data types match expectations, and values fall within allowed ranges.
    - Example validation query:
    
    ```
    SELECT *
    FROM Dev
    WHERE JSON_EXTRACT(rawData, '$.employeeId') IS NULL
       OR typeof(JSON_EXTRACT(rawData, '$.hireDate')) != 'text';
    ```
    
2. **Insert Data**:
    - Use `INSERT INTO` to store JSON in the `rawData` field.
3. **Extract Fields**:
    - Write queries using `JSON_EXTRACT` to parse key fields.
4. **Normalize**:
    - Use `INSERT INTO` with `SELECT` to populate normalized tables.
5. **Evaluate Trade-offs**:
    - Document your reasoning for raw vs. normalized data.

### **Expected Deliverables**:

- SQL scripts for each step.
- Explanation of the chosen approach.
- Analysis of trade-offs and constraints.

### **Scenario**:

- Provided with nested JSON data, your task is to:
    1. Insert the JSON into SQLite.
    2. Extract specific fields.
    3. Normalize the data.
    4. Discuss trade-offs.

### **Steps**:

1. **Insert Data**:
    - Use `INSERT INTO` to store JSON in the `rawData` field.
2. **Extract Fields**:
    - Write queries using `JSON_EXTRACT` to parse key fields.
3. **Normalize**:
    - Use `INSERT INTO` with `SELECT` to populate normalized tables.
4. **Evaluate Trade-offs**:
    - Document your reasoning for raw vs. normalized data.

### **Expected Deliverables**:

- SQL scripts for each step.
- Explanation of the chosen approach.
- Analysis of trade-offs and constraints.

---

### **5. Key Takeaways**

- **Technical Proficiency**:
    - Demonstrate expertise in handling nested JSON and database normalization.
    - Use SQLite JSON functions effectively.
- **Problem-Solving Mindset**:
    - Show structured thinking in decomposing complex problems.
- **Communication**:
    - Explain decisions clearly and adapt explanations to the audience.

By following this guide and practicing the provided exercises, you will develop the skills and confidence needed to excel in technical assessments involving JSON and SQLite.
