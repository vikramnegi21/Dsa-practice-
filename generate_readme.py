import csv, json, urllib.request
from datetime import datetime, timedelta, date
from collections import defaultdict

LEETCODE_USER = "vikramnegi21"
GITHUB_USER = "vikramnegi21"
CSV_FILE = "problems.csv"
README_FILE = "README.md"
HEATMAP_FILE = "heatmap.svg"

# ── LeetCode API ──────────────────────────────────────────────
def fetch_leetcode():
    url = f"https://leetcode-stats-api.herokuapp.com/{LEETCODE_USER}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read())
        if d.get("status") == "success":
            return {
                "total":   d.get("totalSolved", 0),
                "easy":    d.get("easySolved",  0),
                "medium":  d.get("mediumSolved",0),
                "hard":    d.get("hardSolved",  0),
                "ranking": d.get("ranking",    "N/A"),
            }
    except Exception as e:
        print(f"LeetCode API error: {e}")
    return {"total": 0, "easy": 0, "medium": 0, "hard": 0, "ranking": "N/A"}

# ── CSV ───────────────────────────────────────────────────────
def read_csv():
    rows = []
    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            for r in csv.DictReader(f):
                rows.append({k: v.strip() for k, v in r.items()})
    except FileNotFoundError:
        print("problems.csv not found")
    return rows

def parse_date(s):
    for fmt in ["%Y-%m-%d", "%d %b %Y", "%d %b", "%d-%m-%Y", "%b %d, %Y"]:
        try:
            d = datetime.strptime(s.strip(), fmt)
            return d.replace(year=datetime.now().year).date() if d.year == 1900 else d.date()
        except:
            continue
    return None

# ── Streak ───────────────────────────────────────────────────
def calc_streak(problems):
    dates = set(filter(None, (parse_date(p["Date"]) for p in problems)))
    if not dates:
        return 0, 0
    today = date.today()
    cur = 0
    d = today
    while d in dates:
        cur += 1
        d -= timedelta(days=1)
    if cur == 0:
        d = today - timedelta(days=1)
        while d in dates:
            cur += 1
            d -= timedelta(days=1)
    slist = sorted(dates)
    best = cur2 = 1
    for i in range(1, len(slist)):
        if (slist[i] - slist[i-1]).days == 1:
            cur2 += 1
            best = max(best, cur2)
        else:
            cur2 = 1
    best = max(best, cur)
    return cur, best

# ── Helpers ──────────────────────────────────────────────────
def last_n_days(problems, n=7):
    cutoff = date.today() - timedelta(days=n)
    res = [p for p in problems if (parse_date(p["Date"]) or date.min) > cutoff]
    return sorted(res, key=lambda x: parse_date(x["Date"]) or date.min, reverse=True)

def count_by(problems, key):
    c = defaultdict(int)
    for p in problems:
        v = p.get(key, "").strip()
        if v:
            c[v] += 1
    return dict(c)

# ── Heatmap SVG ──────────────────────────────────────────────
def make_heatmap(problems, weeks=13):
    date_counts = defaultdict(int)
    for p in problems:
        d = parse_date(p["Date"])
        if d:
            date_counts[d] += 1

    today = date.today()
    # Align start to Sunday, 13 weeks back
    start = today - timedelta(days=today.weekday() + 1 + (weeks - 1) * 7)

    cell, gap = 12, 3
    step = cell + gap
    w = weeks * step + 44
    h = 7 * step + 44

    cells = []
    month_labels = {}

    for week in range(weeks):
        for dow in range(7):  # 0=Sun … 6=Sat
            day = start + timedelta(weeks=week, days=dow)
            x = 32 + week * step
            y = 20 + dow * step

            if day > today:
                cells.append(
                    f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                    f'rx="2" fill="#161b22" opacity="0.3"/>'
                )
            else:
                cnt = date_counts.get(day, 0)
                color = (
                    "#161b22" if cnt == 0 else
                    "#0e4429" if cnt == 1 else
                    "#006d32" if cnt == 2 else
                    "#26a641" if cnt <= 4 else
                    "#39d353"
                )
                cells.append(
                    f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                    f'rx="2" fill="{color}">'
                    f'<title>{day.strftime("%d %b %Y")}: {cnt} problem{"s" if cnt!=1 else ""}</title>'
                    f'</rect>'
                )
            if dow == 0 and day.day <= 7:
                month_labels[week] = day.strftime("%b")

    month_svg = "".join(
        f'<text x="{32 + w_ * step}" y="13" fill="#8b949e" '
        f'font-size="10" font-family="monospace">{m}</text>'
        for w_, m in month_labels.items()
    )
    day_names = ["S", "M", "T", "W", "T", "F", "S"]
    day_svg = "".join(
        f'<text x="2" y="{20 + i * step + 9}" fill="#8b949e" '
        f'font-size="9" font-family="monospace">{day_names[i]}</text>'
        for i in range(7)
    )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">'
        f'<rect width="{w}" height="{h}" rx="8" fill="#0d1117"/>'
        f'{month_svg}{day_svg}{"".join(cells)}'
        f'<text x="{w - 92}" y="{h - 5}" fill="#8b949e" font-size="9" font-family="monospace">Less</text>'
    )
    for i, col in enumerate(["#161b22", "#0e4429", "#26a641", "#39d353"]):
        svg += f'<rect x="{w - 68 + i * 14}" y="{h - 15}" width="10" height="10" rx="2" fill="{col}"/>'
    svg += (
        f'<text x="{w - 4}" y="{h - 5}" fill="#8b949e" font-size="9" '
        f'font-family="monospace" text-anchor="end">More</text>'
        f'</svg>'
    )
    return svg

# ── README Builder ────────────────────────────────────────────
def build_readme(problems, lc):
    now = datetime.utcnow().strftime("%d %b %Y, %H:%M UTC")
    cur_streak, best_streak = calc_streak(problems)
    topics  = dict(sorted(count_by(problems, "Topic").items(),    key=lambda x: -x[1]))
    diff    = count_by(problems, "Difficulty")
    plat    = count_by(problems, "Platform")
    total   = len(problems)
    recent  = last_n_days(problems, 7)
    local_lc = plat.get("LeetCode", 0)
    local_cf = plat.get("Codeforces", 0)

    # Prefer API data; fallback to local CSV counts
    lc_total  = lc["total"]  if lc["total"]  > 0 else local_lc
    lc_easy   = lc["easy"]   if lc["total"]  > 0 else diff.get("Easy",   0)
    lc_medium = lc["medium"] if lc["total"]  > 0 else diff.get("Medium", 0)
    lc_hard   = lc["hard"]   if lc["total"]  > 0 else diff.get("Hard",   0)
    lc_rank   = lc["ranking"]

    # ── consistency last 30 days ──
    cutoff30 = date.today() - timedelta(days=30)
    active_days = len(set(
        parse_date(p["Date"]) for p in problems
        if parse_date(p["Date"]) and parse_date(p["Date"]) > cutoff30
    ))
    consistency = round(active_days / 30 * 100, 1)

    # ── now / updated badge safe encoding ──
    now_badge = now.replace(" ", "%20").replace(",", "%2C").replace(":", "%3A")

    L = []  # lines

    def ln(s=""): L.append(s)

    # ═══ HEADER ═══════════════════════════════════════════════
    ln('<div align="center">')
    ln()
    ln('

![header](https://capsule-render.vercel.app/api?type=waving'
       '&color=0:0d1117,40:0a3060,100:0d1117'
       '&height=200&section=header'
       '&text=DSA%20Forge%20%E2%9A%94%EF%B8%8F'
       '&fontSize=55&fontColor=58a6ff&animation=fadeIn'
       '&fontAlignY=38'
       '&desc=vikramnegi21%20%E2%80%A2%20CSE%20B.Tech%20%E2%80%A2%20DSA%20Grind'
       '&descAlignY=62&descColor=8b949e)

')
    ln()

    # top badges
    ln(f'

![Views](https://komarev.com/ghpvc/?username={GITHUB_USER}'
       f'&color=58a6ff&style=flat-square&label=Profile+Views)

')
    ln(f'

![LeetCode](https://img.shields.io/badge/LeetCode-{lc_total}%20Solved'
       f'-FFA116?logo=leetcode&logoColor=white&style=flat-square)

')
    ln(f'

![Streak](https://img.shields.io/badge/%F0%9F%94%A5%20Streak'
       f'-{cur_streak}%20days-39d353?style=flat-square)

')
    ln(f'

![Total](https://img.shields.io/badge/Total%20Problems'
       f'-{total}-blueviolet?style=flat-square)

')
    ln(f'

![Updated](https://img.shields.io/badge/Updated-{now_badge}-grey?style=flat-square)

')
    ln()
    ln('</div>')
    ln()
    ln('---')
    ln()

    # ═══ GITHUB STATS ═════════════════════════════════════════
    ln('## 📊 GitHub Stats')
    ln()
    ln('<div align="center">')
    ln()
    ln(f'<img src="https://github-readme-stats.vercel.app/api'
       f'?username={GITHUB_USER}'
       f'&show_icons=true&theme=github_dark&hide_border=true'
       f'&count_private=true&rank_icon=github" height="165"/>')
    ln(f'&nbsp;&nbsp;')
    ln(f'<img src="https://streak-stats.demolab.com'
       f'?user={GITHUB_USER}'
       f'&theme=github-dark-blue&hide_border=true'
       f'&date_format=j%20M%5B%20Y%5D" height="165"/>')
    ln()
    ln('</div>')
    ln()

    # ═══ LEETCODE CARD ════════════════════════════════════════
    ln('## 🧩 LeetCode')
    ln()
    ln('<div align="center">')
    ln()
    ln(f'

![LeetCode Card](https://leetcard.jacoblin.cool/{LEETCODE_USER}'
       f'?theme=dark&font=Karma&ext=heatmap)

')
    ln()
    ln('</div>')
    ln()

    # ═══ METRICS TABLE ════════════════════════════════════════
    ln('## 🏆 Metrics')
    ln()
    ln('| Metric | Value |')
    ln('|--------|-------|')
    ln(f'| 🟢 LeetCode Easy | **{lc_easy}** |')
    ln(f'| 🟡 LeetCode Medium | **{lc_medium}** |')
    ln(f'| 🔴 LeetCode Hard | **{lc_hard}** |')
    ln(f'| 🏅 LeetCode Rank | **{lc_rank}** |')
    ln(f'| ⚡ Codeforces | **{local_cf} solved** |')
    ln(f'| 🔥 Current Streak | **{cur_streak} days** |')
    ln(f'| 🏆 Best Streak | **{best_streak} days** |')
    ln(f'| 📅 30-day Consistency | **{consistency}%** |')
    ln(f'| 📚 Total Problems | **{total}** |')
    ln()

    # ═══ HEATMAP ══════════════════════════════════════════════
    ln('## 📅 Practice Heatmap (Last 91 Days)')
    ln()
    ln('

![Heatmap](heatmap.svg)

')
    ln()

    # ═══ ACTIVITY GRAPH ═══════════════════════════════════════
    ln('## 📈 Activity Graph')
    ln()
    ln(f'

![Activity](https://github-readme-activity-graph.vercel.app/graph'
       f'?username={GITHUB_USER}'
       f'&theme=github-compact&hide_border=true'
       f'&area=true&color=58a6ff&line=58a6ff&point=ffffff)

')
    ln()

    # ═══ LAST 7 DAYS ══════════════════════════════════════════
    ln(f'## ⚡ Last 7 Days ({len(recent)} problems)')
    ln()
    ln('| Date | Problem | Platform | Difficulty |')
    ln('|------|---------|----------|------------|')
    for p in recent:
        d = parse_date(p["Date"])
        dstr = d.strftime("%d %b") if d else p["Date"]
        name = p.get("Problem", "").strip()
        link = p.get("Link", "").strip()
        pval = p.get("Platform", "").strip()
        dval = p.get("Difficulty", "").strip()
        cell = f"[{name}]({link})" if link and link != "-" else name
        ln(f'| {dstr} | {cell} | {pval} | {dval} |')
    ln()

    # ═══ TOPICS ═══════════════════════════════════════════════
    ln('## 🧠 Topics Covered')
    ln()
    badge_line = "  ".join(
        f'

![{t}](https://img.shields.io/badge/{t.replace(" ","_")

}-{c}-0a84ff?style=flat-square)'
        for t, c in topics.items()
    )
    ln(badge_line)
    ln()

    ln('| Topic | Problems |')
    ln('|-------|---------|')
    for t, c in topics.items():
        ln(f'| {t} | {c} |')
    ln()

    # ═══ GOALS ════════════════════════════════════════════════
    ln('## 🎯 Goals')
    ln()
    ln('| Goal | Progress |')
    ln('|------|---------|')
    ln(f"| Striver's A2Z Sheet (455) | {total} / 455 |")
    ln(f'| LeetCode 500+ Solves | {lc_total} / 500 |')
    ln(f'| Codeforces Rating 1000+ | In Progress |')
    ln(f'| 30-Day Streak | {cur_streak} / 30 days |')
    ln()

    # ═══ PLATFORM SPLIT ═══════════════════════════════════════
    ln('## 💻 Platform Split')
    ln()
    ln('| Platform | Count |')
    ln('|----------|-------|')
    for platform, cnt in sorted(plat.items(), key=lambda x: -x[1]):
        ln(f'| {platform} | {cnt} |')
    ln()

    # ═══ ALL PROBLEMS ═════════════════════════════════════════
    ln(f'## 📋 All Problems ({total} total)')
    ln()
    ln('| Date | Problem | Platform | Topic | Difficulty |')
    ln('|------|---------|----------|-------|------------|')
    sorted_probs = sorted(
        problems,
        key=lambda x: parse_date(x["Date"]) or date.min,
        reverse=True
    )
    for p in sorted_probs:
        d = parse_date(p["Date"])
        dstr = d.strftime("%d %b") if d else p["Date"]
        name = p.get("Problem", "").strip()
        link = p.get("Link", "").strip()
        pval = p.get("Platform", "").strip()
        tval = p.get("Topic", "").strip()
        dval = p.get("Difficulty", "").strip()
        cell = f"[{name}]({link})" if link and link != "-" else name
        ln(f'| {dstr} | {cell} | {pval} | {tval} | {dval} |')
    ln()

    # ═══ FOOTER ═══════════════════════════════════════════════
    ln('<div align="center">')
    ln()
    ln('

![footer](https://capsule-render.vercel.app/api?type=waving'
       '&color=0:0d1117,40:0a3060,100:0d1117'
       '&height=100&section=footer)

')
    ln()
    ln('</div>')

    return "\n".join(L)

# ── Main ──────────────────────────────────────────────────────
def main():
    print("Fetching LeetCode stats...")
    lc = fetch_leetcode()
    print(f"  total={lc['total']} easy={lc['easy']} medium={lc['medium']} hard={lc['hard']} rank={lc['ranking']}")

    print("Reading problems.csv...")
    problems = read_csv()
    print(f"  {len(problems)} problems loaded")

    print("Generating heatmap.svg...")
    with open(HEATMAP_FILE, "w", encoding="utf-8") as f:
        f.write(make_heatmap(problems))

    print("Building README.md...")
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(build_readme(problems, lc))

    print("Done ✅")

if __name__ == "__main__":
    main()
