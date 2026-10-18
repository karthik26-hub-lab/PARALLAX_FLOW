import asyncio
import uuid
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from pydantic import BaseModel

from backend.config import settings, UPLOAD_DIR, PROCESSED_DIR, BASE_DIR
from backend.services.pdf_processor import MultiPageProcessor
from backend.services.rubric_parser import RubricParser
from backend.services.evaluator_engine import EvaluatorEngine
from backend.services.vision_engine import VisionOCREngine
from backend.services.easyocr_engine import LocalEasyOCREngine

class EvaluationJob(BaseModel):
    job_id: str
    created_at: str
    title: str
    status: str = "QUEUED"  # QUEUED, EXTRACTING_OCR, EVALUATING, COMPLETED, FAILED
    error_message: Optional[str] = None
    total_questions: int = 0
    total_marks_awarded: float = 0.0
    total_max_marks: float = 0.0
    percentage: float = 0.0
    performance_grade: str = ""
    evaluation_time_sec: float = 0.0
    questions: List[Dict[str, Any]] = []

class EvaluationJobManager:
    """
    Manages asynchronous exam evaluation jobs, linking OCR extraction,
    rubric parsing, and step-wise AI grading.
    """
    _jobs: Dict[str, EvaluationJob] = {}

    @classmethod
    def get_job(cls, job_id: str) -> Optional[EvaluationJob]:
        return cls._jobs.get(job_id)

    @classmethod
    def list_jobs(cls) -> List[EvaluationJob]:
        return sorted(cls._jobs.values(), key=lambda j: j.created_at, reverse=True)

    @classmethod
    async def create_demo_job(
        cls,
        api_key: Optional[str] = None,
        model_name: str = "gemini-3.5-flash-lite"
    ) -> EvaluationJob:
        """
        Instant 1-click evaluation of the Law Test - 1 benchmark dataset.
        """
        job_id = str(uuid.uuid4())
        job = EvaluationJob(
            job_id=job_id,
            created_at=datetime.utcnow().isoformat() + "Z",
            title="Law Test - 1 (Benchmark Evaluation)",
            status="EVALUATING"
        )
        cls._jobs[job_id] = job

        asyncio.create_task(
            cls._run_demo_evaluation(job, api_key or settings.GEMINI_API_KEY, model_name)
        )
        return job

    @classmethod
    async def _run_demo_evaluation(cls, job: EvaluationJob, api_key: Optional[str], model_name: str):
        try:
            demo_dir = BASE_DIR / "backend" / "sample_data" / "evaluation"
            excel_path = demo_dir / "Law_Test_1_Rubric_Master.xlsx"
            answers_path = demo_dir / "student_answers_demo.json"

            # 1. Parse Rubric
            excel_bytes = excel_path.read_bytes()
            rubric_data = RubricParser.parse_file(excel_bytes, "Law_Test_1_Rubric_Master.xlsx")

            # 2. Load Student Pages
            student_pages = json.loads(answers_path.read_text(encoding="utf-8"))

            # 3. Segment Answers
            segmented = EvaluatorEngine.segment_answers_to_questions(
                questions=rubric_data["questions"],
                pages=student_pages
            )

            # 4. Evaluate Full Exam
            eval_result = await EvaluatorEngine.evaluate_full_exam(
                parsed_rubric=rubric_data,
                segmented_answers=segmented,
                api_key=api_key,
                model_name=model_name
            )

            job.status = "COMPLETED"
            job.total_questions = eval_result["total_questions"]
            job.total_marks_awarded = eval_result["total_marks_awarded"]
            job.total_max_marks = eval_result["total_max_marks"]
            job.percentage = eval_result["percentage"]
            job.performance_grade = eval_result["performance_grade"]
            job.evaluation_time_sec = eval_result["evaluation_time_sec"]
            job.questions = eval_result["questions"]

        except Exception as e:
            job.status = "FAILED"
            job.error_message = str(e)

    @classmethod
    async def create_custom_evaluation_job(
        cls,
        title: str,
        student_file_path: Path,
        rubric_file_path: Path,
        question_file_path: Optional[Path] = None,
        api_key: Optional[str] = None,
        model_name: str = "gemini-3.5-flash-lite",
        ocr_engine: str = "gemini"
    ) -> EvaluationJob:
        job_id = str(uuid.uuid4())
        job = EvaluationJob(
            job_id=job_id,
            created_at=datetime.utcnow().isoformat() + "Z",
            title=title or "Exam Evaluation",
            status="EXTRACTING_OCR"
        )
        cls._jobs[job_id] = job

        asyncio.create_task(
            cls._run_custom_evaluation(
                job=job,
                student_file_path=student_file_path,
                rubric_file_path=rubric_file_path,
                question_file_path=question_file_path,
                api_key=api_key or settings.GEMINI_API_KEY,
                model_name=model_name,
                ocr_engine=ocr_engine
            )
        )
        return job

    @classmethod
    async def _run_custom_evaluation(
        cls,
        job: EvaluationJob,
        student_file_path: Path,
        rubric_file_path: Path,
        question_file_path: Optional[Path],
        api_key: Optional[str],
        model_name: str,
        ocr_engine: str
    ):
        try:
            job_dir = PROCESSED_DIR / f"eval_{job.job_id}"
            job_dir.mkdir(parents=True, exist_ok=True)

            # 1. Parse Rubric File (.xlsx or .csv)
            rubric_bytes = rubric_file_path.read_bytes()
            rubric_data = RubricParser.parse_file(rubric_bytes, rubric_file_path.name)

            # 2. Extract pages from student answer document
            extracted_pages = MultiPageProcessor.extract_pages_from_file(
                file_path=student_file_path,
                output_dir=job_dir,
                dpi=200
            )

            # 3. Transcribe each page using selected OCR engine
            loop = asyncio.get_event_loop()
            student_pages = []

            for p_info in extracted_pages:
                page_img = Path(p_info["file_path"])
                if ocr_engine == "gemini" and api_key:
                    ocr_res = await loop.run_in_executor(
                        None,
                        VisionOCREngine.transcribe_page,
                        page_img,
                        api_key,
                        model_name
                    )
                    text = ocr_res.get("transcription_markdown", "")
                else:
                    ocr_res = await loop.run_in_executor(
                        None,
                        LocalEasyOCREngine.transcribe_page,
                        page_img
                    )
                    text = ocr_res.get("transcription_markdown", "")

                student_pages.append({
                    "page_number": p_info["page_number"],
                    "filename": p_info["filename"],
                    "file_path": f"/data/processed/eval_{job.job_id}/{p_info['filename']}",
                    "transcription_markdown": text
                })

            # 4. Segment and evaluate
            job.status = "EVALUATING"
            segmented = EvaluatorEngine.segment_answers_to_questions(
                questions=rubric_data["questions"],
                pages=student_pages
            )

            eval_result = await EvaluatorEngine.evaluate_full_exam(
                parsed_rubric=rubric_data,
                segmented_answers=segmented,
                api_key=api_key,
                model_name=model_name
            )

            job.status = "COMPLETED"
            job.total_questions = eval_result["total_questions"]
            job.total_marks_awarded = eval_result["total_marks_awarded"]
            job.total_max_marks = eval_result["total_max_marks"]
            job.percentage = eval_result["percentage"]
            job.performance_grade = eval_result["performance_grade"]
            job.evaluation_time_sec = eval_result["evaluation_time_sec"]
            job.questions = eval_result["questions"]

        except Exception as e:
            job.status = "FAILED"
            job.error_message = str(e)

    @classmethod
    def export_job_report(cls, job_id: str, format_type: str = "md") -> str:
        job = cls.get_job(job_id)
        if not job:
            raise ValueError("Job not found")

        if format_type == "json":
            return job.model_dump_json(indent=2)

        elif format_type == "csv":
            import csv
            import io
            out = io.StringIO()
            writer = csv.writer(out)
            writer.writerow(["Question No", "Question ID", "Marks Awarded", "Max Marks", "Percentage", "Keywords Matched", "Keywords Missed", "Remarks"])
            for q in job.questions:
                writer.writerow([
                    q["question_no"],
                    q["question_id"],
                    q["marks_awarded"],
                    q["max_marks"],
                    f"{q.get('percentage', 0)}%",
                    " | ".join(q.get("keywords_matched", [])),
                    " | ".join(q.get("keywords_missed", [])),
                    q.get("examiner_remarks", "")
                ])
            return out.getvalue()

        else: # Markdown report
            lines = [
                f"# Evaluation Report: {job.title}",
                f"**Date:** {job.created_at} | **Evaluation Time:** {job.evaluation_time_sec}s",
                f"**Total Score:** {job.total_marks_awarded} / {job.total_max_marks} ({job.percentage}%) — **{job.performance_grade}**",
                "",
                "---",
                "## Question-by-Question Scorecard",
                ""
            ]

            for q in job.questions:
                lines.extend([
                    f"### Question {q['question_no']} ({q['question_id']}) — Score: {q['marks_awarded']} / {q['max_marks']} ({q.get('percentage', 0)}%)",
                    f"**Question Statement:** {q.get('question_text', '')}",
                    f"**Section Reference:** {q.get('section_reference', '')}",
                    "",
                    "#### Step-Wise Rubric Breakdown:",
                    "| Step No | Subpart | Criterion / What Earns Mark | Marks Awarded | Max Marks | Status | Feedback |",
                    "| :---: | :--- | :--- | :---: | :---: | :---: | :--- |"
                ])
                for s in q.get("steps_evaluation", []):
                    lines.append(
                        f"| {s['step_no']} | {s['subpart']} | {s.get('what_earns_mark') or s.get('criterion', '')} | **{s['marks_awarded']}** | {s['max_marks']} | {s['status']} | {s.get('feedback', '')} |"
                    )
                lines.extend([
                    "",
                    f"**Keywords Matched:** {', '.join(q.get('keywords_matched', [])) or 'None'}",
                    f"**Keywords Missed:** {', '.join(q.get('keywords_missed', [])) or 'None'}",
                    f"**Examiner Remarks:** {q.get('examiner_remarks', '')}",
                    "",
                    "---"
                ])
            return "\n".join(lines)
