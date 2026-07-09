# -*- coding: utf-8 -*-
"""Gera terminal-card.svg: janela de terminal com foto real, ficha RPG,
hotbar de inventário com os logos da stack e cursor piscando.
Uso: python gen_card.py <avatar.png> <saida.svg> [dir_icones]"""
import base64, io, os, re, sys
from PIL import Image

INFO_W = 62

def kv(label, value):
    base = f". {label}: "
    room = INFO_W - len(base) - len(value) - 1
    dots = "." * max(room, 2)
    return [("lab", base), ("dim", dots + " "), ("val", value)]

def header(title):
    return [("hdr", f"- {title} " + "-" * max(0, INFO_W - len(title) - 3))]

def photo_b64(path):
    rgba = Image.open(path).convert("RGBA")
    bg = Image.new("RGBA", rgba.size, (13, 17, 23, 255))
    img = Image.alpha_composite(bg, rgba).convert("RGB")
    img = img.resize((320, 320), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    return base64.b64encode(buf.getvalue()).decode()

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
    kv("Maxed", "TypeScript, JavaScript, Ruby"),
    kv("Frontend", "React, Next.js, Tailwind"),
    kv("Backend", "Rails, Node.js, PostgreSQL"),
    kv("Inventory", "Docker, Git, Cypress"),
    kv("Speech", "Portuguese, English, French"),
    [("dim", ".")],
    header("New.Game+"),
    kv("Main.Quest", "Gamedev - OpenGL and Vulkan"),
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
    ("typescript",  "TS",       "#3178C6", "core"),
    ("javascript",  "JS",       "#F7DF1E", "core"),
    ("rubyonrails", "Rails",    "#D30001", "core"),
    ("react",       "React",    "#61DAFB", "core"),
    ("nextdotjs",   "Next",     "#FFFFFF", "core"),
    ("tailwindcss", "Tailwind", "#06B6D4", "core"),
    ("nodedotjs",   "Node",     "#5FA04E", "core"),
    ("postgresql",  "Postgres", "#4A91E2", "core"),
    ("docker",      "Docker",   "#2496ED", "core"),
    ("opengl",      "OpenGL",   "#5586A4", "new"),
    ("vulkan",      "Vulkan",   "#C43B3F", "new"),
]

W, H = 920, 884
TITLE_H = 44
SHEET_X, SHEET_Y, LH, FS = 358, 92, 21, 14.5
PC_X, PC_Y, PC_R = 178, 300, 122
SLOT, PITCH, GROUP_GAP = 48, 62, 34
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
    avatar, out_path = sys.argv[1], sys.argv[2]
    icons_dir = sys.argv[3] if len(sys.argv) > 3 else "icons"
    b64 = photo_b64(avatar)
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
    # foto circular com anel
    p.append(f'<defs><clipPath id="pc"><circle cx="{PC_X}" cy="{PC_Y}" r="{PC_R}"/></clipPath></defs>')
    p.append(f'<circle cx="{PC_X}" cy="{PC_Y}" r="{PC_R + 6}" fill="none" stroke="#2d7cc4" stroke-width="3" opacity="0.9"/>')
    p.append(f'<circle cx="{PC_X}" cy="{PC_Y}" r="{PC_R + 11}" fill="none" stroke="#2d7cc4" stroke-width="1.5" opacity="0.35"/>')
    p.append(f'<image href="data:image/jpeg;base64,{b64}" x="{PC_X - PC_R}" y="{PC_Y - PC_R}" '
             f'width="{PC_R*2}" height="{PC_R*2}" clip-path="url(#pc)" preserveAspectRatio="xMidYMid slice"/>')
    p.append(f'<text x="{PC_X}" y="{PC_Y + PC_R + 48}" text-anchor="middle" font-family="{mono}" font-size="21" font-weight="bold" fill="#e6edf3">Harlley Bastos</text>')
    p.append(f'<text x="{PC_X}" y="{PC_Y + PC_R + 74}" text-anchor="middle" font-family="{mono}" font-size="14" fill="#8b949e">@harlleybastos</text>')
    p.append(f'<text x="{PC_X}" y="{PC_Y + PC_R + 108}" text-anchor="middle" font-family="{mono}" font-size="13" fill="#3fb950">&gt; sprite loaded: 1:1 scale, no ASCII</text>')
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
    n_core = sum(1 for s in STACK if s[3] == "core")
    n_new = len(STACK) - n_core
    total = n_core * PITCH - (PITCH - SLOT) + GROUP_GAP + n_new * PITCH - (PITCH - SLOT)
    x0 = (W - total) / 2
    core_cx = x0 + (n_core * PITCH - (PITCH - SLOT)) / 2
    new_x0 = x0 + n_core * PITCH - (PITCH - SLOT) + GROUP_GAP
    new_cx = new_x0 + (n_new * PITCH - (PITCH - SLOT)) / 2
    p.append(f'<text x="{core_cx:.0f}" y="{GROUP_Y}" text-anchor="middle" font-family="{mono}" font-size="10.5" letter-spacing="2" fill="#8b949e">SKILL.TREE</text>')
    p.append(f'<text x="{new_cx:.0f}" y="{GROUP_Y}" text-anchor="middle" font-family="{mono}" font-size="10.5" letter-spacing="2" fill="#4da3ff">NEW.GAME+</text>')
    x = x0
    for slug, label, color, group in STACK:
        if group == "new" and x < new_x0:
            x = new_x0
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
