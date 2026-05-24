#!/usr/bin/env python3
"""Generate branded covers using actual reference images."""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
import random
import os

random.seed(42)

REF_DIR = "../bible-image-refs"
OUT_DIR = "covers-with-refs"
os.makedirs(OUT_DIR, exist_ok=True)

GOLD = (212, 175, 55)
GOLD_LIGHT = (255, 215, 0)
CREAM = (245, 245, 220)
TEXT_DIM = (200, 195, 185)
DARK_OVERLAY = (10, 10, 10)


def get_font(style, size):
    paths = {
        "bold": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ],
        "regular": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ],
        "italic": [
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Oblique.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
        ],
    }
    for p in paths.get(style, paths["regular"]):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()


def load_random_ref(size=None):
    """Load a random reference image, optionally resize."""
    refs = [f for f in os.listdir(REF_DIR) if f.endswith('.jpg')]
    ref_path = os.path.join(REF_DIR, random.choice(refs))
    img = Image.open(ref_path).convert('RGB')
    if size:
        img = img.resize(size, Image.LANCZOS)
    return img


def add_dark_gradient(img, direction='bottom'):
    """Add a dark gradient overlay for text readability."""
    w, h = img.size
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    if direction == 'bottom':
        for y in range(h):
            alpha = int(180 * (y / h) ** 2)  # stronger at bottom
            draw.line([(0, y), (w, y)], fill=(*DARK_OVERLAY, alpha))
    elif direction == 'center':
        mid = h // 2
        for y in range(h):
            dist = abs(y - mid) / mid
            alpha = int(120 * (1 - dist))
            draw.line([(0, y), (w, y)], fill=(*DARK_OVERLAY, alpha))
    elif direction == 'top':
        for y in range(h):
            alpha = int(180 * ((h - y) / h) ** 2)
            draw.line([(0, y), (w, y)], fill=(*DARK_OVERLAY, alpha))
    elif direction == 'vignette':
        cx, cy = w // 2, h // 2
        max_dist = max(cx, cy)
        for y in range(h):
            for x in range(0, w, 2):  # step 2 for speed
                dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                alpha = int(160 * (dist / max_dist) ** 1.5)
                if alpha > 0:
                    draw.point((x, y), fill=(*DARK_OVERLAY, min(alpha, 200)))
    
    return Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')


def draw_text_with_glow(draw, text, pos, font, fill, glow_color=(212, 175, 55), glow_radius=3):
    """Draw text with subtle glow effect."""
    x, y = pos
    # Glow layers
    for r in range(glow_radius, 0, -1):
        alpha = int(80 * (r / glow_radius))
        glow_img = Image.new('RGBA', (w := draw.im.size[0], h := draw.im.size[1]), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_img)
        glow_draw.text((x, y), text, font=font, fill=(*glow_color, alpha))
        glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=r * 2))
        # Composite glow under text happens implicitly since we draw text on top
    draw.text((x, y), text, fill=fill, font=font)


def generate_book_cover():
    """800x1200 book cover with real art background."""
    w, h = 800, 1200
    img = load_random_ref((w, h))
    
    # Darken for text
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.6)
    img = add_dark_gradient(img, 'bottom')
    
    draw = ImageDraw.Draw(img)
    
    # Corner brackets
    s = 50
    t = 2
    draw.line([(20, 20 + s), (20, 20), (20 + s, 20)], fill=GOLD, width=t)
    draw.line([(w - 20, 20 + s), (w - 20, 20), (w - 20 - s, 20)], fill=GOLD, width=t)
    draw.line([(20, h - 20 - s), (20, h - 20), (20 + s, h - 20)], fill=GOLD, width=t)
    draw.line([(w - 20, h - 20 - s), (w - 20, h - 20), (w - 20 - s, h - 20)], fill=GOLD, width=t)
    
    title_font = get_font("bold", 54)
    subtitle_font = get_font("bold", 36)
    tag_font = get_font("regular", 22)
    creator_font = get_font("regular", 20)
    small_font = get_font("regular", 18)
    
    # Title
    title = "LUNAR MYTH"
    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 340), title, fill=GOLD, font=title_font)
    
    subtitle = "KINTSUGI BIBLE"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 410), subtitle, fill=GOLD_LIGHT, font=subtitle_font)
    
    # Line
    draw.line([(w // 2 - 140, 470), (w // 2 + 140, 470)], fill=GOLD, width=2)
    
    tagline = "357+ Hyper-Tactile Mythpunk Prompts"
    bbox = draw.textbbox((0, 0), tagline, font=tag_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 500), tagline, fill=TEXT_DIM, font=tag_font)
    
    tagline2 = "& Complete Collage System"
    bbox = draw.textbbox((0, 0), tagline2, font=tag_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 530), tagline2, fill=TEXT_DIM, font=tag_font)
    
    creator = "By Jennipher Troup"
    bbox = draw.textbbox((0, 0), creator, font=creator_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 600), creator, fill=GOLD, font=creator_font)
    
    bottom = "Break. Repair. Glow. Repeat."
    bbox = draw.textbbox((0, 0), bottom, font=small_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, h - 90), bottom, fill=TEXT_DIM, font=small_font)
    
    return img


def generate_thumbnail():
    """800x800 square thumbnail."""
    w, h = 800, 800
    img = load_random_ref((w, h))
    
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.5)
    img = add_dark_gradient(img, 'vignette')
    
    draw = ImageDraw.Draw(img)
    
    s = 45
    t = 2
    draw.line([(20, 20 + s), (20, 20), (20 + s, 20)], fill=GOLD, width=t)
    draw.line([(w - 20, 20 + s), (w - 20, 20), (w - 20 - s, 20)], fill=GOLD, width=t)
    draw.line([(20, h - 20 - s), (20, h - 20), (20 + s, h - 20)], fill=GOLD, width=t)
    draw.line([(w - 20, h - 20 - s), (w - 20, h - 20), (w - 20 - s, h - 20)], fill=GOLD, width=t)
    
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
    draw.text(((w - tw) // 2, 375), subtitle, fill=GOLD_LIGHT, font=sub_font)
    
    draw.line([(w // 2 - 120, 440), (w // 2 + 120, 440)], fill=GOLD, width=2)
    
    tag = "Break. Repair. Glow."
    bbox = draw.textbbox((0, 0), tag, font=tag_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 465), tag, fill=TEXT_DIM, font=tag_font)
    
    return img


def generate_banner():
    """1200x400 wide banner."""
    w, h = 1200, 400
    img = load_random_ref((w, h))
    
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.5)
    img = add_dark_gradient(img, 'center')
    
    draw = ImageDraw.Draw(img)
    
    s = 35
    t = 2
    draw.line([(20, 20 + s), (20, 20), (20 + s, 20)], fill=GOLD, width=t)
    draw.line([(w - 20, 20 + s), (w - 20, 20), (w - 20 - s, 20)], fill=GOLD, width=t)
    draw.line([(20, h - 20 - s), (20, h - 20), (20 + s, h - 20)], fill=GOLD, width=t)
    draw.line([(w - 20, h - 20 - s), (w - 20, h - 20), (w - 20 - s, h - 20)], fill=GOLD, width=t)
    
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
    
    tag = "By Jennipher Troup  --  357+ Prompts  --  Break. Repair. Glow. Repeat."
    bbox = draw.textbbox((0, 0), tag, font=tag_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 250), tag, fill=TEXT_DIM, font=tag_font)
    
    return img


def generate_tier_badge(tier_name, price, color):
    """400x400 tier badge with art background."""
    w, h = 400, 400
    img = load_random_ref((w, h))
    
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.4)
    img = add_dark_gradient(img, 'vignette')
    
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([15, 15, w - 15, h - 15], outline=(*color, 150), width=2)
    
    s = 28
    t = 2
    draw.line([(20, 20 + s), (20, 20), (20 + s, 20)], fill=color, width=t)
    draw.line([(w - 20, 20 + s), (w - 20, 20), (w - 20 - s, 20)], fill=color, width=t)
    draw.line([(20, h - 20 - s), (20, h - 20), (20 + s, h - 20)], fill=color, width=t)
    draw.line([(w - 20, h - 20 - s), (w - 20, h - 20), (w - 20 - s, h - 20)], fill=color, width=t)
    
    tier_font = get_font("bold", 24)
    price_font = get_font("bold", 48)
    name_font = get_font("regular", 19)
    
    emoji = "Seed" if "Seed" in tier_name else "Full" if "Full" in tier_name else "Celestial"
    tname = f"{emoji} {tier_name}"
    bbox = draw.textbbox((0, 0), tname, font=name_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 110), tname, fill=color, font=name_font)
    
    bbox = draw.textbbox((0, 0), price, font=price_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 155), price, fill=CREAM, font=price_font)
    
    draw.line([(w // 2 - 55, 220), (w // 2 + 55, 220)], fill=(*color, 120), width=2)
    
    cta = "Get Access"
    bbox = draw.textbbox((0, 0), cta, font=tier_font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, 243), cta, fill=color, font=tier_font)
    
    return img


if __name__ == "__main__":
    print("Generating covers with real reference art...")
    
    generate_book_cover().save(os.path.join(OUT_DIR, "cover-book-800x1200.png"))
    print("  Book cover")
    
    generate_thumbnail().save(os.path.join(OUT_DIR, "thumbnail-800x800.png"))
    print("  Thumbnail")
    
    generate_banner().save(os.path.join(OUT_DIR, "banner-1200x400.png"))
    print("  Banner")
    
    generate_tier_badge("Seed Tier", "$37", GOLD).save(os.path.join(OUT_DIR, "tier-seed-400x400.png"))
    print("  Seed badge")
    
    generate_tier_badge("Full Moon", "$67", GOLD_LIGHT).save(os.path.join(OUT_DIR, "tier-fullmoon-400x400.png"))
    print("  Full Moon badge")
    
    generate_tier_badge("Celestial", "$127", (32, 178, 170)).save(os.path.join(OUT_DIR, "tier-celestial-400x400.png"))
    print("  Celestial badge")
    
    print(f"\nDone! Saved to {OUT_DIR}/")
