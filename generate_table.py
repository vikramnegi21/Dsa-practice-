import csv

rows = []
with open("problems.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        rows.append(row)

table = "| Date | Problem | Platform | Difficulty |\n"
table += "|------|--------|----------|------------|\n"

for r in rows:
    table += f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |\n"

with open("README.md", "r") as f:
    content = f.read()

start = content.find("| Date")
end = content.find("Repository Structure")

if start == -1 or end == -1:
    print("Markers not found!")
    exit()

new_content = content[:start] + table + "\n" + content[end:]

with open("README.md", "w") as f:
    f.write(new_content)
