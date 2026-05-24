#!/usr/bin/env python3
"""Convert markdown sections to styled PDFs using weasyprint."""

import markdown
import os
from weasyprint import HTML, CSS

CSS_STYLES = """
@page {
    size: A4;
    margin: 2.5cm;
    @bottom-center {
        content: "Lunar Myth Kintsugi Bible — Jennipher Troup — Page " counter(page);
        font-size: 8pt;
        color: #888;
    }
}
body {
    font-family: Georgia, "Times New Roman", serif;
    font-size: 11pt;
    line-height: 1.7;
    color: #333;
    background: #fff;
}
h1 {
    font-family: Georgia, serif;
    font-size: 24pt;
    color: #1a1a1a;
    border-bottom: 2px solid #D4AF37;
    padding-bottom: 0.3em;
    margin-top: 0;
}
h2 {
    font-family: Georgia, serif;
    font-size: 16pt;
    color: #1a1a1a;
    margin-top: 1.5em;
    border-left: 4px solid #D4AF37;
    padding-left: 0.5em;
}
h3 {
    font-family: Georgia, serif;
    font-size: 13pt;
    color: #333;
    margin-top: 1.2em;
}
h4 {
    font-size: 11pt;
    font-weight: bold;
    color: #444;
    margin-top: 1em;
}
p {
    margin: 0.8em 0;
    text-align: justify;
}
ul, ol {
    margin: 0.5em 0;
    padding-left: 1.5em;
}
li {
    margin: 0.3em 0;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    font-size: 10pt;
}
th, td {
    border: 1px solid #ccc;
    padding: 6px 10px;
    text-align: left;
}
th {
    background: #f5f5f5;
    font-weight: bold;
}
code {
    font-family: "Courier New", monospace;
    background: #f5f5f5;
    padding: 2px 5px;
    font-size: 9pt;
}
pre {
    background: #f5f5f5;
    padding: 12px;
    border-left: 3px solid #D4AF37;
    overflow-x: auto;
    font-size: 8.5pt;
    line-height: 1.4;
}
blockquote {
    border-left: 3px solid #D4AF37;
    margin: 1em 0;
    padding-left: 1em;
    color: #555;
    font-style: italic;
}
hr {
    border: none;
    border-top: 1px solid #D4AF37;
    margin: 2em 0;
}
.cover-page {
    text-align: center;
    padding-top: 30%;
}
.cover-page h1 {
    border: none;
    font-size: 32pt;
    color: #1a1a1a;
}
.cover-page .subtitle {
    font-size: 14pt;
    color: #666;
    margin-top: 1em;
}
.cover-page .author {
    font-size: 12pt;
    color: #888;
    margin-top: 2em;
}
"""


def md_to_pdf(md_path, pdf_path, title=None, subtitle=None, author=None):
    with open(md_path, 'r') as f:
        md_text = f.read()

    # Add cover page if title provided
    cover = ""
    if title:
        cover = f"""
<div class="cover-page">
<h1>{title}</h1>
<div class="subtitle">{subtitle or ''}</div>
<div class="author">{author or 'By Jennipher Troup'}</div>
</div>
<div style="page-break-after: always;"></div>
"""

    html_body = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{title or 'Lunar Myth Kintsugi Bible'}</title>
</head>
<body>
{cover}
{html_body}
</body>
</html>"""

    HTML(string=html).write_pdf(pdf_path, stylesheets=[CSS(string=CSS_STYLES)])
    print(f"  PDF: {pdf_path}")


if __name__ == "__main__":
    sections_dir = "../sections"
    out_dir = "pdfs"
    os.makedirs(out_dir, exist_ok=True)

    print("Converting sections to PDF...")

    # Core Bible (Seed tier)
    md_to_pdf(
        os.path.join(sections_dir, "03-material-texture-hierarchy.md"),
        os.path.join(out_dir, "Section_03_Material_Texture_Hierarchy.pdf"),
        title="Material & Texture Hierarchy",
        subtitle="The Physical & Digital Alchemy of Repair"
    )
    md_to_pdf(
        os.path.join(sections_dir, "06-lunarpunk-fashion.md"),
        os.path.join(out_dir, "Section_06_Lunarpunk_Fashion.pdf"),
        title="Lunarpunk Fashion Design",
        subtitle="Wearable Mythpunk: From Canvas to Catwalk"
    )

    # Advanced guides
    md_to_pdf(
        os.path.join(sections_dir, "10-lora-training-guide.md"),
        os.path.join(out_dir, "Section_10_LoRA_Training_Guide.pdf"),
        title="LoRA Training Guide",
        subtitle="Forging Your Own Lunar Myth Model"
    )
    md_to_pdf(
        os.path.join(sections_dir, "11-tier-license-commercial.md"),
        os.path.join(out_dir, "Section_11_Tier_License_Sales.pdf"),
        title="Tier Assets, License & Sales",
        subtitle="From Creation to Commerce"
    )

    # Combined comprehensive bible
    print("\nBuilding comprehensive bible...")
    combined_md = ""
    for section in ["03-material-texture-hierarchy.md", "06-lunarpunk-fashion.md", "10-lora-training-guide.md", "11-tier-license-commercial.md"]:
        with open(os.path.join(sections_dir, section), 'r') as f:
            combined_md += f"\n\n---\n\n{f.read()}"

    with open("/tmp/combined_bible.md", 'w') as f:
        f.write(combined_md)

    md_to_pdf(
        "/tmp/combined_bible.md",
        os.path.join(out_dir, "Lunar_Myth_Kintsugi_Bible_Complete.pdf"),
        title="LUNAR MYTH KINTSUGI BIBLE",
        subtitle="357+ Hyper-Tactile Mythpunk Prompts & Complete Collage System",
        author="By Jennipher Troup"
    )

    print(f"\nDone! PDFs saved to {out_dir}/")
