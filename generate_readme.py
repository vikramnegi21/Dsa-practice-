#!/usr/bin/env python3
import csv
import requests
import os
from datetime import datetime, timedelta, date
from collections import defaultdict

# CONFIG
LEETCODE_USER = "__vikram21"
CF_USER       = "__vikram21"
GITHUB_USER   = "vikramnegi21"

# DATE
def parse_date(raw):
    raw = raw.strip()
    if not raw:
        return None
    today = date.today()
    for year in [today.year, today.year - 1]:
        try:
            d = datetime.strptime(f"{raw} {year}", "%d %b %Y").date()
            if d <= today:
                return d
        except:
            pass
    return None

# LOAD CSV
def load_problems():
    rows = []
    with open("problems.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            d = parse_date(row.get("Date", ""))
            if d:
                row["parsed_date"] = d
                rows.append(row)
    return rows

# STREAK
def calc_streaks(problems):
    dates = {p["parsed_date"] for p in problems}
    cur = 0
    d = date.today()
    while d in dates:
        cur += 1
        d -= timedelta(days=1)
    return cur

# GITHUB API
def github_contributions():
    token = os.getenv("GH_TOKEN")
    if not token:
        return 0
    query = f"""
    query {{
      user(login: "{GITHUB_USER}") {{
        contributionsCollection {{
          contributionCalendar {{
            totalContributions
          }}
        }}
      }}
    }}
    """
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.post("https://api.github.com/graphql",
                            json={"query": query}, headers=headers)
        data = res.json()
        return data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    except:
        return 0

# LEETCODE
def leetcode_stats():
    try:
        res = requests.get(f"https://leetcode-stats-api.herokuapp.com/{LEETCODE_USER}")
        return res.json().get("totalSolved", 0)
    except:
        return 0

# CODEFORCES
def cf_rating():
    try:
        res = requests.get(f"https://codeforces.com/api/user.info?handles={CF_USER}")
        return res.json()["result"][0].get("rating", 0)
    except:
        return 0

# HEATMAP SVG
def generate_heatmap(problems):
    date_counts = defaultdict(int)
    for p in problems:
        date_counts[p["parsed_date"]] += 1

    today = date.today()
    start = today - timedelta(days=90)

    cells = []
    d = start
    while d <= today:
        cells.append((d, date_counts.get(d, 0)))
        d += timedelta(days=1)

    rects = ""
    for i, (dt, cnt) in enumerate(cells):
        x = (i // 7) * 15
        y = (i % 7) * 15
        color = "#39d353" if cnt > 0 else "#161b22"
        rects += f'<rect x="{x}" y="{y}" width="10" height="10" fill="{color}"/>'

    return f'<svg width="300" height="120">{rects}</svg>'

# README
def build_readme(problems):
    total = len(problems)
    streak = calc_streaks(problems)

    lc = leetcode_stats()
    cf = cf_rating()
    gh = github_contributions()

    heatmap = generate_heatmap(problems)

    with open("heatmap.svg", "w") as f:
        f.write(heatmap)

    return f"""
# 🚀 DSA Dashboard

## 👨‍💻 Stats

- 🧠 LeetCode: **{lc} problems**
- ⚔️ Codeforces Rating: **{cf}**
- 🟩 GitHub Contributions: **{gh}**
- 🔥 Current Streak: **{streak} days**
- 📊 Total Problems: **{total}**

---

## 📊 Activity Heatmap
![Heatmap](heatmap.svg)

---

## 📁 Problem Log

| Date | Problem | Platform |
|------|--------|----------|
""" + "\n".join(
        f"| {p['Date']} | {p['Problem']} | {p['Platform']} |"
        for p in problems
    )

# MAIN
if __name__ == "__main__":
    problems = load_problems()
    readme = build_readme(problems)

    with open("README.md", "w") as f:
        f.write(readme)

    print("✅ README + Heatmap updated")
