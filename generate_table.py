import csv

# 1. Read CSV
rows = []
try:
    with open("problems.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Header skip
        for row in reader:
            if row: rows.append(row)
except FileNotFoundError:
    print("Error: problems.csv nahi mili!")
    exit()

# 2. Create Table Structure (Fixed Order)
table = "| Date | Problem | Platform | Difficulty | Topic | Status |\n"
table += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"

for r in rows:
    # Sahi indexes: 0=Date, 1=Problem, 2=Platform, 3=Difficulty, 4=Topic, 5=Status
    date = r[0]
    problem = r[1]
    platform = r[2]
    difficulty = r[3]
    topic = r[4]
    status_raw = r[5].strip()

    # Status Emoji Logic
    if status_raw.lower() in ["done", "solved"]:
        status = "✅ Done"
    elif status_raw.lower() == "revision":
        status = "🔁 Revision"
    elif status_raw.lower() == "not clear":
        status = "❌ Not Clear"
    else:
        status = status_raw

    table += f"| {date} | {problem} | {platform} | {difficulty} | {topic} | {status} |\n"

# 3. Update README
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "| Date"
end_marker = "## Repository Structure"

start_index = content.find(start_marker)
end_index = content.find(end_marker)

if start_index != -1 and end_index != -1:
    new_content = content[:start_index] + table + "\n" + content[end_index:]
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("README.md successfully update ho gaya!")
else:
    print("Markers nahi mile! Check README.")
    
