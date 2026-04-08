import csv, json, urllib.request
from datetime import datetime, timedelta, date, timezone
from collections import defaultdict

# --- CONFIG ---
LEETCODE_USER = "__vikram21"
CF_USER       = "__vikram21"
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
    return {"total": 0, "ranking": "N/A", "easy": 0, "medium": 0, "hard": 0}

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
    for fmt in ["%Y-%m-%d","%d %b %Y","%d-%m-%Y"]:
        try: return datetime.strptime(s.strip(), fmt).date()
        except: continue
    return None

def make_heatmap(problems):
    date_counts = defaultdict(int)
    for p in problems:
        d = parse_date(p.get("Date"))
        if d: date_counts[d] += 1
    today = date.today()
    weeks = 20
    start = today - timedelta(days=today.weekday() + 1 + (weeks - 1) * 7)
    cell, gap = 12, 3
    step = cell + gap
    w, h = weeks * step + 40, 7 * step + 40
    cells = []
    for week in range(weeks):
        for dow in range(7):
            day = start + timedelta(weeks=week, days=dow)
            x, y = 30 + week * step, 20 + dow * step
            if day > today: color = "#0d1117"
            else:
                cnt = date_counts.get(day, 0)
                color = "#161b22" if cnt==0 else "#0e4429" if cnt==1 else "#006d32" if cnt==2 else "#26a641" if cnt<=4 else "#39d353"
                cells.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{color}"><title>{day}: {cnt} problems</title></rect>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="#0d1117" rx="6"/><text x="10" y="15" fill="#8b949e" font-size="10" font-family="monospace">Practice Heatmap</text>{"".join(cells)}</svg>'

def get_pbar(done, total):
    percent = min(round((done / total) * 100, 1), 100)
    filled = int(percent / 5)
    return f"`{'█' * filled}{'░' * (20 - filled)}` **{percent}%**"

def build_readme(problems, lc):
    now_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    total_csv = len(problems)
    
    # Links
    lc_link = f"https://leetcode.com/{LEETCODE_USER}"
    cf_link = f"https://codeforces.com/profile/{CF_USER}"
    mail_link = f"mailto:{GMAIL}"

    # Header (Original Style + Animated)
    header = "https://capsule-render.vercel.app/api?type=rect&color=0:0d1117,50:0d2137,100:0d1117&height=180&section=header&text=DSA%20Forge&fontSize=60&fontColor=58a6ff&animation=fadeIn&fontAlignY=40&desc=%E2%9A%94%EF%B8%8F%20Vikram%20Negi%20%7C%20CSE%20Undergrad%20%7C%20Code%20Daily&descAlignY=62&descColor=c9d1d9&stroke=21262d&strokeWidth=1"

    L = [
        f'<div align="center">\n\n![]({header})\n\n',
        f'[![LeetCode](https://img.shields.io/badge/LeetCode-Profile-FFA116?style=for-the-badge&logo=leetcode&logoColor=black)]({lc_link})',
        f'[![Codeforces](https://img.shields.io/badge/Codeforces-Profile-1F8ACB?style=for-the-badge&logo=codeforces&logoColor=white)]({cf_link})',
        f'[![Gmail](https://img.shields.io/badge/Gmail-Connect-D14836?style=for-the-badge&logo=gmail&logoColor=white)]({mail_link})\n\n',
        '</div>\n\n---',
        "\n## 📈 Profile Stats",
        '<div align="center">',
        f'<img src="https://github-readme-stats.vercel.app/api?username={GITHUB_USER}&show_icons=true&theme=github_dark&hide_border=true" height="160" />',
        f'<img src="https://github-readme-streak-stats.herokuapp.com/?user={GITHUB_USER}&theme=github_dark&hide_border=true" height="160" />',
        '</div>\n',
        "## 🧩 LeetCode Mastery",
        f'<div align="center">\n<img src="https://leetcard.jacoblin.cool/{LEETCODE_USER}?theme=dark&font=Karma&ext=heatmap&border=0" width="90%" />\n</div>\n',
        "## 🔥 Practice Heatmap",
        '<div align="center">\n\n![Heatmap](heatmap.svg)\n\n</div>\n',
        "## 🎯 Current Targets",
        "| Target Objective | Progress | Status |",
        "| :--- | :--- | :---: |",
        f"| **Striver A2Z Sheet** | {get_pbar(total_csv, 455)} | 🚀 Grinding |",
        f"| **LeetCode 500+ Solves** | {get_pbar(lc['total'], 500)} | 🧩 {lc['total']}/500 |",
        f"| **CF Rating 1200+** | `In Progress` | 🏆 Competitive |",
        "\n## 🕒 Recent Activity (2 Days)",
        "| Problem | Platform | Difficulty | Date |",
        "| :--- | :--- | :---: | :---: |"
    ]

    sorted_probs = sorted(problems, key=lambda x: parse_date(x.get("Date", "")) or date.min, reverse=True)
    cutoff = date.today() - timedelta(days=2)
    
    count = 0
    for p in sorted_probs:
        p_date = parse_date(p.get("Date"))
        if (p_date and p_date >= cutoff) or count < 5:
            name, link = p.get("Problem", "N/A"), p.get("Link", "#")
            L.append(f"| [{name}]({link}) | {p.get('Platform')} | `{p.get('Difficulty')}` | {p.get('Date')} |")
            count += 1
            if count >= 8: break # Maximum 8 entries to keep it clean

    L.append(f'\n\n<div align="center">**System Sync:** `{now_ist.strftime("%d %b %Y | %I:%M %p")} IST`</div>')
    return "\n".join(L)

def main():
    lc = fetch_leetcode()
    problems = read_csv()
    with open(HEATMAP_FILE, "w", encoding="utf-8") as f: f.write(make_heatmap(problems))
    with open(README_FILE, "w", encoding="utf-8") as f: f.write(build_readme(problems, lc))
    print("✅ Dashboard Updated!")

if __name__ == "__main__":
    main()
    
