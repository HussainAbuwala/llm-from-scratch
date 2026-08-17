#!/usr/bin/env python3
"""Render .excalidraw scenes to a plain HTML/SVG contact sheet.

This is a proof-reading tool, not a faithful Excalidraw renderer: it exists to
catch overlapping elements, overflowing text and empty space before the file is
opened for recording.

    python3 render_preview.py                 # both canvases, 2 columns
    python3 render_preview.py episode_01_bigram.excalidraw 1
"""

import html
import json
import os
import sys

FW, FH = 1600, 900
FONTS = {
    1: "'Segoe Print','Bradley Hand','Comic Sans MS',cursive",
    2: "'Nunito',Helvetica,sans-serif",
    3: "'Cascadia Code','SF Mono',Menlo,monospace",
}


def svg_for(frame, kids):
    out = [f'<svg viewBox="0 0 {FW} {FH}" xmlns="http://www.w3.org/2000/svg" '
           f'style="background:#fff;display:block;width:100%;height:auto">']
    ox, oy = frame["x"], frame["y"]
    bound = {}
    for el in kids:
        if el["type"] == "text" and el.get("containerId"):
            bound[el["containerId"]] = el

    for el in kids:
        if el["type"] == "text" and el.get("containerId"):
            continue
        x, y = el["x"] - ox, el["y"] - oy
        w, h = el["width"], el["height"]
        stroke, fill = el["strokeColor"], el["backgroundColor"]
        fill = "none" if fill == "transparent" else fill
        sw = el["strokeWidth"]
        dash = ""
        if el["strokeStyle"] == "dashed":
            dash = ' stroke-dasharray="12 8"'
        elif el["strokeStyle"] == "dotted":
            dash = ' stroke-dasharray="2 6"'
        t = el["type"]

        if t == "rectangle":
            out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
                       f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{dash}/>')
        elif t == "ellipse":
            out.append(f'<ellipse cx="{x + w / 2}" cy="{y + h / 2}" rx="{w / 2}" '
                       f'ry="{h / 2}" fill="{fill}" stroke="{stroke}" '
                       f'stroke-width="{sw}"{dash}/>')
        elif t == "diamond":
            pts = f"{x + w / 2},{y} {x + w},{y + h / 2} {x + w / 2},{y + h} {x},{y + h / 2}"
            out.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" '
                       f'stroke-width="{sw}"{dash}/>')
        elif t in ("line", "arrow"):
            pts = " ".join(f"{x + px},{y + py}" for px, py in el["points"])
            head = ' marker-end="url(#ah)"' if el.get("endArrowhead") else ""
            tail = ' marker-start="url(#ah2)"' if el.get("startArrowhead") else ""
            out.append(f'<polyline points="{pts}" fill="none" stroke="{stroke}" '
                       f'stroke-width="{sw}"{dash}{head}{tail}/>')
        elif t == "text":
            fs = el["fontSize"]
            fam = FONTS[el["fontFamily"]]
            lines = el["text"].split("\n")
            for i, ln in enumerate(lines):
                out.append(
                    f'<text x="{x}" y="{y + fs * 0.95 + i * fs * 1.25}" '
                    f'font-family="{fam}" font-size="{fs}" fill="{stroke}" '
                    f'xml:space="preserve">{html.escape(ln)}</text>')

        lbl = bound.get(el["id"])
        if lbl:
            fs = lbl["fontSize"]
            fam = FONTS[lbl["fontFamily"]]
            lines = lbl["text"].split("\n")
            cy = y + h / 2 - (len(lines) - 1) * fs * 0.625
            for i, ln in enumerate(lines):
                out.append(
                    f'<text x="{x + w / 2}" y="{cy + fs * 0.35 + i * fs * 1.25}" '
                    f'text-anchor="middle" font-family="{fam}" font-size="{fs}" '
                    f'fill="{lbl["strokeColor"]}">{html.escape(ln)}</text>')

    out.append(
        '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10" fill="none" stroke="context-stroke" '
        'stroke-width="2"/></marker>'
        '<marker id="ah2" viewBox="0 0 10 10" refX="1" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto">'
        '<path d="M10,0 L0,5 L10,10" fill="none" stroke="context-stroke" '
        'stroke-width="2"/></marker></defs>')
    out.append("</svg>")
    return "\n".join(out)


def render(path, cols=2):
    doc = json.load(open(path))
    els = doc["elements"]
    frames = [e for e in els if e["type"] == "frame"]
    frames.sort(key=lambda f: f["x"])
    by_frame = {}
    for e in els:
        if e["type"] != "frame":
            by_frame.setdefault(e["frameId"], []).append(e)

    cards = []
    for f in frames:
        cards.append(
            f'<figure><figcaption>{html.escape(f["name"])}</figcaption>'
            f'{svg_for(f, by_frame.get(f["id"], []))}</figure>')

    out = (
        '<meta charset="utf-8">'
        "<style>"
        f"body{{margin:0;background:#333;font-family:sans-serif}}"
        f".g{{display:grid;grid-template-columns:repeat({cols},1fr);gap:14px;padding:14px}}"
        "figure{margin:0;background:#fff;border-radius:6px;overflow:hidden}"
        "figcaption{background:#111;color:#fff;font-size:13px;padding:5px 10px;"
        "font-family:monospace}"
        "</style><div class='g'>" + "".join(cards) + "</div>")
    dest = path.replace(".excalidraw", "_preview.html")
    with open(dest, "w") as fh:
        fh.write(out)
    print(f"{dest}  ({len(frames)} scenes)")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    args = sys.argv[1:]
    files = [args[0]] if args else ["series_intro.excalidraw",
                                    "episode_01_bigram.excalidraw"]
    cols = int(args[1]) if len(args) > 1 else 2
    for f in files:
        render(os.path.join(here, f), cols)
