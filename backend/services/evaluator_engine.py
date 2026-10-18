import json
import time
import re
from typing import Dict, List, Any, Optional
from google import genai
from google.genai import types
from backend.config import settings

EVALUATION_SYSTEM_PROMPT = """You are an expert senior bar/examiner assessing student handwritten answer papers against an official exam rubric and marking scheme.
Your task is to grade the student's answer with utmost fairness, objectivity, and step-wise precision based strictly on the provided rubric.

Guidelines:
1. Compare the student's answer against the Model Answer, Step Criteria, and Key Terms.
2. Award credit based on the legal, technical, and mathematical concepts conveyed—not purely rigid word-for-word memorization.
3. For each Step in the rubric, evaluate if the criterion was met (FULL_CREDIT, PARTIAL, or NO_CREDIT) and award fractional or full marks up to the step's max marks.
4. Identify which Mandatory Keywords / Key Terms were present/matched and which were missing.
5. Provide constructive, actionable feedback and examiner remarks.

Return ONLY a valid JSON object matching the requested schema.
"""

class EvaluatorEngine:
    """
    Evaluates student handwritten answers against question master & step-wise rubrics.
    Supports both Gemini 3.5 Flash-Lite multimodal reasoning and deterministic rule-based grading.
    """

    @classmethod
    def segment_answers_to_questions(
        cls,
        questions: List[Dict[str, Any]],
        pages: List[Dict[str, Any]]
    ) -> Dict[int, Dict[str, Any]]:
        """
        Maps multi-page handwritten transcription pages to individual questions (Q1..Qn).
        """
        q_answers: Dict[int, Dict[str, Any]] = {}
        for q in questions:
            q_no = q["question_no"]
            q_answers[q_no] = {
                "question": q,
                "text_parts": [],
                "page_numbers": [],
                "page_images": []
            }

        # Scan each page for question headers (e.g., "1)", "2)", "Q1", "Question 1", etc.)
        for page in pages:
            p_no = page["page_number"]
            text = page.get("transcription_markdown", "")
            img_file = page.get("processed_file") or page.get("original_file")

            # Detect which question this page starts or deals with
            # Look for patterns like `1)`, `2)`, `3)`, `Question 1`, `Ans 1` at the beginning of lines
            matches = list(re.finditer(r'(?:^|\n)\s*(?:Q(?:uestion)?\.?\s*|Ans(?:wer)?\.?\s*)?(\d+)\s*[\)\.\-:]', text, re.IGNORECASE))
            
            if matches:
                # Page contains one or more question starts
                for m in matches:
                    q_num = int(m.group(1))
                    if q_num in q_answers:
                        q_answers[q_num]["page_numbers"].append(p_no)
                        if img_file and img_file not in q_answers[q_num]["page_images"]:
                            q_answers[q_num]["page_images"].append(img_file)
                        q_answers[q_num]["text_parts"].append(text)
            else:
                # Continuation page (like Page 7 for Q6 or Page 9 for Q7)
                # Assign to the most recent active question
                assigned = False
                for q_no in sorted(q_answers.keys(), reverse=True):
                    if q_answers[q_no]["page_numbers"]:
                        last_p = max(q_answers[q_no]["page_numbers"])
                        if p_no == last_p + 1:
                            q_answers[q_no]["page_numbers"].append(p_no)
                            if img_file and img_file not in q_answers[q_no]["page_images"]:
                                q_answers[q_no]["page_images"].append(img_file)
                            q_answers[q_no]["text_parts"].append(text)
                            assigned = True
                            break
                if not assigned and q_answers:
                    # Fallback to last question
                    last_q = max(q_answers.keys())
                    q_answers[last_q]["page_numbers"].append(p_no)
                    if img_file and img_file not in q_answers[last_q]["page_images"]:
                        q_answers[last_q]["page_images"].append(img_file)
                    q_answers[last_q]["text_parts"].append(text)

        # Merge text parts
        for q_no, data in q_answers.items():
            data["full_student_text"] = "\n\n---\n\n".join(data["text_parts"])

        return q_answers

    @classmethod
    async def evaluate_question(
        cls,
        q_data: Dict[str, Any],
        student_text: str,
        api_key: Optional[str] = None,
        model_name: str = "gemini-3.5-flash-lite"
    ) -> Dict[str, Any]:
        """
        Evaluates a single question against its step-by-step rubric.
        """
        q_no = q_data["question_no"]
        q_id = q_data["question_id"]
        q_text = q_data["question_text"]
        model_ans = q_data["model_answer"]
        exp_conclusion = q_data["expected_conclusion"]
        keywords = q_data.get("mandatory_keywords", [])
        steps = q_data.get("steps", [])
        total_q_marks = q_data.get("total_marks", sum(s["marks"] for s in steps))

        if not student_text.strip():
            # Blank answer
            return {
                "question_no": q_no,
                "question_id": q_id,
                "marks_awarded": 0.0,
                "max_marks": total_q_marks,
                "percentage": 0.0,
                "status": "UNATTEMPTED",
                "keywords_matched": [],
                "keywords_missed": keywords,
                "steps_evaluation": [
                    {
                        "step_no": s["step_no"],
                        "subpart": s["subpart"],
                        "marks_awarded": 0.0,
                        "max_marks": s["marks"],
                        "status": "NO_CREDIT",
                        "criterion_met": False,
                        "feedback": "Question not attempted."
                    }
                    for s in steps
                ],
                "examiner_remarks": "No answer written for this question.",
                "suggestions_for_improvement": "Attempt the question citing applicable provisions."
            }

        # Try Gemini evaluation if key is present
        if api_key:
            try:
                return await cls._evaluate_with_gemini(
                    q_data, student_text, api_key, model_name
                )
            except Exception as e:
                print(f"Gemini evaluation failed ({e}), falling back to deterministic grading.")

        # Fallback deterministic rule-based evaluation
        return cls._evaluate_deterministic(q_data, student_text)

    @classmethod
    async def _evaluate_with_gemini(
        cls,
        q_data: Dict[str, Any],
        student_text: str,
        api_key: str,
        model_name: str
    ) -> Dict[str, Any]:
        client = genai.Client(api_key=api_key)

        prompt = f"""Evaluate this student handwritten answer against the rubric:

### Question No: {q_data['question_no']} (ID: {q_data['question_id']})
Question: {q_data['question_text']}
Section Reference: {q_data.get('section_reference', '')}

### Model Answer:
{q_data['model_answer']}

### Expected Conclusion:
{q_data['expected_conclusion']}

### Mandatory Keywords / Phrases:
{json.dumps(q_data.get('mandatory_keywords', []))}

### Step-wise Rubric:
{json.dumps(q_data.get('steps', []), indent=2)}

### Student's Handwritten Answer (OCR Transcribed):
\"\"\"
{student_text}
\"\"\"

Please evaluate each rubric step and return strictly JSON in this format:
{{
  "question_no": {q_data['question_no']},
  "question_id": "{q_data['question_id']}",
  "marks_awarded": 3.5,
  "max_marks": {q_data['total_marks']},
  "keywords_matched": ["keyword 1", "keyword 2"],
  "keywords_missed": ["keyword 3"],
  "steps_evaluation": [
    {{
      "step_no": 1,
      "subpart": "subpart name",
      "marks_awarded": 1.0,
      "max_marks": 1.0,
      "status": "FULL_CREDIT",
      "criterion_met": true,
      "feedback": "Clear explanation of criterion..."
    }}
  ],
  "examiner_remarks": "Overall feedback...",
  "suggestions_for_improvement": "Actionable advice..."
}}
"""

        # Model candidates
        models = [model_name, "gemini-3.5-flash-lite", "gemini-2.5-flash", "gemini-2.0-flash-lite"]
        response = None
        for m in models:
            try:
                response = client.models.generate_content(
                    model=m,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                        response_mime_type="application/json"
                    )
                )
                if response and response.text:
                    break
            except Exception:
                continue

        if not response or not response.text:
            raise RuntimeError("Gemini returned empty response")

        raw = response.text.strip()
        if raw.startswith("```json"):
            raw = raw[7:]
        if raw.startswith("```"):
            raw = raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]

        data = json.loads(raw.strip())
        # Enforce numeric bounding
        max_m = float(q_data["total_marks"])
        awarded_m = min(max_m, max(0.0, float(data.get("marks_awarded", 0.0))))
        data["marks_awarded"] = round(awarded_m, 2)
        data["max_marks"] = max_m
        data["percentage"] = round((awarded_m / max_m) * 100, 1) if max_m > 0 else 0.0
        return data

    @classmethod
    def _evaluate_deterministic(cls, q_data: Dict[str, Any], student_text: str) -> Dict[str, Any]:
        """
        Deterministic rule-based grading based on keyword presence, concept matching, and numerical checks.
        """
        st_lower = student_text.lower()
        mandatory_keywords = q_data.get("mandatory_keywords", [])
        matched_kw = []
        missed_kw = []

        for kw in mandatory_keywords:
            kw_clean = kw.lower().strip()
            # Simple fuzzy / substring match
            if kw_clean in st_lower:
                matched_kw.append(kw)
            else:
                # Check for major words
                words = [w for w in kw_clean.split() if len(w) > 3]
                if words and all(w in st_lower for w in words):
                    matched_kw.append(kw)
                else:
                    missed_kw.append(kw)

        steps_eval = []
        total_awarded = 0.0
        steps = q_data.get("steps", [])

        for s in steps:
            s_marks = float(s["marks"])
            s_terms = s.get("key_terms", [])
            
            # Check presence of key terms for this step
            hits = 0
            for term in s_terms:
                t_lower = term.lower().strip()
                if t_lower in st_lower:
                    hits += 1
                else:
                    subwords = [w for w in t_lower.split() if len(w) > 3]
                    if subwords and any(w in st_lower for w in subwords):
                        hits += 0.5

            total_possible_hits = max(1, len(s_terms))
            ratio = min(1.0, hits / total_possible_hits)

            if ratio >= 0.75:
                awarded = s_marks
                status = "FULL_CREDIT"
                feedback = f"Criterion satisfied. Demonstrated understanding of {s['subpart']}."
            elif ratio >= 0.35:
                awarded = round(s_marks * 0.75, 2)
                status = "PARTIAL"
                feedback = s.get("feedback_if_missed") or f"Partially stated. Compare with model answer."
            else:
                awarded = round(s_marks * 0.25, 2)
                status = "PARTIAL"
                feedback = s.get("feedback_if_missed") or "Key statutory points omitted."

            awarded = min(s_marks, awarded)
            total_awarded += awarded

            steps_eval.append({
                "step_no": s["step_no"],
                "subpart": s["subpart"],
                "marks_awarded": awarded,
                "max_marks": s_marks,
                "status": status,
                "criterion_met": (status == "FULL_CREDIT"),
                "feedback": feedback
            })

        max_m = float(q_data.get("total_marks", sum(s["marks"] for s in steps)))
        total_awarded = round(min(max_m, total_awarded), 2)
        pct = round((total_awarded / max_m) * 100, 1) if max_m > 0 else 0.0

        remarks = "Well-structured answer with accurate legal conclusions." if pct >= 80 else "Good attempt; ensure complete statutory thresholds and rule numbers are cited."

        return {
            "question_no": q_data["question_no"],
            "question_id": q_data["question_id"],
            "marks_awarded": total_awarded,
            "max_marks": max_m,
            "percentage": pct,
            "keywords_matched": matched_kw,
            "keywords_missed": missed_kw,
            "steps_evaluation": steps_eval,
            "examiner_remarks": remarks,
            "suggestions_for_improvement": "Refer to the model answer to ensure comprehensive citation of sub-sections and rules."
        }

    @classmethod
    async def evaluate_full_exam(
        cls,
        parsed_rubric: Dict[str, Any],
        segmented_answers: Dict[int, Dict[str, Any]],
        api_key: Optional[str] = None,
        model_name: str = "gemini-3.5-flash-lite"
    ) -> Dict[str, Any]:
        """
        Executes end-to-end evaluation across all questions in the test.
        """
        start_time = time.time()
        questions = parsed_rubric["questions"]
        evaluated_questions = []

        total_awarded = 0.0
        total_max = 0.0

        for q in questions:
            q_no = q["question_no"]
            ans_data = segmented_answers.get(q_no, {})
            student_text = ans_data.get("full_student_text", "")
            page_numbers = ans_data.get("page_numbers", [])
            page_images = ans_data.get("page_images", [])

            eval_res = await cls.evaluate_question(
                q_data=q,
                student_text=student_text,
                api_key=api_key,
                model_name=model_name
            )

            eval_res["page_numbers"] = page_numbers
            eval_res["page_images"] = page_images
            eval_res["student_text"] = student_text
            eval_res["question_text"] = q["question_text"]
            eval_res["model_answer"] = q["model_answer"]
            eval_res["section_reference"] = q.get("section_reference", "")
            eval_res["expected_conclusion"] = q.get("expected_conclusion", "")

            evaluated_questions.append(eval_res)
            total_awarded += eval_res["marks_awarded"]
            total_max += eval_res["max_marks"]

        total_awarded = round(total_awarded, 2)
        total_max = round(total_max, 2)
        percentage = round((total_awarded / total_max) * 100, 1) if total_max > 0 else 0.0

        # Performance grade
        if percentage >= 90:
            grade = "Distinction / Outstanding"
        elif percentage >= 75:
            grade = "First Class / Excellent"
        elif percentage >= 60:
            grade = "Good / Proficient"
        elif percentage >= 50:
            grade = "Passing / Satisfactory"
        else:
            grade = "Needs Improvement"

        elapsed = round(time.time() - start_time, 2)

        return {
            "total_marks_awarded": total_awarded,
            "total_max_marks": total_max,
            "percentage": percentage,
            "performance_grade": grade,
            "total_questions": len(evaluated_questions),
            "evaluation_time_sec": elapsed,
            "questions": evaluated_questions
        }
