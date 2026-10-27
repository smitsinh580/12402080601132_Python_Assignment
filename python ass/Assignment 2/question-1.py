
import re

# Read text file
with open("data.txt", "r") as file:
    text = file.read()

# Compile regular expression
pattern = re.compile(
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:com|edu|org)\b',
    re.IGNORECASE
)

# Extract, normalize and remove duplicates
emails = set(email.lower() for email in pattern.findall(text))

# Process each domain type
for domain in [".com", ".edu", ".org"]:
    result = sorted(email for email in emails if email.endswith(domain))

    print("\nDomain:", domain)
    print("Count:", len(result))

    if result:
        print("Smallest address:", result[0])
    else:
        print("Smallest address: None")
