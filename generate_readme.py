import csv, json, urllib.request
from datetime import datetime, timedelta, date
from collections import defaultdict

# --- CONFIG ---
LEETCODE_USER = "vikramnegi21"
GITHUB_USER   = "vikramnegi21"
CSV_FILE      = "problems.csv"
README_FILE   = "README.md"

def fetch_leetcode():
    url = f"https://leetcode-stats-api.herokuapp.com/{LEETCODE_USER}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())
        if d.get("status") == "success":
            return {
                "total": d.get("totalSolved", 0),
                "easy": d.get("easySolved", 0),
                "medium": d.get("mediumSolved", 0),
                "hard": d.get("hardSolved", 0),
                "ranking": d.get("ranking", "N/A"),
            }
    except: pass
    return {"total":0,"easy":0,"medium":0,"hard":0,"ranking":"N/A"}

def read_csv():
    rows = []
    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                rows.append({k: v.strip() for k, v in r.items()})
    except: pass
    return rows

def parse_date(s):
    for fmt in ["%Y-%m-%d","%d %b %Y","%d-%m-%Y"]:
        try: return datetime.strptime(s.strip(), fmt).date()
        except: continue
    return None

def get_progress_bar(done, total, color="39d353"):
    percent = min(round((done / total) * 100, 1), 100)
    # Using a dynamic SVG progress bar for animation effect
    return f"![Progress](https://geps.dev/progress/{int(percent)}?dangerColor=ff4b4b&warningColor=f1c40f&successColor={color})"

def build_readme(problems, lc):
    now = (datetime.utcnow() + timedelta(hours=5, minutes=30)).strftime("%d %b %Y | %I:%M %p IST")
    total_solved = len(problems)
    
    # Topic & Platform Logic
    topics = defaultdict(int)
    plats = defaultdict(int)
    for p in problems:
        if p.get("Topic"): topics[p["Topic"]] += 1
        if p.get("Platform"): plats[p["Platform"]] += 1
    
    # Header & Styles
    header_url = f"https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:161b22,100:0d1117&height=220&section=header&text=DSA%20FORGE%20v2.0&fontSize=70&animation=twinkling&fontColor=58a6ff&desc=Vikram%20Negi%20•%20B.Tech%20CSE%20•%20Competitive%20Programmer&descSize=20&descAlignY=65"

    L = [
        f'<div align="center">\n\n![]({header_url})\n\n',
        f'[![LeetCode](https://img.shields.io/badge/LeetCode-{lc["total"]}-FFA116?style=for-the-badge&logo=leetcode&logoColor=black)](https://leetcode.com/{LEETCODE_USER})',
        f'![Codeforces](https://img.shields.io/badge/Codeforces-{plats.get("Codeforces", 0)}-1F8ACB?style=for-the-badge&logo=codeforces&logoColor=white)',
        f'![Solved](https://img.shields.io/badge/Total%20Solved-{total_solved}-2ea44f?style=for-the-badge&logo=checkmarx&logoColor=white)\n\n',
        "</div>\n\n",
        "## 🛠️ Performance Dashboard",
        '<table width="100%"><tr>',
        f'<td width="50%"><img src="https://github-readme-stats.vercel.app/api?username={GITHUB_USER}&show_icons=true&theme=transparent&hide_border=true&title_color=58a6ff&icon_color=ff7b00&text_color=c9d1d9" /></td>',
        f'<td width="50%"><img src="https://github-readme-streak-stats.herokuapp.com/?user={GITHUB_USER}&theme=transparent&hide_border=true&currStreakLabel=58a6ff&fire=ff7b00&sideNums=c9d1d9&sideLabels=c9d1d9" /></td>',
        '</tr></table>\n',
        "## 🧩 LeetCode Mastery",
        f'<div align="center">\n<img src="https://leetcard.jacoblin.cool/{LEETCODE_USER}?theme=dark&font=Recursive&ext=heatmap" width="100%" />\n</div>\n',
        "## 🎯 Targeted Goals",
        "| Objective | Mastery Level | Status |",
        "| :--- | :---: | :---: |",
        f"| **Striver A2Z Sheet** | {get_progress_bar(total_solved, 455)} | `Grinding` |",
        f"| **LeetCode 500+** | {get_progress_bar(lc['total'], 500, 'ffa116')} | `Solving` |",
        f"| **Rating 1200+** | ![WIP](https://img.shields.io/badge/Work_In_Progress-eb4034?style=flat-square) | `Competitive` |",
        "\n## 🗂️ Topic-wise Distribution",
        "| Topic | Strength | Count |",
        "| :--- | :--- | :---: |"
    ]

    for t, c in sorted(topics.items(), key=lambda x: -x[1]):
        L.append(f"| {t} | {get_progress_bar(c, 20, '58a6ff')} | `{c}` |")

    L.append("\n## 🕒 Recent Submissions")
    L.append("| Problem | Platform | Difficulty | Date |")
    L.append("| :--- | :--- | :---: | :---: |")
    for p in sorted(problems, key=lambda x: parse_date(x["Date"]) or date.min, reverse=True)[:5]:
        L.append(f"| [{p['Problem']}]({p['Link']}) | `{p['Platform']}` | `{p['Difficulty']}` | {p['Date']} |")

    L.append(f'\n<br/>\n<div align="center">\n\n![]({header_url.replace("section=header", "section=footer&reversal=true&height=80&text=").replace("DSA%20FORGE%20v2.0", "")})')
    L.append(f'\n\n**System Sync:** `{now}`  \n*Every commit makes you 1% better.*')
    L.append('\n</div>')

    return "\n".join(L)

def main():
    print("🚀 Initializing Sync...")
    lc = fetch_leetcode()
    problems = read_csv()
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(build_readme(problems, lc))
    print("✅ Build Complete!")

if __name__ == "__main__":
    main()
    
