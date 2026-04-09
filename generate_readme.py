import csv, json, urllib.request, math
from datetime import datetime, timedelta, date, timezone
from collections import defaultdict

# ─── CONFIG ───────────────────────────────────────────────
LEETCODE_USER = "__vikram21"
CF_USER       = "__vikram21"
GITHUB_USER   = "vikramnegi21"
GMAIL         = "vikramnegi0021@gmail.com"
CSV_FILE      = "problems.csv"
README_FILE   = "README.md"

STRIVER_TOTAL = 455
LC_TARGET     = 500
CF_TARGET     = 1200

# Fallback if CSV streak calc fails
MANUAL_STREAK = 69
# ──────────────────────────────────────────────────────────


def fetch_leetcode_stats():
    url = f"https://leetcode-stats-api.herokuapp.com/{LEETCODE_USER}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=12) as r:
            d = json.loads(r.read())
        if d.get("status") == "success":
            return {
                "total":   d.get("totalSolved", 0),
                "easy":    d.get("easySolved",  0),
                "medium":  d.get("mediumSolved", 0),
                "hard":    d.get("hardSolved",   0),
                "ranking": d.get("ranking", "N/A"),
            }
    except Exception as e:
        print(f"[WARN] LeetCode API: {e}")
    return {"total": 106, "easy": 62, "medium": 44, "hard": 0, "ranking": "N/A"}


def read_csv():
    rows = []
    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append({str(k).strip(): str(v).strip() for k, v in r.items() if k})
    except Exception as e:
        print(f"[WARN] CSV read: {e}")
    return rows


def parse_date(s):
    if not s: return None
    for fmt in ["%Y-%m-%d", "%d %b %Y", "%d %b", "%d-%m-%Y", "%b %d, %Y"]:
        try:
            d = datetime.strptime(s.strip(), fmt)
            if d.year == 1900:
                d = d.replace(year=date.today().year)
            return d.date()
        except:
            continue
    return None


def compute_streak(problems):
    solved_dates = set()
    for p in problems:
        d = parse_date(p.get("Date", ""))
        if d:
            solved_dates.add(d)
    if not solved_dates:
        return MANUAL_STREAK, MANUAL_STREAK

    today = date.today()
    streak = 0
    check = today
    while check in solved_dates:
        streak += 1
        check -= timedelta(days=1)
    if streak == 0:
        check = today - timedelta(days=1)
        while check in solved_dates:
            streak += 1
            check -= timedelta(days=1)

    sorted_dates = sorted(solved_dates)
    longest = cur = 1
    for i in range(1, len(sorted_dates)):
        if (sorted_dates[i] - sorted_dates[i - 1]).days == 1:
            cur += 1
            longest = max(longest, cur)
        else:
            cur = 1

    final_streak = max(streak, MANUAL_STREAK)
    return final_streak, max(longest, final_streak)


def count_by_date(problems):
    counts = defaultdict(int)
    for p in problems:
        d = parse_date(p.get("Date", ""))
        if d:
            counts[d] += 1
    return counts


# ─── HEATMAP SVG (last 24 weeks) ──────────────────────────
def generate_heatmap_svg(problems):
    counts = count_by_date(problems)
    today  = date.today()

    days_since_sunday = (today.weekday() + 1) % 7
    end_date   = today + timedelta(days=(6 - days_since_sunday))
    start_date = end_date - timedelta(weeks=24) + timedelta(days=1)

    CELL  = 13
    GAP   = 3
    COLS  = 24
    ROWS  = 7
    PAD_L = 28
    PAD_T = 28
    W = PAD_L + COLS * (CELL + GAP) + 10
    H = PAD_T + ROWS * (CELL + GAP) + 30

    grid = []
    cur = start_date
    col = []
    while cur <= end_date:
        col.append(cur)
        if cur.weekday() == 6:
            grid.append(col)
            col = []
        cur += timedelta(days=1)
    if col:
        grid.append(col)

    max_count = max((counts.get(d, 0) for col in grid for d in col), default=1)
    max_count = max(max_count, 1)

    def cell_color(c):
        if c == 0: return "#161b22"
        t = c / max_count
        if t < 0.25: return "#0e4429"
        if t < 0.50: return "#006d32"
        if t < 0.75: return "#26a641"
        return "#39d353"

    cells_svg = ""
    month_labels = {}

    for ci, col in enumerate(grid):
        for ri, d in enumerate(col):
            if d > today: continue
            x = PAD_L + ci * (CELL + GAP)
            y = PAD_T + ri * (CELL + GAP)
            c = counts.get(d, 0)
            tip = f"{d.strftime('%d %b')}: {c} problem{'s' if c!=1 else ''}"
            cells_svg += (
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                f'rx="3" fill="{cell_color(c)}"><title>{tip}</title></rect>\n'
            )
            if ri == 0 and d.day <= 7:
                month_labels[ci] = d.strftime('%b')

    month_svg = ""
    for ci, label in month_labels.items():
        x = PAD_L + ci * (CELL + GAP)
        month_svg += f'<text x="{x}" y="{PAD_T - 6}" font-family="Segoe UI" font-size="9" fill="#484f58">{label}</text>\n'

    day_labels = ["", "Mon", "", "Wed", "", "Fri", ""]
    day_svg = ""
    for ri, label in enumerate(day_labels):
        if label:
            y = PAD_T + ri * (CELL + GAP) + CELL - 2
            day_svg += f'<text x="2" y="{y}" font-family="Segoe UI" font-size="9" fill="#484f58">{label}</text>\n'

    total_solved = sum(counts.values())

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" rx="12" fill="#0d1117"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="none" stroke="#21262d" stroke-width="1"/>
  <text x="{W//2}" y="16" font-family="Segoe UI" font-size="10" font-weight="700"
    fill="#484f58" text-anchor="middle" letter-spacing="2">DSA ACTIVITY  —  LAST 24 WEEKS</text>
  {month_svg}
  {day_svg}
  {cells_svg}
  <text x="{PAD_L}" y="{H - 6}" font-family="Segoe UI" font-size="9" fill="#484f58">{total_solved} problems logged</text>
  <text x="{W - 86}" y="{H - 6}" font-family="Segoe UI" font-size="9" fill="#484f58">Less</text>
  <rect x="{W - 78}" y="{H - 18}" width="{CELL}" height="{CELL}" rx="3" fill="#161b22"/>
  <rect x="{W - 62}" y="{H - 18}" width="{CELL}" height="{CELL}" rx="3" fill="#0e4429"/>
  <rect x="{W - 46}" y="{H - 18}" width="{CELL}" height="{CELL}" rx="3" fill="#006d32"/>
  <rect x="{W - 30}" y="{H - 18}" width="{CELL}" height="{CELL}" rx="3" fill="#26a641"/>
  <rect x="{W - 14}" y="{H - 18}" width="{CELL}" height="{CELL}" rx="3" fill="#39d353"/>
</svg>"""

    with open("heatmap.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("heatmap.svg -> done")


# ─── TARGETS SVG ──────────────────────────────────────────
def generate_targets_svg(total_csv, lc_solved, striver_pct, lc_pct):
    def bar_w(pct, max_w=632):
        return max(10, round(pct / 100 * max_w))

    def grad_cols(pct):
        if pct < 30: return "#e74c3c", "#c0392b"
        if pct < 65: return "#f39c12", "#e67e22"
        return "#2ecc71", "#27ae60"

    s_c1, s_c2 = grad_cols(striver_pct)
    l_c1, l_c2 = grad_cols(lc_pct)
    s_w = bar_w(striver_pct)
    l_w = bar_w(lc_pct)
    cf_w = bar_w(20)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="720" height="220" viewBox="0 0 720 220">
  <defs>
    <style>
      @keyframes b1 {{ from{{width:0}} to{{width:{s_w}px}} }}
      @keyframes b2 {{ from{{width:0}} to{{width:{l_w}px}} }}
      @keyframes b3 {{ from{{width:0}} to{{width:{cf_w}px}} }}
      .r1 {{ animation: b1 1.6s cubic-bezier(.4,0,.2,1) 0.1s both }}
      .r2 {{ animation: b2 1.6s cubic-bezier(.4,0,.2,1) 0.25s both }}
      .r3 {{ animation: b3 1.6s cubic-bezier(.4,0,.2,1) 0.4s both }}
    </style>
    <linearGradient id="g1" x1="0" x2="1"><stop offset="0%" stop-color="{s_c1}"/><stop offset="100%" stop-color="{s_c2}"/></linearGradient>
    <linearGradient id="g2" x1="0" x2="1"><stop offset="0%" stop-color="{l_c1}"/><stop offset="100%" stop-color="{l_c2}"/></linearGradient>
    <linearGradient id="g3" x1="0" x2="1"><stop offset="0%" stop-color="#89b4fa"/><stop offset="100%" stop-color="#74c7ec"/></linearGradient>
    <linearGradient id="bg" x1="0" x2="0" y1="0" y2="1"><stop offset="0%" stop-color="#1e1e2e"/><stop offset="100%" stop-color="#181825"/></linearGradient>
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="720" height="220" rx="14" fill="url(#bg)"/>
  <rect x="1" y="1" width="718" height="218" rx="14" fill="none" stroke="#313244" stroke-width="1.5"/>

  <text x="26" y="36" font-family="Segoe UI" font-size="11" font-weight="700" fill="#a6adc8" letter-spacing="1">STRIVER A2Z SHEET</text>
  <text x="694" y="36" font-family="Segoe UI" font-size="12" font-weight="700" fill="#cba6f7" text-anchor="end">{total_csv} / {STRIVER_TOTAL}   {striver_pct}%</text>
  <rect x="26" y="44" width="668" height="12" rx="6" fill="#313244"/>
  <rect x="26" y="44" width="0"   height="12" rx="6" fill="url(#g1)" class="r1" filter="url(#glow)"/>
  <text x="26" y="72" font-family="Segoe UI" font-size="10" fill="#45475a">Complete Striver's A2Z DSA Course Sheet — 455 problems total</text>

  <text x="26" y="100" font-family="Segoe UI" font-size="11" font-weight="700" fill="#a6adc8" letter-spacing="1">LEETCODE 500+</text>
  <text x="694" y="100" font-family="Segoe UI" font-size="12" font-weight="700" fill="#cba6f7" text-anchor="end">{lc_solved} / {LC_TARGET}   {lc_pct}%</text>
  <rect x="26" y="108" width="668" height="12" rx="6" fill="#313244"/>
  <rect x="26" y="108" width="0"   height="12" rx="6" fill="url(#g2)" class="r2" filter="url(#glow)"/>
  <text x="26" y="136" font-family="Segoe UI" font-size="10" fill="#45475a">Reach 500 LeetCode accepted solutions — {LEETCODE_USER}</text>

  <text x="26" y="164" font-family="Segoe UI" font-size="11" font-weight="700" fill="#a6adc8" letter-spacing="1">CODEFORCES RATING 1200+</text>
  <text x="694" y="164" font-family="Segoe UI" font-size="12" font-weight="700" fill="#89b4fa" text-anchor="end">Targeting {CF_TARGET}</text>
  <rect x="26" y="172" width="668" height="12" rx="6" fill="#313244"/>
  <rect x="26" y="172" width="0"   height="12" rx="6" fill="url(#g3)" class="r3" filter="url(#glow)"/>
  <text x="26" y="200" font-family="Segoe UI" font-size="10" fill="#45475a">Active on Codeforces — handle: {CF_USER}</text>
</svg>"""

    with open("targets.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("targets.svg -> done")


# ─── RECENT ACTIVITY SVG ──────────────────────────────────
def generate_recent_activity_svg(problems, days=7):
    today  = date.today()
    cutoff = today - timedelta(days=days)

    recent = []
    for p in problems:
        d = parse_date(p.get("Date", ""))
        if d and d >= cutoff:
            recent.append((d, p))
    recent.sort(key=lambda x: x[0], reverse=True)
    recent = recent[:10]

    if not recent:
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="720" height="70">'
            '<rect width="720" height="70" rx="12" fill="#1e1e2e"/>'
            '<text x="360" y="42" font-family="Segoe UI" font-size="13" '
            'fill="#585b70" text-anchor="middle">No problems logged in last 7 days.</text>'
            '</svg>'
        )
        with open("recent_activity.svg", "w", encoding="utf-8") as f:
            f.write(svg)
        return

    ROW_H = 38
    H = 48 + len(recent) * ROW_H + 10

    def diff_style(d):
        d = d.lower().strip()
        if d == 'easy':   return '#a6e3a1', '#1a3329'
        if d == 'medium': return '#fab387', '#3a2515'
        if d == 'hard':   return '#f38ba8', '#3a1520'
        try:
            n = int(d)
            if n <= 1000: return '#a6e3a1', '#1a3329'
            if n <= 1500: return '#fab387', '#3a2515'
            return '#f38ba8', '#3a1520'
        except:
            return '#89b4fa', '#151f3a'

    rows_svg = ""
    for i, (d, p) in enumerate(recent):
        y = 50 + i * ROW_H
        bg = "#181825" if i % 2 == 0 else "#1e1e2e"
        prob = p.get('Problem', 'Unknown')[:44]
        plat = p.get('Platform', '')
        diff = p.get('Difficulty', '')
        tc, bc = diff_style(diff)
        date_str = d.strftime('%d %b')
        delay = i * 0.07

        rows_svg += f"""
  <g style="animation: fi 0.35s ease {delay:.2f}s both">
    <rect x="0" y="{y - 14}" width="720" height="{ROW_H}" fill="{bg}"/>
    <text x="18" y="{y + 6}" font-family="Segoe UI" font-size="11" fill="#6c7086">{i+1}</text>
    <text x="36" y="{y + 6}" font-family="Segoe UI" font-size="12" fill="#cdd6f4">{prob}</text>
    <text x="450" y="{y + 6}" font-family="Segoe UI" font-size="11" fill="#89b4fa">{plat}</text>
    <rect x="552" y="{y - 7}" width="74" height="19" rx="9" fill="{bc}"/>
    <text x="589" y="{y + 6}" font-family="Segoe UI" font-size="11" fill="{tc}" text-anchor="middle">{diff}</text>
    <text x="702" y="{y + 6}" font-family="Segoe UI" font-size="11" fill="#585b70" text-anchor="end">{date_str}</text>
  </g>"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{H}" viewBox="0 0 720 {H}">
  <defs>
    <style>@keyframes fi {{ from{{opacity:0;transform:translateY(5px)}} to{{opacity:1;transform:none}} }}</style>
    <linearGradient id="bg" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stop-color="#1e1e2e"/>
      <stop offset="100%" stop-color="#181825"/>
    </linearGradient>
  </defs>
  <rect width="720" height="{H}" rx="14" fill="url(#bg)"/>
  <rect x="1" y="1" width="718" height="{H-2}" rx="14" fill="none" stroke="#313244" stroke-width="1.5"/>
  <text x="18"  y="26" font-family="Segoe UI" font-size="10" font-weight="700" fill="#45475a" letter-spacing="1">#</text>
  <text x="36"  y="26" font-family="Segoe UI" font-size="10" font-weight="700" fill="#45475a" letter-spacing="1">PROBLEM</text>
  <text x="450" y="26" font-family="Segoe UI" font-size="10" font-weight="700" fill="#45475a" letter-spacing="1">PLATFORM</text>
  <text x="589" y="26" font-family="Segoe UI" font-size="10" font-weight="700" fill="#45475a" text-anchor="middle" letter-spacing="1">DIFF</text>
  <text x="702" y="26" font-family="Segoe UI" font-size="10" font-weight="700" fill="#45475a" text-anchor="end" letter-spacing="1">DATE</text>
  <line x1="0" y1="34" x2="720" y2="34" stroke="#313244" stroke-width="1"/>
  {rows_svg}
</svg>"""

    with open("recent_activity.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("recent_activity.svg -> done")


# ─── BUILD README ──────────────────────────────────────────
def build_readme(problems, lc):
    now_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)

    total       = len(problems)
    lc_solved   = max(lc['total'], 106)
    striver_pct = min(100, round(total / STRIVER_TOTAL * 100, 1))
    lc_pct      = min(100, round(lc_solved / LC_TARGET * 100, 1))
    cur_streak, longest = compute_streak(problems)

    generate_heatmap_svg(problems)
    generate_targets_svg(total, lc_solved, striver_pct, lc_pct)
    generate_recent_activity_svg(problems, days=7)

    header_url = (
        "https://capsule-render.vercel.app/api?type=waving"
        "&color=0:0d1117,30:0a192f,70:0d2137,100:0d1117"
        "&height=230&section=header"
        "&text=DSA%20FORGE%20v4&fontSize=78&fontColor=58a6ff"
        "&animation=twinkling&fontAlignY=42"
        "&desc=Vikram%20Negi%20%7C%20Code%20.%20Survive%20.%20Win"
        "&descAlignY=66&descColor=8b949e&descSize=18"
    )
    anim_graph = (
        "https://github-readme-activity-graph.vercel.app/graph"
        f"?username={GITHUB_USER}"
        "&bg_color=0d1117&color=58a6ff&line=1f6feb"
        "&point=58a6ff&area=true&area_color=0a192f"
        "&hide_border=true&custom_title=LIVE%20CODING%20PULSE&radius=6"
    )

    L = []
    a = L.append

    a('<div align="center">\n\n')
    a(f'![]({header_url})\n\n')
    a(
        f'[![Gmail](https://img.shields.io/badge/GMAIL-vikramnegi0021-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:{GMAIL})'
        f'&nbsp;&nbsp;'
        f'[![LeetCode](https://img.shields.io/badge/LEETCODE-{LEETCODE_USER}-FFA116?style=for-the-badge&logo=leetcode&logoColor=black)](https://leetcode.com/{LEETCODE_USER})\n\n'
        f'[![Codeforces](https://img.shields.io/badge/CODEFORCES-{CF_USER}-1F8ACB?style=for-the-badge&logo=codeforces&logoColor=white)](https://codeforces.com/profile/{CF_USER})'
        f'&nbsp;&nbsp;'
        f'[![Streak](https://img.shields.io/badge/STREAK-{cur_streak}%20DAYS-FF7B00?style=for-the-badge&logo=fire&logoColor=white)](https://leetcode.com/{LEETCODE_USER})\n\n'
    )
    a('</div>\n\n---\n\n')

    a('## System Performance\n\n<div align="center">\n\n')
    a(f'<img src="https://github-readme-stats.vercel.app/api?username={GITHUB_USER}&show_icons=true&theme=tokyonight&hide_border=true&rank_icon=github" height="170" />&nbsp;')
    a(f'<img src="https://github-readme-streak-stats.herokuapp.com/?user={GITHUB_USER}&theme=tokyonight&hide_border=true" height="170" />\n\n')
    a('</div>\n\n---\n\n')

    a('## Activity Flow\n\n<div align="center">\n\n')
    a(f'<img src="{anim_graph}" width="100%" />\n\n')
    a('</div>\n\n---\n\n')

    a('## LeetCode\n\n<div align="center">\n\n')
    a(f'<img src="https://leetcard.jacoblin.cool/{LEETCODE_USER}?theme=dark&font=Karma&ext=heatmap&border=0&radius=12" width="96%" />\n\n')
    a('</div>\n\n---\n\n')

    a('## DSA Heatmap\n\n<div align="center">\n\n')
    a('<img src="heatmap.svg" width="100%" />\n\n')
    a('</div>\n\n---\n\n')

    a('## Targets\n\n<div align="center">\n\n')
    a('<img src="targets.svg" width="100%" />\n\n')
    a('</div>\n\n---\n\n')

    a('## Recent Activity\n\n<div align="center">\n\n')
    a('<img src="recent_activity.svg" width="100%" />\n\n')
    a('</div>\n\n---\n\n')

    a(f'<div align="center">\n\n`Last Sync : {now_ist.strftime("%d %b %Y  |  %I:%M %p IST")}`\n\n</div>\n')

    return "".join(L)


def main():
    print("DSA Forge — starting sync...")
    lc_stats      = fetch_leetcode_stats()
    problems_data = read_csv()
    readme        = build_readme(problems_data, lc_stats)
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"Done — {len(problems_data)} problems loaded, all SVGs + README updated.")

if __name__ == "__main__":
    main()
    
