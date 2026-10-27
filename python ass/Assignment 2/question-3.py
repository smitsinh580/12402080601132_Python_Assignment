
import mysql.connector
import csv

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password"
)

cur = db.cursor()
cur.execute("CREATE DATABASE IF NOT EXISTS college")
cur.execute("USE college")

# Create tables
cur.execute("""
CREATE TABLE IF NOT EXISTS Student (
    sid INT PRIMARY KEY,
    name VARCHAR(50),
    spi FLOAT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS CourseRegistration (
    sid INT,
    course VARCHAR(50),
    FOREIGN KEY (sid) REFERENCES Student(sid)
)
""")

# Load Student CSV using bulk insert
with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    students = [
        (int(r["sid"]), r["name"], float(r["spi"]))
        for r in reader
    ]

cur.executemany(
    "INSERT INTO Student VALUES (%s, %s, %s) "
    "ON DUPLICATE KEY UPDATE name=VALUES(name), spi=VALUES(spi)",
    students
)

# Load Course Registration CSV
with open("registrations.csv", "r") as f:
    reader = csv.DictReader(f)
    registrations = [
        (int(r["sid"]), r["course"])
        for r in reader
    ]

cur.executemany(
    "INSERT INTO CourseRegistration (sid, course) "
    "SELECT %s, %s WHERE NOT EXISTS "
    "(SELECT 1 FROM CourseRegistration WHERE sid=%s AND course=%s)",
    [(sid, course, sid, course) for sid, course in registrations]
)

db.commit()

# Search students by course and SPI threshold
course = input("Enter course name: ")
threshold = float(input("Enter minimum SPI: "))

cur.execute("""
SELECT DISTINCT s.sid, s.name, s.spi
FROM Student s
JOIN CourseRegistration c ON s.sid = c.sid
WHERE c.course = %s AND s.spi > %s
ORDER BY s.sid
""", (course, threshold))

print("\nRegistered Students:")
for row in cur.fetchall():
    print(row)

cur.close()
db.close()
