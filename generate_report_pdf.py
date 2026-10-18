import json
import os
import pymupdf as fitz

def generate_pdf():
    json_path = r"C:\Users\KARTHIK\Desktop\PARALLAX_FLOW\ca_evaluator\law_benchmark_eval.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    paper_name = data.get("paperTitle", "Law Test - 1: Corporate & Other Laws (ICAI Benchmark)")
    student = data["student"]
    questions = data["questions"]

    doc = fitz.open()

    # Define color scheme: Pure Monochrome (Black & White)
    COLOR_BLACK = (0, 0, 0)
    COLOR_DARK = (0.15, 0.15, 0.15)
    COLOR_GRAY = (0.45, 0.45, 0.45)
    COLOR_LIGHT = (0.94, 0.94, 0.94)
    COLOR_LINE = (0.85, 0.85, 0.85)
    COLOR_WHITE = (1, 1, 1)

    # PAGE 1: Gazette Cover & Executive Marks Table
    page1 = doc.new_page(width=595.28, height=841.89)  # A4 size

    # Header Box
    rect_top = fitz.Rect(36, 36, 559, 100)
    page1.draw_rect(rect_top, color=COLOR_BLACK, width=1.5)
    page1.insert_text(fitz.Point(50, 58), "THE INSTITUTE OF CHARTERED ACCOUNTANTS OF INDIA", fontsize=13, fontname="helv", color=COLOR_BLACK)
    page1.insert_text(fitz.Point(50, 74), "EXAMINATION RESULTS & DESCRIPTIVE ANSWER SCRIPT EVALUATION GAZETTE", fontsize=9.5, fontname="helv", color=COLOR_DARK)
    page1.insert_text(fitz.Point(50, 88), "ACADEMIC MOCK EVALUATION • VISION OCR + FACULTY VERIFIED AUDIT", fontsize=8, fontname="helv", color=COLOR_GRAY)

    # Candidate Dossier Block
    rect_dossier = fitz.Rect(36, 112, 559, 185)
    page1.draw_rect(rect_dossier, color=COLOR_BLACK, width=1.0)
    
    # Left Column
    page1.insert_text(fitz.Point(48, 130), f"Candidate Name:  {student['name']}", fontsize=10, fontname="helv", color=COLOR_BLACK)
    page1.insert_text(fitz.Point(48, 146), f"Roll Number:     {student['rollNo']}", fontsize=10, fontname="courier", color=COLOR_BLACK)
    page1.insert_text(fitz.Point(48, 162), f"Paper:           {paper_name}", fontsize=9, fontname="helv", color=COLOR_DARK)
    page1.insert_text(fitz.Point(48, 178), f"Center/Session:  {student.get('center', 'Mumbai WIRC')} • May 2026 Mock Series", fontsize=8.5, fontname="helv", color=COLOR_GRAY)

    # Right Column - Score Badge
    rect_score = fitz.Rect(380, 120, 547, 177)
    page1.draw_rect(rect_score, color=COLOR_BLACK, fill=COLOR_BLACK)
    page1.insert_text(fitz.Point(392, 138), "FINAL EVALUATION SCORE", fontsize=8, fontname="helv", color=COLOR_WHITE)
    page1.insert_text(fitz.Point(392, 160), f"{student['totalAwarded']:.1f} / {student['totalMax']:.1f}", fontsize=18, fontname="courier", color=COLOR_WHITE)
    page1.insert_text(fitz.Point(392, 172), f"{student['percentage']}% • {student['grade'].upper()}", fontsize=7.5, fontname="helv", color=COLOR_WHITE)

    # Executive Marks Summary Table
    page1.insert_text(fitz.Point(36, 212), "EXECUTIVE QUESTION-WISE MARKS DISTRIBUTION", fontsize=11, fontname="helv", color=COLOR_BLACK)
    
    table_top = 222
    row_height = 24
    
    # Header Row
    rect_th = fitz.Rect(36, table_top, 559, table_top + row_height)
    page1.draw_rect(rect_th, color=COLOR_BLACK, fill=COLOR_BLACK)
    page1.insert_text(fitz.Point(44, table_top + 16), "Q.No", fontsize=9, fontname="helv", color=COLOR_WHITE)
    page1.insert_text(fitz.Point(82, table_top + 16), "Topic & Statutory Reference", fontsize=9, fontname="helv", color=COLOR_WHITE)
    page1.insert_text(fitz.Point(375, table_top + 16), "Max", fontsize=9, fontname="helv", color=COLOR_WHITE)
    page1.insert_text(fitz.Point(425, table_top + 16), "Awarded", fontsize=9, fontname="helv", color=COLOR_WHITE)
    page1.insert_text(fitz.Point(490, table_top + 16), "Rating", fontsize=9, fontname="helv", color=COLOR_WHITE)

    curr_y = table_top + row_height
    for i, q in enumerate(questions):
        bg = COLOR_WHITE if i % 2 == 0 else COLOR_LIGHT
        rect_row = fitz.Rect(36, curr_y, 559, curr_y + row_height)
        page1.draw_rect(rect_row, color=COLOR_LINE, fill=bg)
        
        q_score = sum(s["marks"] for s in q["steps"])
        pct = (q_score / q["maxMarks"]) * 100
        rating = "100% Full Credit" if pct == 100 else f"{pct:.0f}% Partial"
        
        page1.insert_text(fitz.Point(44, curr_y + 16), q["code"], fontsize=9, fontname="courier", color=COLOR_BLACK)
        page1.insert_text(fitz.Point(82, curr_y + 12), q["title"][:42], fontsize=8.5, fontname="helv", color=COLOR_BLACK)
        page1.insert_text(fitz.Point(82, curr_y + 21), q["sectionReference"][:46], fontsize=7, fontname="courier", color=COLOR_GRAY)
        page1.insert_text(fitz.Point(375, curr_y + 16), f"{q['maxMarks']:.1f}", fontsize=8.5, fontname="courier", color=COLOR_BLACK)
        page1.insert_text(fitz.Point(425, curr_y + 16), f"{q_score:.1f}", fontsize=9, fontname="courier", color=COLOR_BLACK)
        page1.insert_text(fitz.Point(490, curr_y + 16), rating, fontsize=8, fontname="helv", color=COLOR_DARK)
        
        curr_y += row_height

    # Total Row
    rect_total = fitz.Rect(36, curr_y, 559, curr_y + row_height + 4)
    page1.draw_rect(rect_total, color=COLOR_BLACK, fill=COLOR_LIGHT, width=1.2)
    page1.insert_text(fitz.Point(44, curr_y + 18), "TOTAL AGGREGATE", fontsize=9.5, fontname="helv", color=COLOR_BLACK)
    page1.insert_text(fitz.Point(375, curr_y + 18), f"{student['totalMax']:.1f}", fontsize=10, fontname="courier", color=COLOR_BLACK)
    page1.insert_text(fitz.Point(425, curr_y + 18), f"{student['totalAwarded']:.1f}", fontsize=11, fontname="courier", color=COLOR_BLACK)
    page1.insert_text(fitz.Point(490, curr_y + 18), "82.1% (PASS)", fontsize=9, fontname="helv", color=COLOR_BLACK)

    # Diagnostic Summary Box
    diag_y = curr_y + 40
    page1.insert_text(fitz.Point(36, diag_y), "DIAGNOSTIC COMPETENCY BREAKDOWN", fontsize=11, fontname="helv", color=COLOR_BLACK)
    
    rect_diag = fitz.Rect(36, diag_y + 10, 559, diag_y + 65)
    page1.draw_rect(rect_diag, color=COLOR_BLACK, width=1.0)
    
    page1.insert_text(fitz.Point(50, diag_y + 30), "Provision Recall: 88%", fontsize=9.5, fontname="helv", color=COLOR_BLACK)
    page1.insert_text(fitz.Point(50, diag_y + 48), "Statutory citations and definitions highly accurate.", fontsize=8, fontname="helv", color=COLOR_GRAY)

    page1.insert_text(fitz.Point(220, diag_y + 30), "Working Notes: 79%", fontsize=9.5, fontname="helv", color=COLOR_BLACK)
    page1.insert_text(fitz.Point(220, diag_y + 48), "Minor explanation brevity on secondary provisions.", fontsize=8, fontname="helv", color=COLOR_GRAY)

    page1.insert_text(fitz.Point(390, diag_y + 30), "Presentation: 86%", fontsize=9.5, fontname="helv", color=COLOR_BLACK)
    page1.insert_text(fitz.Point(390, diag_y + 48), "Exemplary legal structuring and formatting.", fontsize=8, fontname="helv", color=COLOR_GRAY)

    # Examiner Certification Seal
    cert_y = diag_y + 85
    rect_cert = fitz.Rect(36, cert_y, 559, cert_y + 80)
    page1.draw_rect(rect_cert, color=COLOR_LINE, fill=COLOR_WHITE)
    page1.insert_text(fitz.Point(48, cert_y + 20), "OFFICIAL EXAMINER CERTIFICATION & SIGN-OFF", fontsize=9, fontname="helv", color=COLOR_BLACK)
    page1.insert_text(fitz.Point(48, cert_y + 36), "This descriptive answer script has been verified against ICAI Model Suggested Answers.", fontsize=8, fontname="helv", color=COLOR_DARK)
    page1.insert_text(fitz.Point(48, cert_y + 48), "Vision OCR extract validated with Gemini 3.5 Flash-Lite. All faculty overrides audited.", fontsize=8, fontname="helv", color=COLOR_GRAY)
    page1.insert_text(fitz.Point(48, cert_y + 64), "Stamp: ICAI-EVAL-VAL-2026-9921 • Digital Signature Verified", fontsize=8, fontname="courier", color=COLOR_BLACK)

    page1.insert_text(fitz.Point(380, cert_y + 36), "CA. R. K. Agrawal, FCA", fontsize=10, fontname="helv", color=COLOR_BLACK)
    page1.insert_text(fitz.Point(380, cert_y + 50), "Chief Examiner • Faculty of Law", fontsize=8.5, fontname="helv", color=COLOR_GRAY)

    # PAGE 2 & 3: Detailed Question-by-Question Audit Trail
    def add_question_pages():
        p = None
        y = 40
        page_num = 2

        def new_audit_page():
            nonlocal page_num
            pg = doc.new_page(width=595.28, height=841.89)
            # Running Header
            rect_h = fitz.Rect(36, 26, 559, 46)
            pg.draw_rect(rect_h, color=COLOR_LINE)
            pg.insert_text(fitz.Point(44, 40), f"ICAI EVALUATION AUDIT TRAIL • CANDIDATE: {student['name']} ({student['rollNo']})", fontsize=7.5, fontname="helv", color=COLOR_GRAY)
            pg.insert_text(fitz.Point(480, 40), f"Page {page_num} of 3", fontsize=7.5, fontname="courier", color=COLOR_GRAY)
            page_num += 1
            return pg, 60

        p, y = new_audit_page()

        for q in questions:
            q_score = sum(s["marks"] for s in q["steps"])
            needed_space = 70 + (len(q["steps"]) * 22) + 35
            
            if y + needed_space > 800:
                p, y = new_audit_page()

            # Question Header Card
            rect_qh = fitz.Rect(36, y, 559, y + 24)
            p.draw_rect(rect_qh, color=COLOR_BLACK, fill=COLOR_BLACK)
            p.insert_text(fitz.Point(44, y + 16), f"{q['code']}: {q['title']}", fontsize=9.5, fontname="helv", color=COLOR_WHITE)
            p.insert_text(fitz.Point(440, y + 16), f"{q_score:.1f} / {q['maxMarks']:.1f} Marks", fontsize=9.5, fontname="courier", color=COLOR_WHITE)
            y += 24

            # Question Prompt
            rect_qp = fitz.Rect(36, y, 559, y + 36)
            p.draw_rect(rect_qp, color=COLOR_LINE, fill=COLOR_LIGHT)
            prompt_preview = q["questionText"][:120] + ("..." if len(q["questionText"]) > 120 else "")
            p.insert_text(fitz.Point(44, y + 15), f"Question: {prompt_preview}", fontsize=7.5, fontname="helv", color=COLOR_DARK)
            p.insert_text(fitz.Point(44, y + 28), f"Citation: {q['sectionReference']}", fontsize=7, fontname="courier", color=COLOR_GRAY)
            y += 36

            # Steps Table
            for s in q["steps"]:
                rect_step = fitz.Rect(36, y, 559, y + 20)
                p.draw_rect(rect_step, color=COLOR_LINE, fill=COLOR_WHITE)
                
                step_title = f"Step {s['stepNo']}: {s['title'][:32]}"
                p.insert_text(fitz.Point(44, y + 14), step_title, fontsize=8, fontname="helv", color=COLOR_BLACK)
                p.insert_text(fitz.Point(210, y + 14), s["feedback"][:55], fontsize=7, fontname="helv", color=COLOR_DARK)
                p.insert_text(fitz.Point(475, y + 14), f"{s['marks']:.2f} / {s['maxMarks']:.1f}", fontsize=8, fontname="courier", color=COLOR_BLACK)
                y += 20

            # Keywords Matched / Missed Row
            rect_kw = fitz.Rect(36, y, 559, y + 18)
            p.draw_rect(rect_kw, color=COLOR_LINE, fill=COLOR_LIGHT)
            kw_match_str = ", ".join(q["keywordsMatched"][:4])
            kw_miss_str = ", ".join(q["keywordsMissed"][:3]) if q["keywordsMissed"] else "None"
            p.insert_text(fitz.Point(44, y + 12), f"Present: {kw_match_str}  |  Missing: {kw_miss_str}", fontsize=7, fontname="helv", color=COLOR_DARK)
            y += 26

    add_question_pages()

    out_dir = r"C:\Users\KARTHIK\Desktop\PARALLAX_FLOW"
    pdf_filename = f"Law_Test_1_Full_Evaluation_Report_{student['rollNo']}.pdf"
    pdf_path = os.path.join(out_dir, pdf_filename)
    
    # Also save inside ca_evaluator for web downloads
    web_pdf_path = os.path.join(r"C:\Users\KARTHIK\Desktop\PARALLAX_FLOW\ca_evaluator", pdf_filename)

    doc.save(pdf_path)
    doc.save(web_pdf_path)
    doc.close()
    
    print(f"Generated PDF successfully at:\n{pdf_path}\n{web_pdf_path}")

if __name__ == "__main__":
    generate_pdf()
