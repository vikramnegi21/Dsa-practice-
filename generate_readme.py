import csv, json, urllib.request
from datetime import datetime, timedelta, date, timezone
from collections import defaultdict

# --- CONFIG ---
LEETCODE_USER = "__vikram21"
CF_USER       = "__vikram21"
STRIVER_NAME  = "__vikram"
GITHUB_USER   = "vikramnegi21"
GMAIL         = "vikramnegi0021@gmail.com"
CSV_FILE      = "problems.csv"
README_FILE   = "README.md"
HEATMAP_FILE  = "heatmap.svg"

def fetch_leetcode_stats():
    url = f"https://leetcode-stats-api.herokuapp.com/{LEETCODE_USER}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())
        if d.get("status") == "success":
            return {
                "total": d.get("totalSolved", 0),
                "ranking": d.get("ranking", "N/A")
            }
    except: pass
    return {"total": 104, "ranking": "N/A"} # Fallback

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
    formats = ["%Y-%m-%d", "%d %b %Y", "%d %b", "%d-%m-%Y", "%b %d, %Y", "%d %B", "%Y/%m/%d"]
    for fmt in formats:
        try:
            d = datetime.strptime(s.strip(), fmt)
            if d.year == 1900: d = d.replace(year=date.today().year)
            return d.date()
        except: continue
    return None

# --- Custom Heatmap (Static based on CSV) ---
def make_heatmap(problems):
    date_counts = defaultdict(int)
    for p in problems:
        d = parse_date(p.get("Date"))
        if d: date_counts[d] += 1
    today = date.today()
    weeks = 20
    start = today - timedelta(days=today.weekday() + 1 + (weeks - 1) * 7)
    cell, gap = 13, 3
    step = cell + gap
    w, h = weeks * step + 60, 7 * step + 50
    cells = []
    for week in range(weeks):
        for dow in range(7):
            day = start + timedelta(weeks=week, days=dow)
            x, y = 40 + week * step, 30 + dow * step
            if day > today: color = "#0d1117"; opacity="0.3"
            else:
                cnt = date_counts.get(day, 0)
                opacity="1.0"
                if cnt == 0: color = "#161b22"
                elif cnt == 1: color = "#0e4429"
                elif cnt == 2: color = "#006d32"
                elif cnt <= 4: color = "#26a641"
                else: color = "#39d353"
            cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{color}" opacity="{opacity}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">
    <rect width="100%" height="100%" fill="#0d1117" rx="10"/>
    <text x="20" y="20" fill="#8b949e" font-size="11" font-family="monospace" font-weight="bold">LOGGED PRACTICE LOG (CSV)</text>
    {"".join(cells)}</svg>'''

def calculate_streak(problems):
    lc_dates = set()
    for p in problems:
        if p.get("Platform") == "LeetCode":
            d = parse_date(p.get("Date"))
            if d: lc_dates.add(d)
    if not lc_dates: return 0
    today = date.today()
    curr_date = today
    streak = 0
    while curr_date in lc_dates:
        streak += 1
        curr_date -= timedelta(days=1)
    if streak == 0: # Check if yesterday was logged to maintain streak
        yesterday = today - timedelta(days=1)
        curr_date = yesterday
        while curr_date in lc_dates:
            streak += 1
            curr_date -= timedelta(days=1)
    return streak

def get_progress_bar(percent, color="39d353"):
    return f"![Progress](https://geps.dev/progress/{int(percent)}?successColor={color}&warningColor=f1c40f&dangerColor=ff4b4b)"

def build_readme(problems, lc):
    now_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    
    # Progress Calcs
    total_problems = len(problems)
    striver_progress = 19
    lc_solved = max(lc['total'], 104)
    lc_percent = (lc_solved / 500) * 100
    lc_streak = calculate_streak(problems)

    # Dynamic Graph & Badges
    header = "https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:0d2137,100:0d1117&height=180&section=header&text=DSA%20FORGE%20v3.1&fontSize=65&fontColor=58a6ff&animation=fadeIn&fontAlignY=40&desc=%F0%9F%9A%80%20Vikram%20Negi%20%7C%20Leveling%20Up%20Daily&descAlignY=62&descColor=c9d1d9&stroke=21262d&strokeWidth=1"
    
    # Fully Animated Contribution Graph (Live data, not CSV)
    animated_graph_url = f"https://github-readme-activity-graph.vercel.app/graph?username={GITHUB_USER}&bg_color=0d1117&color=58a6ff&line=58a6ff&point=ffffff&area=true&area_color=121d2f&hide_border=true&custom_title=LIVE%20CODING%20ACTIVITY%20FLOW"

    L = [
        f'<div align="center">\n\n![]({header})\n\n',
        f'[![Gmail](https://img.shields.io/badge/vikramnegi0021-Connect-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:{GMAIL})',
        f'[![LeetCode](https://img.shields.io/badge/LeetCode-Profile-FFA116?style=flat-square&logo=leetcode&logoColor=black)](https://leetcode.com/{LEETCODE_USER})',
        f'[![Codeforces](https://img.shields.io/badge/Codeforces-Profile-1F8ACB?style=flat-square&logo=codeforces&logoColor=white)](https://codeforces.com/profile/{CF_USER})',
        f'[![LeetCode Streak](https://img.shields.io/badge/LeetCode%20Streak-{lc_streak}%20Days-FF7B00?style=flat-square&logo=checkmarx)](https://leetcode.com/{LEETCODE_USER})\n\n',
        '</div>\n\n---',
        "\n## ⚡ Live Performance Dashboard",
        '<div align="center">',
        f'<img src="https://github-readme-stats.vercel.app/api?username={GITHUB_USER}&show_icons=true&theme=tokyonight&hide_border=true" height="170" />',
        f'<img src="https://github-readme-streak-stats.herokuapp.com/?user={GITHUB_USER}&theme=tokyonight&hide_border=true" height="170" />',
        '</div>\n',
        "## 🔥 Dynamic Activity Graph",
        f'<div align="center">\n<img src="{animated_graph_url}" width="100%" alt="Animated Contribution Graph"/>\n</div>\n',
        "## 🧩 LeetCode Mastery",
        f'<div align="center">\n<img src="https://leetcard.jacoblin.cool/{LEETCODE_USER}?theme=dark&font=Karma&ext=heatmap&border=0" width="100%" />\n</div>\n',
        "## 🎯 Strategic Targets",
        "| Objective | Animated Progress | Status Tracking |",
        "| :--- | :--- | :---: |",
        f"| **Striver A2Z Sheet** | {get_progress_bar(striver_progress, '58a6ff')} | `⚡ {STRIVER_NAME}: {striver_progress}%` |",
        f"| **LeetCode 500+** | {get_progress_bar(lc_percent, 'ffa116')} | `🧩 Solved: {lc_solved}` |",
        f"| **CF Rating 1200** | ![WIP](https://img.shields.io/badge/Work_In_Progress-eb4034?style=flat-square) | `🏆 Competing` |",
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
    print("🚀 Initializing Animated Dashboard Sync...")
    lc_stats = fetch_leetcode_stats()
    problems_data = read_csv()
    with open(README_FILE, "w", encoding="utf-8") as f: f.write(build_readme(problems_data, lc_stats))
    print("✅ System Fully Updated & Animated!")

if __name__ == "__main__":
    main()
    
