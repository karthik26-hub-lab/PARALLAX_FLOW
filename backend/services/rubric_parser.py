import io
import csv
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import pandas as pd

class RubricParser:
    """
    Parses exam rubrics, model answers, keywords, and step-wise criteria
    from uploaded Excel (.xlsx, .xls) or CSV files.
    """

    @classmethod
    def parse_file(cls, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        ext = Path(filename).suffix.lower()
        if ext in [".xlsx", ".xls"]:
            return cls._parse_excel(file_bytes)
        elif ext == ".csv":
            return cls._parse_csv(file_bytes)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Please upload .xlsx, .xls, or .csv")

    @classmethod
    def _parse_excel(cls, file_bytes: bytes) -> Dict[str, Any]:
        excel_file = io.BytesIO(file_bytes)
        xls = pd.ExcelFile(excel_file)
        sheet_names = [s.strip() for s in xls.sheet_names]

        # Check for multi-sheet layout (Question_Master + Step_Rubric)
        q_sheet = next((s for s in sheet_names if "question" in s.lower() or "master" in s.lower()), None)
        s_sheet = next((s for s in sheet_names if "step" in s.lower() or "rubric" in s.lower()), None)

        questions = []
        steps = []

        if q_sheet and s_sheet and q_sheet != s_sheet:
            df_q = pd.read_excel(xls, sheet_name=q_sheet).fillna("")
            df_s = pd.read_excel(xls, sheet_name=s_sheet).fillna("")
            questions = cls._normalize_questions_df(df_q)
            steps = cls._normalize_steps_df(df_s)
        elif s_sheet:
            # Single sheet that contains step rubric
            df_s = pd.read_excel(xls, sheet_name=s_sheet).fillna("")
            steps = cls._normalize_steps_df(df_s)
            questions = cls._infer_questions_from_steps(steps)
        else:
            # First available sheet
            df = pd.read_excel(xls, sheet_name=sheet_names[0]).fillna("")
            # Detect whether it has step columns or question columns
            cols = [str(c).lower() for c in df.columns]
            if any("step" in c for c in cols):
                steps = cls._normalize_steps_df(df)
                questions = cls._infer_questions_from_steps(steps)
            else:
                questions = cls._normalize_questions_df(df)

        return cls._assemble_rubric_bundle(questions, steps)

    @classmethod
    def _parse_csv(cls, file_bytes: bytes) -> Dict[str, Any]:
        # Handle possible multiple tables separated by blank lines
        text = file_bytes.decode("utf-8", errors="replace")
        
        # Check if text contains both question master and step rubric sections
        sections = text.split("\n\n")
        dfs = []
        for sec in sections:
            sec_clean = sec.strip()
            if not sec_clean:
                continue
            try:
                df = pd.read_csv(io.StringIO(sec_clean)).fillna("")
                if len(df) > 0:
                    dfs.append(df)
            except Exception:
                pass

        questions = []
        steps = []

        if len(dfs) >= 2:
            # First might be questions, second steps
            for df in dfs:
                cols = [str(c).lower() for c in df.columns]
                if any("step no" in c or "step" in c for c in cols):
                    steps.extend(cls._normalize_steps_df(df))
                elif any("question" in c for c in cols):
                    questions.extend(cls._normalize_questions_df(df))
        elif len(dfs) == 1:
            df = dfs[0]
            cols = [str(c).lower() for c in df.columns]
            if any("step no" in c or "step" in c for c in cols):
                steps = cls._normalize_steps_df(df)
                questions = cls._infer_questions_from_steps(steps)
            else:
                questions = cls._normalize_questions_df(df)
        else:
            # Fallback to direct read
            df = pd.read_csv(io.StringIO(text)).fillna("")
            cols = [str(c).lower() for c in df.columns]
            if any("step no" in c or "step" in c for c in cols):
                steps = cls._normalize_steps_df(df)
                questions = cls._infer_questions_from_steps(steps)
            else:
                questions = cls._normalize_questions_df(df)

        return cls._assemble_rubric_bundle(questions, steps)

    @classmethod
    def _normalize_questions_df(cls, df: pd.DataFrame) -> List[Dict[str, Any]]:
        questions = []
        for _, row in df.iterrows():
            q_id = str(row.get("Question ID") or row.get("question_id") or row.get("ID") or "").strip()
            q_no = row.get("Source Question No.") or row.get("Question No") or row.get("Q No") or row.get("q_no") or ""
            try:
                q_no_int = int(q_no)
            except Exception:
                q_no_int = len(questions) + 1

            if not q_id:
                q_id = f"Q-{q_no_int}"

            q_text = str(row.get("Original Question") or row.get("Question") or row.get("question_text") or "").strip()
            model_ans = str(row.get("Model Answer (Exam-ready)") or row.get("Model Answer") or row.get("Answer") or "").strip()
            exp_conclusion = str(row.get("Expected Conclusion") or row.get("Conclusion") or "").strip()
            keywords = str(row.get("Mandatory Keywords / Key Phrases") or row.get("Keywords") or "").strip()
            section_ref = str(row.get("Provision / Section Reference") or row.get("Section") or "").strip()
            common_mistakes = str(row.get("Common Mistakes / Traps") or row.get("Common Mistakes") or "").strip()

            tot_marks_raw = row.get("Suggested Total Marks") or row.get("Total Marks") or row.get("Marks") or 4.0
            try:
                tot_marks = float(tot_marks_raw)
            except Exception:
                tot_marks = 4.0

            keywords_list = [k.strip() for k in keywords.split("|") if k.strip()] if "|" in keywords else [k.strip() for k in keywords.split(",") if k.strip()]

            questions.append({
                "question_id": q_id,
                "question_no": q_no_int,
                "question_text": q_text,
                "section_reference": section_ref,
                "model_answer": model_ans,
                "expected_conclusion": exp_conclusion,
                "mandatory_keywords": keywords_list,
                "common_mistakes": common_mistakes,
                "total_marks": tot_marks
            })
        return questions

    @classmethod
    def _normalize_steps_df(cls, df: pd.DataFrame) -> List[Dict[str, Any]]:
        steps = []
        for _, row in df.iterrows():
            q_id = str(row.get("Question ID") or row.get("question_id") or "").strip()
            q_no = row.get("Source Question No.") or row.get("Question No") or ""
            try:
                q_no_int = int(q_no)
            except Exception:
                q_no_int = 1

            if not q_id:
                q_id = f"Q-{q_no_int}"

            step_no_raw = row.get("Step No.") or row.get("Step No") or row.get("step") or 1
            try:
                step_no = int(step_no_raw)
            except Exception:
                step_no = len(steps) + 1

            subpart = str(row.get("Subpart / Component") or row.get("Subpart") or row.get("Component") or f"Step {step_no}").strip()
            criterion = str(row.get("Expected Answer Step / Criterion") or row.get("Criterion") or "").strip()
            what_earns_mark = str(row.get("What earns the mark") or row.get("Rubric") or criterion).strip()
            key_terms = str(row.get("Key Terms / Figures") or row.get("Key Terms") or "").strip()
            
            marks_raw = row.get("Marks") or row.get("Step Marks") or 1.0
            try:
                marks = float(marks_raw)
            except Exception:
                marks = 1.0

            importance = str(row.get("Importance") or "Critical").strip()
            feedback = str(row.get("Feedback if Missed") or "").strip()
            common_error = str(row.get("Common Error") or "").strip()

            key_terms_list = [k.strip() for k in key_terms.split("|") if k.strip()] if "|" in key_terms else [k.strip() for k in key_terms.split(",") if k.strip()]

            steps.append({
                "question_id": q_id,
                "question_no": q_no_int,
                "step_no": step_no,
                "subpart": subpart,
                "criterion": criterion,
                "what_earns_mark": what_earns_mark,
                "key_terms": key_terms_list,
                "marks": marks,
                "importance": importance,
                "feedback_if_missed": feedback,
                "common_error": common_error
            })
        return steps

    @classmethod
    def _infer_questions_from_steps(cls, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        q_map: Dict[str, Dict[str, Any]] = {}
        for s in steps:
            qid = s["question_id"]
            if qid not in q_map:
                q_map[qid] = {
                    "question_id": qid,
                    "question_no": s["question_no"],
                    "question_text": f"Question {s['question_no']}",
                    "section_reference": "",
                    "model_answer": "",
                    "expected_conclusion": "",
                    "mandatory_keywords": [],
                    "common_mistakes": "",
                    "total_marks": 0.0
                }
            q_map[qid]["total_marks"] += s["marks"]
            for term in s["key_terms"]:
                if term not in q_map[qid]["mandatory_keywords"]:
                    q_map[qid]["mandatory_keywords"].append(term)
        return list(q_map.values())

    @classmethod
    def _assemble_rubric_bundle(cls, questions: List[Dict[str, Any]], steps: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Group steps by question_id or question_no
        grouped_questions = []
        for q in questions:
            qid = q["question_id"]
            qno = q["question_no"]
            matching_steps = [s for s in steps if s["question_id"] == qid or s["question_no"] == qno]
            
            # If no steps found, generate a default 1-step rubric
            if not matching_steps:
                matching_steps = [{
                    "question_id": qid,
                    "question_no": qno,
                    "step_no": 1,
                    "subpart": "Comprehensive Answer",
                    "criterion": q["model_answer"] or "Complete and correct legal answer",
                    "what_earns_mark": "Accuracy of provision, facts application, and conclusion",
                    "key_terms": q["mandatory_keywords"],
                    "marks": q["total_marks"],
                    "importance": "Critical",
                    "feedback_if_missed": "Compare your answer with model answer",
                    "common_error": q["common_mistakes"]
                }]

            q_copy = dict(q)
            q_copy["steps"] = matching_steps
            # Verify sum of marks
            sum_marks = sum(s["marks"] for s in matching_steps)
            if sum_marks > 0:
                q_copy["total_marks"] = sum_marks
            grouped_questions.append(q_copy)

        total_exam_marks = sum(q["total_marks"] for q in grouped_questions)
        return {
            "total_questions": len(grouped_questions),
            "total_marks": total_exam_marks,
            "questions": grouped_questions
        }
