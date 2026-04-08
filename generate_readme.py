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

# AGAR API SE STREAK SAHI NAHI AA RAHI, TOH YE MANUALLY UPDATE KAR SAKTE HO
MY_ACTUAL_STREAK = 68 

def fetch_leetcode_stats():
    url = f"https://leetcode-stats-api.herokuapp.com/{LEETCODE_USER}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())
        if d.get("status") == "success":
            return {"total": d.get("totalSolved", 0), "ranking": d.get("ranking", "N/A")}
    except: pass
    return {"total": 104, "ranking": "N/A"}

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

def get_anim_bar(percent, color="00ff00"):
    # Animated SVG Progress Bar
    return f"![Progress](https://geps.dev/progress/{int(percent)}?successColor={color}&warningColor=ffff00&dangerColor=ff0000)"

def build_readme(problems, lc):
    now_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    
    # Logic: Agar CSV se streak zyada hai toh woh, varna manual waali
    total_problems = len(problems)
    striver_progress = 19
    lc_solved = max(lc['total'], 104)
    lc_percent = (lc_solved / 500) * 100

    # Header & Graphics
    # Capsule Render with 'waving' and 'twinkling' for animation
    header = "https://capsule-render.vercel.app/api?type=waving&color=0:0d1117,50:1a2332,100:0d1117&height=220&section=header&text=DSA%20FORGE%20v4&fontSize=75&fontColor=58a6ff&animation=twinkling&fontAlignY=40&desc=%E2%9A%94%EF%B8%8F%20Vikram%20Negi%20%7C%20Code%20.%20Survive%20.%20Win&descAlignY=65&descColor=c9d1d9"
    
    # Tgda Animated Activity Graph
    anim_graph = f"https://github-readme-activity-graph.vercel.app/graph?username={GITHUB_USER}&bg_color=0d1117&color=58a6ff&line=58a6ff&point=ffffff&area=true&area_color=121d2f&hide_border=true&custom_title=LIVE%20CODING%20PULSE"

    L = [
        f'<div align="center">\n\n![]({header})\n\n',
        # Uniform Heavy Badges
        f'[![Gmail](https://img.shields.io/badge/GMAIL-vikramnegi0021-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:{GMAIL}) ',
        f'[![LeetCode](https://img.shields.io/badge/LEETCODE-Profile-FFA116?style=for-the-badge&logo=leetcode&logoColor=black)](https://leetcode.com/{LEETCODE_USER}) ',
        f'[![Codeforces](https://img.shields.io/badge/CODEFORCES-Profile-1F8ACB?style=for-the-badge&logo=codeforces&logoColor=white)](https://codeforces.com/profile/{CF_USER}) ',
        f'[![Streak](https://img.shields.io/badge/LEETCODE_STREAK-{MY_ACTUAL_STREAK}_DAYS-FF7B00?style=for-the-badge&logo=fire&logoColor=white)](https://leetcode.com/{LEETCODE_USER})\n\n',
        '</div>\n\n---',
        "\n## 🚀 System Performance",
        '<div align="center">',
        f'<img src="https://github-readme-stats.vercel.app/api?username={GITHUB_USER}&show_icons=true&theme=tokyonight&hide_border=true" height="175" />',
        f'<img src="https://github-readme-streak-stats.herokuapp.com/?user={GITHUB_USER}&theme=tokyonight&hide_border=true" height="175" />',
        '</div>\n',
        "## 📈 Animated Activity Flow",
        f'<div align="center">\n<img src="{anim_graph}" width="100%" />\n</div>\n',
        "## 🧩 LeetCode Mastery",
        f'<div align="center">\n<img src="https://leetcard.jacoblin.cool/{LEETCODE_USER}?theme=dark&font=Karma&ext=heatmap&border=0" width="100%" />\n</div>\n',
        "## 🎯 Targets",
        "| Objective | Mastery Progress (Animated) | Current Status |",
        "| :--- | :--- | :---: |",
        f"| **Striver A2Z Sheet** | {get_anim_bar(striver_progress, '58a6ff')} | `⚡ {STRIVER_NAME}: {striver_progress}%` |",
        f"| **LeetCode 500+** | {get_anim_bar(lc_percent, 'ffa116')} | `🧩 Solved: {lc_solved}` |",
        f"| **CF Rating 1200** | ![WIP](https://img.shields.io/badge/Targeting-1200-eb4034?style=flat-square&logo=target) | `🏆 Active` |",
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
    print("🚀 Initializing Cyber-Dashboard Sync...")
    lc_stats = fetch_leetcode_stats()
    problems_data = read_csv()
    with open(README_FILE, "w", encoding="utf-8") as f: f.write(build_readme(problems_data, lc_stats))
    print("✅ Full Animated Update Complete!")

if __name__ == "__main__":
    main()
    
