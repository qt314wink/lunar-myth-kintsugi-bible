#!/usr/bin/env python3
"""Convert markdown sections to PDFs using fpdf2 with Unicode support."""

import markdown
import os
import re
from fpdf import FPDF


class BiblePDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('DejaVu', '', 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 10, f'Lunar Myth Kintsugi Bible -- Jennipher Troup -- Page {self.page_no()}', align='C')
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


def clean_html_for_fpdf(html):
    html = re.sub(r'<code class="[^"]*">', '<code>', html)
    html = re.sub(r'<pre><code>', '<pre>', html)
    html = re.sub(r'</code></pre>', '</pre>', html)
    html = re.sub(r'<img[^>]*>', '', html)
    html = re.sub(r'<blockquote>\s*<p>', '<blockquote>', html)
    html = re.sub(r'</p>\s*</blockquote>', '</blockquote>', html)
    html = html.replace('\u2014', '--').replace('\u2013', '-')
    return html


def md_to_pdf(md_path, pdf_path, title=None, subtitle=None):
    with open(md_path, 'r') as f:
        md_text = f.read()

    md_text = md_text.replace('\u2014', '--').replace('\u2013', '-')
    html = markdown.markdown(md_text, extensions=['tables', 'fenced_code'])
    html = clean_html_for_fpdf(html)

    pdf = BiblePDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add all font variants
    font_dir = "/usr/share/fonts/truetype/dejavu"
    pdf.add_font('DejaVu', '', f"{font_dir}/DejaVuSans.ttf")
    pdf.add_font('DejaVu', 'B', f"{font_dir}/DejaVuSans-Bold.ttf")
    pdf.add_font('DejaVu', 'I', f"{font_dir}/DejaVuSansMono-Oblique.ttf")
    pdf.add_font('DejaVu', 'BI', f"{font_dir}/DejaVuSansMono-BoldOblique.ttf")

    # Cover page
    pdf.add_page()
    pdf.set_font('DejaVu', 'B', 26)
    pdf.set_text_color(212, 175, 55)
    pdf.ln(80)
    if title:
        pdf.cell(0, 15, title, align='C')
        pdf.ln()
    pdf.set_font('DejaVu', '', 13)
    pdf.set_text_color(100, 100, 100)
    if subtitle:
        pdf.ln(5)
        pdf.cell(0, 10, subtitle, align='C')
        pdf.ln()
    pdf.set_font('DejaVu', '', 11)
    pdf.ln(10)
    pdf.cell(0, 10, 'By Jennipher Troup', align='C')
    pdf.ln()
    pdf.set_font('DejaVu', '', 9)
    pdf.ln(5)
    pdf.cell(0, 8, 'Break. Repair. Glow. Repeat.', align='C')
    pdf.ln()

    # Content pages
    pdf.add_page()
    pdf.set_font('DejaVu', '', 9)
    pdf.set_text_color(40, 40, 40)

    try:
        pdf.write_html(html)
    except Exception as e:
        print(f"  HTML render failed ({e}), using plain text fallback")
        # Need fresh page since write_html might have corrupted state
        pdf.add_page()
        pdf.set_font('DejaVu', '', 9)
        text = re.sub(r'<[^>]+>', '', html)
        pdf.multi_cell(0, 5, text)

    pdf.output(pdf_path)
    print(f"  PDF: {pdf_path}")


if __name__ == "__main__":
    sections_dir = "../sections"
    out_dir = "pdfs"
    os.makedirs(out_dir, exist_ok=True)

    print("Converting sections to PDF...")

    conversions = [
        ("03-material-texture-hierarchy.md", "Section_03_Material_Texture_Hierarchy.pdf",
         "Material & Texture Hierarchy", "The Physical & Digital Alchemy of Repair"),
        ("06-lunarpunk-fashion.md", "Section_06_Lunarpunk_Fashion.pdf",
         "Lunarpunk Fashion Design", "Wearable Mythpunk: From Canvas to Catwalk"),
        ("10-lora-training-guide.md", "Section_10_LoRA_Training_Guide.pdf",
         "LoRA Training Guide", "Forging Your Own Lunar Myth Model"),
        ("11-tier-license-commercial.md", "Section_11_Tier_License_Sales.pdf",
         "Tier Assets, License & Sales", "From Creation to Commerce"),
    ]

    for md_file, pdf_file, title, subtitle in conversions:
        md_to_pdf(
            os.path.join(sections_dir, md_file),
            os.path.join(out_dir, pdf_file),
            title=title,
            subtitle=subtitle
        )

    # Combined comprehensive bible
    print("\nBuilding comprehensive bible...")
    combined_md = "# LUNAR MYTH KINTSUGI BIBLE\n\n"
    combined_md += "**357+ Hyper-Tactile Mythpunk Prompts & Complete Collage System**\n\n"
    combined_md += "*By Jennipher Troup*\n\n"
    combined_md += "---\n\n"

    for md_file, _, _, _ in conversions:
        with open(os.path.join(sections_dir, md_file), 'r') as f:
            combined_md += f.read() + "\n\n---\n\n"

    with open("/tmp/combined_bible.md", 'w') as f:
        f.write(combined_md)

    md_to_pdf(
        "/tmp/combined_bible.md",
        os.path.join(out_dir, "Lunar_Myth_Kintsugi_Bible_Complete.pdf"),
        title="LUNAR MYTH KINTSUGI BIBLE",
        subtitle="357+ Hyper-Tactile Mythpunk Prompts & Complete Collage System"
    )

    print(f"\nDone! PDFs saved to {out_dir}/")
