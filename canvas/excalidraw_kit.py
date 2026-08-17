"""Minimal Excalidraw scene builder.

Writes .excalidraw JSON files that open directly at excalidraw.com.

Design notes
------------
Every scene is a 1600x900 frame, i.e. exactly 16:9. Select a frame and press
Shift+2 ("zoom to selection") and the viewport matches the video frame, so a
scene never needs repositioning while recording.

Frames are laid out left to right in a single row, so presenting the canvas is
one continuous rightward pan through the story.

Coordinates passed to helpers are LOCAL to the scene (0..1600, 0..900).
"""

import itertools
import json

# ---------------------------------------------------------------- constants

FRAME_W, FRAME_H = 1600, 900
FRAME_GAP = 260

HAND = 1  # Excalifont / Virgil - handwritten
NORMAL = 2  # Nunito / Helvetica
CODE = 3  # Cascadia - monospace

BLACK = "#1e1e1e"
GRAY = "#868e96"
RED = "#e03131"
GREEN = "#2f9e44"
BLUE = "#1971c2"
ORANGE = "#f08c00"
VIOLET = "#6741d9"
TEAL = "#0c8599"

BG_NONE = "transparent"
BG_YELLOW = "#ffec99"
BG_GREEN = "#b2f2bb"
BG_BLUE = "#a5d8ff"
BG_RED = "#ffc9c9"
BG_VIOLET = "#d0bfff"
BG_GRAY = "#e9ecef"

_ids = itertools.count(1)
_seeds = itertools.count(101)


def _nid(prefix="el"):
    return f"{prefix}_{next(_ids):05d}"


def _char_w(font, size):
    return size * (0.60 if font == CODE else 0.52)


def est_text_size(s, size, font):
    lines = s.split("\n")
    width = max((len(line) for line in lines), default=1) * _char_w(font, size)
    return width, len(lines) * size * 1.25


# ---------------------------------------------------------------- elements


def _base(kind, x, y, w, h, **kw):
    return {
        "id": kw.pop("id", None) or _nid(kind[:4]),
        "type": kind,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": kw.pop("stroke", BLACK),
        "backgroundColor": kw.pop("bg", BG_NONE),
        "fillStyle": kw.pop("fill", "solid"),
        "strokeWidth": kw.pop("sw", 2),
        "strokeStyle": kw.pop("dash", "solid"),
        "roughness": kw.pop("roughness", 1),
        "opacity": kw.pop("opacity", 100),
        "groupIds": [],
        "frameId": None,
        "roundness": kw.pop("roundness", {"type": 3}),
        "seed": next(_seeds) * 977 % 2000000,
        "version": 1,
        "versionNonce": next(_seeds) * 1543 % 2000000,
        "isDeleted": False,
        "boundElements": kw.pop("bound", None),
        "updated": 1755000000000,
        "link": None,
        "locked": False,
        **kw,
    }


def text(x, y, s, size=20, font=HAND, color=BLACK, align="left", **kw):
    w, h = est_text_size(s, size, font)
    el = _base("text", x, y, kw.pop("width", w), kw.pop("height", h),
               stroke=color, roundness=None, **kw)
    el.update({
        "text": s,
        "fontSize": size,
        "fontFamily": font,
        "textAlign": align,
        "verticalAlign": "top",
        "containerId": None,
        "originalText": s,
        "autoResize": True,
        "lineHeight": 1.25,
    })
    return el


def _bound_label(container, s, size, font, color):
    """Text bound to a container: Excalidraw centres and wraps it on load."""
    tid = _nid("lbl")
    w, h = est_text_size(s, size, font)
    el = _base("text", container["x"] + 8, container["y"] + 8, w, h,
               id=tid, stroke=color, roundness=None)
    el.update({
        "text": s,
        "fontSize": size,
        "fontFamily": font,
        "textAlign": "center",
        "verticalAlign": "middle",
        "containerId": container["id"],
        "originalText": s,
        "autoResize": True,
        "lineHeight": 1.25,
    })
    container["boundElements"] = (container["boundElements"] or []) + [
        {"type": "text", "id": tid}
    ]
    return el


def box(x, y, w, h, label=None, size=20, font=HAND, label_color=BLACK,
        kind="rectangle", **kw):
    el = _base(kind, x, y, w, h, **kw)
    if label is None:
        return [el]
    return [el, _bound_label(el, label, size, font, label_color)]


def ellipse(x, y, w, h, label=None, **kw):
    return box(x, y, w, h, label, kind="ellipse", roundness={"type": 2}, **kw)


def diamond(x, y, w, h, label=None, **kw):
    return box(x, y, w, h, label, kind="diamond", roundness={"type": 2}, **kw)


def arrow(x1, y1, x2, y2, via=None, head="arrow", tail=None, **kw):
    pts = [[0, 0]]
    if via:
        pts += [[vx - x1, vy - y1] for vx, vy in via]
    pts.append([x2 - x1, y2 - y1])
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    el = _base("arrow", x1, y1, max(xs) - min(xs), max(ys) - min(ys),
               roundness={"type": 2}, **kw)
    el.update({
        "points": pts,
        "lastCommittedPoint": None,
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": tail,
        "endArrowhead": head,
        "elbowed": False,
    })
    return el


def line(pts, **kw):
    x0, y0 = pts[0]
    rel = [[px - x0, py - y0] for px, py in pts]
    xs = [p[0] for p in rel]
    ys = [p[1] for p in rel]
    el = _base("line", x0, y0, max(xs) - min(xs), max(ys) - min(ys),
               roundness={"type": 2}, **kw)
    el.update({
        "points": rel,
        "lastCommittedPoint": None,
        "startBinding": None,
        "endBinding": None,
        "startArrowhead": None,
        "endArrowhead": None,
    })
    return el


# ---------------------------------------------------------------- scene


class Scene:
    def __init__(self, canvas, index, name):
        self.ox = index * (FRAME_W + FRAME_GAP)
        self.oy = 0
        self.canvas = canvas
        frame = _base("frame", self.ox, self.oy, FRAME_W, FRAME_H,
                      stroke="#bbb", bg=BG_NONE, roundness=None, roughness=0)
        frame.update({"type": "frame", "name": name})
        self.frame_id = frame["id"]
        canvas.elements.append(frame)

    def add(self, *items):
        for item in items:
            for el in (item if isinstance(item, list) else [item]):
                el["x"] += self.ox
                el["y"] += self.oy
                el["frameId"] = self.frame_id
                self.canvas.elements.append(el)
        return self

    # -- composite helpers -------------------------------------------------

    def heading(self, title, sub=None, color=BLACK):
        self.add(text(70, 52, title, 46, HAND, color))
        if sub:
            self.add(text(70, 116, sub, 24, HAND, GRAY))
        return self

    def note(self, x, y, s, size=22, color=VIOLET):
        return self.add(text(x, y, s, size, HAND, color))

    def cards(self, x, y, items, w=92, h=92, gap=14, size=34, bg=BG_BLUE,
              font=CODE, colors=None):
        """A row of token cards."""
        for i, s in enumerate(items):
            fillc = colors[i] if colors else bg
            self.add(box(x + i * (w + gap), y, w, h, s, size, font, bg=fillc))
        return x + len(items) * (w + gap) - gap

    def bars(self, x, y, items, maxw=380, bh=42, gap=14, bg=BG_BLUE,
             highlight=None, label_w=110, show_value=True):
        """Horizontal probability bars: items = [(label, prob), ...]"""
        for i, (label, p) in enumerate(items):
            yy = y + i * (bh + gap)
            self.add(text(x, yy + 8, label, 24, CODE))
            w = max(8, maxw * p)
            fillc = BG_YELLOW if (highlight and label == highlight) else bg
            self.add(box(x + label_w, yy, w, bh, bg=fillc))
            if show_value:
                self.add(text(x + label_w + w + 16, yy + 8,
                              f"{p:.2f}" if p >= 0.01 else f"{p:g}",
                              22, CODE, GRAY))
        return y + len(items) * (bh + gap) - gap

    def table(self, x, y, col_heads, row_heads, cells, cw=104, ch=64,
              size=24, hi_row=None, hi_cells=(), corner=""):
        """Labelled matrix. hi_cells = [(row_idx, col_idx), ...]"""
        self.add(box(x, y, cw, ch, corner, size, CODE, bg=BG_GRAY, sw=1))
        for j, c in enumerate(col_heads):
            self.add(box(x + cw * (j + 1), y, cw, ch, c, size, CODE,
                         bg=BG_GRAY, sw=1))
        for i, r in enumerate(row_heads):
            yy = y + ch * (i + 1)
            self.add(box(x, yy, cw, ch, r, size, CODE, bg=BG_GRAY, sw=1))
            for j, val in enumerate(cells[i]):
                cell_bg = BG_NONE
                if hi_row == i:
                    cell_bg = BG_YELLOW
                if (i, j) in hi_cells:
                    cell_bg = BG_GREEN
                self.add(box(x + cw * (j + 1), yy, cw, ch, str(val), size,
                             CODE, bg=cell_bg, sw=1))
        return x + cw * (len(col_heads) + 1), y + ch * (len(row_heads) + 1)

    def tickets(self, x, y, items, tw=76, th=76, gap=10, size=26):
        """items = [(text, colour), ...] - the 'four tickets' visual."""
        for i, (s, c) in enumerate(items):
            self.add(box(x + i * (tw + gap), y, tw, th, s, size, CODE, bg=c))
        return x + len(items) * (tw + gap) - gap

    def panel(self, x, y, w, h, title, lines, bg=BG_NONE, stroke=BLACK,
              title_color=BLACK, size=22, dash="solid"):
        self.add(box(x, y, w, h, bg=bg, stroke=stroke, dash=dash))
        self.add(text(x + 26, y + 22, title, 28, HAND, title_color))
        self.add(text(x + 26, y + 74, "\n".join(lines), size, HAND))
        return self


class Canvas:
    def __init__(self):
        self.elements = []
        self._n = 0

    def scene(self, name):
        sc = Scene(self, self._n, name)
        self._n += 1
        return sc

    def save(self, path):
        doc = {
            "type": "excalidraw",
            "version": 2,
            "source": "https://excalidraw.com",
            "elements": self.elements,
            "appState": {
                "gridSize": None,
                "gridStep": 5,
                "gridModeEnabled": False,
                "viewBackgroundColor": "#ffffff",
            },
            "files": {},
        }
        with open(path, "w") as fh:
            json.dump(doc, fh, indent=1)
        return len(self.elements)
