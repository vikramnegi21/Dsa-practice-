import csv

# Read CSV
rows = []
with open("problems.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # skip header
    for row in reader:
        rows.append(row)

# Create table
table = "| Date | Problem | Platform | Difficulty | Topic |\n"
table += "|------|--------|----------|------------|--------|\n"

for r in rows:
    if len(r) >= 5:
        table += f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |\n"

# Read existing README
with open("README.md", "r") as f:
    content = f.read()

# Find table section
start = content.find("| Date")
end = content.find("Repository Structure")

if start == -1 or end == -1:
    print("Markers not found!")
    exit()

# Replace table
new_content = content[:start] + table + "\n" + content[end:]

# Write back
with open("README.md", "w") as f:
    f.write(new_content)
