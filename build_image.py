#!/usr/bin/env python3
"""Compose entry.png: the world news of Saturday 21 November 2026 in one image.

A newspaper front page drawn with Pillow: a masthead naming the day, one
lead story with a drawn scene, and five more stories with pictogram icons.
Every headline below was reported on 21 November 2026 (see README.md).
Run:  python3 build_image.py   ->  writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont
import os
import textwrap

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
W, H = 1024, 1024

PAPER = (247, 243, 234)
INK = (24, 24, 28)
MUTED = (92, 88, 80)
RED = (178, 34, 40)
NAVY = (23, 37, 66)
GOLD = (201, 150, 39)
TEAL = (24, 110, 110)
GREEN = (46, 120, 66)
SKY = (16, 24, 44)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw, text, fnt, width):
    """Wrap text to a pixel width, return list of lines."""
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading=1.18):
    x, y = xy
    lines = wrap(draw, text, fnt, width)
    step = int(fnt.size * leading)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y


def star(draw, cx, cy, r, fill):
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def lead_scene(draw, box):
    """Night sky over a city: missile trails, bursts, skyline."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    # stars
    for sx, sy in [(40, 30), (120, 70), (210, 25), (300, 60), (90, 120), (250, 110)]:
        draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 4, y0 + sy + 4], fill=(210, 215, 230))
    # missile trails (arcs of light)
    for (tx, ty, ex, ey) in [(30, 20, 150, 130), (120, 10, 215, 120), (230, 30, 285, 110)]:
        draw.line([x0 + tx, y0 + ty, x0 + ex, y0 + ey], fill=(240, 190, 90), width=5)
        star(draw, x0 + ex, y0 + ey, 20, (245, 160, 60))
    star(draw, x0 + 70, y0 + 150, 26, (238, 120, 55))
    # skyline
    for bx, bw, bh in [(10, 44, 60), (62, 34, 88), (104, 52, 66), (164, 30, 96),
                       (202, 46, 58), (256, 36, 80), (300, 44, 64), (352, 40, 72)]:
        draw.rectangle([x0 + bx, y1 - 30 - bh, x0 + bx + bw, y1 - 30], fill=(8, 12, 24))
        for wy in range(y1 - 30 - bh + 10, y1 - 44, 18):
            for wx in range(x0 + bx + 7, x0 + bx + bw - 8, 13):
                draw.rectangle([wx, wy, wx + 5, wy + 7], fill=(250, 205, 110))
    draw.rectangle([x0, y1 - 30, x1, y1], fill=(8, 12, 24))
    tag = font(SANS_B, 19)
    draw.text((x0 + 12, y1 - 25), "KYIV, UKRAINE", font=tag, fill=(240, 240, 240))
    tw = draw.textlength("INTO POLAND", font=tag)
    draw.text((x1 - tw - 12, y1 - 25), "INTO POLAND", font=tag, fill=(255, 170, 120))


def icon_scales(draw, box, bg):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=bg)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    draw.line([cx, cy - 34, cx, cy + 26], fill=(255, 255, 255), width=6)
    draw.line([cx - 30, cy - 22, cx + 30, cy - 22], fill=(255, 255, 255), width=6)
    for sgn in (-1, 1):
        px = cx + sgn * 30
        draw.line([px, cy - 22, px - 11, cy + 4], fill=(255, 255, 255), width=4)
        draw.line([px, cy - 22, px + 11, cy + 4], fill=(255, 255, 255), width=4)
        draw.arc([px - 13, cy - 2, px + 13, cy + 16], 0, 180, fill=(255, 255, 255), width=4)
    draw.rectangle([cx - 16, cy + 28, cx + 16, cy + 34], fill=(255, 255, 255))


def icon_chart(draw, box, bg):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=bg)
    pts = [(x0 + 14, y0 + 22), (x0 + 38, y0 + 34), (x0 + 56, y0 + 28),
           (x0 + 78, y0 + 52), (x0 + 96, y0 + 66)]
    draw.line(pts, fill=(255, 255, 255), width=6, joint="curve")
    draw.polygon([(x0 + 96, y0 + 66), (x0 + 80, y0 + 64), (x0 + 92, y0 + 50)], fill=(255, 255, 255))
    draw.line([x0 + 12, y1 - 14, x1 - 12, y1 - 14], fill=(255, 255, 255), width=3)


def icon_globe(draw, box, bg):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=bg)
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2, 32
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=5)
    draw.ellipse([cx - 12, cy - r, cx + 12, cy + r], outline=(255, 255, 255), width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=3)
    # heat rays
    for dx, dy in [(-44, -30), (44, -30), (0, -48)]:
        draw.line([cx + dx * 0.72, cy + dy * 0.72, cx + dx, cy + dy], fill=(255, 205, 90), width=5)


def icon_flags(draw, box, bg):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=bg)
    # EU flag (blue, circle of stars)
    draw.rectangle([x0 + 10, y0 + 18, x0 + 52, y0 + 48], fill=(30, 60, 160))
    import math
    for i in range(8):
        ang = 2 * math.pi * i / 8
        sx, sy = x0 + 31 + 11 * math.cos(ang), y0 + 33 + 9 * math.sin(ang)
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(250, 210, 60))
    # UK flag (simplified: blue, white diagonals and crosses, red cross)
    draw.rectangle([x0 + 58, y0 + 18, x0 + 100, y0 + 48], fill=(30, 50, 130))
    draw.line([x0 + 58, y0 + 18, x0 + 100, y0 + 48], fill=(255, 255, 255), width=5)
    draw.line([x0 + 100, y0 + 18, x0 + 58, y0 + 48], fill=(255, 255, 255), width=5)
    draw.rectangle([x0 + 72, y0 + 18, x0 + 86, y0 + 48], fill=(255, 255, 255))
    draw.rectangle([x0 + 58, y0 + 26, x0 + 100, y0 + 40], fill=(255, 255, 255))
    draw.rectangle([x0 + 76, y0 + 18, x0 + 82, y0 + 48], fill=(200, 40, 50))
    draw.rectangle([x0 + 58, y0 + 30, x0 + 100, y0 + 36], fill=(200, 40, 50))
    draw.line([x0 + 31, y0 + 52, x0 + 31, y1 - 10], fill=(255, 255, 255), width=4)
    draw.line([x0 + 79, y0 + 52, x0 + 79, y1 - 10], fill=(255, 255, 255), width=4)


def icon_pill(draw, box, bg):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=bg)
    draw.rounded_rectangle([x0 + 18, y0 + 30, x0 + 92, y0 + 62], radius=16, fill=(255, 255, 255))
    draw.rounded_rectangle([x0 + 55, y0 + 30, x0 + 92, y0 + 62], radius=16, fill=(240, 130, 90))
    draw.line([x0 + 55, y0 + 33, x0 + 55, y0 + 59], fill=bg, width=3)
    star(draw, x0 + 84, y0 + 22, 11, (255, 230, 140))


def icon_dove(draw, box, bg):
    """Two overlapping speech bubbles: talks."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=bg)
    draw.rounded_rectangle([x0 + 14, y0 + 18, x0 + 66, y0 + 56], radius=10, fill=(255, 255, 255))
    draw.polygon([(x0 + 24, y0 + 54), (x0 + 24, y0 + 70), (x0 + 38, y0 + 55)], fill=(255, 255, 255))
    draw.rounded_rectangle([x0 + 44, y0 + 44, x0 + 96, y0 + 82], radius=10, fill=(240, 225, 190))
    draw.polygon([(x0 + 86, y0 + 80), (x0 + 86, y0 + 94), (x0 + 72, y0 + 81)], fill=(240, 225, 190))
    for cx in (28, 40, 52):
        draw.ellipse([x0 + cx, y0 + 33, x0 + cx + 6, y0 + 39], fill=bg)
    for cx in (58, 70, 82):
        draw.ellipse([x0 + cx, y0 + 59, x0 + cx + 6, y0 + 65], fill=bg)


def story(draw, x, y, w, icon_fn, color, kicker, headline, summary):
    icon_fn(draw, (x, y, x + 110, y + 110), color)
    tx = x + 126
    draw.text((tx, y - 2), kicker, font=font(SANS_B, 19), fill=color)
    y2 = text_block(draw, (tx, y + 22), headline, font(SANS_B, 26), INK, w - 126, 1.12)
    text_block(draw, (tx, y2 + 2), summary, font(SANS, 20), MUTED, w - 126, 1.16)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # frame
    d.rectangle([14, 14, W - 14, H - 14], outline=INK, width=3)
    d.rectangle([22, 22, W - 22, H - 22], outline=INK, width=1)

    # masthead
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 62)
    d.text(((W - d.textlength(title, font=tf)) / 2, 30), title, font=tf, fill=INK)
    d.line([48, 112, W - 48, 112], fill=INK, width=3)
    date = "Saturday, 21 November 2026"
    df = font(SANS_B, 36)
    d.text(((W - d.textlength(date, font=df)) / 2, 124), date, font=df, fill=RED)
    sub = "The day's world news in one image"
    sf = font(SANS, 20)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 168), sub, font=sf, fill=MUTED)
    d.line([48, 202, W - 48, 202], fill=INK, width=1)

    # lead story
    lead_scene(d, (48, 218, 470, 478))
    lx = 494
    d.text((lx, 216), "UKRAINE WAR", font=font(SANS_B, 20), fill=RED)
    y = text_block(d, (lx, 242),
                   "Russia fires 400+ drones and 110 missiles at Ukraine; missiles land in Poland",
                   font(SANS_B, 33), INK, W - lx - 48, 1.14)
    text_block(d, (lx, y + 8),
               "Overnight strikes kill at least eight in Kyiv, hitting bridges and "
               "rail stations. Two missiles and a drone come down in Poland — "
               "PM Tusk calls it a deliberate provocation.",
               font(SANS, 20), MUTED, W - lx - 48, 1.18)
    d.line([48, 494, W - 48, 494], fill=INK, width=1)

    # middle grid, two columns
    col_w = (W - 96 - 28) // 2
    story(d, 48, 512, col_w, icon_scales, NAVY, "WORLD COURT · THE HAGUE",
          "Myanmar guilty of genocide, ICJ rules",
          "The UN court finds Myanmar responsible for genocide against the Rohingya.")
    story(d, 48 + col_w + 28, 512, col_w, icon_chart, RED, "MARKETS · NEW YORK",
          "AI stock rout pushes US into correction",
          "Shares fall 3.7% as AI and chip stocks slide.")
    story(d, 48, 676, col_w, icon_globe, TEAL, "CLIMATE · ANTALYA",
          "COP31 talks run overtime",
          "Nearly 200 nations in Turkey miss the deadline without a deal.")
    story(d, 48 + col_w + 28, 676, col_w, icon_flags, (58, 84, 160), "POLITICS · BRUSSELS",
          "UK, EU sign biggest post-Brexit deals",
          "Deals cover food exports, carbon markets, youth mobility.")
    d.line([48, 830, W - 48, 830], fill=INK, width=1)

    # bottom row
    story(d, 48, 846, col_w, icon_pill, GREEN, "HEALTH · LONDON",
          "Cancer pill clears tumours in trial",
          "Drug daraxonrasib leaves tumours undetectable in 1 in 12 patients.")
    story(d, 48 + col_w + 28, 846, col_w, icon_dove, GOLD, "DIPLOMACY · TEHRAN",
          "Iran seeks diplomacy to end the war",
          "Tehran wants guarantees on talks; Trump calls its terms unacceptable.")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
