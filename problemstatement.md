# Problem Statement

**What broke?**

The client's endpoints now send data in JSON format, which is being stored in the rawData column of our employees table. Previously, data was stored in a tabular structure, so our application is unable to process the data correctly.

**What do we need to do?**

- Extract the JSON data from the rawData column.
- Populate the missing columns in the employees table so our application can continue working seamlessly with tabular data.

**Goal:**

Ensure that our app receives the data in the same tabular format it expects by parsing the JSON from rawData and transforming it back into structured columns.

---

# Resolution Steps Summary

- Implemented JSON parsing and transformation logic.
- Updated database schema to include Staging for intermediate processing.
- Created an ETL pipeline to move data from Dev -> Staging -> Production.
- Validated data at each stage to ensure correctness and completeness.
- Restored application functionality, ensuring compatibility with the new JSON data format.

---

# Lessons Learned

**Proactive Communication**

Ensure clients communicate API changes in advance to allow for adequate preparation.

**Flexible System Design**

Incorporate mechanisms to handle changes in data formats, such as supporting JSON or other formats in addition to tabular data.

**Validation and Testing**

Continuously validate data integrity and completeness during transformations to avoid gaps in the pipeline.

---

# Key Changes

**Database Scripts**

- Updated the Python scripts to dynamically process incoming data, handle JSON parsing, and transfer transformed data through the pipeline.
- Introduced logging and clear outputs to monitor each step of the pipeline.

**ETL Pipeline Overview**

- **Dev:** Received raw data, including JSON-formatted rows.
- **Staging:** Temporarily stored parsed and validated rows.
- **Production:** Final destination for clean tabular data consumed by the application.

**Dynamic Path Handling**

Scripts were updated to dynamically determine the path to the database file, allowing the solution to run in multiple environments without requiring manual path updates.

---

# Outcome

**Data Processing Restored**

- The application now seamlessly processes incoming data, whether it arrives in tabular or JSON format.
- All JSON data is transformed back into the expected tabular format before reaching Production.

**Database Integrity Ensured**

- The Production table contains only clean tabular data.
- Duplicate rows are avoided, and unprocessed data is flagged and logged for review.
