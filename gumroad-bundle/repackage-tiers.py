#!/usr/bin/env python3
"""Repackage tier ZIPs with new covers + gallery images"""

import zipfile, os, glob, random

base = "/home/wildfiremelody/lunar-myth-kintsugi-bible/gumroad-bundle"

# Clean old zips
for f in glob.glob(f"{base}/tier-zips/*.zip"):
    os.remove(f)
    print(f"Removed old: {os.path.basename(f)}")

random.seed(42)

all_prompts = sorted(glob.glob(f"{base}/prompts/*.txt"))
all_textures = sorted(glob.glob(f"{base}/textures/*"))
all_gallery = sorted(glob.glob(f"{base}/gallery/*.jpg"))

os.makedirs(f"{base}/tier-zips", exist_ok=True)

# Seed Tier ($37): covers, quickstart, 1 prompt pack, 5 textures, 5 gallery
with zipfile.ZipFile(f"{base}/tier-zips/lunar-myth-kintsugi-bible-seed.zip", 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in glob.glob(f"{base}/covers/*"):
        zf.write(f, f"covers/{os.path.basename(f)}")
    zf.write(f"{base}/pdfs/README_Quickstart.pdf", "pdfs/README_Quickstart.pdf")
    if all_prompts:
        zf.write(all_prompts[0], f"prompts/{os.path.basename(all_prompts[0])}")
    for f in random.sample(all_textures, min(5, len(all_textures))):
        zf.write(f, f"textures/{os.path.basename(f)}")
    for f in random.sample(all_gallery, min(5, len(all_gallery))):
        zf.write(f, f"gallery/{os.path.basename(f)}")

seed_size = os.path.getsize(f"{base}/tier-zips/lunar-myth-kintsugi-bible-seed.zip")
print(f"Seed tier: {seed_size/1024/1024:.2f} MB")

# Full Moon Tier ($67): Everything except LoRA notebook
with zipfile.ZipFile(f"{base}/tier-zips/lunar-myth-kintsugi-bible-fullmoon.zip", 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in glob.glob(f"{base}/covers/*"):
        zf.write(f, f"covers/{os.path.basename(f)}")
    for f in glob.glob(f"{base}/pdfs/*.pdf"):
        zf.write(f, f"pdfs/{os.path.basename(f)}")
    for f in all_prompts:
        zf.write(f, f"prompts/{os.path.basename(f)}")
    for f in all_textures:
        zf.write(f, f"textures/{os.path.basename(f)}")
    for f in all_gallery:
        zf.write(f, f"gallery/{os.path.basename(f)}")
    for f in glob.glob(f"{base}/workflows/*.json"):
        zf.write(f, f"workflows/{os.path.basename(f)}")

fullmoon_size = os.path.getsize(f"{base}/tier-zips/lunar-myth-kintsugi-bible-fullmoon.zip")
print(f"Full Moon tier: {fullmoon_size/1024/1024:.2f} MB")

# Celestial Tier ($127): Everything including LoRA notebook
with zipfile.ZipFile(f"{base}/tier-zips/lunar-myth-kintsugi-bible-celestial.zip", 'w', zipfile.ZIP_DEFLATED) as zf:
    for f in glob.glob(f"{base}/covers/*"):
        zf.write(f, f"covers/{os.path.basename(f)}")
    for f in glob.glob(f"{base}/pdfs/*.pdf"):
        zf.write(f, f"pdfs/{os.path.basename(f)}")
    for f in all_prompts:
        zf.write(f, f"prompts/{os.path.basename(f)}")
    for f in all_textures:
        zf.write(f, f"textures/{os.path.basename(f)}")
    for f in all_gallery:
        zf.write(f, f"gallery/{os.path.basename(f)}")
    for f in glob.glob(f"{base}/workflows/*.json"):
        zf.write(f, f"workflows/{os.path.basename(f)}")
    zf.write(f"{base}/Kohya_SS_LoRA_Training.ipynb", "Kohya_SS_LoRA_Training.ipynb")

celestial_size = os.path.getsize(f"{base}/tier-zips/lunar-myth-kintsugi-bible-celestial.zip")
print(f"Celestial tier: {celestial_size/1024/1024:.2f} MB")

print("\nAll tiers repackaged!")
