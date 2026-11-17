#!/usr/bin/env python3
"""Generates every SVG under ../../assets from code.

    python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
    .venv/bin/python build.py

Grenze (OFL) is converted to outlines, so the SVGs never depend on a webfont.
"""
import json, re
from datetime import date, timedelta
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "assets"

# ---------- palette ----------
T, TX, SOFT, MU = "#6FE0C8", "#f2f4f5", "#c7cdd3", "#aab1b8"
BG, PANEL, LINE = "#1c1d1f", "#26282b", "#3a3d41"
WARN = "#ff8a7a"
R = 22  # one corner radius for every card
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"

# ---------- Grenze as outlines ----------
_font = instantiateVariableFont(TTFont(HERE / "fonts/Grenze-var.ttf"), {"wght": 800})
_gs, _cm, _hm, _upm = _font.getGlyphSet(), _font.getBestCmap(), _font["hmtx"], _font["head"].unitsPerEm


def width(text, size):
    return sum(_hm[_cm[ord(c)]][0] for c in text) * size / _upm


def gtext(text, size, x, y, fill, anchor="start"):
    x -= {"start": 0, "middle": width(text, size) / 2, "end": width(text, size)}[anchor]
    pen, sc = SVGPathPen(_gs, ntos=lambda v: f"{v:.1f}"), size / _upm
    for c in text:
        g = _cm[ord(c)]
        _gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x, y)))
        x += _hm[g][0] * sc
    return f'<path d="{pen.getCommands()}" fill="{fill}"/>'


# ---------- shared SVG parts ----------
def defs(extra=""):
    return f"""<defs>
<linearGradient id="cg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2c2e32"/><stop offset="1" stop-color="#1e1f22"/></linearGradient>
<linearGradient id="cs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".20"/><stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity=".04"/></linearGradient>
<radialGradient id="glow" cx=".85" cy="0" r="1"><stop offset="0" stop-color="{T}" stop-opacity=".22"/><stop offset="1" stop-color="{T}" stop-opacity="0"/></radialGradient>
<marker id="ar" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{T}"/></marker>
<marker id="ar2" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 z" fill="{WARN}"/></marker>{extra}</defs>"""


def card(x, y, w, h, glow=False):
    s = f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="{R}" fill="url(#cg)" stroke="url(#cs)"/>'
    if glow:
        s += (f'<clipPath id="k{x}_{y}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{R}"/></clipPath>'
              f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#glow)" clip-path="url(#k{x}_{y})"/>')
    return s


def tx(x, y, s, size=14, fill=SOFT, w=400, anchor="start", font=SANS, ls=0):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{w}" '
            f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{s}</text>')


def eyebrow(x, y, s, anchor="start"):
    return tx(x, y, s, 11, T, 700, anchor, MONO, 2)


def svg(w, h, body, label, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{label}">{defs(extra)}{body}</svg>')


def save(folder, name, content):
    p = OUT / folder
    p.mkdir(parents=True, exist_ok=True)
    (p / f"{name}.svg").write_text(content, encoding="utf-8")


# ---------- widgets/terminal ----------
def terminal():
    lines = [("$ ", "whoami", TX), ("", "Mário Lucas · Full Stack Engineer", T),
             ("$ ", "cat focus.txt", TX), ("", "architecture · code · cloud · delivery", MU),
             ("$ ", "uptime", TX), ("", "shipping to production, and it keeps running", T)]
    W, H, cw = 900, 300, 10.2
    s = card(0, 0, W, H)
    s += f'<clipPath id="tb"><rect width="{W}" height="40" rx="{R}"/></clipPath><rect width="{W}" height="40" fill="#fff" fill-opacity=".05" clip-path="url(#tb)"/>'
    for i, c in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        s += f'<circle cx="{28 + i * 22}" cy="20" r="6" fill="{c}"/>'
    s += tx(W / 2, 25, "mario@production: ~", 13, MU, 400, "middle", MONO)
    t, y = 0.4, 88
    for i, (p, txt, col) in enumerate(lines):
        full, dur = p + txt, max(0.3, len(p + txt) * 0.035)
        s += (f'<clipPath id="c{i}"><rect x="30" y="{y - 22}" width="0" height="30"><animate attributeName="width" '
              f'from="0" to="{len(full) * cw + 4}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>')
        s += (f'<text x="30" y="{y}" font-family="{MONO}" font-size="17" clip-path="url(#c{i})">'
              f'<tspan fill="{T}">{p}</tspan><tspan fill="{col}">{txt}</tspan></text>')
        t += dur + 0.25
        y += 34 if p else 44
    s += (f'<rect x="{30 + len(lines[-1][1]) * cw + 6}" y="{y - 62}" width="10" height="22" fill="{T}" opacity="0">'
          f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.01;0.5;0.51;1" dur="1.1s" '
          f'begin="{t:.2f}s" repeatCount="indefinite"/></rect>')
    save("widgets", "terminal", svg(W, H, s, "Terminal: Mário Lucas, Full Stack Engineer."))


# ---------- widgets/toolkit ----------
def toolkit():
    def icon(n):
        return re.search(r' d="([^"]+)"', (HERE / f"icons/{n}.svg").read_text()).group(1)
    rows = [("INTERFACES", [("React", "react", "087EA4"), ("Next.js", "nextdotjs", "000000"), ("TypeScript", "typescript", "3178C6"),
                            ("Tailwind", "tailwindcss", "06B6D4"), ("shadcn/ui", "shadcnui", "000000")]),
            ("SERVICES &amp; DATA", [("Node.js", "nodedotjs", "5FA04E"), ("Express", "express", "000000"), ("Python", "python", "3776AB"),
                                     ("Django", "django", "092E20"), ("PostgreSQL", "postgresql", "4169E1"), ("Redis", "redis", "FF4438"),
                                     ("Prisma", "prisma", "2D3748")]),
            ("INFRA &amp; FLOW", [("AWS", "amazonwebservices", "FF9900"), ("Docker", "docker", "2496ED"), ("Git", "git", "F05032"),
                                  ("RabbitMQ", "rabbitmq", "FF6600"), ("Temporal", "temporal", "141414")])]
    W, RH, orb = 900, 150, 38
    H = 30 + len(rows) * RH
    extra = ('<radialGradient id="o" cx=".35" cy=".25" r=".95"><stop offset="0" stop-color="#fff"/><stop offset=".6" stop-color="#f4f5f7"/><stop offset="1" stop-color="#d9dce1"/></radialGradient>'
             '<linearGradient id="gl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
             '<filter id="sh" x="-40%" y="-40%" width="180%" height="190%"><feDropShadow dx="0" dy="10" stdDeviation="9" flood-color="#000" flood-opacity=".55"/></filter>')
    s, k = card(0, 0, W, H), 0
    for r, (lab, items) in enumerate(rows):
        cy = 15 + r * RH + RH / 2 - 8
        s += eyebrow(32, cy + 4, lab)
        if r:
            s += f'<line x1="32" y1="{15 + r * RH}" x2="{W - 32}" y2="{15 + r * RH}" stroke="#fff" stroke-opacity=".07"/>'
        for i, (name, ic, col) in enumerate(items):
            cx = 250 + i * 90
            s += (f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="{4 + (k % 3) * .7:.1f}s" '
                  f'begin="{-(k * .6):.1f}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
                  f'<circle cx="{cx}" cy="{cy}" r="{orb}" fill="url(#o)" filter="url(#sh)"/>'
                  f'<ellipse cx="{cx}" cy="{cy - orb * .52}" rx="{orb * .66}" ry="{orb * .36}" fill="url(#gl)" opacity=".85"/>'
                  f'<g transform="translate({cx - 15},{cy - 15}) scale(1.25)"><path d="{icon(ic)}" fill="#{col}"/></g>'
                  + tx(cx, cy + orb + 22, name, 12.5, TX, 600, "middle") + '</g>')
            k += 1
    save("widgets", "toolkit", svg(W, H, s, "Toolkit: React, Next.js, TypeScript, Tailwind, shadcn/ui, Node.js, Express, Python, Django, PostgreSQL, Redis, Prisma, AWS, Docker, Git, RabbitMQ, Temporal.", extra))


# ---------- cards/bento ----------
def bento():
    b = card(0, 0, 540, 264) + card(556, 0, 344, 264, True) + card(0, 280, 262, 160) + card(278, 280, 262, 160) + card(556, 280, 344, 160)
    b += eyebrow(36, 48, "OWNERSHIP")
    b += gtext("Real problems,", 50, 36, 112, TX) + gtext("owned end to end.", 50, 36, 166, T)
    for i, l in enumerate(["Four years in software: almost three reviewing other",
                           "people’s code at Kenzie, then over a year running a",
                           "production platform alone at CECAPE."]):
        b += tx(36, 200 + i * 21, l, 14.5)

    def stat(x, y, w, eb, num, l1, l2, size, ny):
        return (eyebrow(x + w / 2, y + 40, eb, "middle") + gtext(num, size, x + w / 2, ny, T, "middle")
                + tx(x + w / 2, ny + 30, l1, 15, SOFT, 500, "middle") + (tx(x + w / 2, ny + 50, l2, 12.5, MU, 400, "middle") if l2 else ""))
    b += stat(556, 0, 344, "KENZIE ACADEMY BRASIL", "1,650+", "technical issues resolved", "as mentor and code reviewer", 92, 150)
    b += stat(0, 280, 262, "CODE REVIEWS", "450+", "delivered across cohorts", "", 64, 384)
    b += stat(278, 280, 262, "IFCE · INFO. SYSTEMS", "9.17", "academic average, out of 10", "", 64, 384)
    b += stat(556, 280, 344, "ENGLISH", "C1", "fluent · EF SET 66/100", "", 64, 384)
    save("cards", "bento", svg(900, 440, b, "Real problems, owned end to end. 1,650+ technical issues resolved, 450+ code reviews, 9.17 academic average, English C1."))


# ---------- cards/decisions + cards/ledger ----------
def feature_cards(name, items, label, cols, H, tsize):
    W, g = 900, 16
    cw, b = (W - g * (cols - 1)) / cols, ""
    for i, (eb, title, lines) in enumerate(items):
        x = i * (cw + g)
        b += card(x, 0, cw, H, i == 0) + eyebrow(x + cw / 2, 50, eb, "middle") + gtext(title, tsize, x + cw / 2, 108, TX, "middle")
        for j, l in enumerate(lines):
            b += tx(x + cw / 2, 148 + j * 22, l, 13.5, SOFT, 400, "middle")
    save("cards", name, svg(W, H, b, label))



# ---------- cards/repo-stats ----------
def repo_stats():
    items = [("260", "publications"), ("418", "authors"), ("17", "courses"), ("6", "collections")]
    W, H, g = 900, 150, 16
    cw, b = (W - g * 3) / 4, ""
    for i, (n, l) in enumerate(items):
        x = i * (cw + g)
        b += card(x, 0, cw, H, i == 0) + gtext(n, 62, x + cw / 2, 82, T, "middle") + tx(x + cw / 2, 116, l, 14.5, SOFT, 500, "middle")
    save("cards", "repo-stats", svg(W, H, b, "Academic Repository: 260 publications from 418 authors, across 17 courses, in 6 collections."))


# ---------- cards/now (data: now.json, refreshed by hand every N days) ----------
def now():
    d = json.loads((HERE / "now.json").read_text())
    upd = date.fromisoformat(d["updated"])
    nxt = upd + timedelta(days=d["refresh_days"])
    fmt = lambda x: f"{x.day:02d} {x.strftime('%b')} {x.year}"
    W, H = 900, 232
    b = card(0, 0, W, H) + '<circle cx="36" cy="40" r="4" fill="#27c93f"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></circle>'
    b += eyebrow(50, 44, f"NOW · UPDATED {fmt(upd).upper()}")
    cw = (W - 72) / 3
    for i, c in enumerate(d["columns"]):
        x = 36 + i * cw
        if i:
            b += f'<line x1="{x - 18}" y1="78" x2="{x - 18}" y2="170" stroke="#fff" stroke-opacity=".08"/>'
        b += tx(x, 92, c["label"], 11, MU, 700, "start", MONO, 2) + gtext(c["title"], 27, x, 134, TX) + tx(x, 160, c["line"], 13.5, SOFT)
    b += f'<line x1="36" y1="190" x2="{W - 36}" y2="190" stroke="#fff" stroke-opacity=".07"/>'
    b += tx(36, 213, f"Refreshed every {d['refresh_days']} days · next update {fmt(nxt)}", 12.5, MU)
    save("cards", "now", svg(W, H, b, "Now: building Iron Ledger, running the Academic Repository in production, studying Information Systems at IFCE."))

# ---------- cards/cta ----------
def cta():
    W, H = 900, 170
    b = card(0, 0, W, H, True) + gtext("Let’s build something useful.", 64, W / 2, 108, TX, "middle")
    save("cards", "cta", svg(W, H, b, "Let’s build something useful."))


# ---------- diagrams/architecture ----------
def architecture():
    W, H = 900, 420
    b = card(0, 0, W, H) + gtext("CECAPE Academic Repository", 30, 28, 46, TX)
    b += tx(28 + width("CECAPE Academic Repository", 30) + 14, 45, "PRODUCTION TOPOLOGY", 13, T, 700, "start", SANS, 2)
    b += tx(28, 70, "AWS · isolated network, managed data, scoped permissions", 13, MU)
    b += f'<rect x="190" y="84" width="690" height="310" rx="16" fill="none" stroke="{T}" stroke-width="1.5" stroke-dasharray="6 6" opacity=".7"/>'
    b += tx(206, 106, "VPC", 12, T, 700, "start", SANS, 2)

    def box(x, y, w, h, title, sub, hl=False):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{PANEL}" stroke="{T if hl else "#fff"}" stroke-opacity="{1 if hl else .14}" stroke-width="{1.6 if hl else 1}"/>'
                + tx(x + w / 2, y + h / 2 - 3, title, 15, TX, 700, "middle") + tx(x + w / 2, y + h / 2 + 16, sub, 12, MU, 400, "middle"))

    def arrow(x1, y1, x2, y2):
        return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{T}" stroke-width="2" stroke-dasharray="6 6" marker-end="url(#ar)">'
                '<animate attributeName="stroke-dashoffset" from="24" to="0" dur="1.2s" repeatCount="indefinite"/></line>')
    b += box(28, 190, 130, 80, "Readers", "browser · mobile") + box(230, 190, 200, 80, "App Runner", "DDD · event-driven", True)
    b += box(520, 130, 240, 80, "RDS · PostgreSQL", "full-text search catalog", True) + box(520, 280, 240, 80, "S3", "publications · files")
    b += arrow(158, 230, 228, 230) + arrow(430, 215, 518, 175) + arrow(430, 245, 518, 315)
    b += f'<rect x="230" y="318" width="200" height="40" rx="20" fill="none" stroke="{T}" stroke-width="1.2"/>'
    b += tx(330, 343, "IAM · least privilege", 13, T, 700, "middle") + f'<line x1="330" y1="318" x2="330" y2="270" stroke="#fff" stroke-opacity=".15" stroke-dasharray="3 4"/>'
    b += tx(790, 170, "tsvector", 12, MU) + tx(790, 190, "no extra", 12, MU) + tx(790, 206, "search service", 12, MU)
    save("diagrams", "architecture", svg(W, H, b, "Architecture: readers reach App Runner inside a VPC, which talks to RDS PostgreSQL for full-text search and to S3 for files, with IAM scoping permissions."))


# ---------- diagrams/ledger-flow ----------
def ledger_flow():
    W, H, nw, nh, gap, x0 = 900, 372, 156, 58, 70, 33
    xs = [x0 + i * (nw + gap) for i in range(4)]
    b = card(0, 0, W, H) + tx(W / 2, 46, "Iron Ledger · how a change travels", 15, SOFT, 500, "middle")

    def node(x, y, t, sub, dash=False):
        st = f'stroke="{WARN}" stroke-dasharray="5 5"' if dash else 'stroke="#fff" stroke-opacity=".18"'
        return (f'<rect x="{x}" y="{y}" width="{nw}" height="{nh}" rx="14" fill="#232528" {st}/>'
                + tx(x + nw / 2, y + 25, t, 14, TX, 700, "middle") + tx(x + nw / 2, y + 43, sub, 11.5, MU, 400, "middle"))

    def lane(y, label, nodes):  # packets are drawn before nodes so they pass *behind* them
        s = eyebrow(x0, y - 14, label)
        for i in range(3):
            s += f'<line x1="{xs[i] + nw + 4}" y1="{y + nh / 2}" x2="{xs[i + 1] - 4}" y2="{y + nh / 2}" stroke="{T}" stroke-opacity=".55" stroke-width="1.6" marker-end="url(#ar)"/>'
        s += (f'<circle r="4.5" fill="{T}"><animateMotion dur="4.5s" repeatCount="indefinite" path="M{x0 + 10} {y + nh / 2} H{xs[3] + nw - 10}"/>'
              '<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.08;.92;1" dur="4.5s" repeatCount="indefinite"/></circle>')
        return s + "".join(node(xs[i], y, t, sub) for i, (t, sub) in enumerate(nodes))
    b += lane(96, "EVERY MUTATION LEAVES A TRACE", [("Stock movement", "REST · RBAC"), ("PostgreSQL", "balance + outbox · 1 tx"), ("RabbitMQ", "domain events"), ("Audit log", "append-only")])
    b += lane(204, "EVERY TRANSACTION CAN BE UNDONE", [("Transaction", "REST · starts the saga"), ("Temporal", "durable workflow"), ("Reserve stock", "through the API"), ("Confirm", "stock out + movement")])
    b += node(xs[3], 286, "Release", "reservation freed", True)
    b += f'<path d="M{xs[2] + nw / 2} {204 + nh + 4} V{286 + nh / 2} H{xs[3] - 4}" fill="none" stroke="{WARN}" stroke-width="1.6" stroke-dasharray="5 5" marker-end="url(#ar2)"/>'
    b += tx(xs[2] + nw / 2 + 12, 286 + nh / 2 - 8, "on failure", 11.5, WARN, 600)
    save("diagrams", "ledger-flow", svg(W, H, b, "Iron Ledger flow: a stock movement is written with its outbox event in PostgreSQL, relayed through RabbitMQ and stored in an append-only audit log. A transaction starts a Temporal saga that reserves and confirms stock, or releases the reservation on failure."))


# ---------- sections/*-dark|light ----------
def headings():
    for fn, num, eb, title in [("what", "01", "OWNERSHIP", "What I do"), ("work", "02", "SHIPPED", "Selected work"),
                               ("building", "03", "IN PROGRESS", "Currently building"), ("toolkit", "04", "TOOLS", "Toolkit"),
                               ("background", "05", "EDUCATION", "Background")]:
        for mode, (ink, acc, ln) in {"dark": (TX, T, "#ffffff"), "light": ("#15171a", "#0e8f78", "#000000")}.items():
            W, H = 900, 132
            s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{title}">'
                 f'<defs><linearGradient id="l"><stop offset="0" stop-color="{ln}" stop-opacity="0"/><stop offset=".5" stop-color="{ln}" stop-opacity=".22"/><stop offset="1" stop-color="{ln}" stop-opacity="0"/></linearGradient></defs>'
                 f'<rect width="{W}" height="1" fill="url(#l)"/>' + tx(W / 2, 42, f"{num} — {eb}", 12, acc, 700, "middle", MONO, 3)
                 + gtext(title, 62, W / 2, 106, ink, "middle") + "</svg>")
            save("sections", f"{fn}-{mode}", s)


if __name__ == "__main__":
    terminal(); toolkit(); bento(); repo_stats(); now(); cta(); architecture(); ledger_flow(); headings()
    feature_cards("decisions", [("ARCHITECTURE", "DDD + events", ["Business rules stay isolated;", "new features are cheap to add."]),
                                ("SEARCH", "Postgres FTS", ["Catalog search with no extra", "service to run or pay for."]),
                                ("CLOUD", "Least privilege", ["Isolated VPC, managed database,", "scoped IAM permissions."])],
                  "Decisions: DDD plus events, native PostgreSQL full-text search, least-privilege AWS.", 3, 236, 38)
    feature_cards("ledger", [("RELIABILITY", "Outbox", ["Balance and event written", "in one transaction, then", "relayed to RabbitMQ."]),
                             ("WORKFLOWS", "Sagas", ["Temporal reserves and", "confirms stock, or releases", "it when a step fails."]),
                             ("TRACEABILITY", "Append-only", ["An audit log the database", "refuses to edit", "or delete."]),
                             ("STRUCTURE", "DDD", ["Five bounded contexts,", "four ADRs on the big", "trade-offs."])],
                  "Iron Ledger: transactional outbox, sagas, append-only audit, DDD.", 4, 250, 32)
    print("assets rebuilt in", OUT)
