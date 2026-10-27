import pandas as pd
import matplotlib.pyplot as plt

# Read marks CSV file
df = pd.read_csv("marks.csv")

# Replace invalid or missing marks with subject average
subjects = ["Maths", "Science", "English"]

for sub in subjects:
    df[sub] = pd.to_numeric(df[sub], errors="coerce")
    df[sub] = df[sub].apply(lambda x: x if 0 <= x <= 100 else None)
    df[sub] = df[sub].fillna(df[sub].mean())

# Calculate Total and Average
df["Total"] = df[subjects].sum(axis=1)
df["Average"] = df[subjects].mean(axis=1)

# Calculate Grade
def grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 75:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 40:
        return "D"
    else:
        return "F"

df["Grade"] = df["Average"].apply(grade)

# Save cleaned data
df.to_csv("cleaned_marks.csv", index=False)

# Save summary
summary = df.groupby("Grade").size().reset_index(name="Students")
summary.to_csv("marks_summary.csv", index=False)

# Bar chart: Grade distribution
df["Grade"].value_counts().plot(kind="bar", title="Grade Distribution")
plt.xlabel("Grade")
plt.ylabel("Number of Students")
plt.show()

# Bar chart: Subject averages
df[subjects].mean().plot(kind="bar", title="Subject Averages")
plt.ylabel("Average Marks")
plt.show()

# Bar chart: Top 5 performers
top = df.nlargest(5, "Total")
plt.bar(top["Name"], top["Total"])
plt.title("Top 5 Performers")
plt.xlabel("Student")
plt.ylabel("Total Marks")
plt.show()

print("Analysis completed successfully!")
print(df)