#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news poster (1024x1024 PNG).

Every element is drawn from scratch with PIL: no photos, no downloaded
assets, no AI-generated imagery. Text uses DejaVu fonts shipped with the OS.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 246, 236)
INK = (22, 19, 14)
RED = (166, 27, 27)
RED_DARK = (140, 20, 20)
RULE = (180, 172, 150)
CARD = (255, 255, 255)
SKY = (216, 231, 242)
SEA = (38, 98, 140)
SEA_DARK = (24, 70, 104)
GRAY = (110, 110, 108)
MUTED = (74, 68, 58)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SR = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w, max_lines=None):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(".,") + "…"
    return lines


def para(draw, x, y, text, fnt, color, max_w, leading, max_lines=None):
    lines = wrap(draw, text, fnt, max_w, max_lines)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def explosion(draw, cx, cy, r, fill):
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_lead_art(draw, x0, y0, x1, y1):
    """Kerch Strait: a bridge with a collapsed span, smoke and fire."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    # clouds
    draw.ellipse([x0 + 18, y0 + 16, x0 + 78, y0 + 38], fill=(255, 255, 255))
    draw.ellipse([x0 + 52, y0 + 10, x0 + 118, y0 + 34], fill=(255, 255, 255))
    draw.ellipse([x1 - 120, y0 + 22, x1 - 58, y0 + 44], fill=(255, 255, 255))
    # sea
    sea_y = y0 + int((y1 - y0) * 0.62)
    draw.rectangle([x0, sea_y, x1, y1], fill=SEA)
    draw.line([x0, sea_y, x1, sea_y], fill=SEA_DARK, width=2)
    for wx in range(x0 + 12, x1 - 10, 46):
        draw.arc([wx, sea_y + 14, wx + 30, sea_y + 26], 0, 180, fill=(255, 255, 255), width=2)
    # bridge deck with a gap in the middle
    deck_y = y0 + int((y1 - y0) * 0.42)
    gap_cx = (x0 + x1) // 2
    gap = 74
    draw.rectangle([x0 + 8, deck_y, gap_cx - gap // 2, deck_y + 12], fill=(52, 52, 50))
    draw.rectangle([gap_cx + gap // 2, deck_y, x1 - 8, deck_y + 12], fill=(52, 52, 50))
    # support pillars
    for px in (x0 + 52, x1 - 62):
        draw.rectangle([px, deck_y + 12, px + 12, sea_y + 34], fill=(74, 74, 72))
    # collapsed span tilted into the water
    draw.polygon(
        [(gap_cx - gap // 2 + 4, deck_y + 12), (gap_cx + gap // 2 - 4, deck_y + 12),
         (gap_cx + gap // 2 - 26, sea_y + 26), (gap_cx - gap // 2 - 14, sea_y + 26)],
        fill=(90, 88, 84))
    # smoke above the gap
    draw.ellipse([gap_cx - 34, deck_y - 66, gap_cx + 6, deck_y - 26], fill=(150, 150, 148))
    draw.ellipse([gap_cx - 8, deck_y - 84, gap_cx + 34, deck_y - 42], fill=(128, 128, 126))
    # fire burst at the gap
    explosion(draw, gap_cx, deck_y - 6, 26, (232, 122, 24))
    explosion(draw, gap_cx, deck_y - 6, 14, (246, 196, 66))
    # label
    draw.text((x0 + 14, y1 - 26), "THE KERCH STRAIT", font=font(FB, 15),
              fill=(255, 255, 255))


def draw_tanker(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(232, 238, 244))
    draw.rectangle([x0, y1 - 18, x1, y1], fill=SEA)
    # hull
    draw.polygon([(x0 + 8, y1 - 30), (x1 - 8, y1 - 30), (x1 - 20, y1 - 16),
                  (x0 + 20, y1 - 16)], fill=(52, 52, 50))
    # containers
    draw.rectangle([x0 + 26, y1 - 48, x0 + 66, y1 - 30], fill=(166, 27, 27))
    draw.rectangle([x0 + 70, y1 - 48, x0 + 110, y1 - 30], fill=(38, 98, 140))
    draw.rectangle([x0 + 114, y1 - 48, x0 + 148, y1 - 30], fill=(232, 122, 24))
    # flame on the far tanker
    explosion(draw, x1 - 30, y0 + 16, 12, (232, 122, 24))
    explosion(draw, x1 - 30, y0 + 16, 6, (246, 196, 66))


def draw_aid(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(238, 232, 218))
    # crates
    draw.rectangle([x0 + 16, y1 - 34, x0 + 66, y1 - 8], fill=(196, 164, 110))
    draw.rectangle([x0 + 72, y1 - 34, x0 + 122, y1 - 8], fill=(176, 142, 92))
    # red cross flag
    draw.rectangle([x0 + 128, y0 + 6, x0 + 132, y1 - 8], fill=(90, 84, 72))
    draw.rectangle([x0 + 132, y0 + 6, x0 + 172, y0 + 30], fill=(255, 255, 255))
    draw.rectangle([x0 + 148, y0 + 10, x0 + 156, y0 + 26], fill=RED)
    draw.rectangle([x0 + 140, y0 + 14, x0 + 164, y0 + 22], fill=RED)
    # cross on crate
    draw.rectangle([x0 + 36, y1 - 30, x0 + 44, y1 - 12], fill=RED)
    draw.rectangle([x0 + 28, y1 - 24, x0 + 52, y1 - 16], fill=RED)


def draw_flags(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(232, 238, 244))
    cols = [(166, 27, 27), (38, 98, 140), (232, 122, 24)]
    for i, c in enumerate(cols):
        fx = x0 + 22 + i * 52
        draw.rectangle([fx, y0 + 8, fx + 3, y1 - 8], fill=(90, 84, 72))
        draw.polygon([(fx + 3, y0 + 8), (fx + 40, y0 + 14), (fx + 3, y0 + 24)], fill=c)
    draw.rectangle([x0, y1 - 10, x1, y1 - 6], fill=(120, 116, 104))


def draw_jet(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(232, 238, 244))
    # contrail
    for i in range(5):
        draw.ellipse([x0 + 12 + i * 16, y0 + 34 - i * 2, x0 + 22 + i * 16, y0 + 40 - i * 2],
                     fill=(255, 255, 255))
    # jet silhouette
    draw.polygon([(x0 + 96, y0 + 12), (x0 + 150, y0 + 30), (x0 + 96, y0 + 34),
                  (x0 + 108, y0 + 26)], fill=(52, 52, 50))
    draw.polygon([(x0 + 108, y0 + 20), (x0 + 128, y0 + 12), (x0 + 128, y0 + 22)],
                 fill=(52, 52, 50))
    draw.polygon([(x0 + 108, y0 + 30), (x0 + 128, y0 + 40), (x0 + 128, y0 + 30)],
                 fill=(52, 52, 50))


def draw_eu(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(238, 232, 218))
    # five bars for five states, arrow to a return hub box
    for i in range(5):
        bx = x0 + 18 + i * 22
        h = 14 + i * 6
        draw.rectangle([bx, y1 - 12 - h, bx + 14, y1 - 12], fill=(38, 98, 140))
    draw.line([x0 + 132, y1 - 30, x0 + 158, y1 - 30], fill=RED, width=4)
    draw.polygon([(x0 + 158, y1 - 38), (x0 + 172, y1 - 30), (x0 + 158, y1 - 22)], fill=RED)
    draw.rectangle([x0 + 174, y1 - 44, x1 - 8, y1 - 12], fill=(255, 255, 255),
                   outline=INK, width=2)
    draw.text((x0 + 180, y1 - 38), "HUB", font=font(FB, 15), fill=INK)


def card(draw, x0, y0, w, h, kicker, headline, deck, art, accent=RED):
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=CARD, outline=RULE, width=1)
    draw.rectangle([x0, y0, x0 + w, y0 + 6], fill=accent)
    ix0, iy0, ix1, iy1 = x0 + 14, y0 + 14, x0 + w - 14, y0 + 66
    art(draw, ix0, iy0, ix1, iy1)
    tx = x0 + 14
    ty = y0 + 76
    draw.text((tx, ty), kicker, font=font(FB, 15), fill=RED)
    ty += 23
    ty = para(draw, tx, ty, headline, font(FB, 24), INK, w - 28, 27, max_lines=3)
    ty += 4
    para(draw, tx, ty, deck, font(FR, 18), MUTED, w - 28, 22, max_lines=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36

    # ---- masthead ----
    d.text((W // 2, 30), "WORLD NEWS", font=font(SB, 60), fill=INK, anchor="ma")
    d.line([mx, 102, W - mx, 102], fill=INK, width=3)
    d.line([mx, 108, W - mx, 108], fill=INK, width=1)
    d.text((W // 2, 120), "TUESDAY, 17 NOVEMBER 2026",
           font=font(FB, 46), fill=RED, anchor="ma")
    d.text((W // 2, 172), "Six stories that defined the day",
           font=font(SR, 21), fill=MUTED, anchor="ma")

    # ---- lead story: Kerch Bridge ----
    ly0, ly1 = 200, 430
    d.rectangle([mx, ly0, W - mx, ly1], fill=CARD, outline=INK, width=2)
    d.rectangle([mx, ly0, W - mx, ly0 + 6], fill=RED)
    tx = mx + 24
    d.text((tx, ly0 + 20), "EUROPE  ·  WAR IN UKRAINE", font=font(FB, 19), fill=RED)
    d.text((tx, ly0 + 50), "KERCH BRIDGE", font=font(SB, 47), fill=INK)
    d.text((tx, ly0 + 100), "STRUCK AGAIN", font=font(SB, 47), fill=INK)
    deck = ("Ukraine hits the Crimea link for a second straight day; "
            "a span collapses into the sea.")
    para(d, tx, ly0 + 162, deck, font(FR, 21), MUTED, 520, 27, max_lines=2)
    draw_lead_art(d, mx + 584, ly0 + 20, W - mx - 24, ly1 - 20)

    # ---- grid of five stories + one "also" panel ----
    gy0 = 446
    gh = 252
    gap = 14
    cw = (W - 2 * mx - 2 * gap) // 3
    rows = [
        ("MIDDLE EAST · STRAIT OF HORMUZ",
         "Tankers hit as Gulf tensions flare",
         "US strikes hit Qeshm Island; drones target a US base in Bahrain; "
         "a tanker hits a mine.",
         draw_tanker, SEA),
        ("GAZA · AID",
         "West urges Israel: open Gaza crossings",
         "Four nations call it catastrophic; the UN warns "
         "1.7m remain displaced.",
         draw_aid, RED),
        ("ASIA · DIPLOMACY",
         "Trump opens Asia trip; Xi meeting set",
         "Trump lands in Manila for a Quad summit; a Xi–Trump–Putin "
         "meeting is set.",
         draw_flags, (38, 98, 140)),
        ("ASIA · SECURITY",
         "Japan scrambles jets after Russian incursion",
         "Two suspected Russian aircraft enter Japanese airspace; "
         "Tokyo lodges a strong protest.",
         draw_jet, (38, 98, 140)),
        ("EUROPE · MIGRATION",
         "Five EU states plan Rwanda return hub",
         "Five EU states move to send rejected asylum seekers to "
         "a return hub in Rwanda.",
         draw_eu, (38, 98, 140)),
    ]
    for i, (kick, head, deck, art, accent) in enumerate(rows):
        r, c = divmod(i, 3)
        x0 = mx + c * (cw + gap)
        y0 = gy0 + r * (gh + gap)
        card(d, x0, y0, cw, gh, kick, head, deck, art, accent)

    # ---- "also" panel, bottom right ----
    ax0 = mx + 2 * (cw + gap)
    ay0 = gy0 + gh + gap
    d.rectangle([ax0, ay0, ax0 + cw, ay0 + gh], fill=(238, 232, 218),
                outline=RULE, width=1)
    d.rectangle([ax0, ay0, ax0 + cw, ay0 + 6], fill=RED)
    d.text((ax0 + 14, ay0 + 18), "ALSO ON 17 NOVEMBER", font=font(FB, 15), fill=RED)
    briefs = [
        "Mongolia's president resigns amid a corruption scandal.",
        "Depardieu admits a sexual assault charge in Paris.",
        "COP31 climate talks enter a decisive stage in Antalya.",
    ]
    by = ay0 + 52
    for b in briefs:
        d.rectangle([ax0 + 14, by + 6, ax0 + 24, by + 16], fill=RED)
        by = para(d, ax0 + 34, by, b, font(FR, 18), INK, cw - 48, 22, max_lines=2)
        by += 10

    # ---- footer ----
    d.line([mx, 976, W - mx, 976], fill=RULE, width=1)
    d.text((W // 2, 984), "17 NOVEMBER 2026  ·  The day's news, drawn from world news reports",
           font=font(FB, 15), fill=MUTED, anchor="ma")

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
