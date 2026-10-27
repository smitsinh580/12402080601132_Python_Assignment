
import sqlite3

# Create sample database
conn = sqlite3.connect("students.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    spi REAL
)
""")

cur.execute("DELETE FROM students")
cur.executemany(
    "INSERT INTO students (name, department, spi) VALUES (?, ?, ?)",
    [
        ("Amit", "IT", 8.5),
        ("Rahul", "CSE", 7.2),
        ("Neha", "IT", 9.1),
        ("Priya", "CSE", 8.8)
    ]
)
conn.commit()

# Whitelists
columns = ["id", "name", "department", "spi"]
operators = ["=", ">", "<", ">=", "<=", "!="]
sort_directions = ["ASC", "DESC"]

# User input
column = input("Enter column (id/name/department/spi): ")
operator = input("Enter operator (=, >, <, >=, <=, !=): ")
value = input("Enter value: ")
sort_column = input("Sort by column: ")
direction = input("Sort direction (ASC/DESC): ").upper()
limit = int(input("Enter limit (1-100): "))

# Validate input
if column not in columns or sort_column not in columns:
    print("Invalid column!")
elif operator not in operators:
    print("Invalid operator!")
elif direction not in sort_directions:
    print("Invalid sort direction!")
elif not 1 <= limit <= 100:
    print("Limit must be between 1 and 100!")
else:
    # Build safe query
    query = (
        f"SELECT * FROM students "
        f"WHERE {column} {operator} ? "
        f"ORDER BY {sort_column} {direction} LIMIT ?"
    )

    try:
        cur.execute(query, (value, limit))
        rows = cur.fetchall()

        print("\nQuery Results:")
        for row in rows:
            print(row)

    except sqlite3.Error as e:
        print("Database error:", e)

conn.close()
