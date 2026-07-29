"""
generate_readme.py
-------------------
Reads problems/problems.csv aur README.md ke andar do markers
(<!--STATS_START--> ... <!--STATS_END-->) ke beech ka hissa
naye stats se replace kar deta hai.
"""

import csv
import os
from collections import Counter
from datetime import datetime

CSV_PATH = "problems/problems.csv"
README_PATH = "README.md"
START_MARKER = "<!--STATS_START-->"
END_MARKER = "<!--STATS_END-->"


def load_problems():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_stats_block(problems):
    total = len(problems)
    diff_count = Counter(p["Difficulty"].strip() for p in problems if p.get("Difficulty"))
    topic_count = Counter(p["Topic"].strip() for p in problems if p.get("Topic"))
    platform_count = Counter(p["Platform"].strip() for p in problems if p.get("Platform"))

    lines = []
    lines.append(f"**Total Problems Solved:** `{total}`\n")

    lines.append("| Difficulty | Count |")
    lines.append("|---|---|")
    for level in ["Easy", "Medium", "Hard"]:
        lines.append(f"| {level} | {diff_count.get(level, 0)} |")
    lines.append("")

    lines.append("**Platform-wise:**")
    lines.append("| Platform | Count |")
    lines.append("|---|---|")
    for plat, cnt in platform_count.most_common():
        lines.append(f"| {plat} | {cnt} |")
    lines.append("")

    lines.append("**Top Topics:**")
    lines.append("| Topic | Count |")
    lines.append("|---|---|")
    for topic, cnt in topic_count.most_common(8):
        lines.append(f"| {topic} | {cnt} |")
    lines.append("")

    recent = problems[-10:][::-1]
    lines.append("**Recently Solved:**")
    lines.append("| Date | Problem | Difficulty | Platform |")
    lines.append("|---|---|---|---|")
    for p in recent:
        link = p.get("Link", "").strip()
        name = p.get("Problem", "").strip()
        problem_cell = f"[{name}]({link})" if link else name
        lines.append(f"| {p.get('Date','')} | {problem_cell} | {p.get('Difficulty','')} | {p.get('Platform','')} |")

    lines.append("")
    lines.append(f"_Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_")

    return "\n".join(lines)


def update_readme(stats_block):
    with open(README_PATH, encoding="utf-8") as f:
        content = f.read()

    start_idx = content.find(START_MARKER)
    end_idx = content.find(END_MARKER)

    if start_idx == -1 or end_idx == -1:
        raise ValueError("README.md me STATS_START / STATS_END markers nahi mile.")

    new_content = (
        content[: start_idx + len(START_MARKER)]
        + "\n\n" + stats_block + "\n\n"
        + content[end_idx:]
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    problems = load_problems()
    stats_block = build_stats_block(problems)
    update_readme(stats_block)
    print("README.md updated successfully.")
