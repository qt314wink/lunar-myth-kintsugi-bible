# Section 10: LoRA Training Guide — Forging Your Own Lunar Myth Model

*Pages 53–72 — Train a Custom AI That Understands Your Vision*

---

## The Power of a Personal LoRA

Imagine an AI that *knows* your style before you speak a word. A model that understands the weight of embroidery, the glow of kintsugi, the density of botanical growth, and the melancholy of moonlight. That is what a custom LoRA (Low-Rank Adaptation) gives you.

A LoRA is a small, lightweight neural network attachment (typically 50–200MB) that fine-tunes a base model (like SDXL or Flux.1) to recognize and reproduce a specific visual style. Unlike full model training (which requires terabytes of data and weeks of GPU time), LoRA training is accessible, affordable, and astoundingly effective.

**Why Train a Lunar Myth LoRA?**
- **Consistency:** Generate 100 images and they all feel like *your* work.
- **Efficiency:** Shorten prompts from 200 words to 50 — the LoRA knows the rest.
- **Commercial Edge:** Offer clients "trained on my exclusive style" — a genuine differentiator.
- **Evolution:** Retrain as your style evolves. Your LoRA grows with you.

---

## Chapter 1: Understanding LoRA Architecture

### What Is LoRA, Really?

LoRA works by injecting small, trainable matrices into the attention layers of a diffusion model. Instead of updating billions of parameters, LoRA updates only millions — making it fast, lightweight, and portable.

**Key Concepts:**

| Term | Explanation | Why It Matters |
|------|-------------|--------------|
| **Rank (Dim)** | The size of the injected matrices. Higher = more capacity to learn. | 32–64 is ideal for complex styles like Lunar Myth. |
| **Alpha** | Controls how strongly the LoRA influences the base model. | Typically half the rank (rank 48 → alpha 24). |
| **Trigger Word** | A special token you add to prompts to activate the LoRA. | Use `lunar myth kintsugi botanist` — unique and memorable. |
| **Base Model** | The foundation model the LoRA attaches to. | SDXL 1.0 or Flux.1-dev for best results. |
| **Dataset** | The images you train on. | 20–100 high-quality, consistent images. |
| **Steps/Epochs** | How many times the model sees your data. | 800–2,000 steps for style LoRAs. |

**The Math (Simplified):**
Think of the base model as a vast library of all possible images. A LoRA is a specialized index that says: *"When you see the word 'lunar myth,' prioritize these specific combinations of shapes, colors, and textures."* It doesn't rewrite the library — it adds a powerful bookmark system.

---

## Chapter 2: Dataset Curation — The Foundation of Quality

### The Golden Rule: Garbage In, Garbage Out

Your LoRA is only as good as the images you train it on. A sloppy dataset produces sloppy results. A curated, consistent dataset produces magic.

**Dataset Size Recommendations:**
- **Minimum:** 20 images (if they are extremely consistent)
- **Sweet Spot:** 50–80 images (variety + consistency)
- **Maximum:** 100–150 images (beyond this, diminishing returns for style LoRAs)

**Image Selection Criteria:**

1. **Style Consistency:** Every image should clearly belong to the Lunar Myth aesthetic. Do not mix in unrelated styles.
2. **Variety of Subject:** Include different poses, angles, and compositions — but keep the *style* identical.
3. **Resolution:** 1024×1024 for SDXL. 768×1344 for vertical full-body shots (crop to multiple of 64).
4. **Quality Over Quantity:** One perfect image is worth ten mediocre ones.

**Recommended Dataset Composition:**

| Category | Count | Purpose |
|----------|-------|---------|
| **Full-body heroes** | 15–20 | Establish figure style, proportions, poses |
| **Close-up portraits** | 10–15 | Train face detail, embroidery, kintsugi on skin |
| **Torso/mid-shots** | 10–15 | Train botanical placement, garment detail |
| **Hand/arm detail** | 5–8 | Train embroidery, beading, kintsugi on limbs |
| **Botanical close-ups** | 5–8 | Train plant rendering independent of figure |
| **Texture studies** | 5–8 | Train newspaper, watercolor, mosaic, obsidian |
| **Fashion/garment focus** | 5–8 | Train clothing construction and draping |

**Generating Your Dataset:**

Use the **Lunar Myth Prompt Library** (Section 5) to generate your training images:

1. Select 50–80 prompts from different moods.
2. Generate at high resolution (1024×1024 or higher).
3. Upscale using 4x-UltraSharp or similar upscaler.
4. Manually review and curate. Delete any image that:
   - Has deformed anatomy
   - Lacks clear Lunar Myth elements
   - Is blurry or low-detail
   - Has unwanted text/watermarks
5. Optional but recommended: Manually refine 10–20 images in Photoshop — strengthen kintsugi lines, enhance embroidery, deepen colors. These "hero images" anchor the LoRA's quality ceiling.

**Captioning Your Images:**

Every image needs a text description (caption). The caption teaches the LoRA *what* is in each image.

**Captioning Strategy:**
- Use the **full prompt** as the caption for the first 10–15 images. This teaches the complete style.
- For remaining images, use **shorter captions** focusing on what makes that image unique: `lunar myth kintsugi botanist full-body female, defiant rebellion pose, thorned shadow roses, heavy gold embroidery`
- Always include the **trigger word** in every caption: `lunar myth kintsugi botanist`
- Use **automatic captioning** (BLIP, WD14 Tagger) for speed, then manually edit for accuracy.

**Example Caption File Structure:**
```
dataset/
├── 0001.png
├── 0001.txt  <-- "lunar myth kintsugi botanist full-body female primordial goddess standing powerfully, newspaper collage with watercolor bleed, stained-glass mosaic and obsidian with golden kintsugi, regenerative moonflowers and iridescent ivy, heavy embroidery and beading, datamosh glitch, lunarpunk moonlight, vibrant jewel tones, chromatic aberration, ultra-detailed mixed-media collage"
├── 0002.png
├── 0002.txt
└── ...
```

---

## Chapter 3: Training with Kohya SS — The Complete Guide

### Why Kohya SS?

Kohya SS is the industry-standard GUI and training framework for Stable Diffusion LoRAs. It is powerful, well-documented, and supports all the advanced features you need: Prodigy optimizer, bucketing, latent caching, and more.

**Two Ways to Use Kohya SS:**
1. **Local installation** (requires 12GB+ VRAM, preferably RTX 3060 or better)
2. **Google Colab** (cloud GPU, accessible to everyone — recommended for beginners)

---

### Method A: Google Colab Training (Recommended)

This is the most accessible method. You need a Google account and Google Drive.

#### Step 1: Prepare Your Dataset in Google Drive

1. Create a folder in Google Drive: `MyDrive/LunarMyth_Dataset/`
2. Inside, create a folder with your images and captions: `MyDrive/LunarMyth_Dataset/dataset/`
3. Upload all your `.png` images and `.txt` caption files.
4. Ensure every image has a matching caption file with the same name.

#### Step 2: Open a Colab Notebook

Use the Kohya SS Colab notebook (search for "kohya-ss colab" or use a community-maintained version).

#### Step 3: Run the Setup Cells

```python
# === CELL 1: Mount Google Drive ===
from google.colab import drive
drive.mount('/content/drive')

# === CELL 2: Install Dependencies ===
!pip install -q torch==2.1.2+cu121 torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
!pip install -q xformers==0.0.23.post1
!git clone https://github.com/bmaltais/kohya_ss.git
%cd kohya_ss
!pip install -q -r requirements.txt

# === CELL 3: Verify Installation ===
!python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

#### Step 4: Configure Training Parameters

```python
# === CELL 4: Training Configuration ===
import os

# Paths
DATASET_DIR = "/content/drive/MyDrive/LunarMyth_Dataset/dataset"
OUTPUT_DIR = "/content/drive/MyDrive/LunarMyth_Output"
MODEL_DIR = "/content/drive/MyDrive/LunarMyth_Models"
BASE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

# Create output directories
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# Training Parameters (Optimized for Lunar Myth Style)
TRAINING_CONFIG = {
    "pretrained_model_name_or_path": BASE_MODEL,
    "train_data_dir": DATASET_DIR,
    "output_dir": OUTPUT_DIR,
    "output_name": "lunar_myth_kintsugi_botanist_v1",
    
    # Network Architecture
    "network_module": "networks.lora",
    "network_dim": 48,           # Rank — high enough for complex style
    "network_alpha": 24,         # Alpha — half of rank
    
    # Training Length
    "max_train_steps": 1200,     # Adjust based on dataset size
    "save_every_n_steps": 200,   # Save checkpoints frequently
    
    # Learning & Optimization
    "learning_rate": 1.0,        # Prodigy auto-adjusts from this
    "optimizer_type": "Prodigy",
    "optimizer_args": [
        "decouple=True",
        "weight_decay=0.01",
        "d0=0.0001",
        "use_bias_correction=True",
        "safeguard_warmup=True",
        "betas=0.9,0.99",
        "d_coef=2.0"
    ],
    "lr_scheduler": "constant",
    
    # Training Efficiency
    "resolution": "1024,1024",
    "train_batch_size": 1,       # Increase to 2 if you have 16GB+ VRAM
    "mixed_precision": "bf16",
    "save_precision": "bf16",
    "cache_latents": True,
    "cache_latents_to_disk": True,
    "gradient_checkpointing": True,  # Saves VRAM
    
    # Caption & Bucketing
    "caption_extension": ".txt",
    "shuffle_caption": True,
    "keep_tokens": 1,            # Keep trigger word in position
    "enable_bucket": True,
    "min_bucket_reso": 640,
    "max_bucket_reso": 1536,
    
    # Regularization (optional — helps prevent overfitting)
    "reg_data_dir": "",          # Add regularization images if desired
    
    # Logging
    "logging_dir": f"{OUTPUT_DIR}/logs",
    "log_with": "tensorboard",
    
    # Model Saving
    "save_model_as": "safetensors",
    "clip_skip": 2,              # SDXL default
}

# Print config for verification
import json
print(json.dumps(TRAINING_CONFIG, indent=2))
```

#### Step 5: Launch Training

```python
# === CELL 5: Start Training ===
!accelerate launch \
  --mixed_precision="bf16" \
  --num_processes=1 \
  --num_machines=1 \
  --dynamo_backend="no" \
  /content/kohya_ss/sdxl_train_network.py \
  --pretrained_model_name_or_path="{TRAINING_CONFIG['pretrained_model_name_or_path']}" \
  --train_data_dir="{TRAINING_CONFIG['train_data_dir']}" \
  --output_dir="{TRAINING_CONFIG['output_dir']}" \
  --output_name="{TRAINING_CONFIG['output_name']}" \
  --network_module="{TRAINING_CONFIG['network_module']}" \
  --network_dim={TRAINING_CONFIG['network_dim']} \
  --network_alpha={TRAINING_CONFIG['network_alpha']} \
  --max_train_steps={TRAINING_CONFIG['max_train_steps']} \
  --save_every_n_steps={TRAINING_CONFIG['save_every_n_steps']} \
  --learning_rate={TRAINING_CONFIG['learning_rate']} \
  --optimizer_type="{TRAINING_CONFIG['optimizer_type']}" \
  --optimizer_args {','.join(TRAINING_CONFIG['optimizer_args'])} \
  --lr_scheduler="{TRAINING_CONFIG['lr_scheduler']}" \
  --resolution="{TRAINING_CONFIG['resolution']}" \
  --train_batch_size={TRAINING_CONFIG['train_batch_size']} \
  --mixed_precision="{TRAINING_CONFIG['mixed_precision']}" \
  --save_precision="{TRAINING_CONFIG['save_precision']}" \
  --cache_latents \
  --cache_latents_to_disk \
  --gradient_checkpointing \
  --caption_extension="{TRAINING_CONFIG['caption_extension']}" \
  --shuffle_caption \
  --keep_tokens={TRAINING_CONFIG['keep_tokens']} \
  --enable_bucket \
  --min_bucket_reso={TRAINING_CONFIG['min_bucket_reso']} \
  --max_bucket_reso={TRAINING_CONFIG['max_bucket_reso']} \
  --logging_dir="{TRAINING_CONFIG['logging_dir']}" \
  --log_with="{TRAINING_CONFIG['log_with']}" \
  --save_model_as="{TRAINING_CONFIG['save_model_as']}" \
  --clip_skip={TRAINING_CONFIG['clip_skip']}
```

#### Step 6: Monitor & Evaluate

```python
# === CELL 6: List Output Files ===
import os
output_files = sorted(os.listdir(OUTPUT_DIR))
for f in output_files:
    size_mb = os.path.getsize(os.path.join(OUTPUT_DIR, f)) / (1024*1024)
    print(f"{f} ({size_mb:.1f} MB)")
```

**Training Time Estimates:**
- 50 images × 1200 steps on A100: ~20–30 minutes
- 50 images × 1200 steps on T4 (free Colab): ~45–90 minutes

---

### Method B: Local Training (Advanced)

**Hardware Requirements:**
- GPU: RTX 3060 12GB minimum (RTX 4090 24GB recommended)
- RAM: 32GB recommended
- Storage: 50GB free space

**Installation:**
```bash
git clone https://github.com/bmaltais/kohya_ss.git
cd kohya_ss
./setup.sh  # Linux/Mac
setup.bat   # Windows
```

**GUI Usage:**
1. Launch the GUI: `python kohya_gui.py`
2. Navigate to the "LoRA" training tab.
3. Fill in the same parameters from the Colab configuration above.
4. Click "Start Training."

---

## Chapter 4: Prodigy Optimizer Deep Dive

### Why Prodigy?

Prodigy is an adaptive optimizer that automatically adjusts the learning rate during training. Unlike AdamW (which requires you to guess the perfect learning rate), Prodigy starts high and dynamically finds the optimal rate for your specific dataset.

**Prodigy Settings for Lunar Myth LoRA:**

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `decouple=True` | Required | Separates weight decay from learning rate adaptation |
| `weight_decay=0.01` | Light regularization | Prevents overfitting without crushing the style |
| `d0=0.0001` | Initial LR estimate | Conservative starting point for style LoRAs |
| `use_bias_correction=True` | Recommended | Improves early training stability |
| `safeguard_warmup=True` | Recommended | Prevents catastrophic early steps |
| `betas=0.9,0.99` | Standard | Momentum parameters — keep default |
| `d_coef=2.0` | Aggressive adaptation | Higher = faster adaptation to dataset quirks |

**Reading the Logs:**
Watch for these indicators during training:
- **Loss decreasing steadily** → Good. The model is learning.
- **Loss oscillating wildly** → Learning rate may be too high. Lower `d0` to `0.00005`.
- **Loss plateauing early** → Increase steps or dataset diversity.
- **Loss increasing after ~800 steps** → Overfitting. Stop training or add regularization.

---

## Chapter 5: Testing & Refining Your LoRA

### The Evaluation Process

Training is only half the battle. A LoRA must be tested rigorously before it enters your production workflow.

**Test Prompt Matrix:**

Test your LoRA with a grid of prompts covering:
1. **Trigger word only:** `lunar myth kintsugi botanist full-body female` — Does it produce recognizable style?
2. **Minimal prompt:** `lunar myth kintsugi botanist goddess` — Does it fill in details?
3. **Mood variations:** Add `luminous wonder`, `defiant rebellion`, `melancholic reverie` — Does mood translate?
4. **Without trigger word:** `full-body female goddess, embroidery, kintsugi` — Does the LoRA activate implicitly? (It shouldn't — if it does, it's overfitted.)
5. **Negative tests:** `anime style, cartoon, 3d render` with trigger word — Does the LoRA resist corruption?

**Strength Testing:**
Test at multiple LoRA strengths:
- **0.3–0.5** — Subtle influence, base model dominates
- **0.6–0.8** — Balanced, recommended range
- **0.9–1.2** — Strong influence, may overpower base model
- **1.3+** — Extreme, likely artifacts. Use only for specific effects.

**Recommended workflow:** Start at 0.7. Adjust up for more style intensity, down for more prompt adherence.

---

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| **Faces look same in every image** | Overfitting to dataset faces | Increase dataset diversity. Add face-less images. Use lower network_dim (32). |
| **Style is weak/unclear** | Underfitting | Increase steps (1500+). Increase network_dim (64). Improve caption quality. |
| **Colors are muddy** | Learning rate too high | Lower `d0` to `0.00005`. Reduce `d_coef` to `1.0`. |
| **Anatomy is distorted** | Too much emphasis on style over structure | Add more full-body images with good anatomy. Use `min_snr_gamma=5`. |
| **Kintsugi lines are missing** | Not enough close-up detail in dataset | Add 10+ texture studies showing kintsugi clearly. |
| **Botanicals don't glow** | LoRA not capturing luminescence | Add glow-heavy images. Caption specifically: `bioluminescent botanicals, glowing moonflowers`. |
| **Embroidery looks flat** | Tactility not trained | Add extreme close-ups of embroidery. Use `network_dim=64` for finer detail. |

---

### Iterative Refinement

Your first LoRA will not be perfect. Expect to train 3–5 versions before you find the sweet spot.

**Versioning Strategy:**
- **v1:** Baseline. Test the concept.
- **v2:** Adjust based on v1 failures. Usually dataset or parameter tweaks.
- **v3:** Fine-tuning. Minor adjustments for consistency.
- **v4+:** Specialized variants (e.g., "Lunar Myth — Fashion Focus" or "Lunar Myth — Portrait Focus")

**Dataset Iteration:**
After each training run, generate 20 test images. Identify the worst 5. Ask: *What is missing?* Generate new training images that specifically address the gap. Retrain.

---

## Chapter 6: Advanced LoRA Techniques

### Multi-LoRA Stacking

Combine multiple LoRAs for complex results:

```
Base Model: SDXL 1.0
+ Lunar Myth Kintsugi LoRA (0.7) — Style foundation
+ Embroidery Detail LoRA (0.4) — Extra tactile richness
+ Botanical Glow LoRA (0.3) — Enhanced luminescence
+ Pose Control LoRA (0.5) — Specific body positioning
```

**Tips for Stacking:**
- Total strength should rarely exceed 1.5 combined.
- Stack from broadest (style) to most specific (detail).
- Test each LoRA individually before combining.

### LoRA + ControlNet + IP-Adapter

The ultimate control stack:

1. **IP-Adapter** (0.8) — Transfer the overall Lunar Myth aesthetic from a reference image.
2. **ControlNet Canny** (0.7) — Preserve collage edge structure and figure outline.
3. **ControlNet Depth** (0.6) — Maintain 3D tactility and spatial relationships.
4. **Lunar Myth LoRA** (0.7) — Inject the trained style.
5. **Text Prompt** — Direct the mood, botanicals, and composition.

### LoRA for Animation (AnimateDiff)

Train a motion LoRA to animate your Lunar Myth style:
- Use AnimateDiff Evolved in ComfyUI.
- Combine with your static style LoRA.
- Add motion modules (mm_sdxl_v10_beta) for smooth movement.
- Use dynamic prompt scheduling to animate botanical growth or kintsugi glow pulsing.

---

## Chapter 7: Packaging & Selling Your LoRA

### The Celestial Tier Deliverable

Your custom LoRA is a premium product. Treat it as such.

**File Package:**
```
lunar_myth_kintsugi_botanist_v3/
├── lunar_myth_kintsugi_botanist_v3.safetensors    (The LoRA file)
├── README.md                                       (Usage guide)
├── TRIGGER_WORDS.txt                               (Quick reference)
├── SAMPLE_PROMPTS.txt                              (10 tested prompts)
├── SAMPLE_IMAGES/                                  (20 showcase images)
│   ├── full_body_01.png
│   ├── portrait_02.png
│   └── ...
├── TRAINING_NOTES.md                               (For advanced users)
└── LICENSE.txt                                     (Commercial terms)
```

**README.md Template:**
```markdown
# Lunar Myth Kintsugi Botanist LoRA v3

## Trigger Words
- `lunar myth kintsugi botanist` (primary)
- `heavy embroidery and beading` (tactility boost)
- `regenerative botanical overgrowth` (botanical density)

## Recommended Settings
- Base Model: SDXL 1.0 or Flux.1-dev
- LoRA Strength: 0.6–0.9
- Resolution: 1024×1024 or 768×1344
- Sampler: DPM++ 2M Karras, 30–50 steps

## Sample Prompt
"lunar myth kintsugi botanist full-body female primordial goddess, luminous wonder mood, newspaper collage with watercolor bleed, stained-glass mosaic and obsidian with golden kintsugi, regenerative moonflowers and iridescent ivy, heavy embroidery and beading, datamosh glitch, lunarpunk moonlight, vibrant jewel tones, chromatic aberration --ar 3:4 --stylize 250"

## Commercial Use
This LoRA is provided for personal and commercial use. You may sell art generated with it. You may not resell or redistribute the LoRA file itself.
```

---

*End of Section 10*
