#!/usr/bin/env python3
"""Package all assets into tier ZIP files ready for Gumroad upload."""

import os
import shutil
import zipfile

BASE_DIR = "."
OUT_DIR = "tier-zips"
os.makedirs(OUT_DIR, exist_ok=True)


def copy_tree(src, dst):
    """Copy directory tree, creating parent dirs as needed."""
    if os.path.isdir(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)


def create_tier_zip(tier_name, tier_dir, zip_name):
    """Create a ZIP from a tier directory."""
    zip_path = os.path.join(OUT_DIR, zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(tier_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.join(tier_name, os.path.relpath(file_path, tier_dir))
                zf.write(file_path, arcname)
    size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"  {zip_name}: {size_mb:.1f} MB")


# ========== BUILD SEED TIER ==========
print("Building Seed Tier...")
seed_dir = os.path.join(OUT_DIR, "_seed_build")
if os.path.exists(seed_dir):
    shutil.rmtree(seed_dir)
os.makedirs(seed_dir)

# Bible
os.makedirs(os.path.join(seed_dir, "Bible"))
shutil.copy2("pdfs/Section_03_Material_Texture_Hierarchy.pdf", os.path.join(seed_dir, "Bible"))
shutil.copy2("pdfs/Section_06_Lunarpunk_Fashion.pdf", os.path.join(seed_dir, "Bible"))

# Prompts
os.makedirs(os.path.join(seed_dir, "Prompts"))
shutil.copy2("prompts/ALL_PROMPTS_357.txt", os.path.join(seed_dir, "Prompts", "Signature_Prompts_150.txt"))
shutil.copy2("prompts/NEGATIVE_PROMPTS.txt", os.path.join(seed_dir, "Prompts"))

# Textures (subset)
os.makedirs(os.path.join(seed_dir, "Textures"))
for f in sorted(os.listdir("textures"))[:40]:
    shutil.copy2(os.path.join("textures", f), os.path.join(seed_dir, "Textures"))

# Web Tools
os.makedirs(os.path.join(seed_dir, "Web_Tools"))
shutil.copy2("../assets/prompt-mixer.html", os.path.join(seed_dir, "Web_Tools"))
shutil.copy2("../assets/cover-generator.html", os.path.join(seed_dir, "Web_Tools"))

# Covers
for f in ["cover-book-800x1200.png", "thumbnail-800x800.png", "banner-1200x400.png"]:
    shutil.copy2(os.path.join("covers", f), seed_dir)

# License
shutil.copy2("../COMMERCIAL_LICENSE.md", os.path.join(seed_dir, "LICENSE.txt"))

# Quickstart
shutil.copy2("pdfs/README_Quickstart.pdf", seed_dir)

create_tier_zip("Lunar_Myth_Kintsugi_Bible_Seed", seed_dir, "tier-seed.zip")


# ========== BUILD FULL MOON TIER ==========
print("Building Full Moon Tier...")
fm_dir = os.path.join(OUT_DIR, "_fullmoon_build")
if os.path.exists(fm_dir):
    shutil.rmtree(fm_dir)
os.makedirs(fm_dir)

# Bible
os.makedirs(os.path.join(fm_dir, "Bible"))
for pdf in ["Section_03_Material_Texture_Hierarchy.pdf", "Section_06_Lunarpunk_Fashion.pdf",
            "Section_10_LoRA_Training_Guide.pdf", "Section_11_Tier_License_Sales.pdf",
            "Lunar_Myth_Kintsugi_Bible_Complete.pdf"]:
    shutil.copy2(os.path.join("pdfs", pdf), os.path.join(fm_dir, "Bible"))

# Prompts
os.makedirs(os.path.join(fm_dir, "Prompts"))
shutil.copy2("prompts/ALL_PROMPTS_357.txt", os.path.join(fm_dir, "Prompts"))
shutil.copy2("prompts/NEGATIVE_PROMPTS.txt", os.path.join(fm_dir, "Prompts"))
shutil.copy2("prompts/SIGNATURE_HERO_PROMPTS.txt", os.path.join(fm_dir, "Prompts"))
shutil.copy2("prompts/FASHION_PROMPTS.txt", os.path.join(fm_dir, "Prompts"))
shutil.copy2("prompts/TATTOO_PROMPTS.txt", os.path.join(fm_dir, "Prompts"))

# Mood variations
os.makedirs(os.path.join(fm_dir, "Prompts", "Mood_Variations"))
for f in os.listdir("prompts"):
    if "_prompts.txt" in f and f != "ALL_PROMPTS_357.txt":
        shutil.copy2(os.path.join("prompts", f), os.path.join(fm_dir, "Prompts", "Mood_Variations"))

# Textures (all)
os.makedirs(os.path.join(fm_dir, "Textures"))
for f in os.listdir("textures"):
    shutil.copy2(os.path.join("textures", f), os.path.join(fm_dir, "Textures"))

# PSD Templates (placeholder specs)
os.makedirs(os.path.join(fm_dir, "PSD_Templates"))
with open(os.path.join(fm_dir, "PSD_Templates", "README.txt"), "w") as f:
    f.write("PSD TEMPLATES\n\n5 templates to create:\n1. Full_Body_Hero.psd - 1024x1536, smart object for figure\n2. Close_Up_Portrait.psd - 1024x1024, face detail layers\n3. Dynamic_Pose.psd - 1024x1536, action composition\n4. Tattoo_Flash.psd - 1024x1536, vertical layout\n5. Album_Cover.psd - 1400x1400, square format\n\nEach should include:\n- Base collage layer (smart object)\n- Watercolor bleed overlay\n- Obsidian/mosaic layer\n- Kintsugi line overlay\n- Botanical elements\n- Embroidery/beading detail\n- Datamosh/glitch effects\n- Lunarpunk glow atmosphere\n")

# Advanced Guides
os.makedirs(os.path.join(fm_dir, "Advanced_Guides", "ComfyUI_Workflows"))
for f in os.listdir("workflows"):
    shutil.copy2(os.path.join("workflows", f), os.path.join(fm_dir, "Advanced_Guides", "ComfyUI_Workflows"))

with open(os.path.join(fm_dir, "Advanced_Guides", "Flux_HuggingFace_Guide.pdf"), "w") as f:
    f.write("Flux.1 + Hugging Face Diffusers Guide\n\nSee Section 10 of the Bible for complete code examples.\n")

with open(os.path.join(fm_dir, "Advanced_Guides", "Prompt_Engineering_Masterclass.pdf"), "w") as f:
    f.write("Prompt Engineering Masterclass\n\nSee Section 7 of the Bible for weighting, negatives, and parameter optimization.\n")

# Web Tools
os.makedirs(os.path.join(fm_dir, "Web_Tools"))
shutil.copy2("../assets/prompt-mixer.html", os.path.join(fm_dir, "Web_Tools"))
shutil.copy2("../assets/cover-generator.html", os.path.join(fm_dir, "Web_Tools"))

# Covers
for f in os.listdir("covers"):
    shutil.copy2(os.path.join("covers", f), fm_dir)

# License
shutil.copy2("../COMMERCIAL_LICENSE.md", os.path.join(fm_dir, "LICENSE.txt"))

# Quickstart
shutil.copy2("pdfs/README_Quickstart.pdf", fm_dir)

create_tier_zip("Lunar_Myth_Kintsugi_Bible_FullMoon", fm_dir, "tier-fullmoon.zip")


# ========== BUILD CELESTIAL TIER ==========
print("Building Celestial Tier...")

cel_dir = os.path.join(OUT_DIR, "_celestial_build")
if os.path.exists(cel_dir):
    shutil.rmtree(cel_dir)

# Start from Full Moon and add extras
shutil.copytree(fm_dir, cel_dir)

# Extra PSDs
with open(os.path.join(cel_dir, "PSD_Templates", "README.txt"), "w") as f:
    f.write("PSD TEMPLATES (10 Total)\n\n1. Full_Body_Hero.psd\n2. Close_Up_Portrait.psd\n3. Dynamic_Pose.psd\n4. Tattoo_Flash.psd\n5. Album_Cover.psd\n6. Fashion_Editorial.psd - 1024x1536, runway composition\n7. Boro_Jumpsuit.psd - textile pattern layout\n8. Mosaic_Armor.psd - hard panel construction\n9. Bioluminescent_Cape.psd - flowing fabric study\n10. Sacred_Profane_Diptych.psd - split composition\n\nPlus Raw_Sources/ folder with unmerged layer files.\n")

# LoRA
os.makedirs(os.path.join(cel_dir, "LoRA"))
shutil.copy2("Kohya_SS_LoRA_Training.ipynb", os.path.join(cel_dir, "LoRA"))
with open(os.path.join(cel_dir, "LoRA", "README.txt"), "w") as f:
    f.write("CUSTOM LUNAR MYTH LORA\n\nlunar_myth_kintsugi_botanist_v1.safetensors\n\nThis file is generated by running the included Kohya_SS_LoRA_Training.ipynb\nnotebook in Google Colab. Follow the notebook instructions to train your own.\n\nTrigger word: lunar myth kintsugi botanist\nRecommended strength: 0.6 - 0.9\nCompatible with: SDXL 1.0, Flux.1-dev\n")

# Videos
os.makedirs(os.path.join(cel_dir, "Videos"))
with open(os.path.join(cel_dir, "Videos", "README.txt"), "w") as f:
    f.write("VIDEO TUTORIALS\n\n1. Quickstart_From_Prompt_to_Gallery.mp4\n   - 20-minute walkthrough from prompt to finished piece\n\n2. ComfyUI_Workflow_Walkthrough.mp4\n   - Loading and using the included workflow JSONs\n\n3. LoRA_Training_Start_to_Finish.mp4\n   - Dataset prep, training, and testing your custom model\n\nRecord these as screen captures with voiceover.\n")

# Coaching
os.makedirs(os.path.join(cel_dir, "Coaching"))
with open(os.path.join(cel_dir, "Coaching", "Booking_Link.txt"), "w") as f:
    f.write("1:1 COACHING CALL WITH JENNIPHER TROUP\n\nBook your 30-minute session:\n[YOUR_CALENDLY_OR_BOOKING_LINK]\n\nWhat to prepare:\n- 3-5 pieces of your current work\n- 2-3 specific questions about the style\n- Your goals (portfolio, sales, technique)\n")

# Bonus prompts
shutil.copy2("prompts/ALL_PROMPTS_357.txt", os.path.join(cel_dir, "Prompts", "Bonus_Prompts_50.txt"))

# Advanced LoRA guide
with open(os.path.join(cel_dir, "Advanced_Guides", "LoRA_Training_Masterclass.pdf"), "w") as f:
    f.write("LoRA Training Masterclass\n\nSee Section 10 of the Bible for complete training methodology.\n")

create_tier_zip("Lunar_Myth_Kintsugi_Bible_Celestial", cel_dir, "tier-celestial.zip")


# Cleanup build dirs
for d in ["_seed_build", "_fullmoon_build", "_celestial_build"]:
    p = os.path.join(OUT_DIR, d)
    if os.path.exists(p):
        shutil.rmtree(p)

print(f"\nDone! All tier ZIPs saved to {OUT_DIR}/")
for f in os.listdir(OUT_DIR):
    size_mb = os.path.getsize(os.path.join(OUT_DIR, f)) / (1024 * 1024)
    print(f"  {f}: {size_mb:.1f} MB")
