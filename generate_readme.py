import csv, json, urllib.request
from datetime import datetime, timedelta, date, timezone
from collections import defaultdict

# --- CONFIG ---
LEETCODE_USER = "__vikram21"
CF_USER       = "__vikram21"
STRIVER_NAME  = "__vikram" # Updated as per your sheet name
GITHUB_USER   = "vikramnegi21"
GMAIL         = "vikramnegi0021@gmail.com"
CSV_FILE      = "problems.csv"
README_FILE   = "README.md"
HEATMAP_FILE  = "heatmap.svg"

def fetch_leetcode():
    url = f"https://leetcode-stats-api.herokuapp.com/{LEETCODE_USER}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())
        if d.get("status") == "success":
            return {
                "total": d.get("totalSolved", 0),
                "ranking": d.get("ranking", "N/A"),
                "easy": d.get("easySolved", 0),
                "medium": d.get("mediumSolved", 0),
                "hard": d.get("hardSolved", 0)
            }
    except: pass
    return {"total": 104, "ranking": "N/A", "easy": 0, "medium": 0, "hard": 0} # Fallback to 104

def read_csv():
    rows = []
    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append({str(k).strip(): str(v).strip() for k, v in r.items() if k})
    except: pass
    return rows

def parse_date(s):
    if not s: return None
    for fmt in ["%Y-%m-%d", "%d %b %Y", "%d %b", "%d-%m-%Y", "%b %d, %Y"]:
        try:
            d = datetime.strptime(s.strip(), fmt)
            if d.year == 1900: d = d.replace(year=date.today().year)
            return d.date()
        except: continue
    return None

def make_heatmap(problems):
    date_counts = defaultdict(int)
    for p in problems:
        d = parse_date(p.get("Date"))
        if d: date_counts[d] += 1
    
    today = date.today()
    weeks = 22
    start = today - timedelta(days=today.weekday() + 1 + (weeks - 1) * 7)
    cell, gap = 14, 3
    step = cell + gap
    w, h = weeks * step + 60, 7 * step + 50
    
    cells = []
    for week in range(weeks):
        for dow in range(7):
            day = start + timedelta(weeks=week, days=dow)
            x, y = 40 + week * step, 30 + dow * step
            if day > today: color = "#0d1117"
            else:
                cnt = date_counts.get(day, 0)
                if cnt == 0: color = "#161b22"
                elif cnt == 1: color = "#0e4429"
                elif cnt == 2: color = "#006d32"
                elif cnt <= 4: color = "#26a641"
                else: color = "#39d353"
            cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{color}"></rect>')
    
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">
    <rect width="100%" height="100%" fill="#0d1117" rx="10"/>
    <text x="20" y="20" fill="#58a6ff" font-size="12" font-family="monospace" font-weight="bold">COMMIT ENGINE: STREAK ACTIVE</text>
    {"".join(cells)}</svg>'''

def get_tgda_progress(percent, color="39d353"):
    return f"![Progress](https://geps.dev/progress/{int(percent)}?successColor={color}&warningColor=f1c40f&dangerColor=ff4b4b)"

def build_readme(problems, lc):
    now_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    
    # Progress Calcs
    striver_progress = 19 # Updated to 19%
    lc_solved = max(lc['total'], 104)
    lc_percent = (lc_solved / 500) * 100

    header = "https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:0d2137,100:0d1117&height=180&section=header&text=DSA%20FORGE%20v3&fontSize=65&fontColor=58a6ff&animation=fadeIn&fontAlignY=40&desc=%F0%9F%9A%80%20Vikram%20Negi%20%7C%20Leveling%20Up%20Daily&descAlignY=62&descColor=c9d1d9&stroke=21262d&strokeWidth=1"

    L = [
        f'<div align="center">\n\n![]({header})\n\n',
        f'[![LeetCode](https://img.shields.io/badge/LeetCode-Profile-FFA116?style=flat-square&logo=leetcode&logoColor=black)](https://leetcode.com/{LEETCODE_USER})',
        f'[![Codeforces](https://img.shields.io/badge/Codeforces-Profile-1F8ACB?style=flat-square&logo=codeforces&logoColor=white)](https://codeforces.com/profile/{CF_USER})',
        f'[![Gmail](https://img.shields.io/badge/Gmail-Connect-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:{GMAIL})\n\n',
        '</div>\n\n---',
        "\n## ⚡ Engine Stats",
        '<div align="center">',
        f'<img src="https://github-readme-stats.vercel.app/api?username={GITHUB_USER}&show_icons=true&theme=tokyonight&hide_border=true" height="165" />',
        f'<img src="https://github-readme-streak-stats.herokuapp.com/?user={GITHUB_USER}&theme=tokyonight&hide_border=true" height="165" />',
        '</div>\n',
        "## 🔥 Consistency Graph",
        '<div align="center">\n\n![Heatmap](heatmap.svg)\n\n</div>\n',
        "## 🎯 Strategic Targets",
        "| Objective | Mastery Level | Tracking |",
        "| :--- | :--- | :---: |",
        f"| **Striver A2Z Sheet** | {get_tgda_progress(striver_progress, '58a6ff')} | `⚡ {STRIVER_NAME}: {striver_progress}%` |",
        f"| **LeetCode 500+** | {get_tgda_progress(lc_percent, 'ffa116')} | `🧩 Solved: {lc_solved}` |",
        f"| **CF Rating 1200** | ![WIP](https://img.shields.io/badge/Work_In_Progress-eb4034?style=flat-square) | `🏆 Active` |",
        "\n## 🕒 Recent Activity (Last 2 Days)",
        "| Problem | Platform | Difficulty | Date |",
        "| :--- | :--- | :---: | :---: |"
    ]

    sorted_probs = sorted(problems, key=lambda x: parse_date(x.get("Date", "")) or date.min, reverse=True)
    cutoff = date.today() - timedelta(days=2)
    count = 0
    for p in sorted_probs:
        p_date = parse_date(p.get("Date"))
        if (p_date and p_date >= cutoff) or count < 5:
            L.append(f"| [{p.get('Problem')}]({p.get('Link', '#')}) | {p.get('Platform')} | `{p.get('Difficulty')}` | {p.get('Date')} |")
            count += 1
            if count >= 8: break

    L.append(f'\n\n<div align="center">**System Last Sync:** `{now_ist.strftime("%d %b %Y | %I:%M %p IST")}`</div>')
    return "\n".join(L)

def main():
    lc = fetch_leetcode()
    problems = read_csv()
    with open(HEATMAP_FILE, "w", encoding="utf-8") as f: f.write(make_heatmap(problems))
    with open(README_FILE, "w", encoding="utf-8") as f: f.write(build_readme(problems, lc))
    print("✅ System Updated!")

if __name__ == "__main__":
    main()
    
