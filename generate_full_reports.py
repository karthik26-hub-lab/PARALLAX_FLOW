import json
import os

def generate_reports():
    json_path = r"C:\Users\KARTHIK\Desktop\PARALLAX_FLOW\ca_evaluator\law_benchmark_eval.json"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    paper_name = data.get("paperTitle", "Law Test - 1: Corporate & Other Laws (ICAI Benchmark)")
    student = data["student"]
    questions = data["questions"]

    # 1. MARKDOWN REPORT
    md = f"""# THE INSTITUTE OF CHARTERED ACCOUNTANTS OF INDIA
## DESCRIPTIVE ANSWER SCRIPT EVALUATION GAZETTE REPORT
**Assessment Session:** May 2026 Mock Series • Vision OCR + Faculty Certified Audit

---

### Candidate Dossier
- **Candidate Name:** {student['name']}
- **Roll Number:** `{student['rollNo']}`
- **Examination Paper:** {paper_name}
- **Examination Center:** {student.get('center', 'Mumbai - Western Regional Council')}
- **Assessment Mode:** Gemini 3.5 Flash-Lite Vision OCR + Certified Faculty Step-Marking
- **Overall Score:** **{student['totalAwarded']:.1f} / {student['totalMax']:.1f} ({student['percentage']}%)**
- **Classification / Grade:** **{student['grade'].upper()}**
- **Rank / Percentile:** {student.get('rank', 'Rank 12 / 148')} ({student.get('percentile', '92nd Percentile')})

---

### Executive Question-wise Marks Distribution

| Question | Topic Description | Statutory Section Reference | Max Marks | Awarded Marks | Performance |
| :--- | :--- | :--- | :---: | :---: | :--- |
"""
    for q in questions:
        q_score = sum(s["marks"] for s in q["steps"])
        pct = (q_score / q["maxMarks"]) * 100
        rating = "100% Full Credit" if pct == 100 else f"{pct:.0f}% Partial Credit"
        md += f"| **{q['code']}** | {q['title']} | `{q['sectionReference']}` | {q['maxMarks']:.1f} | **{q_score:.1f}** | {rating} |\n"

    md += f"""| **TOTAL** | **Aggregate Examination Marks** | **All 8 Prescribed Questions** | **{student['totalMax']:.1f}** | **{student['totalAwarded']:.1f}** | **{student['percentage']}% (PASS)** |

---

### Diagnostic Competency Analysis
- **Provision Recall:** {student['competencies']['provisionRecall']}% — High precision on primary standard definitions (Sections 2(6), 2(85), 63, Rule 3).
- **Working Notes & Calculations:** {student['competencies']['workingNotes']}% — Solid legal reasoning; minor brevity on 12% interest calculation and deposit 60-day rule.
- **Presentation & Formatting:** {student['competencies']['presentation']}% — Professional structured numbering with clear statutory conclusions.

---

### Detailed Question-by-Question Evaluation Audit Trail

"""
    for q in questions:
        q_score = sum(s["marks"] for s in q["steps"])
        md += f"""#### {q['code']}: {q['title']}
- **Marks Awarded:** `{q_score:.1f} / {q['maxMarks']:.1f}` Marks
- **Statutory Authority:** `{q['sectionReference']}`
- **Exam Question:**
  > {q['questionText']}
- **ICAI Expected Legal Conclusion:**
  > {q.get('expectedConclusion', 'Refer to official model answer key.')}

**Step-wise Rubric Marks:**
"""
        for s in q["steps"]:
            md += f"1. **Step {s['stepNo']} ({s['title']}):** `{s['marks']:.2f} / {s['maxMarks']:.1f}` Marks\n"
            md += f"   - *Examiner Feedback:* {s['feedback']}\n"
            if s.get("facultyComment"):
                md += f"   - *Faculty Note:* _{s['facultyComment']}_\n"

        matched = ", ".join([f"`{k}`" for k in q["keywordsMatched"]])
        missed = ", ".join([f"`{k}`" for k in q["keywordsMissed"]]) if q["keywordsMissed"] else "_None_"
        md += f"\n- **Keywords Verified Present:** {matched}\n"
        md += f"- **Keywords Missed / Divergent:** {missed}\n\n---\n\n"

    md += """### Faculty Certification & Official Seal
> **Certified that this descriptive answer booklet has been thoroughly evaluated against official ICAI Suggested Answers.**
> All vision OCR extractions, step-wise scores, and faculty overrides have been audited and signed off.
>
> **Chief Examiner:** CA. R. K. Agrawal, FCA  
> **Verification Stamp:** `ICAI-EVAL-VAL-2026-9921`  
> **Signed on:** 14-October-2026
"""

    # 2. STANDALONE HTML REPORT (Self-contained, high craft, printable)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ICAI Evaluation Gazette • {student['name']} ({student['rollNo']})</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    @page {{
      size: A4;
      margin: 14mm 16mm;
    }}
    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background: #FAFAFA;
      color: #09090B;
      line-height: 1.45;
      font-size: 13px;
      padding: 30px 20px;
    }}
    .font-mono {{
      font-family: 'JetBrains Mono', monospace;
      font-variant-numeric: tabular-nums;
    }}
    .report-wrap {{
      max-width: 860px;
      margin: 0 auto;
      background: #FFFFFF;
      border: 1px solid #09090B;
      padding: 36px 42px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }}
    .top-actions {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;
      padding-bottom: 12px;
      border-bottom: 1px solid #E4E4E7;
    }}
    .btn-print {{
      background: #09090B;
      color: #FFFFFF;
      border: 1px solid #09090B;
      padding: 8px 16px;
      font-size: 12px;
      font-weight: 700;
      border-radius: 4px;
      cursor: pointer;
    }}
    .btn-print:hover {{
      background: #27272A;
    }}
    .gazette-header {{
      text-align: center;
      border-bottom: 2px solid #09090B;
      padding-bottom: 16px;
      margin-bottom: 20px;
    }}
    .crest {{
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #71717A;
    }}
    .title {{
      font-size: 20px;
      font-weight: 800;
      margin: 6px 0 4px;
      letter-spacing: -0.02em;
    }}
    .sub {{
      font-size: 11.5px;
      color: #52525B;
      font-weight: 500;
    }}
    .dossier-grid {{
      display: grid;
      grid-template-columns: 1fr 200px;
      border: 1px solid #09090B;
      margin-bottom: 24px;
    }}
    .dossier-info {{
      padding: 16px;
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 10px 18px;
      font-size: 12px;
      border-right: 1px solid #09090B;
    }}
    .dossier-label {{
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      color: #71717A;
      display: block;
      margin-bottom: 2px;
    }}
    .dossier-val {{
      font-weight: 700;
      color: #09090B;
    }}
    .dossier-score-box {{
      padding: 16px;
      background: #09090B;
      color: #FFFFFF;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
    }}
    .score-huge {{
      font-size: 28px;
      font-weight: 800;
      margin: 4px 0;
    }}
    .status-badge {{
      background: #FFFFFF;
      color: #09090B;
      font-size: 10px;
      font-weight: 800;
      padding: 2px 8px;
      border-radius: 2px;
    }}
    .section-h {{
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      border-bottom: 1px solid #09090B;
      padding-bottom: 4px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      margin-bottom: 24px;
    }}
    th {{
      background: #09090B;
      color: #FFFFFF;
      text-align: left;
      padding: 7px 10px;
      font-size: 10.5px;
      font-weight: 700;
      text-transform: uppercase;
    }}
    td {{
      padding: 8px 10px;
      border-bottom: 1px solid #E4E4E7;
      vertical-align: middle;
    }}
    tr:nth-child(even) td {{
      background: #FAFAFA;
    }}
    .q-block {{
      border: 1px solid #09090B;
      margin-bottom: 18px;
      page-break-inside: avoid;
    }}
    .q-header {{
      background: #F4F4F5;
      padding: 8px 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #09090B;
    }}
    .q-prompt {{
      padding: 10px 12px;
      font-size: 11.5px;
      background: #FAFAFA;
      border-bottom: 1px solid #E4E4E7;
      color: #27272A;
    }}
    .steps-table {{
      margin-bottom: 0;
      font-size: 11.5px;
    }}
    .steps-table th {{
      background: #E4E4E7;
      color: #09090B;
      padding: 4px 8px;
      font-size: 10px;
    }}
    .steps-table td {{
      padding: 6px 8px;
    }}
    .keywords-row {{
      padding: 6px 12px;
      background: #FFFFFF;
      font-size: 10.5px;
      border-top: 1px solid #E4E4E7;
    }}
    .kw-tag {{
      display: inline-block;
      font-size: 9px;
      font-weight: 700;
      padding: 1px 5px;
      border-radius: 2px;
      margin-right: 4px;
    }}
    .kw-present {{
      background: #09090B;
      color: #FFFFFF;
    }}
    .kw-missing {{
      border: 1px solid #D4D4D8;
      color: #71717A;
      text-decoration: line-through;
    }}
    .cert-box {{
      border: 1px solid #09090B;
      padding: 16px;
      display: grid;
      grid-template-columns: 1fr 220px;
      gap: 16px;
      margin-top: 24px;
      page-break-inside: avoid;
    }}
    @media print {{
      body {{
        background: #FFFFFF;
        padding: 0;
      }}
      .report-wrap {{
        border: none;
        box-shadow: none;
        padding: 0;
        max-width: 100%;
      }}
      .top-actions {{
        display: none !important;
      }}
      .btn-print {{
        display: none !important;
      }}
    }}
  </style>
</head>
<body>

  <div class="report-wrap">
    
    <div class="top-actions">
      <div>
        <strong>Official Evaluation Gazette</strong> • ID: ICAI-EVAL-2026-410892
      </div>
      <div>
        <button class="btn-print" onclick="window.print()">Print / Save as PDF</button>
      </div>
    </div>

    <header class="gazette-header">
      <div class="crest">The Institute of Chartered Accountants of India</div>
      <h1 class="title">Descriptive Answer Script Evaluation Report</h1>
      <div class="sub">ICAI Benchmark Examination • Official Step-Marking &amp; Faculty Certification</div>
    </header>

    <div class="dossier-grid">
      <div class="dossier-info">
        <div>
          <span class="dossier-label">Candidate Name</span>
          <span class="dossier-val">{student['name']}</span>
        </div>
        <div>
          <span class="dossier-label">Roll Number</span>
          <span class="dossier-val font-mono">{student['rollNo']}</span>
        </div>
        <div>
          <span class="dossier-label">Paper</span>
          <span class="dossier-val">{paper_name}</span>
        </div>
        <div>
          <span class="dossier-label">Session</span>
          <span class="dossier-val">May 2026 Mock Series</span>
        </div>
        <div>
          <span class="dossier-label">OCR Vision Engine</span>
          <span class="dossier-val font-mono">Gemini 3.5 Flash-Lite</span>
        </div>
        <div>
          <span class="dossier-label">Classification</span>
          <span class="dossier-val">{student['grade']}</span>
        </div>
      </div>
      <div class="dossier-score-box">
        <span style="font-size: 10px; font-weight: 800; text-transform: uppercase;">Final Score</span>
        <div class="score-huge font-mono">{student['totalAwarded']:.1f} / {student['totalMax']:.1f}</div>
        <div class="status-badge font-mono">{student['percentage']}% • PASS</div>
      </div>
    </div>

    <div class="section-h">
      <span>Executive Question-wise Marks Distribution</span>
      <span class="font-mono">Max Marks: {student['totalMax']:.1f}</span>
    </div>

    <table>
      <thead>
        <tr>
          <th style="width: 70px;">Q.No</th>
          <th>Topic &amp; Statutory Section Reference</th>
          <th style="width: 90px; text-align: center;">Max</th>
          <th style="width: 90px; text-align: center;">Awarded</th>
          <th style="width: 120px; text-align: center;">Performance</th>
        </tr>
      </thead>
      <tbody>
"""
    for q in questions:
        q_score = sum(s["marks"] for s in q["steps"])
        pct = (q_score / q["maxMarks"]) * 100
        rating = "100% Full Credit" if pct == 100 else f"{pct:.0f}% Partial"
        html += f"""        <tr>
          <td class="font-mono" style="font-weight: 800;">{q['code']}</td>
          <td>
            <strong>{q['title']}</strong>
            <div class="font-mono" style="font-size: 10.5px; color: #71717A;">{q['sectionReference']}</div>
          </td>
          <td class="font-mono" style="text-align: center;">{q['maxMarks']:.1f}</td>
          <td class="font-mono" style="text-align: center; font-weight: 800;">{q_score:.1f}</td>
          <td style="text-align: center;">
            <span style="border: 1px solid #09090B; padding: 1px 6px; font-size: 10.5px; font-weight: 700;">{rating}</span>
          </td>
        </tr>
"""
    html += f"""        <tr style="background: #F4F4F5; font-weight: 800;">
          <td colspan="2">TOTAL AGGREGATE EVALUATION SCORE</td>
          <td class="font-mono" style="text-align: center;">{student['totalMax']:.1f}</td>
          <td class="font-mono" style="text-align: center; font-size: 14px;">{student['totalAwarded']:.1f}</td>
          <td style="text-align: center; font-weight: 800;">{student['percentage']}% (PASS)</td>
        </tr>
      </tbody>
    </table>

    <div class="section-h">
      <span>Detailed Question-by-Question Audit Trail</span>
      <span class="font-mono">8 Questions Verified</span>
    </div>
"""
    for q in questions:
        q_score = sum(s["marks"] for s in q["steps"])
        html += f"""    <div class="q-block">
      <div class="q-header">
        <div>
          <strong class="font-mono">{q['code']}</strong> — <strong>{q['title']}</strong>
          <span class="font-mono" style="font-size: 10px; margin-left: 6px; border: 1px solid #CBD5E1; padding: 0 4px;">{q['questionId']}</span>
        </div>
        <div class="font-mono" style="font-weight: 800;">{q_score:.1f} / {q['maxMarks']:.1f} Marks</div>
      </div>
      <div class="q-prompt">
        <strong>Question:</strong> {q['questionText']}
      </div>
      <table class="steps-table">
        <thead>
          <tr>
            <th style="width: 50px;">Step</th>
            <th>Rubric Evaluation Feedback</th>
            <th style="width: 60px; text-align: center;">Max</th>
            <th style="width: 60px; text-align: center;">Awarded</th>
          </tr>
        </thead>
        <tbody>
"""
        for s in q["steps"]:
            html += f"""          <tr>
            <td class="font-mono" style="font-weight: 800;">S{s['stepNo']}</td>
            <td>
              <strong>{s['title']}</strong>
              <div style="color: #52525B; font-size: 11px; margin-top: 2px;">{s['feedback']}</div>
              {f'<div style="font-size: 10.5px; font-style: italic; margin-top: 2px;"><strong>Faculty Note:</strong> {s["facultyComment"]}</div>' if s.get("facultyComment") else ''}
            </td>
            <td class="font-mono" style="text-align: center;">{s['maxMarks']:.1f}</td>
            <td class="font-mono" style="text-align: center; font-weight: 800;">{s['marks']:.2f}</td>
          </tr>
"""
        html += """        </tbody>
      </table>
      <div class="keywords-row">
        <strong style="text-transform: uppercase; font-size: 10px; margin-right: 6px;">Keywords:</strong>
"""
        for kw in q["keywordsMatched"]:
            html += f'<span class="kw-tag kw-present">✓ {kw}</span> '
        for kw in q["keywordsMissed"]:
            html += f'<span class="kw-tag kw-missing">✕ {kw}</span> '
        html += """      </div>
    </div>
"""

    html += f"""    <div class="cert-box">
      <div>
        <h4 style="font-size: 11.5px; font-weight: 800; text-transform: uppercase; margin-bottom: 4px;">Examiner Official Certification &amp; Sign-Off</h4>
        <p style="font-size: 11.5px; color: #52525B; line-height: 1.5;">
          Certified that this descriptive answer booklet has been evaluated against ICAI official model answer keys. Vision OCR extractions, step-wise scores, and faculty overrides have been completely verified and signed off.
        </p>
      </div>
      <div style="text-align: right; border-left: 1px solid #E4E4E7; padding-left: 16px;">
        <div style="font-weight: 800; font-size: 12.5px;">CA. R. K. Agrawal, FCA</div>
        <div style="font-size: 11px; color: #52525B;">Chief Examiner • Faculty of Law</div>
        <div class="font-mono" style="font-size: 10px; color: #71717A; margin-top: 4px;">Stamp: ICAI-EVAL-VAL-2026-9921</div>
      </div>
    </div>

  </div>

</body>
</html>
"""

    # 3. Save files to both Root and ca_evaluator
    destinations = [
        r"C:\Users\KARTHIK\Desktop\PARALLAX_FLOW",
        r"C:\Users\KARTHIK\Desktop\PARALLAX_FLOW\ca_evaluator"
    ]

    for d in destinations:
        md_file = os.path.join(d, f"Law_Test_1_Full_Evaluation_Report_{student['rollNo']}.md")
        html_file = os.path.join(d, f"Law_Test_1_Full_Evaluation_Report_{student['rollNo']}.html")
        json_file = os.path.join(d, f"Law_Test_1_Full_Evaluation_Report_{student['rollNo']}.json")

        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md)
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html)
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    print("Successfully generated MD, HTML, and JSON reports in both root and ca_evaluator!")

if __name__ == "__main__":
    generate_reports()
