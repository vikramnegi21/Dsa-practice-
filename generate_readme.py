import csv, json, urllib.request
from datetime import datetime, timedelta, date
from collections import defaultdict

LEETCODE_USER = "vikramnegi21"
GITHUB_USER   = "vikramnegi21"
CSV_FILE      = "problems.csv"
README_FILE   = "README.md"
HEATMAP_FILE  = "heatmap.svg"

def fetch_leetcode():
    url = "https://leetcode-stats-api.herokuapp.com/" + LEETCODE_USER
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )
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
        print("LeetCode API error: " + str(e))
    return {"total":0,"easy":0,"medium":0,"hard":0,"ranking":"N/A"}

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
    for fmt in ["%Y-%m-%d","%d %b %Y","%d %b","%d-%m-%Y","%b %d, %Y"]:
        try:
            d = datetime.strptime(s.strip(), fmt)
            if d.year == 1900:
                d = d.replace(year=datetime.now().year)
            return d.date()
        except:
            continue
    return None

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
            if cur2 > best:
                best = cur2
        else:
            cur2 = 1
    if cur > best:
        best = cur
    return cur, best

def last_n_days(problems, n=7):
    cutoff = date.today() - timedelta(days=n)
    res = [p for p in problems
           if (parse_date(p["Date"]) or date.min) > cutoff]
    return sorted(res,
                  key=lambda x: parse_date(x["Date"]) or date.min,
                  reverse=True)

def count_by(problems, key):
    c = defaultdict(int)
    for p in problems:
        v = p.get(key, "").strip()
        if v:
            c[v] += 1
    return dict(c)

def make_heatmap(problems, weeks=13):
    date_counts = defaultdict(int)
    for p in problems:
        d = parse_date(p["Date"])
        if d:
            date_counts[d] += 1
    today = date.today()
    start = today - timedelta(days=today.weekday()+1+(weeks-1)*7)
    cell, gap = 12, 3
    step = cell + gap
    w = weeks * step + 44
    h = 7 * step + 44

    cells = []
    month_labels = {}

    for week in range(weeks):
        for dow in range(7):
            day = start + timedelta(weeks=week, days=dow)
            x = 32 + week * step
            y = 20 + dow * step
            if day > today:
                cells.append(
                    '<rect x="' + str(x) + '" y="' + str(y) +
                    '" width="' + str(cell) + '" height="' + str(cell) +
                    '" rx="2" fill="#161b22" opacity="0.3"/>'
                )
            else:
                cnt = date_counts.get(day, 0)
                if cnt == 0:
                    color = "#161b22"
                elif cnt == 1:
                    color = "#0e4429"
                elif cnt == 2:
                    color = "#006d32"
                elif cnt <= 4:
                    color = "#26a641"
                else:
                    color = "#39d353"
                label = day.strftime("%d %b %Y")
                ps = "problems" if cnt != 1 else "problem"
                cells.append(
                    '<rect x="' + str(x) + '" y="' + str(y) +
                    '" width="' + str(cell) + '" height="' + str(cell) +
                    '" rx="2" fill="' + color + '">' +
                    '<title>' + label + ': ' + str(cnt) + ' ' + ps +
                    '</title></rect>'
                )
            if dow == 0 and day.day <= 7:
                month_labels[week] = day.strftime("%b")

    month_svg = ""
    for w_, m in month_labels.items():
        month_svg += (
            '<text x="' + str(32 + w_ * step) + '" y="13"' +
            ' fill="#8b949e" font-size="10"' +
            ' font-family="monospace">' + m + '</text>'
        )

    day_names = ["S","M","T","W","T","F","S"]
    day_svg = ""
    for i in range(7):
        day_svg += (
            '<text x="2" y="' + str(20 + i * step + 9) + '"' +
            ' fill="#8b949e" font-size="9"' +
            ' font-family="monospace">' + day_names[i] + '</text>'
        )

    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg"' +
        ' width="' + str(w) + '" height="' + str(h) + '">' +
        '<rect width="' + str(w) + '" height="' + str(h) +
        '" rx="8" fill="#0d1117"/>' +
        month_svg + day_svg + "".join(cells)
    )
    legend_colors = ["#161b22","#0e4429","#26a641","#39d353"]
    svg += (
        '<text x="' + str(w-92) + '" y="' + str(h-5) + '"' +
        ' fill="#8b949e" font-size="9" font-family="monospace">Less</text>'
    )
    for i, col in enumerate(legend_colors):
        svg += (
            '<rect x="' + str(w-68+i*14) + '" y="' + str(h-15) +
            '" width="10" height="10" rx="2" fill="' + col + '"/>'
        )
    svg += (
        '<text x="' + str(w-4) + '" y="' + str(h-5) + '"' +
        ' fill="#8b949e" font-size="9" font-family="monospace"' +
        ' text-anchor="end">More</text></svg>'
    )
    return svg

def build_readme(problems, lc):
    now = datetime.utcnow().strftime("%d %b %Y, %H:%M UTC")
    cur_streak, best_streak = calc_streak(problems)
    topics = dict(sorted(count_by(problems,"Topic").items(),
                         key=lambda x: -x[1]))
    diff   = count_by(problems, "Difficulty")
    plat   = count_by(problems, "Platform")
    total  = len(problems)
    recent = last_n_days(problems, 7)

    local_lc = plat.get("LeetCode", 0)
    local_cf = plat.get("Codeforces", 0)

    lc_total  = lc["total"]  if lc["total"]  > 0 else local_lc
    lc_easy   = lc["easy"]   if lc["total"]  > 0 else diff.get("Easy",   0)
    lc_medium = lc["medium"] if lc["total"]  > 0 else diff.get("Medium", 0)
    lc_hard   = lc["hard"]   if lc["total"]  > 0 else diff.get("Hard",   0)
    lc_rank   = lc["ranking"]

    cutoff30 = date.today() - timedelta(days=30)
    active_days = len(set(
        parse_date(p["Date"]) for p in problems
        if parse_date(p["Date"]) and parse_date(p["Date"]) > cutoff30
    ))
    consistency = round(active_days / 30 * 100, 1)

    now_b = now.replace(" ","%20").replace(",","%2C").replace(":","%3A")

    cap_url = (
        "https://capsule-render.vercel.app/api?type=waving"
        "&color=0:0d1117,40:0a3060,100:0d1117"
        "&height=200&section=header"
        "&text=DSA%20Forge%20%E2%9A%94%EF%B8%8F"
        "&fontSize=55&fontColor=58a6ff&animation=fadeIn"
        "&fontAlignY=38"
        "&desc=vikramnegi21%20%E2%80%A2%20CSE%20B.Tech%20%E2%80%A2%20DSA%20Grind"
        "&descAlignY=62&descColor=8b949e"
    )
    cap_footer = (
        "https://capsule-render.vercel.app/api?type=waving"
        "&color=0:0d1117,40:0a3060,100:0d1117"
        "&height=100&section=footer"
    )
    gh_stats = (
        "https://github-readme-stats.vercel.app/api"
        "?username=" + GITHUB_USER +
        "&show_icons=true&theme=github_dark&hide_border=true"
        "&count_private=true&rank_icon=github"
    )
    streak_url = (
        "https://streak-stats.demolab.com"
        "?user=" + GITHUB_USER +
        "&theme=github-dark-blue&hide_border=true"
        "&date_format=j%20M%5B%20Y%5D"
    )
    lc_card = (
        "https://leetcard.jacoblin.cool/" + LEETCODE_USER +
        "?theme=dark&font=Karma&ext=heatmap"
    )
    activity = (
        "https://github-readme-activity-graph.vercel.app/graph"
        "?username=" + GITHUB_USER +
        "&theme=github-compact&hide_border=true"
        "&area=true&color=58a6ff&line=58a6ff&point=ffffff"
    )
    views_badge = (
        "https://komarev.com/ghpvc/?username=" + GITHUB_USER +
        "&color=58a6ff&style=flat-square&label=Profile+Views"
    )

    L = []

    L.append('<div align="center">')
    L.append("")
    L.append("![](" + cap_url + ")")
    L.append("")
    L.append("![](" + views_badge + ")")
    lc_b = (
        "https://img.shields.io/badge/LeetCode-" +
        str(lc_total) +
        "%20Solved-FFA116?logo=leetcode&logoColor=white&style=flat-square"
    )
    L.append("![](" + lc_b + ")")
    sk_b = (
        "https://img.shields.io/badge/Streak-" +
        str(cur_streak) +
        "%20days-39d353?style=flat-square"
    )
    L.append("![](" + sk_b + ")")
    tot_b = (
        "https://img.shields.io/badge/Total%20Problems-" +
        str(total) +
        "-blueviolet?style=flat-square"
    )
    L.append("![](" + tot_b + ")")
    upd_b = (
        "https://img.shields.io/badge/Updated-" +
        now_b +
        "-grey?style=flat-square"
    )
    L.append("![](" + upd_b + ")")
    L.append("")
    L.append("</div>")
    L.append("")
    L.append("---")
    L.append("")

    L.append("## Stats")
    L.append("")
    L.append('<div align="center">')
    L.append("")
    L.append('<img src="' + gh_stats + '" height="165"/>')
    L.append('<img src="' + streak_url + '" height="165"/>')
    L.append("")
    L.append("</div>")
    L.append("")

    L.append("## LeetCode")
    L.append("")
    L.append('<div align="center">')
    L.append("")
    L.append("![](" + lc_card + ")")
    L.append("")
    L.append("</div>")
    L.append("")

    L.append("## Metrics")
    L.append("")
    L.append("| Metric | Value |")
    L.append("|--------|-------|")
    L.append("| LeetCode Easy   | **" + str(lc_easy)    + "** |")
    L.append("| LeetCode Medium | **" + str(lc_medium)  + "** |")
    L.append("| LeetCode Hard   | **" + str(lc_hard)    + "** |")
    L.append("| LeetCode Rank   | **" + str(lc_rank)    + "** |")
    L.append("| Codeforces      | **" + str(local_cf)   + " solved** |")
    L.append("| Current Streak  | **" + str(cur_streak) + " days** |")
    L.append("| Best Streak     | **" + str(best_streak)+ " days** |")
    L.append("| 30-day Consistency | **" + str(consistency) + "%** |")
    L.append("| Total Problems  | **" + str(total)      + "** |")
    L.append("")

    L.append("## Practice Heatmap (Last 91 Days)")
    L.append("")
    L.append("![Heatmap](heatmap.svg)")
    L.append("")

    L.append("## Activity Graph")
    L.append("")
    L.append("![](" + activity + ")")
    L.append("")

    L.append("## Last 7 Days (" + str(len(recent)) + " problems)")
    L.append("")
    L.append("| Date | Problem | Platform | Difficulty |")
    L.append("|------|---------|----------|------------|")
    for p in recent:
        d    = parse_date(p["Date"])
        ds   = d.strftime("%d %b") if d else p["Date"]
        name = p.get("Problem","").strip()
        link = p.get("Link","").strip()
        pv   = p.get("Platform","").strip()
        dv   = p.get("Difficulty","").strip()
        if link and link != "-":
            cell = "[" + name + "](" + link + ")"
        else:
            cell = name
        L.append("| " + ds + " | " + cell + " | " + pv + " | " + dv + " |")
    L.append("")

    L.append("## Topics Covered")
    L.append("")
    badges = []
    for t, c in topics.items():
        b_url = (
            "https://img.shields.io/badge/" +
            t.replace(" ","_") + "-" + str(c) +
            "-0a84ff?style=flat-square"
        )
        badges.append("![](" + b_url + ")")
    L.append("  ".join(badges))
    L.append("")
    L.append("| Topic | Count |")
    L.append("|-------|-------|")
    for t, c in topics.items():
        L.append("| " + t + " | " + str(c) + " |")
    L.append("")

    L.append("## Goals")
    L.append("")
    L.append("| Goal | Progress |")
    L.append("|------|---------|")
    L.append("| Striver A2Z (455) | " + str(total)    + " / 455 |")
    L.append("| LeetCode 500+     | " + str(lc_total) + " / 500 |")
    L.append("| CF Rating 1000+   | In Progress |")
    L.append("| 30-Day Streak     | " + str(cur_streak) + " / 30 |")
    L.append("")

    L.append("## Platform Split")
    L.append("")
    L.append("| Platform | Count |")
    L.append("|----------|-------|")
    for platform, cnt in sorted(plat.items(), key=lambda x: -x[1]):
        L.append("| " + platform + " | " + str(cnt) + " |")
    L.append("")

    L.append("## All Problems (" + str(total) + " total)")
    L.append("")
    L.append("| Date | Problem | Platform | Topic | Difficulty |")
    L.append("|------|---------|----------|-------|------------|")
    sorted_p = sorted(problems,
                      key=lambda x: parse_date(x["Date"]) or date.min,
                      reverse=True)
    for p in sorted_p:
        d    = parse_date(p["Date"])
        ds   = d.strftime("%d %b") if d else p["Date"]
        name = p.get("Problem","").strip()
        link = p.get("Link","").strip()
        pv   = p.get("Platform","").strip()
        tv   = p.get("Topic","").strip()
        dv   = p.get("Difficulty","").strip()
        if link and link != "-":
            cell = "[" + name + "](" + link + ")"
        else:
            cell = name
        L.append("| "+ds+" | "+cell+" | "+pv+" | "+tv+" | "+dv+" |")
    L.append("")

    L.append('<div align="center">')
    L.append("")
    L.append("![](" + cap_footer + ")")
    L.append("")
    L.append("</div>")

    return "\n".join(L)

def main():
    print("Fetching LeetCode...")
    lc = fetch_leetcode()
    print("LC total=" + str(lc["total"]) + " rank=" + str(lc["ranking"]))

    print("Reading CSV...")
    problems = read_csv()
    print(str(len(problems)) + " problems loaded")

    print("Generating heatmap...")
    with open(HEATMAP_FILE, "w", encoding="utf-8") as f:
        f.write(make_heatmap(problems))

    print("Building README...")
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(build_readme(problems, lc))

    print("Done!")

if __name__ == "__main__":
    main()
    
