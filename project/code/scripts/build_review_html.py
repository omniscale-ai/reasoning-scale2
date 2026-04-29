#!/usr/bin/env python3
"""Generate a self-contained HTML review page from tasks_annotated.jsonl."""

import json
from pathlib import Path

IN = Path("data/annotation_pilot/tasks_annotated.jsonl")
OUT = Path("data/annotation_pilot/review.html")

DIFF_COLORS = {
    "Trivial": "#4caf50",
    "Easy": "#8bc34a",
    "Medium": "#ff9800",
    "Hard": "#f44336",
    "Expert": "#9c27b0",
    "?": "#9e9e9e",
}

BENCH_COLORS = {
    "FrontierScience-Olympiad": "#1565c0",
    "SWE-bench Verified": "#00695c",
    "tau-bench": "#6a1b9a",
    "WorkArena++": "#e65100",
}


def load():
    seen = {}
    with IN.open() as f:
        for line in f:
            line = line.strip()
            if line:
                obj = json.loads(line)
                seen[obj["task_id"]] = obj  # last entry wins (most recent retry)
    return list(seen.values())


def badge(text, color):
    return f'<span style="background:{color};color:#fff;padding:2px 8px;border-radius:10px;font-size:12px;font-weight:bold">{text}</span>'


def dim_bars(dims):
    if not dims:
        return "<em>—</em>"
    html = '<table style="border-collapse:collapse;width:100%;font-size:12px">'
    for name, val in dims.items():
        if isinstance(val, dict):
            score = val.get("score", 0)
            note = val.get("note", "")
        else:
            score = int(val) if val else 0
            note = ""
        pct = score * 20
        html += f"""
        <tr>
          <td style="width:160px;padding:2px 4px;color:#555">{name}</td>
          <td style="padding:2px 4px">
            <div style="background:#eee;border-radius:4px;height:10px;width:200px;display:inline-block">
              <div style="background:#1976d2;width:{pct}%;height:10px;border-radius:4px"></div>
            </div>
            <span style="color:#333;margin-left:6px">{score}/5</span>
            <span style="color:#888;font-size:11px;margin-left:6px">{note}</span>
          </td>
        </tr>"""
    html += "</table>"
    return html


def step_nodes(nodes):
    if not nodes:
        return "<em>—</em>"
    TYPE_COLORS = {
        "strategic": "#7b1fa2",
        "conceptual": "#1565c0",
        "computational": "#2e7d32",
        "verification": "#e65100",
    }
    html = '<div style="font-size:12px">'
    for n in nodes:
        tc = TYPE_COLORS.get(n.get("type", ""), "#999")
        deps = ", ".join(f"#{d}" for d in n.get("depends_on", []))
        html += f"""
        <div style="margin:4px 0;padding:6px;background:#f5f5f5;border-left:3px solid {tc};border-radius:2px">
          <b style="color:{tc}">#{n["id"]} [{n["type"]}]</b>
          <b style="margin-left:8px">{n.get("label", "")}</b>
          <span style="color:#888;font-size:11px;margin-left:8px">complexity: {n.get("complexity", "?")}/5</span>
          {"<span style='color:#aaa;font-size:11px;margin-left:8px'>← " + deps + "</span>" if deps else ""}
          <div style="color:#555;margin-top:2px">{n.get("detail", "")}</div>
        </div>"""
    html += "</div>"
    return html


def card(t, idx):
    diff = t.get("difficulty") or {}
    steps = t.get("steps") or {}
    label = diff.get("overall_label", "?")
    score = diff.get("overall_difficulty", "?")
    bench = t.get("benchmark", "")
    domain = t.get("domain", "")
    tid = t.get("task_id", "")
    errors = t.get("errors", [])

    dc = DIFF_COLORS.get(label, "#9e9e9e")
    bc = BENCH_COLORS.get(bench, "#555")

    summary_line = t.get("graph_summary") or steps.get("graph_summary") or {}
    n_nodes = summary_line.get("total_nodes", "?")
    bot_ids = steps.get("bottleneck_node_ids", [])

    problem_short = (t.get("problem") or "")[:400].replace("<", "&lt;").replace(">", "&gt;")
    problem_full = (t.get("problem") or "").replace("<", "&lt;").replace(">", "&gt;")
    solution_short = (t.get("solution") or "")[:300].replace("<", "&lt;").replace(">", "&gt;")

    error_html = ""
    if errors:
        error_html = f'<div style="background:#fff3e0;padding:6px;border-radius:4px;font-size:12px;color:#e65100;margin-top:8px">⚠ {"; ".join(errors)}</div>'

    nodes_html = step_nodes(steps.get("nodes", []))
    dims_html = dim_bars(diff.get("dimensions", {}))

    return f"""
<div class="card" id="card-{idx}"
     data-bench="{bench}" data-score="{score}" data-label="{label}"
     style="border:1px solid #e0e0e0;border-radius:8px;margin:12px 0;padding:0;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.1)">

  <!-- Header (always visible) -->
  <div class="card-header" onclick="toggle({idx})"
       style="display:flex;align-items:center;gap:10px;padding:10px 14px;cursor:pointer;background:#fafafa;flex-wrap:wrap">
    <span style="color:#aaa;font-size:12px;min-width:28px">#{idx + 1}</span>
    {badge(bench, bc)}
    <span style="font-size:12px;color:#666;flex:1;min-width:120px">{domain[:40]}</span>
    {badge(f"{label} ({score})", dc)}
    <span style="font-size:12px;color:#888">nodes: {n_nodes} | bottlenecks: {len(bot_ids)}</span>
    <span style="font-size:11px;color:#bbb;word-break:break-all">{tid[:40]}</span>
    <span id="arrow-{idx}" style="margin-left:auto;color:#aaa">▼</span>
  </div>

  <!-- Body (toggled) -->
  <div id="body-{idx}" style="display:none;padding:14px;border-top:1px solid #eee">

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">

      <!-- Left: problem + solution -->
      <div>
        <div style="font-weight:bold;color:#333;margin-bottom:6px">Problem</div>
        <div style="font-size:13px;color:#444;background:#f9f9f9;padding:8px;border-radius:4px;white-space:pre-wrap;max-height:200px;overflow:auto">{problem_short}{"…" if len(t.get("problem", "")) > 400 else ""}</div>
        <div style="font-weight:bold;color:#333;margin:10px 0 6px">Solution (excerpt)</div>
        <div style="font-size:12px;color:#666;background:#f9f9f9;padding:8px;border-radius:4px;white-space:pre-wrap;max-height:120px;overflow:auto">{solution_short}…</div>
        {error_html}
      </div>

      <!-- Right: difficulty -->
      <div>
        <div style="font-weight:bold;color:#333;margin-bottom:6px">Difficulty dimensions</div>
        {dims_html}
        <div style="margin-top:10px;font-size:12px;color:#555">
          <b>Justification:</b> {(diff.get("Justification") or diff.get("justification") or "—")[:400]}
        </div>
      </div>
    </div>

    <!-- Step graph -->
    <div style="margin-top:14px">
      <div style="font-weight:bold;color:#333;margin-bottom:6px">
        Step graph — {n_nodes} nodes
        {"| bottlenecks: " + ", ".join(f"#{b}" for b in bot_ids) if bot_ids else ""}
        <span style="font-size:12px;color:#888;font-weight:normal;margin-left:8px">{summary_line.get("comment", "")}</span>
      </div>
      {nodes_html}
    </div>

  </div>
</div>"""


def build(tasks):
    cards_html = "\n".join(card(t, i) for i, t in enumerate(tasks))

    bench_opts = "".join(
        f'<option value="{b}">{b}</option>' for b in sorted({t.get("benchmark", "") for t in tasks})
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Annotation Review — {len(tasks)} tasks</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
          margin: 0; padding: 20px; background: #f4f4f4; color: #222; }}
  .toolbar {{ display:flex;gap:12px;align-items:center;flex-wrap:wrap;
              background:#fff;padding:12px 16px;border-radius:8px;
              box-shadow:0 1px 3px rgba(0,0,0,.1);margin-bottom:16px;
              position:sticky;top:0;z-index:100 }}
  select, input {{ padding:6px 10px;border:1px solid #ccc;border-radius:6px;font-size:14px }}
  button {{ padding:6px 14px;border:none;border-radius:6px;cursor:pointer;font-size:14px }}
  #count {{ font-size:13px;color:#888;margin-left:auto }}
</style>
</head>
<body>

<h2 style="margin:0 0 12px">Annotation Review &nbsp;
  <span style="font-size:16px;color:#888;font-weight:normal">{len(tasks)} tasks</span>
</h2>

<div class="toolbar">
  <label>Benchmark:
    <select id="fBench" onchange="filter()">
      <option value="">All</option>
      {bench_opts}
    </select>
  </label>
  <label>Min difficulty:
    <select id="fMinD" onchange="filter()">
      <option value="0">Any</option>
      <option value="1">1+</option><option value="2">2+</option>
      <option value="3">3+</option><option value="4">4+</option><option value="5">5</option>
    </select>
  </label>
  <label>Max difficulty:
    <select id="fMaxD" onchange="filter()">
      <option value="5">Any</option>
      <option value="4">≤4</option><option value="3">≤3</option>
      <option value="2">≤2</option><option value="1">≤1</option>
    </select>
  </label>
  <label>Label:
    <select id="fLabel" onchange="filter()">
      <option value="">All</option>
      <option>Trivial</option><option>Easy</option><option>Medium</option>
      <option>Hard</option><option>Expert</option>
    </select>
  </label>
  <button onclick="expandAll()" style="background:#e3f2fd">Expand all</button>
  <button onclick="collapseAll()" style="background:#fce4ec">Collapse all</button>
  <span id="count"></span>
</div>

<div id="cards">{cards_html}</div>

<script>
function toggle(i) {{
  const b = document.getElementById('body-'+i);
  const a = document.getElementById('arrow-'+i);
  if (b.style.display === 'none') {{ b.style.display='block'; a.textContent='▲'; }}
  else {{ b.style.display='none'; a.textContent='▼'; }}
}}
function expandAll() {{
  document.querySelectorAll('[id^="body-"]').forEach(el => el.style.display='block');
  document.querySelectorAll('[id^="arrow-"]').forEach(el => el.textContent='▲');
}}
function collapseAll() {{
  document.querySelectorAll('[id^="body-"]').forEach(el => el.style.display='none');
  document.querySelectorAll('[id^="arrow-"]').forEach(el => el.textContent='▼');
}}
function filter() {{
  const bench = document.getElementById('fBench').value;
  const minD  = parseInt(document.getElementById('fMinD').value);
  const maxD  = parseInt(document.getElementById('fMaxD').value);
  const label = document.getElementById('fLabel').value;
  let visible = 0;
  document.querySelectorAll('.card').forEach(c => {{
    const cb = c.dataset.bench;
    const cs = parseFloat(c.dataset.score) || 0;
    const cl = c.dataset.label;
    const show = (!bench || cb === bench)
              && cs >= minD && cs <= maxD
              && (!label || cl === label);
    c.style.display = show ? '' : 'none';
    if (show) visible++;
  }});
  document.getElementById('count').textContent = visible + ' tasks shown';
}}
filter();
</script>
</body>
</html>"""


if __name__ == "__main__":
    tasks = load()
    html = build(tasks)
    OUT.write_text(html, encoding="utf-8")
    print(f"Written: {OUT}  ({len(tasks)} tasks)")
