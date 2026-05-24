#!/usr/bin/env python3
"""Generate Lunar Myth Kintsugi Bible branded covers using PIL."""

from PIL import Image, ImageDraw, ImageFont
import random
import os

random.seed(42)

GOLD = (212, 175, 55)
GOLD_LIGHT = (255, 215, 0)
OBSIDIAN = (10, 10, 10)
OBSIDIAN_LIGHT = (26, 26, 26)
TEAL = (32, 178, 170)
CREAM = (245, 245, 220)
TEXT_DIM = (160, 152, 136)


def get_font(name, size):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except:
                pass
    return ImageFont.load_default()


def draw_kintsugi_cracks(draw, width, height, color, count=5, alpha=80):
    for _ in range(count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        points = [(x, y)]
        for _ in range(random.randint(5, 12)):
            x += random.randint(-80, 80)
            y += random.randint(-80, 80)
            points.append((x, y))
        for i in range(len(points) - 1):
            draw.line([points[i], points[i + 1]], fill=(*color, alpha), width=random.randint(1, 3))


def draw_corner_decorations(draw, width, height, color, size=50):
    s = size
    t = 2
    draw.line([(20, 20 + s), (20, 20), (20 + s, 20)], fill=(*color, 100), width=t)
    draw.line([(width - 20, 20 + s), (width - 20, 20), (width - 20 - s, 20)], fill=(*color, 100), width=t)
    draw.line([(20, height - 20 - s), (20, height - 20), (20 + s, height - 20)], fill=(*color, 100), width=t)
    draw.line([(width - 20, height - 20 - s), (width - 20, height - 20), (width - 20 - s, height - 20)], fill=(*color, 100), width=t)


def generate_book_cover():
    w, h = 800, 1200
    img = Image.new('RGBA', (w, h), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    # Background gradient
    for y in range(h):
        ratio = y / h
        r = int(OBSIDIAN[0] + (OBSIDIAN_LIGHT[0] - OBSIDIAN[0]) * ratio * 0.3)
        g = int(OBSIDIAN[1] + (OBSIDIAN_LIGHT[1] - OBSIDIAN[1]) * ratio * 0.15)
        b = int(OBSIDIAN[2] + 12 * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    # Noise
    for _ in range(3000):
        x, y = random.randint(0, w - 1), random.randint(0, h - 1)
        draw.point((x, y), fill=(255, 255, 255, random.randint(2, 6)))

    # Kintsugi cracks
    draw_kintsugi_cracks(draw, w, h, GOLD, count=5, alpha=45)

    # Corner decorations
    draw_corner_decorations(draw, w, h, GOLD, size=55)

    # Fonts
    title_font = get_font("bold", 56)
    subtitle_font = get_font("bold", 36)
    tagline_font = get_font("regular", 24)
    creator_font = get_font("regular", 22)
    small_font = get_font("regular", 18)

    # Main title
    title = "LUNAR MYTH"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 320), title, fill=GOLD, font=title_font)

    # Subtitle
    subtitle = "KINTSUGI BIBLE"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 395), subtitle, fill=GOLD_LIGHT, font=subtitle_font)

    # Decorative line
    draw.line([(w // 2 - 140, 460), (w // 2 + 140, 460)], fill=GOLD, width=2)

    # Tagline
    tagline = "357+ Hyper-Tactile Mythpunk Prompts"
    bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 495), tagline, fill=TEXT_DIM, font=tagline_font)

    tagline2 = "& Complete Collage System"
    bbox = draw.textbbox((0, 0), tagline2, font=tagline_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 525), tagline2, fill=TEXT_DIM, font=tagline_font)

    # Creator
    creator = "By Jennipher Troup"
    bbox = draw.textbbox((0, 0), creator, font=creator_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 600), creator, fill=GOLD, font=creator_font)

    # Bottom tagline
    bottom = "Break. Repair. Glow. Repeat."
    bbox = draw.textbbox((0, 0), bottom, font=small_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, h - 90), bottom, fill=TEXT_DIM, font=small_font)

    return img.convert('RGB')


def generate_thumbnail():
    w, h = 800, 800
    img = Image.new('RGBA', (w, h), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    for y in range(h):
        ratio = y / h
        r = int(OBSIDIAN[0] + 12 * ratio)
        g = int(OBSIDIAN[1] + 8 * ratio)
        b = int(OBSIDIAN[2] + 15 * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    draw_kintsugi_cracks(draw, w, h, GOLD, count=4, alpha=40)
    draw_corner_decorations(draw, w, h, GOLD, size=45)

    title_font = get_font("bold", 64)
    sub_font = get_font("bold", 44)
    tag_font = get_font("regular", 22)

    title = "LUNAR"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 300), title, fill=GOLD, font=title_font)

    subtitle = "MYTH"
    bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 380), subtitle, fill=GOLD_LIGHT, font=sub_font)

    draw.line([(w // 2 - 120, 450), (w // 2 + 120, 450)], fill=GOLD, width=2)

    tag = "Break. Repair. Glow."
    bbox = draw.textbbox((0, 0), tag, font=tag_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 475), tag, fill=TEXT_DIM, font=tag_font)

    return img.convert('RGB')


def generate_banner():
    w, h = 1200, 400
    img = Image.new('RGBA', (w, h), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    for y in range(h):
        ratio = y / h
        r = int(OBSIDIAN[0] + 8 * ratio)
        g = int(OBSIDIAN[1] + 12 * ratio)
        b = int(OBSIDIAN[2] + 20 * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))

    draw_kintsugi_cracks(draw, w, h, GOLD, count=3, alpha=30)
    draw_corner_decorations(draw, w, h, GOLD, size=35)

    title_font = get_font("bold", 42)
    sub_font = get_font("bold", 26)
    tag_font = get_font("regular", 17)

    title = "LUNAR MYTH KINTSUGI BIBLE"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 130), title, fill=GOLD, font=title_font)

    subtitle = "The Complete Creative System"
    bbox = draw.textbbox((0, 0), subtitle, font=sub_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 185), subtitle, fill=GOLD_LIGHT, font=sub_font)

    draw.line([(w // 2 - 180, 230), (w // 2 + 180, 230)], fill=GOLD, width=2)

    tag = "By Jennipher Troup  ·  357+ Prompts  ·  Break. Repair. Glow. Repeat."
    bbox = draw.textbbox((0, 0), tag, font=tag_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 250), tag, fill=TEXT_DIM, font=tag_font)

    return img.convert('RGB')


def generate_tier_badge(tier_name, price, color, filename):
    w, h = 400, 400
    img = Image.new('RGBA', (w, h), OBSIDIAN)
    draw = ImageDraw.Draw(img)

    # Subtle border
    draw.rectangle([15, 15, w - 15, h - 15], outline=(*color, 100), width=2)
    draw_corner_decorations(draw, w, h, color, size=28)

    tier_font = get_font("bold", 24)
    price_font = get_font("bold", 46)
    name_font = get_font("regular", 19)

    emoji = "🌱" if "Seed" in tier_name else "🌕" if "Full" in tier_name else "🌟"
    tname = f"{emoji} {tier_name}"
    bbox = draw.textbbox((0, 0), tname, font=name_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 115), tname, fill=color, font=name_font)

    bbox = draw.textbbox((0, 0), price, font=price_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 160), price, fill=CREAM, font=price_font)

    draw.line([(w // 2 - 55, 225), (w // 2 + 55, 225)], fill=(*color, 100), width=2)

    cta = "Get Access"
    bbox = draw.textbbox((0, 0), cta, font=tier_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 248), cta, fill=color, font=tier_font)

    return img.convert('RGB')


if __name__ == "__main__":
    out_dir = "covers"
    os.makedirs(out_dir, exist_ok=True)

    print("Generating book cover...")
    generate_book_cover().save(os.path.join(out_dir, "cover-book-800x1200.png"))

    print("Generating thumbnail...")
    generate_thumbnail().save(os.path.join(out_dir, "thumbnail-800x800.png"))

    print("Generating banner...")
    generate_banner().save(os.path.join(out_dir, "banner-1200x400.png"))

    print("Generating tier badges...")
    generate_tier_badge("Seed Tier", "$37", GOLD, os.path.join(out_dir, "tier-seed-400x400.png"))
    generate_tier_badge("Full Moon", "$67", GOLD_LIGHT, os.path.join(out_dir, "tier-fullmoon-400x400.png"))
    generate_tier_badge("Celestial", "$127", TEAL, os.path.join(out_dir, "tier-celestial-400x400.png"))

    print(f"Done! Images saved to {out_dir}/")
