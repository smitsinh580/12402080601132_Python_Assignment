
import os
import pickle
import zipfile
import re

folder = "logs"
index = {}

# Create inverted index
if not os.path.exists(folder):
    os.mkdir(folder)
    print("Created 'logs' folder. Add log files and run again.")

else:
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        if filename.endswith(".log") or filename.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as file:
                for line_no, line in enumerate(file, 1):
                    words = re.findall(r"\b\w+\b", line.lower())

                    for word in words:
                        index.setdefault(word, []).append(
                            (filename, line_no)
                        )

    # Save index using pickle
    with open("index.pkl", "wb") as file:
        pickle.dump(index, file)

    # Compress logs and index into ZIP
    with zipfile.ZipFile("logs.zip", "w",
                         zipfile.ZIP_DEFLATED) as zipf:
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)
            if os.path.isfile(path):
                zipf.write(path, os.path.join(folder, filename))

        zipf.write("index.pkl")

    print("Index created and files compressed!")

# Search mode
if os.path.exists("index.pkl"):
    with open("index.pkl", "rb") as file:
        index = pickle.load(file)

    word = input("Enter word to search: ").lower()

    if word in index:
        print("Word found at:")
        for filename, line_no in index[word]:
            print(filename, "Line:", line_no)
    else:
        print("Word not found.")
