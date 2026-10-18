from PIL import Image, ImageDraw, ImageFont
import fitz
from pathlib import Path

def create_sample_handwritten_pdf(output_path: Path):
    """
    Creates a multi-page test PDF simulating realistic handwritten notes
    across multiple notebook pages.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()

    pages_data = [
        {
            "title": "Meeting Notes & System Architecture (Oct 12)",
            "lines": [
                "1. Core Objective: High-throughput Handwritten OCR pipeline.",
                "2. Pipeline requirements:",
                "   - Multi-page ingest (PDF, multi-image scan, mobile photos).",
                "   - Shadow removal and deskewing using adaptive filters.",
                "   - Parallel batch workers for high-volume production.",
                "3. Benchmarks & accuracy metrics:",
                "   - Cursive text recognition target > 95% accuracy.",
                "   - Latency: under 2.5 seconds per page with parallel scaling.",
                "~~Old approach: basic Tesseract 4~~ -> Discarded due to poor cursive recall.",
                "Action item: Hook up Gemini Vision API + EasyOCR local fallback."
            ]
        },
        {
            "title": "Mathematical Formulas & Derivations",
            "lines": [
                "Loss Function Definition:",
                "  L_total = lambda_1 * L_ctc + lambda_2 * L_seq2seq + lambda_3 * L_attention",
                "",
                "Key parameters for deskewing:",
                "  theta = median(arctan(-dy / dx)) for all detected line contours.",
                "  Range: -45 deg <= theta <= 45 deg.",
                "",
                "Illumination Correction:",
                "  I_norm(x, y) = 255 - |I(x, y) - Blur(Dilate(I(x, y), K))|",
                "Verified: Contrast ratio boosts ink legibility by ~38%."
            ]
        },
        {
            "title": "Production Deployment Checklist",
            "lines": [
                "[X] Asynchronous queue management with concurrency limiter.",
                "[X] PyMuPDF 300 DPI high-definition page extraction.",
                "[X] Human-in-the-loop review studio with side-by-side verification.",
                "[X] Export formats: Markdown, Plain Text, Structured JSON, ZIP bundle.",
                "[ ] Final stress testing with 50+ page continuous notebook scans.",
                "",
                "Sign-off: ParallaxFlow Engineering Team"
            ]
        }
    ]

    for p_idx, p_data in enumerate(pages_data, start=1):
        # Create image with ruled paper background (lined notebook look)
        img = Image.new("RGB", (1200, 1600), color=(252, 250, 242))  # warm notebook paper tone
        draw = ImageDraw.Draw(img)

        # Draw notebook margin line (red vertical line)
        draw.line([(140, 0), (140, 1600)], fill=(225, 170, 170), width=2)

        # Draw notebook horizontal ruled lines (light blue lines)
        for y in range(160, 1550, 50):
            draw.line([(0, y), (1200, y)], fill=(215, 230, 245), width=1)

        # Try to use a font or default
        try:
            font_title = ImageFont.truetype("arial.ttf", 36)
            font_text = ImageFont.truetype("arial.ttf", 26)
        except Exception:
            font_title = ImageFont.load_default()
            font_text = ImageFont.load_default()

        # Draw page header
        draw.text((160, 90), p_data["title"], fill=(30, 45, 90), font=font_title)
        draw.text((1050, 95), f"Page {p_idx}", fill=(120, 120, 130), font=font_text)

        # Draw handwritten text lines
        cur_y = 175
        for line in p_data["lines"]:
            if line:
                draw.text((165, cur_y), line, fill=(20, 30, 60), font=font_text)
            cur_y += 50

        # Save page to PDF
        page_pdf_bytes = fitz.open()
        import io
        img_bytes_io = io.BytesIO()
        img.save(img_bytes_io, format="JPEG", quality=95)
        img_bytes = img_bytes_io.getvalue()
        
        pdf_page = doc.new_page(width=612, height=792)  # standard letter
        pdf_page.insert_image(pdf_page.rect, stream=img_bytes)

    doc.save(str(output_path))
    doc.close()
    return output_path

if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "sample_handwritten_notebook.pdf"
    create_sample_handwritten_pdf(out)
    print(f"Sample PDF generated at {out}")
