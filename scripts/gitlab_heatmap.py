import json, urllib.request, datetime as dt

USER = "ridoan"
req = urllib.request.Request(
    f"https://gitlab.com/users/{USER}/calendar.json",
    headers={"User-Agent": "Mozilla/5.0"}
)
with urllib.request.urlopen(req, timeout=15) as res:
    data = json.load(res)

end = dt.date.today()
start = end - dt.timedelta(days=364)
start -= dt.timedelta(days=(start.weekday() + 1) % 7)  # align to Sunday

cell, gap = 11, 3
colors = ["#1e1b2e", "#4c3b8f", "#6b4fc4", "#8b6df0", "#c4b5fd"]

def level(n):
    if n == 0: return 0
    if n < 3: return 1
    if n < 6: return 2
    if n < 10: return 3
    return 4

rects, total, d = [], 0, start
while d <= end:
    n = data.get(d.isoformat(), 0)
    total += n
    col = (d - start).days // 7
    row = (d.weekday() + 1) % 7
    x, y = 12 + col * (cell + gap), 34 + row * (cell + gap)
    rects.append(
        f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" '
        f'fill="{colors[level(n)]}"><title>{d}: {n}</title></rect>'
    )
    d += dt.timedelta(days=1)

max_col = (end - start).days // 7
width = 12 + (max_col + 1) * (cell + gap) - gap + 12

legend_x = width - 12 - (len(colors) * (cell + gap) - gap)
legend = "".join(
    f'<rect x="{legend_x + i * (cell + gap)}" y="10" width="{cell}" height="{cell}" rx="2" fill="{c}"/>'
    for i, c in enumerate(colors)
)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="145" viewBox="0 0 {width} 145">
<rect width="100%" height="100%" rx="8" fill="#0d1117"/>
<text x="12" y="20" fill="#c9d1d9" font-family="Segoe UI, Arial, sans-serif" font-size="13">{total} GitLab contributions in the last year</text>
{legend}
{''.join(rects)}
</svg>'''

with open("gitlab-activity.svg", "w", encoding="utf-8") as f:
    f.write(svg)
