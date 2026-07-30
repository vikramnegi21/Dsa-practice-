import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

CSV_FILE = "problems.csv"
README_FILE = "README.md"
CHART_FILE = "assets/progress_chart.png"

START_MARKER = "<!-- CHART_START -->"
END_MARKER = "<!-- CHART_END -->"

def load_data():
    df = pd.read_csv(CSV_FILE)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df

def generate_chart(df):
    os.makedirs("assets", exist_ok=True)

    if df.empty:
        plt.figure(figsize=(10, 4))
        plt.text(0.5, 0.5, "No problems logged yet", ha="center", va="center")
        plt.axis("off")
        plt.savefig(CHART_FILE, dpi=150)
        plt.close()
        return

    daily = df.groupby(df["date"].dt.date).size().cumsum()
    x = pd.to_datetime(daily.index)
    y = daily.values.astype(float)

    plt.figure(figsize=(10, 4))
    plt.plot(x, y, marker="o", color="#1F8ACB", linewidth=2)
    plt.fill_between(x, y, alpha=0.1, color="#1F8ACB")
    plt.title("Problems Solved Over Time", fontsize=13, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Problems")
    plt.grid(alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHART_FILE, dpi=150)
    plt.close()

def generate_platform_chart(df):
    if df.empty:
        plt.figure(figsize=(5, 5))
        plt.text(0.5, 0.5, "No data yet", ha="center", va="center")
        plt.axis("off")
        plt.savefig("assets/platform_chart.png", dpi=150)
        plt.close()
        return

    counts = df["platform"].value_counts()
    plt.figure(figsize=(5, 5))
    plt.pie(counts.values, labels=counts.index, autopct="%1.1f%%",
            colors=["#FFA116", "#1F8ACB", "#6C63FF"])
    plt.title("Problems by Platform")
    plt.tight_layout()
    plt.savefig("assets/platform_chart.png", dpi=150)
    plt.close()

def build_table(df, n=15):
    recent = df.sort_values("date", ascending=False).head(n)
    lines = [
        "| Date | Problem | Difficulty | Platform | Link |",
        "|---|---|---|---|---|",
    ]
    for _, row in recent.iterrows():
        lines.append(
            f"| {row['date'].date()} | {row['problem_name']} | {row['difficulty']} | "
            f"{row['platform']} | [Solve]({row['link']}) |"
        )
    return "\n".join(lines)

def build_section(df):
    total = len(df)
    ts = int(datetime.now().timestamp())
    section = f"""{START_MARKER}
## 📈 Progress Chart

![Progress](assets/progress_chart.png?t={ts})
![Platform Split](assets/platform_chart.png?t={ts})

**Total Problems Solved: {total}**

<details>
<summary>🕒 Recent Submissions (click to expand)</summary>

{build_table(df)}

</details>
{END_MARKER}"""
    return section

def update_readme(section):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if START_MARKER in content and END_MARKER in content:
        before = content.split(START_MARKER)[0]
        after = content.split(END_MARKER)[1]
        new_content = before + section + after
    else:
        new_content = content + "\n\n" + section

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    df = load_data()
    generate_chart(df)
    generate_platform_chart(df)
    section = build_section(df)
    update_readme(section)
    print("README updated successfully.")
    
