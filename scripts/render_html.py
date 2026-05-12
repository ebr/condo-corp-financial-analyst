#!/usr/bin/env python3
"""Render a financial position report Markdown file to self-contained HTML.

Usage: python render_html.py Reports/YYYY-MM-DD_..._Financial-Position-Report.md
Writes: Reports/YYYY-MM-DD_..._Financial-Position-Report.html
"""

import re
import sys
from pathlib import Path

# ── Design system ─────────────────────────────────────────────────────────────

FONTS = """\
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">"""

CSS = """\
:root {
  --paper:#f3efe6; --paper-2:#ece6d8; --ink:#1b1a17; --ink-2:#3a3833;
  --ink-3:#6f6a60; --rule:#cfc6b3; --accent:#2f5740;
  --flag-high:#a8412b; --flag-pos:#3f6b46; --flag-med:#a07a26;
}
* { box-sizing:border-box; }
html,body { margin:0; padding:0; background:var(--paper); color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,sans-serif; -webkit-font-smoothing:antialiased; }
.page { max-width:900px; margin:0 auto; padding:48px 56px 96px; }
@media (max-width:700px) { .page { padding:28px 22px 64px; } }
.report { background:#fbf8f0; border:1px solid var(--rule); border-radius:6px;
  padding:32px 36px; box-shadow:0 1px 0 rgba(0,0,0,.02),0 24px 48px -32px rgba(27,26,23,.18);
  position:relative; overflow:hidden; }
.report::before { content:""; position:absolute; left:0; top:0; bottom:0;
  width:3px; background:var(--accent); }
.rhead { display:flex; justify-content:space-between; align-items:baseline;
  border-bottom:1px solid var(--rule); padding-bottom:16px; margin-bottom:22px; }
.rhead h1 { font-family:"Instrument Serif",serif; font-weight:400; font-size:32px;
  letter-spacing:-.01em; margin:0; color:var(--ink); }
.rhead .stamp { font-family:"IBM Plex Mono",monospace; font-size:11px;
  letter-spacing:.1em; color:var(--ink-3); text-transform:uppercase; white-space:nowrap; }
.meta-block { font-family:"IBM Plex Mono",monospace; font-size:11px; color:var(--ink-3);
  line-height:1.7; margin-bottom:24px; padding-bottom:16px; border-bottom:1px solid var(--rule); }
.meta-block .k { color:var(--ink-3); letter-spacing:.08em; text-transform:uppercase; font-size:10px; }
.meta-block .v { color:var(--ink-2); }
h5 { font-family:"IBM Plex Sans",sans-serif; font-weight:600; font-size:11px;
  letter-spacing:.14em; text-transform:uppercase; color:var(--ink); margin:24px 0 10px; }
.row { display:flex; justify-content:space-between; align-items:baseline;
  padding:5px 0; border-bottom:1px dotted var(--rule);
  font-family:"IBM Plex Mono",monospace; font-size:13px; }
.row .lbl { color:var(--ink-2); }
.row .val { color:var(--ink); font-variant-numeric:tabular-nums; }
.row .val.neg { color:var(--flag-high); }
.row .val.pos { color:var(--flag-pos); }
.flag { display:flex; gap:12px; align-items:flex-start;
  padding:10px 0; border-bottom:1px dotted var(--rule); }
.flag:last-child { border-bottom:0; }
.flag .tag { font-family:"IBM Plex Mono",monospace; font-size:9.5px;
  letter-spacing:.1em; padding:3px 8px; border-radius:3px;
  text-transform:uppercase; color:#fff; flex-shrink:0; margin-top:2px; font-weight:500; }
.flag .tag.high { background:var(--flag-high); }
.flag .tag.med  { background:var(--flag-med); }
.flag .tag.pos  { background:var(--flag-pos); }
.flag .txt { font-family:"IBM Plex Mono",monospace; font-size:12px;
  color:var(--ink-2); line-height:1.55; }
.flag .txt em { color:var(--ink-3); font-style:normal; font-size:10.5px;
  display:block; margin-top:3px; }
.scorecard { width:100%; border-collapse:collapse; font-family:"IBM Plex Mono",monospace;
  font-size:12px; margin:8px 0 16px; }
.scorecard th { font-family:"IBM Plex Sans",sans-serif; font-weight:600; font-size:10px;
  letter-spacing:.12em; text-transform:uppercase; color:var(--ink-3);
  padding:6px 8px; text-align:right; border-bottom:1px solid var(--rule); }
.scorecard th:first-child { text-align:left; }
.scorecard td { padding:5px 8px; text-align:right; border-bottom:1px dotted var(--rule);
  color:var(--ink-2); font-variant-numeric:tabular-nums; }
.scorecard td.metric { text-align:left; }
.scorecard tr:last-child td { border-bottom:none; }
.data-table { width:100%; border-collapse:collapse; font-size:13px; margin:8px 0 16px; }
.data-table th { font-family:"IBM Plex Sans",sans-serif; font-weight:600; font-size:10.5px;
  letter-spacing:.1em; text-transform:uppercase; color:var(--ink-3);
  padding:6px 8px 6px 0; border-bottom:1px solid var(--rule); text-align:left; }
.data-table td { padding:5px 8px 5px 0; border-bottom:1px dotted var(--rule);
  color:var(--ink-2); vertical-align:top; }
.prose { font-size:14px; line-height:1.6; color:var(--ink-2); margin:8px 0 16px; }
.prose strong { color:var(--ink); }
.section-divider { border:none; border-top:1px solid var(--rule); margin:24px 0; }
footer.page-footer { margin-top:32px; font-family:"IBM Plex Mono",monospace;
  font-size:11px; color:var(--ink-3); letter-spacing:.06em; text-align:center; }"""

# ── Emoji → flag class ────────────────────────────────────────────────────────

EMOJI_CLASS = {
    "🔴": ("high", "HIGH"),
    "🟡": ("med",  "MED"),
    "🟢": ("pos",  "POS"),
    "❌": ("high", "HIGH"),
}

# ── Inline markdown helpers ───────────────────────────────────────────────────

def esc(text: str) -> str:
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;"))

def inline(text: str) -> str:
    """Apply bold, italic, code inline markdown to already-escaped text."""
    # bold must come before italic (** before *)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*',     r'<em>\1</em>',         text)
    text = re.sub(r'`(.+?)`',       r'<code>\1</code>',     text)
    return text

def render_inline(text: str) -> str:
    return inline(esc(text))

# ── Markdown table parsing ────────────────────────────────────────────────────

def parse_table(lines: list[str]) -> tuple[list[str], list[list[str]]]:
    headers: list[str] = []
    rows: list[list[str]] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            break
        if re.match(r"^\|[\s\-\|:]+\|$", stripped):  # separator row
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not headers:
            headers = cells
        else:
            rows.append(cells)
    return headers, rows

def render_table(headers: list[str], rows: list[list[str]], css_class: str = "data-table") -> str:
    parts = [f'<table class="{css_class}"><thead><tr>']
    for h in headers:
        parts.append(f"<th>{render_inline(h)}</th>")
    parts.append("</tr></thead><tbody>")
    for row in rows:
        parts.append("<tr>")
        for i, cell in enumerate(row):
            td_class = ' class="metric"' if (css_class == "scorecard" and i == 0) else ""
            parts.append(f"<td{td_class}>{render_inline(cell)}</td>")
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts)

# ── Flag rendering ────────────────────────────────────────────────────────────

def render_flag(tag_class: str, tag_label: str, issue: str, action: str = "") -> str:
    txt = render_inline(issue)
    if action:
        txt += f"<em>{render_inline(action)}</em>"
    return (
        f'<div class="flag">'
        f'<span class="tag {tag_class}">{tag_label}</span>'
        f'<span class="txt">{txt}</span>'
        f"</div>"
    )

def render_flags_section(content: str) -> str:
    lines = content.split("\n")
    table_lines = [l for l in lines if l.strip().startswith("|")]
    if not table_lines:
        return render_prose(content)
    _, rows = parse_table(table_lines)
    parts = []
    for row in rows:
        if not row:
            continue
        priority_cell = row[0] if row else ""
        tag_class, tag_label = "med", "MED"
        for emoji, (cls, lbl) in EMOJI_CLASS.items():
            if emoji in priority_cell:
                tag_class, tag_label = cls, lbl
                break
        issue  = row[1] if len(row) > 1 else ""
        action = row[2] if len(row) > 2 else ""
        parts.append(render_flag(tag_class, tag_label, issue, action))
    return "".join(parts)

def render_forward_section(content: str) -> str:
    parts = []
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            parts.append(render_flag("med", "FWD", stripped[2:]))
    return "".join(parts) if parts else render_prose(content)

# ── Prose rendering ───────────────────────────────────────────────────────────

def render_prose(text: str) -> str:
    paragraphs = []
    for para in re.split(r"\n\n+", text.strip()):
        para = para.strip()
        if not para:
            continue
        lines = para.split("\n")
        html = "<br>".join(render_inline(l) for l in lines)
        paragraphs.append(f'<p class="prose">{html}</p>')
    return "".join(paragraphs)

# ── Generic section renderer (tables + prose + sub-headings) ──────────────────

def render_mixed(content: str) -> str:
    lines = content.split("\n")
    parts: list[str] = []
    prose_buf: list[str] = []

    def flush():
        text = "\n".join(prose_buf).strip()
        if text:
            parts.append(render_prose(text))
        prose_buf.clear()

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("### "):
            flush()
            parts.append(f"<h5>{esc(stripped[4:])}</h5>")
            i += 1
            continue

        if stripped.startswith("|"):
            flush()
            tbl_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl_lines.append(lines[i])
                i += 1
            headers, rows = parse_table(tbl_lines)
            if headers and rows:
                parts.append(render_table(headers, rows, "data-table"))
            continue

        if stripped == "---":
            i += 1
            continue

        prose_buf.append(line)
        i += 1

    flush()
    return "".join(parts)

# ── Section routing ───────────────────────────────────────────────────────────

def render_section_body(sec_num: str, content: str) -> str:
    if sec_num == "5":
        lines = content.split("\n")
        tbl = [l for l in lines if l.strip().startswith("|")]
        if tbl:
            headers, rows = parse_table(tbl)
            return render_table(headers, rows, "scorecard")
        return render_prose(content)

    if sec_num == "6":
        return render_flags_section(content)

    if sec_num == "9":
        return render_forward_section(content)

    return render_mixed(content)

# ── Header / metadata parsing ─────────────────────────────────────────────────

def parse_preamble(preamble_text: str) -> tuple[str, str, list[tuple[str, str]]]:
    corp_name = ""
    meta_pairs: list[tuple[str, str]] = []
    stamp_year = ""
    for line in preamble_text.split("\n"):
        if line.startswith("# ") and not corp_name:
            corp_name = line[2:].strip()
            continue
        m = re.match(r"^\*\*(.+?):\*\*\s*(.*)", line)
        if m:
            key, val = m.group(1).strip(), m.group(2).strip()
            meta_pairs.append((key, val))
            if key.lower() == "date" and not stamp_year:
                m2 = re.search(r"(\d{4})", val)
                if m2:
                    stamp_year = m2.group(1)
    return corp_name, stamp_year, meta_pairs

# ── Main render ───────────────────────────────────────────────────────────────

def render(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")

    # Peel off trailing italic footer line (*Report generated…*)
    footer_text = ""
    lines_all = text.split("\n")
    for idx in range(len(lines_all) - 1, -1, -1):
        stripped = lines_all[idx].strip()
        if stripped and re.match(r"^\*[^*].+[^*]\*$", stripped):
            footer_text = stripped[1:-1]
            text = "\n".join(lines_all[:idx]).rstrip()
            break
        elif stripped:
            break

    # Everything before the first "## N. " numbered section is preamble
    first_numbered = re.search(r"^## \d+\. ", text, re.MULTILINE)
    if first_numbered:
        preamble_text = text[:first_numbered.start()]
        body_text     = text[first_numbered.start():]
    else:
        preamble_text = text
        body_text     = ""

    body_sections = re.split(r"\n(?=## \d+\. )", body_text.strip())
    if body_sections == [""]:
        body_sections = []

    corp_name, stamp_year, meta_pairs = parse_preamble(preamble_text)

    corp_abbrev = corp_name.split("—")[0].strip() if "—" in corp_name else corp_name[:12]
    stamp = f"{esc(corp_abbrev)} · {esc(stamp_year)}" if stamp_year else esc(corp_abbrev)

    # Meta block
    meta_rows = "".join(
        f'<div><span class="k">{esc(k)}:</span> <span class="v">{esc(v)}</span></div>'
        for k, v in meta_pairs
    )
    meta_block = f'<div class="meta-block">{meta_rows}</div>'

    # rhead
    rhead = (
        f'<div class="rhead">'
        f'<h1>Financial Briefing</h1>'
        f'<span class="stamp">{stamp}</span>'
        f'</div>'
    )

    # Body sections
    section_parts: list[str] = []
    for chunk in body_sections:
        m = re.match(r"^## (\d+)\. (.+?)\n(.*)", chunk, re.DOTALL)
        if m:
            sec_num   = m.group(1)
            sec_title = m.group(2).strip()
            content   = m.group(3)
            h5 = f"<h5>{esc(sec_title)}</h5>"
            body = render_section_body(sec_num, content)
            section_parts.append(f'<hr class="section-divider">{h5}{body}')
        else:
            # Non-numbered section — render generically
            first_line, _, rest = chunk.partition("\n")
            section_parts.append(
                f'<hr class="section-divider">'
                f'<h5>{esc(first_line.lstrip("# ").strip())}</h5>'
                f'{render_mixed(rest)}'
            )

    footer_html = (
        f'<footer class="page-footer">{render_inline(footer_text)}</footer>'
        if footer_text else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(corp_name)} — Financial Position Report</title>
{FONTS}
<style>
{CSS}
</style>
</head>
<body>
<div class="page">
  <div class="report">
    {rhead}
    {meta_block}
    {"".join(section_parts)}
    {footer_html}
  </div>
</div>
</body>
</html>"""

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <report.md>", file=sys.stderr)
        sys.exit(1)
    md = Path(sys.argv[1])
    if not md.exists():
        print(f"Error: {md} not found", file=sys.stderr)
        sys.exit(1)
    out = md.with_suffix(".html")
    out.write_text(render(md), encoding="utf-8")
    print(f"Written: {out}")
