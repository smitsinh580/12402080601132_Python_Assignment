
# Campus Merit Analyzer using Compound Data Structures

students = [
    {
        "enrollment": 101,
        "name": "Amit",
        "semester": 3,
        "cpi": 8.8,
        "marks": (85, 90, 88),
        "subjects": ("CS301", "CS302", "CS303")
    },
    {
        "enrollment": 102,
        "name": "Rahul",
        "semester": 3,
        "cpi": 9.2,
        "marks": (80, 95, 92),
        "subjects": ("CS301", "CS302", "CS303")
    },
    {
        "enrollment": 103,
        "name": "Neha",
        "semester": 3,
        "cpi": 9.2,
        "marks": (90, 88, 96),
        "subjects": ("CS301", "CS302", "CS303")
    },
    {
        "enrollment": 104,
        "name": "Priya",
        "semester": 4,
        "cpi": 9.5,
        "marks": (95, 92, 89),
        "subjects": ("CS401", "CS402", "CS403")
    },
    {
        "enrollment": 105,
        "name": "Karan",
        "semester": 4,
        "cpi": 8.9,
        "marks": (88, 96, 94),
        "subjects": ("CS401", "CS402", "CS403")
    }
]

K = int(input("Enter K (number of top students): "))

# Find top K students in every semester
semesters = sorted(set(s["semester"] for s in students))

for sem in semesters:
    semester_students = [
        s for s in students if s["semester"] == sem
    ]

    # Sort by CPI, average marks, then enrollment number
    semester_students.sort(
        key=lambda s: (
            -s["cpi"],
            -sum(s["marks"]) / len(s["marks"]),
            s["enrollment"]
        )
    )

    print(f"\nTop {K} Students - Semester {sem}")
    for s in semester_students[:K]:
        avg = sum(s["marks"]) / len(s["marks"])
        print(
            s["enrollment"], s["name"],
            "CPI:", s["cpi"],
            "Average Marks:", round(avg, 2)
        )

# Find subject-wise toppers
topper = {}

for s in students:
    for subject, mark in zip(s["subjects"], s["marks"]):
        if subject not in topper or mark > topper[subject]["mark"]:
            topper[subject] = {
                "name": s["name"],
                "enrollment": s["enrollment"],
                "mark": mark
            }
        elif mark == topper[subject]["mark"]:
            # Break ties using smaller enrollment number
            if s["enrollment"] < topper[subject]["enrollment"]:
                topper[subject] = {
                    "name": s["name"],
                    "enrollment": s["enrollment"],
                    "mark": mark
                }

print("\nSubject-wise Toppers")
for subject, data in sorted(topper.items()):
    print(
        subject, "-", data["name"],
        "| Enrollment:", data["enrollment"],
        "| Marks:", data["mark"]
    )
