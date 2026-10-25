#!/usr/bin/env python3
"""Generate the Ing.Dylan GitHub activity banners from public GitHub data."""

from __future__ import annotations

import json
import re
import shutil
import urllib.request
from collections import Counter
from datetime import UTC, date, datetime
from html import escape
from pathlib import Path


USERNAME = "dylanneymarmontalvo2014-lgtm"
ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source"
CANVA = ROOT / "canva"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "Ing-Dylan-profile-artwork",
    "X-GitHub-Api-Version": "2022-11-28",
}


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def api(path: str):
    return json.loads(fetch(f"https://api.github.com{path}"))


def text(x: int, y: int, value: str, size: int, *, color: str = "#FFFFFF", weight: int = 400,
         family: str = "DejaVu Sans, sans-serif", spacing: float = 0, anchor: str = "start") -> str:
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" '
        f'font-weight="{weight}" letter-spacing="{spacing}" text-anchor="{anchor}">{escape(value)}</text>'
    )


def shell(content: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="300" viewBox="0 0 900 300">
  <defs>
    <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M36 0H0V36" fill="none" stroke="#B8B8B8" stroke-opacity="0.035"/>
    </pattern>
  </defs>
  <rect width="900" height="300" fill="#080808"/>
  <rect width="900" height="300" fill="url(#grid)"/>
  <rect x="30" y="28" width="840" height="244" fill="none" stroke="#B8B8B8" stroke-opacity="0.16"/>
  <rect x="60" y="48" width="9" height="9" fill="#E50914"/>
  {content}
</svg>'''


def stats_svg(user: dict, repos: list[dict], contributions: int, updated: str) -> str:
    metrics = [
        (str(contributions), "CONTRIBUTIONS"),
        (str(user["public_repos"]), "PUBLIC REPOS"),
        (str(sum(repo["stargazers_count"] for repo in repos)), "STARS EARNED"),
        (str(sum(repo["forks_count"] for repo in repos)), "FORKS"),
        (str(user["followers"]), "FOLLOWERS"),
    ]
    pieces = [
        text(60, 88, "GitHub Activity", 32, weight=700, spacing=-0.5),
        text(840, 83, f"@{USERNAME}", 10, color="#B8B8B8", family="Noto Sans Mono, monospace", spacing=0.5, anchor="end"),
        '<rect x="60" y="101" width="56" height="3" fill="#E50914"/>',
    ]
    for index, (value, label) in enumerate(metrics):
        x = 60 + index * 156
        pieces.extend([
            f'<rect x="{x}" y="126" width="144" height="104" fill="#111111" stroke="#B8B8B8" stroke-opacity="0.16"/>',
            f'<rect x="{x}" y="126" width="4" height="104" fill="#E50914" fill-opacity="{1 if index == 0 else 0.45}"/>',
            text(x + 18, 183, value, 40, weight=700),
            text(x + 18, 210, label, 9, color="#B8B8B8", family="Noto Sans Mono, monospace", spacing=1.2),
        ])
    pieces.append(text(840, 254, f"PUBLIC DATA • UPDATED {updated} UTC", 9, color="#B8B8B8", family="Noto Sans Mono, monospace", spacing=1, anchor="end"))
    return shell("\n  ".join(pieces))


def languages_svg(languages: Counter[str], updated: str) -> str:
    total = sum(languages.values())
    ranked = languages.most_common()
    max_bytes = ranked[0][1]
    pieces = [
        text(60, 88, "Top Languages", 32, weight=700, spacing=-0.5),
        text(840, 83, "BYTES ACROSS PUBLIC OWNED REPOSITORIES", 9, color="#B8B8B8", family="Noto Sans Mono, monospace", spacing=0.8, anchor="end"),
        '<rect x="60" y="101" width="56" height="3" fill="#E50914"/>',
    ]
    fills = ["#E50914", "#8F0008", "#E50914", "#8F0008", "#B8B8B8"]
    opacities = ["1", "1", "0.68", "0.62", "0.38"]
    for index, (language, amount) in enumerate(ranked):
        y = 132 + index * 27
        percent = amount / total * 100
        width = max(3, round(510 * amount / max_bytes))
        pieces.extend([
            text(60, y + 9, language, 12, weight=600),
            '<rect x="200" y="%d" width="510" height="10" fill="#111111" stroke="#B8B8B8" stroke-opacity="0.12"/>' % y,
            f'<rect x="200" y="{y}" width="{width}" height="10" fill="{fills[index]}" fill-opacity="{opacities[index]}"/>',
            text(840, y + 9, f"{percent:.2f}%", 11, color="#B8B8B8", family="Noto Sans Mono, monospace", anchor="end"),
        ])
    pieces.append(text(840, 278, f"{total:,} LANGUAGE BYTES • UPDATED {updated} UTC", 9, color="#B8B8B8", family="Noto Sans Mono, monospace", spacing=0.9, anchor="end"))
    return shell("\n  ".join(pieces))


def contributions_svg(days: list[tuple[date, int]], total: int, updated: str) -> str:
    start = min(day for day, _ in days)
    levels = dict(days)
    cell = 10
    step = 13
    grid_x = 122
    grid_y = 104
    level_colors = {0: "#111111", 1: "#8F0008", 2: "#8F0008", 3: "#E50914", 4: "#E50914"}
    level_opacity = {0: "1", 1: "0.55", 2: "1", 3: "0.72", 4: "1"}
    pieces = [
        text(60, 76, "Contribution Graph", 30, weight=700, spacing=-0.5),
        text(840, 72, f"{total} CONTRIBUTIONS • LAST YEAR", 11, color="#FFFFFF", family="Noto Sans Mono, monospace", spacing=0.9, anchor="end"),
        '<rect x="60" y="88" width="56" height="3" fill="#E50914"/>',
    ]
    for label, row in [("MON", 1), ("WED", 3), ("FRI", 5)]:
        pieces.append(text(102, grid_y + row * step + 9, label, 8, color="#B8B8B8", family="Noto Sans Mono, monospace", spacing=0.6, anchor="end"))

    month_columns: dict[tuple[int, int], int] = {}
    for day, level in days:
        column = (day - start).days // 7
        row = (day.weekday() + 1) % 7
        if day.day <= 7:
            month_columns.setdefault((day.year, day.month), column)
        x = grid_x + column * step
        y = grid_y + row * step
        pieces.append(
            f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="1.5" fill="{level_colors[level]}" '
            f'fill-opacity="{level_opacity[level]}" stroke="#B8B8B8" stroke-opacity="{0.08 if level == 0 else 0.12}"/>'
        )
    for (year, month), column in month_columns.items():
        month_name = date(year, month, 1).strftime("%b").upper()
        x = grid_x + column * step
        if x < 835:
            pieces.append(text(x, 99, month_name, 8, color="#B8B8B8", family="Noto Sans Mono, monospace", spacing=0.5))

    legend_x = 676
    pieces.append(text(660, 245, "LESS", 8, color="#B8B8B8", family="Noto Sans Mono, monospace", anchor="end"))
    for level in range(5):
        pieces.append(
            f'<rect x="{legend_x + level * 16}" y="237" width="10" height="10" rx="1.5" fill="{level_colors[level]}" '
            f'fill-opacity="{level_opacity[level]}" stroke="#B8B8B8" stroke-opacity="0.1"/>'
        )
    pieces.append(text(772, 245, "MORE", 8, color="#B8B8B8", family="Noto Sans Mono, monospace"))
    active_days = sum(level > 0 for _, level in days)
    pieces.append(text(60, 253, f"{active_days} ACTIVE DAYS • {start.isoformat()} — {max(levels).isoformat()}", 9, color="#B8B8B8", family="Noto Sans Mono, monospace", spacing=0.8))
    pieces.append(text(840, 269, f"UPDATED {updated} UTC", 8, color="#B8B8B8", family="Noto Sans Mono, monospace", spacing=0.8, anchor="end"))
    return shell("\n  ".join(pieces))


def main() -> None:
    SOURCE.mkdir(parents=True, exist_ok=True)
    CANVA.mkdir(parents=True, exist_ok=True)
    user = api(f"/users/{USERNAME}")
    repos = api(f"/users/{USERNAME}/repos?per_page=100&type=owner")
    languages: Counter[str] = Counter()
    for repo in repos:
        if not repo["fork"]:
            languages.update(api(f"/repos/{USERNAME}/{repo['name']}/languages"))

    contributions_html = fetch(f"https://github.com/users/{USERNAME}/contributions").decode("utf-8")
    day_matches = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*data-level="(\d)"', contributions_html)
    days = [(date.fromisoformat(day), int(level)) for day, level in day_matches]
    total_match = re.search(r"(\d+)\s+contributions?\s+in\s+(?:the\s+)?last\s+year", contributions_html)
    if not days or not total_match:
        raise RuntimeError("GitHub contribution data could not be parsed")
    total = int(total_match.group(1))
    updated = datetime.now(UTC).date().isoformat()

    outputs = {
        "07-github-stats.svg": stats_svg(user, repos, total, updated),
        "08-top-languages.svg": languages_svg(languages, updated),
        "09-contribution-graph.svg": contributions_svg(days, total, updated),
    }
    for name, svg in outputs.items():
        source_path = SOURCE / name
        source_path.write_text(svg, encoding="utf-8")
        shutil.copy2(source_path, CANVA / name)

    snapshot = {
        "username": USERNAME,
        "updated_utc": updated,
        "public_repos": user["public_repos"],
        "followers": user["followers"],
        "following": user["following"],
        "stars_earned": sum(repo["stargazers_count"] for repo in repos),
        "forks": sum(repo["forks_count"] for repo in repos),
        "contributions_last_year": total,
        "active_days": sum(level > 0 for _, level in days),
        "languages_bytes": dict(languages.most_common()),
    }
    (SOURCE / "github-activity-data.json").write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(snapshot, indent=2))


if __name__ == "__main__":
    main()
