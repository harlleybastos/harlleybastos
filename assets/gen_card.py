# -*- coding: utf-8 -*-
"""Gera terminal-card.svg: janela de terminal com sprite pixel-art (a marca),
ficha RPG, hotbar de inventário com os logos da stack e cursor piscando.
Uso: python gen_card.py <saida.svg> [dir_icones]"""
import os, re, sys

INFO_W = 62

def kv(label, value):
    base = f". {label}: "
    room = INFO_W - len(base) - len(value) - 1
    dots = "." * max(room, 2)
    return [("lab", base), ("dim", dots + " "), ("val", value)]

def header(title):
    return [("hdr", f"- {title} " + "-" * max(0, INFO_W - len(title) - 3))]

# Sprite pixel-art 20x22 — a marca registrada
SPRITE_PALETTE = {
    "H": "#1b1b1b", "S": "#c98a5e", "D": "#a86f49", "G": "#101010",
    "W": "#9fc3dd", "P": "#20130c", "E": "#e9ddc8", "B": "#191919",
    "T": "#f2ede4", "C": "#3e7d5a", "K": "#2c5940",
}
SPRITE = [
    "......HHHHHHHH......",
    "....HHHHHHHHHHHH....",
    "...HHHHHHHHHHHHHH...",
    "..HHSSSSSSSSSSSSHH..",
    "..HSSSSSSSSSSSSSSH..",
    "..SSSSSSSSSSSSSSSS..",
    ".GGGGGGGG..GGGGGGGG.",
    ".GSEPPESGGGGSEPPESG.",
    ".GSEPPESGSSGSEPPESG.",
    ".SGGGGGGSDDSGGGGGGS.",
    "..SSSSSSSDDSSSSSSS..",
    "..SBBSSSSDDSSSSBBS..",
    "..BBBBBBBBBBBBBBBB..",
    "..BBBTTTTTTTTTTBBB..",
    "..BBBBTTTTTTTTBBBB..",
    "..BBBBBBBBBBBBBBBB..",
    "...BBBBBBBBBBBBBB...",
    "....BBBBBBBBBBBB....",
    "......BBBBBBBB......",
    "..CCCCCKBBBBKCCCCC..",
    ".CCCCCCCKKKKCCCCCCC.",
    ".CCCCCCCCCCCCCCCCCC.",
]

def icon_path(icons_dir, slug):
    svg = open(os.path.join(icons_dir, f"{slug}.svg"), encoding="utf-8").read()
    return re.search(r'd="([^"]+)"', svg).group(1)

LINES = [
    [("pr", "harlley@bastos:~$ "), ("val", "./whoami --verbose")],
    kv("Class", "Senior Full Stack Engineer"),
    kv("Base", "Piracicaba, BR (UTC-3)"),
    kv("Uptime.GitHub", "grinding since Mar 2018"),
    kv("Difficulty", "Nightmare (never lowered)"),
    [("lab", ". HP: "), ("dim", "." * 24 + " "), ("hp", "[##########]"), ("val", " not tired yet")],
    [("dim", ".")],
    header("Skill.Tree"),
    kv("Languages", "TypeScript, JavaScript, Ruby"),
    kv("Frameworks", "Next.js, Rails, Node.js"),
    kv("Tools", "Docker, PostgreSQL, Git"),
    kv("Speech", "Portuguese, English, French"),
    [("dim", ".")],
    header("New.Game+"),
    kv("Main.Quest", "Gamedev - C++, OpenGL, Vulkan"),
    kv("Grinding", "real-time rendering"),
    kv("Side.Quest", "content creation"),
    [],
    header("Contact"),
    kv("Email", "harlleybastos@hotmail.com"),
    kv("LinkedIn", "harlley-bastos"),
    kv("YouTube", "@harlleybastos"),
    kv("Instagram", "@harlleybastos"),
    kv("TikTok", "@harlleybastos"),
    [],
    header("Motto"),
    [("mot", '. "I don\'t stop when I\'m tired, I stop when I\'m done."')],
]

COLORS = {
    "lab": "#8b949e", "dim": "#3d444d", "val": "#e6edf3",
    "hdr": "#4da3ff", "pr": "#3fb950", "hp": "#3fb950", "mot": "#d29922",
}

# (slug, rótulo, cor do logo, grupo)
STACK = [
    ("typescript",  "TS",       "#3178C6", "lang"),
    ("javascript",  "JS",       "#F7DF1E", "lang"),
    ("ruby",        "Ruby",     "#D91F26", "lang"),
    ("nextdotjs",   "Next",     "#FFFFFF", "fw"),
    ("rubyonrails", "Rails",    "#D30001", "fw"),
    ("nodedotjs",   "Node",     "#5FA04E", "fw"),
    ("docker",      "Docker",   "#2496ED", "tool"),
    ("postgresql",  "Postgres", "#4A91E2", "tool"),
    ("git",         "Git",      "#F05032", "tool"),
    ("cplusplus",   "C++",      "#5E97D0", "new"),
    ("opengl",      "OpenGL",   "#5586A4", "new"),
    ("vulkan",      "Vulkan",   "#C43B3F", "new"),
]
GROUPS = [("lang", "LANGUAGES", "#8b949e"), ("fw", "FRAMEWORKS", "#8b949e"),
          ("tool", "TOOLS", "#8b949e"), ("new", "NEW.GAME+", "#4da3ff")]

W, H = 920, 884
TITLE_H = 44
SHEET_X, SHEET_Y, LH, FS = 358, 92, 21, 14.5
PC_X, PC_Y, PC_R = 178, 300, 122
SLOT, PITCH, GROUP_GAP = 48, 62, 30
BAR_PROMPT_Y, GROUP_Y, SLOT_Y = 710, 740, 750
NAME_Y, END_Y = SLOT_Y + SLOT + 17, 852

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def prompt_line(p, x, y, mono, cmd, cursor=False):
    pre = "harlley@bastos:~$ "
    p.append(f'<text x="{x}" y="{y}" font-family="{mono}" font-size="{FS}" xml:space="preserve">'
             f'<tspan fill="{COLORS["pr"]}">{esc(pre)}</tspan><tspan fill="#e6edf3">{esc(cmd)}</tspan></text>')
    if cursor:
        cx = x + (len(pre) + len(cmd)) * FS * 0.551
        p.append(f'<rect x="{cx:.0f}" y="{y - FS + 2}" width="9" height="{FS + 2}" fill="#3fb950">'
                 '<animate attributeName="opacity" values="1;1;0;0;1" keyTimes="0;0.45;0.5;0.95;1" dur="1.2s" repeatCount="indefinite"/></rect>')

def main():
    out_path = sys.argv[1]
    icons_dir = sys.argv[2] if len(sys.argv) > 2 else "icons"
    mono = "Consolas, 'Courier New', Menlo, monospace"
    p = []
    p.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
    # janela
    p.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="#0d1117" stroke="#30363d" stroke-width="2"/>')
    p.append(f'<path d="M15 1 h{W-30} a14 14 0 0 1 14 14 v{TITLE_H-15} h-{W-2} v-{TITLE_H-15} a14 14 0 0 1 14 -14 z" fill="#161b22"/>')
    p.append(f'<line x1="1" y1="{TITLE_H}" x2="{W-1}" y2="{TITLE_H}" stroke="#30363d" stroke-width="1"/>')
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        p.append(f'<circle cx="{26 + i*22}" cy="{TITLE_H//2}" r="7" fill="{c}"/>')
    p.append(f'<text x="{W//2}" y="{TITLE_H//2 + 5}" text-anchor="middle" font-family="{mono}" font-size="13" fill="#8b949e">harlley@bastos: ~/new-game-plus</text>')
    # slot de personagem com o sprite (marca registrada)
    cell = 11
    sw, sh = len(SPRITE[0]) * cell, len(SPRITE) * cell
    box_w, box_h = sw + 40, sh + 38
    bx, by = PC_X - box_w / 2, PC_Y - box_h / 2
    p.append(f'<rect x="{bx:.0f}" y="{by:.0f}" width="{box_w}" height="{box_h}" rx="18" fill="#10151b" stroke="#30363d" stroke-width="1.5"/>')
    p.append(f'<rect x="{bx - 5:.0f}" y="{by - 5:.0f}" width="{box_w + 10}" height="{box_h + 10}" rx="22" fill="none" stroke="#2d7cc4" stroke-width="1.5" opacity="0.55"/>')
    x0, y0 = bx + 20, by + 19
    for gy, row in enumerate(SPRITE):
        for gx, ch in enumerate(row):
            if ch != ".":
                p.append(f'<rect x="{x0 + gx * cell:.0f}" y="{y0 + gy * cell:.0f}" width="{cell}" height="{cell}" fill="{SPRITE_PALETTE[ch]}"/>')
    p.append(f'<text x="{bx + box_w - 12:.0f}" y="{by + box_h - 10:.0f}" text-anchor="end" font-family="{mono}" font-size="12" fill="#8b949e">&#8482;</text>')
    ny = by + box_h + 40
    p.append(f'<text x="{PC_X}" y="{ny:.0f}" text-anchor="middle" font-family="{mono}" font-size="21" font-weight="bold" fill="#e6edf3">Harlley Bastos</text>')
    p.append(f'<text x="{PC_X}" y="{ny + 26:.0f}" text-anchor="middle" font-family="{mono}" font-size="14" fill="#8b949e">@harlleybastos</text>')
    p.append(f'<text x="{PC_X}" y="{ny + 60:.0f}" text-anchor="middle" font-family="{mono}" font-size="13" fill="#3fb950">&gt; sprite loaded: 20x22 px, 1 of 1</text>')
    p.append(f'<text x="{PC_X}" y="{ny + 86:.0f}" text-anchor="middle" font-family="{mono}" font-size="13"><tspan fill="#3fb950">&gt; </tspan><tspan fill="#d29922">gl_FragColor = vec4(me, 1.0);</tspan></text>')
    # hello triangle RGB (OpenGL/Vulkan) renderizado como output do shader
    ty = ny + 116
    p.append('<defs>'
             '<linearGradient id="tgb" x1="0" y1="0" x2="1" y2="0">'
             '<stop offset="0" stop-color="#3ddc5a"/><stop offset="1" stop-color="#3f7bff"/></linearGradient>'
             '<linearGradient id="trt" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#ff4b4b"/><stop offset="0.92" stop-color="#ff4b4b" stop-opacity="0"/></linearGradient>'
             '</defs>')
    tri = f"{PC_X},{ty} {PC_X - 29},{ty + 50} {PC_X + 29},{ty + 50}"
    p.append(f'<polygon points="{tri}" fill="url(#tgb)"/>')
    p.append(f'<polygon points="{tri}" fill="url(#trt)"/>')
    p.append(f'<text x="{PC_X}" y="{ty + 72:.0f}" text-anchor="middle" font-family="{mono}" font-size="11.5" font-style="italic" fill="#8b949e">// hello, triangle</text>')
    # ficha
    for i, parts in enumerate(LINES):
        if not parts:
            continue
        y = SHEET_Y + i * LH
        spans = "".join(
            f'<tspan fill="{COLORS[k]}"{" font-style=\"italic\"" if k == "mot" else ""}>{esc(t)}</tspan>'
            for k, t in parts)
        p.append(f'<text x="{SHEET_X}" y="{y}" font-family="{mono}" font-size="{FS}" xml:space="preserve">{spans}</text>')
    # hotbar
    prompt_line(p, 40, BAR_PROMPT_Y, mono, "ls ./loadout --equipped")
    counts = {g: sum(1 for s in STACK if s[3] == g) for g, _, _ in GROUPS}
    gw = {g: counts[g] * PITCH - (PITCH - SLOT) for g in counts}
    total = sum(gw.values()) + GROUP_GAP * (len(GROUPS) - 1)
    x = (W - total) / 2
    gx = {}
    for g, glabel, gcolor in GROUPS:
        gx[g] = x
        p.append(f'<text x="{x + gw[g] / 2:.0f}" y="{GROUP_Y}" text-anchor="middle" font-family="{mono}" font-size="10.5" letter-spacing="2" fill="{gcolor}">{glabel}</text>')
        x += gw[g] + GROUP_GAP
    x = min(gx.values())
    prev_group = STACK[0][3]
    for slug, label, color, group in STACK:
        if group != prev_group:
            x = gx[group]
            prev_group = group
        stroke = "#2d7cc4" if group == "new" else "#30363d"
        slot_rect = (f'<rect x="{x:.0f}" y="{SLOT_Y}" width="{SLOT}" height="{SLOT}" rx="10" '
                     f'fill="#161b22" stroke="{stroke}" stroke-width="1.5"')
        if group == "new":
            slot_rect += ('><animate attributeName="stroke-opacity" values="0.35;1;0.35" dur="2s" '
                          'repeatCount="indefinite"/></rect>')
        else:
            slot_rect += "/>"
        p.append(slot_rect)
        d = icon_path(icons_dir, slug)
        ix, iy, scale = x + (SLOT - 28) / 2, SLOT_Y + (SLOT - 28) / 2, 28 / 24
        p.append(f'<g transform="translate({ix:.1f} {iy:.1f}) scale({scale:.4f})"><path d="{d}" fill="{color}"/></g>')
        p.append(f'<text x="{x + SLOT/2:.0f}" y="{NAME_Y}" text-anchor="middle" font-family="{mono}" font-size="9.5" fill="#8b949e">{esc(label)}</text>')
        x += PITCH
    # prompt final com cursor
    prompt_line(p, 40, END_Y, mono, "", cursor=True)
    p.append("</svg>")
    out = "\n".join(p)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"ok {len(out)/1024:.0f} KB")

if __name__ == "__main__":
    main()
