#!/usr/bin/env python3
"""Generate procedural texture assets for the Lunar Myth Kintsugi Bible."""

from PIL import Image, ImageDraw, ImageFilter
import random
import os
import math

random.seed(42)

OUT_DIR = "textures"
os.makedirs(OUT_DIR, exist_ok=True)

GOLD = (212, 175, 55)
GOLD_LIGHT = (255, 215, 0)
TEAL = (32, 178, 170)
MAGENTA = (199, 21, 133)
INDIGO = (25, 25, 112)
CREAM = (245, 245, 220)
DARK = (10, 10, 10)


def save(img, name):
    img.save(os.path.join(OUT_DIR, name))


def new_img(size=(512, 512), bg=DARK):
    return Image.new('RGB', size, bg)


# ========== NEWSPAPER CLIPPINGS (10) ==========
def generate_newspaper(i):
    """Generate aged newspaper clipping textures with text-like patterns."""
    w, h = 600, 800
    img = new_img((w, h), (240, 235, 220))
    draw = ImageDraw.Draw(img)

    # Age the paper
    for _ in range(5000):
        x, y = random.randint(0, w - 1), random.randint(0, h - 1)
        draw.point((x, y), fill=(230, 220, 200, random.randint(1, 3)))

    # Text columns
    for col in range(random.randint(2, 4)):
        cx = 40 + col * 140
        for line in range(random.randint(30, 60)):
            ly = 30 + line * 12
            line_len = random.randint(80, 120)
            draw.line([(cx, ly), (cx + line_len, ly)], fill=(40, 40, 40), width=random.randint(1, 2))

    # Headline block
    hy = random.randint(40, 100)
    draw.rectangle([(30, hy), (w - 30, hy + 25)], fill=(30, 30, 30))

    # Coffee stain
    sx, sy = random.randint(100, w - 100), random.randint(100, h - 100)
    for r in range(40, 0, -1):
        alpha = int(15 * (r / 40))
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(160, 140, 100, alpha))

    # Torn edge
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    for _ in range(50):
        if edge == 'top':
            x = random.randint(0, w)
            draw.line([(x, 0), (x, random.randint(5, 20))], fill=DARK, width=1)
        elif edge == 'bottom':
            x = random.randint(0, w)
            draw.line([(x, h), (x, h - random.randint(5, 20))], fill=DARK, width=1)

    save(img, f"newspaper_{i:02d}.png")


# ========== STAINED GLASS / OBSIDIAN (15) ==========
def generate_stained_glass(i):
    """Generate stained glass mosaic and obsidian shard textures."""
    w, h = 512, 512
    img = new_img((w, h))
    draw = ImageDraw.Draw(img)

    if i < 8:  # Stained glass
        colors = [GOLD, GOLD_LIGHT, TEAL, MAGENTA, INDIGO, (100, 50, 150), (50, 150, 100), (200, 100, 50)]
        # Generate polygon mosaic
        points = []
        for _ in range(random.randint(15, 30)):
            px = random.randint(0, w)
            py = random.randint(0, h)
            points.append((px, py))

        # Draw polygons between nearby points
        for j, (x1, y1) in enumerate(points):
            for x2, y2 in points[j + 1:]:
                if abs(x1 - x2) < 150 and abs(y1 - y2) < 150:
                    poly = [(x1, y1), (x2, y2), ((x1 + x2) // 2 + random.randint(-30, 30), (y1 + y2) // 2 + random.randint(-30, 30))]
                    draw.polygon(poly, fill=random.choice(colors))

        # Lead lines
        for j, (x1, y1) in enumerate(points):
            for x2, y2 in points[j + 1:]:
                if abs(x1 - x2) < 150 and abs(y1 - y2) < 150:
                    draw.line([(x1, y1), (x2, y2)], fill=(30, 30, 30), width=2)

        # Inner glow on some pieces
        for _ in range(5):
            gx, gy = random.randint(50, w - 50), random.randint(50, h - 50)
            for r in range(30, 0, -2):
                draw.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(*GOLD_LIGHT, int(20 * (r / 30))))

        save(img, f"stained_glass_{i:02d}.png")
    else:  # Obsidian
        # Dark reflective shards
        for _ in range(random.randint(20, 40)):
            poly = []
            cx, cy = random.randint(0, w), random.randint(0, h)
            for _ in range(random.randint(3, 6)):
                poly.append((cx + random.randint(-40, 40), cy + random.randint(-40, 40)))
            shade = random.randint(5, 25)
            draw.polygon(poly, fill=(shade, shade, shade + 5))

        # Specular highlights
        for _ in range(random.randint(10, 20)):
            hx, hy = random.randint(0, w), random.randint(0, h)
            draw.ellipse([hx - 2, hy - 2, hx + 2, hy + 2], fill=(200, 200, 220))

        save(img, f"obsidian_{i:02d}.png")


# ========== KINTSUGI GOLD OVERLAYS (10) ==========
def generate_kintsugi(i):
    """Generate golden kintsugi crack repair line overlays."""
    w, h = 512, 512
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Crack paths
    for _ in range(random.randint(3, 8)):
        x, y = random.randint(0, w), random.randint(0, h)
        points = [(x, y)]
        for _ in range(random.randint(5, 15)):
            x += random.randint(-60, 60)
            y += random.randint(-60, 60)
            points.append((x, y))

        width = random.randint(2, 6)
        for j in range(len(points) - 1):
            draw.line([points[j], points[j + 1]], fill=(*GOLD, 200), width=width)
            # Inner highlight
            if width > 2:
                draw.line([points[j], points[j + 1]], fill=(*GOLD_LIGHT, 150), width=width - 2)

    # Glow
    img_blur = img.filter(ImageFilter.GaussianBlur(radius=3))
    img_final = Image.alpha_composite(Image.new('RGBA', (w, h), (0, 0, 0, 0)), img_blur)
    img_final = Image.alpha_composite(img_final, img)

    save(img_final.convert('RGB'), f"kintsugi_gold_{i:02d}.png")


# ========== EMBROIDERY / BEADING (20) ==========
def generate_embroidery(i):
    """Generate embroidery stitch and beadwork texture overlays."""
    w, h = 512, 512
    img = new_img((w, h), (30, 25, 20))
    draw = ImageDraw.Draw(img)

    if i < 10:  # Embroidery stitches
        thread_colors = [GOLD, CREAM, TEAL, MAGENTA, (200, 200, 200), (180, 140, 100)]
        # Running stitch lines
        for _ in range(random.randint(20, 40)):
            x1, y1 = random.randint(0, w), random.randint(0, h)
            x2, y2 = x1 + random.randint(-100, 100), y1 + random.randint(-100, 100)
            color = random.choice(thread_colors)
            # Dashed line effect
            dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            steps = int(dist / 6)
            for s in range(steps):
                t1 = s / steps
                t2 = (s + 0.5) / steps
                sx1 = int(x1 + (x2 - x1) * t1)
                sy1 = int(y1 + (y2 - y1) * t1)
                sx2 = int(x1 + (x2 - x1) * t2)
                sy2 = int(y1 + (y2 - y1) * t2)
                draw.line([(sx1, sy1), (sx2, sy2)], fill=color, width=2)

        # French knots
        for _ in range(random.randint(30, 60)):
            kx, ky = random.randint(0, w), random.randint(0, h)
            kr = random.randint(2, 4)
            draw.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=random.choice(thread_colors))

        save(img, f"embroidery_stitches_{i:02d}.png")
    else:  # Beading
        bead_colors = [GOLD, GOLD_LIGHT, CREAM, (200, 200, 220), (180, 160, 140), TEAL]
        for _ in range(random.randint(100, 200)):
            bx, by = random.randint(0, w), random.randint(0, h)
            br = random.randint(3, 6)
            color = random.choice(bead_colors)
            # Bead with highlight
            draw.ellipse([bx - br, by - br, bx + br, by + br], fill=color)
            draw.ellipse([bx - br // 2, by - br // 2, bx, by], fill=(255, 255, 255, 100))

        save(img, f"beading_texture_{i:02d}.png")


# ========== BOTANICAL ELEMENTS (10) ==========
def generate_botanical(i):
    """Generate botanical silhouette and pattern textures."""
    w, h = 512, 512
    img = new_img((w, h))
    draw = ImageDraw.Draw(img)

    botanical_colors = [TEAL, (40, 200, 150), (100, 220, 180), (60, 180, 160), GOLD_LIGHT]

    if i < 5:  # Vine patterns
        for _ in range(random.randint(5, 10)):
            x, y = random.randint(0, w), random.randint(0, h)
            points = [(x, y)]
            for _ in range(random.randint(10, 20)):
                x += random.randint(-30, 30)
                y += random.randint(-20, 20)
                points.append((x, y))
                # Leaf
                if random.random() > 0.5:
                    lx, ly = x + random.randint(-10, 10), y + random.randint(-10, 10)
                    draw.ellipse([lx - 5, ly - 3, lx + 5, ly + 3], fill=random.choice(botanical_colors))
            for j in range(len(points) - 1):
                draw.line([points[j], points[j + 1]], fill=random.choice(botanical_colors), width=2)
    else:  # Flower clusters
        for _ in range(random.randint(10, 20)):
            cx, cy = random.randint(0, w), random.randint(0, h)
            # Petals
            for a in range(0, 360, 45):
                rad = math.radians(a)
                px = cx + int(15 * math.cos(rad))
                py = cy + int(15 * math.sin(rad))
                draw.ellipse([px - 6, py - 6, px + 6, py + 6], fill=random.choice(botanical_colors))
            # Center
            draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=GOLD_LIGHT)

    save(img, f"botanical_{i:02d}.png")


# ========== WATERCOLOR BLEEDS (10) ==========
def generate_watercolor(i):
    """Generate watercolor bleed and splotch textures."""
    w, h = 512, 512
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    colors = [
        (TEAL[0], TEAL[1], TEAL[2], 80),
        (MAGENTA[0], MAGENTA[1], MAGENTA[2], 60),
        (GOLD[0], GOLD[1], GOLD[2], 70),
        (100, 50, 200, 50),
        (50, 150, 200, 60),
        (200, 100, 50, 50),
    ]

    for _ in range(random.randint(3, 8)):
        cx, cy = random.randint(0, w), random.randint(0, h)
        color = random.choice(colors)
        for r in range(random.randint(40, 100), 0, -3):
            alpha = int(color[3] * (r / 100))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color[:3], alpha))

    # Pooling edges
    for _ in range(random.randint(20, 40)):
        px, py = random.randint(0, w), random.randint(0, h)
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(*random.choice(colors)[:3], 30))

    save(img.convert('RGB'), f"watercolor_bleed_{i:02d}.png")


# ========== DATAMOSH GLITCH MAPS (10) ==========
def generate_glitch(i):
    """Generate datamosh glitch distortion map textures."""
    w, h = 512, 512
    img = new_img((w, h))
    draw = ImageDraw.Draw(img)

    # Pixel sorting bars
    for _ in range(random.randint(20, 50)):
        y = random.randint(0, h)
        height = random.randint(2, 20)
        x1 = random.randint(0, w // 2)
        x2 = x1 + random.randint(50, 200)
        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        draw.rectangle([(x1, y), (min(x2, w), y + height)], fill=color)

    # Channel shift lines
    for _ in range(random.randint(10, 30)):
        y = random.randint(0, h)
        draw.line([(0, y), (w, y)], fill=(random.randint(0, 255), 0, 0), width=1)
        draw.line([(random.randint(-20, 20), y + 1), (w + random.randint(-20, 20), y + 1)], fill=(0, random.randint(0, 255), 0), width=1)
        draw.line([(random.randint(-10, 10), y + 2), (w + random.randint(-10, 10), y + 2)], fill=(0, 0, random.randint(0, 255)), width=1)

    save(img, f"datamosh_glitch_{i:02d}.png")


if __name__ == "__main__":
    print("Generating textures...")

    for i in range(10):
        generate_newspaper(i)
    print("  Newspaper clippings: 10")

    for i in range(15):
        generate_stained_glass(i)
    print("  Stained glass / Obsidian: 15")

    for i in range(10):
        generate_kintsugi(i)
    print("  Kintsugi gold overlays: 10")

    for i in range(20):
        generate_embroidery(i)
    print("  Embroidery / Beading: 20")

    for i in range(10):
        generate_botanical(i)
    print("  Botanical elements: 10")

    for i in range(10):
        generate_watercolor(i)
    print("  Watercolor bleeds: 10")

    for i in range(10):
        generate_glitch(i)
    print("  Datamosh glitch maps: 10")

    total = len(os.listdir(OUT_DIR))
    print(f"\nDone! {total} textures generated in {OUT_DIR}/")
