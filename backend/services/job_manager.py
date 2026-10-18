import asyncio
import uuid
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel

from backend.config import UPLOAD_DIR, PROCESSED_DIR, settings
from backend.services.pdf_processor import MultiPageProcessor
from backend.services.document_scanner import DocumentScanner
from backend.services.vision_engine import VisionOCREngine
from backend.services.easyocr_engine import LocalEasyOCREngine

class PageStatus(BaseModel):
    page_number: int
    original_file: str
    thumbnail_file: str
    processed_file: Optional[str] = None
    status: str = "PENDING"  # PENDING, PREPROCESSING, TRANSCRIBING, COMPLETED, ERROR
    error_message: Optional[str] = None
    transcription_markdown: str = ""
    summary: str = ""
    confidence_rating: str = "UNKNOWN"
    estimated_confidence_percent: int = 0
    handwriting_style: str = ""
    document_type: str = ""
    key_entities: List[str] = []
    engine_used: str = ""
    processing_time_sec: float = 0.0
    char_count: int = 0
    word_count: int = 0
    scan_filter: str = "magic_color"
    corners: Optional[List[List[float]]] = None
    preprocessing_meta: Dict[str, Any] = {}

class BatchJob(BaseModel):
    job_id: str
    created_at: str
    filename: str
    file_type: str
    total_pages: int = 0
    completed_pages: int = 0
    status: str = "QUEUED"  # QUEUED, PROCESSING, COMPLETED, FAILED
    error_message: Optional[str] = None
    engine: str = "gemini"
    model_name: str = "gemini-3.5-flash-lite"
    scan_filter: str = "magic_color"
    auto_warp: bool = True
    pages: List[PageStatus] = []
    combined_markdown: str = ""
    total_processing_time: float = 0.0

class JobManager:
    """
    Production asynchronous batch job manager for multi-page handwritten OCR.
    Handles concurrency, queueing, state persistence, document scanning & live subscriptions.
    """
    _jobs: Dict[str, BatchJob] = {}
    _listeners: Dict[str, List[asyncio.Queue]] = {}

    @classmethod
    def get_job(cls, job_id: str) -> Optional[BatchJob]:
        return cls._jobs.get(job_id)

    @classmethod
    def list_jobs(cls) -> List[BatchJob]:
        return sorted(cls._jobs.values(), key=lambda j: j.created_at, reverse=True)

    @classmethod
    async def create_job_from_file(
        cls,
        upload_path: Path,
        original_filename: str,
        engine: str = "gemini",
        model_name: str = "gemini-3.5-flash-lite",
        api_key: Optional[str] = None,
        custom_prompt: Optional[str] = None,
        scan_filter: str = "magic_color",
        auto_warp: bool = True,
        page_corners: Optional[Dict[int, List[List[float]]]] = None
    ) -> BatchJob:
        job_id = str(uuid.uuid4())
        job_dir = PROCESSED_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=True)

        # 1. Extract pages (PDF to 300 DPI, ZIP, or single image)
        extracted_pages = MultiPageProcessor.extract_pages_from_file(
            file_path=upload_path,
            output_dir=job_dir,
            dpi=settings.RENDER_DPI
        )

        pages_status = [
            PageStatus(
                page_number=p["page_number"],
                original_file=f"/data/processed/{job_id}/{Path(p['file_path']).name}",
                thumbnail_file=f"/data/processed/{job_id}/{Path(p['thumbnail_path']).name}",
                scan_filter=scan_filter,
                corners=page_corners.get(p["page_number"]) if page_corners else None,
                status="PENDING"
            )
            for p in extracted_pages
        ]

        job = BatchJob(
            job_id=job_id,
            created_at=datetime.utcnow().isoformat() + "Z",
            filename=original_filename,
            file_type=upload_path.suffix.lower(),
            total_pages=len(extracted_pages),
            completed_pages=0,
            status="PROCESSING",
            engine=engine,
            model_name=model_name,
            scan_filter=scan_filter,
            auto_warp=auto_warp,
            pages=pages_status
        )
        cls._jobs[job_id] = job

        # Launch background processing task
        asyncio.create_task(
            cls._process_job_pages(
                job=job,
                extracted_pages=extracted_pages,
                job_dir=job_dir,
                engine=engine,
                model_name=model_name,
                api_key=api_key or settings.GEMINI_API_KEY,
                custom_prompt=custom_prompt,
                scan_filter=scan_filter,
                auto_warp=auto_warp
            )
        )

        return job

    @classmethod
    async def _process_job_pages(
        cls,
        job: BatchJob,
        extracted_pages: List[Dict[str, Any]],
        job_dir: Path,
        engine: str,
        model_name: str,
        api_key: Optional[str],
        custom_prompt: Optional[str],
        scan_filter: str,
        auto_warp: bool
    ):
        start_all = time.time()
        semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_PAGES)

        async def process_single_page(idx: int, page_info: Dict[str, Any]):
            page_status = job.pages[idx]
            async with semaphore:
                try:
                    # 1. Document Scanning & Preprocessing
                    page_status.status = "PREPROCESSING"
                    cls._notify_update(job.job_id)

                    raw_path = Path(page_info["file_path"])
                    enhanced_filename = f"scanned_{page_status.page_number:03d}.jpg"
                    enhanced_path = job_dir / enhanced_filename

                    loop = asyncio.get_event_loop()
                    enhanced_out, meta = await loop.run_in_executor(
                        None,
                        DocumentScanner.process_scan,
                        raw_path,
                        enhanced_path,
                        page_status.corners,
                        scan_filter,
                        auto_warp
                    )
                    page_status.processed_file = f"/data/processed/{job.job_id}/{enhanced_filename}"
                    page_status.preprocessing_meta = meta
                    if "corners_detected" in meta and not page_status.corners:
                        page_status.corners = meta["corners_detected"]

                    # 2. Transcription
                    page_status.status = "TRANSCRIBING"
                    cls._notify_update(job.job_id)

                    if engine == "gemini":
                        result = await loop.run_in_executor(
                            None,
                            VisionOCREngine.transcribe_page,
                            enhanced_out,
                            api_key,
                            model_name,
                            custom_prompt
                        )
                    else:
                        result = await loop.run_in_executor(
                            None,
                            LocalEasyOCREngine.transcribe_page,
                            enhanced_out
                        )

                    # Populate results
                    page_status.status = "COMPLETED"
                    page_status.transcription_markdown = result.get("transcription_markdown", "")
                    page_status.summary = result.get("summary", "")
                    page_status.confidence_rating = result.get("confidence_rating", "HIGH")
                    page_status.estimated_confidence_percent = result.get("estimated_confidence_percent", 90)
                    page_status.handwriting_style = result.get("handwriting_style", "")
                    page_status.document_type = result.get("document_type", "")
                    page_status.key_entities = result.get("key_entities", [])
                    page_status.engine_used = result.get("engine", engine)
                    page_status.processing_time_sec = result.get("processing_time_sec", 0.0)
                    page_status.char_count = result.get("char_count", 0)
                    page_status.word_count = result.get("word_count", 0)

                    job.completed_pages += 1

                except Exception as e:
                    page_status.status = "ERROR"
                    page_status.error_message = str(e)
                    job.completed_pages += 1
                finally:
                    cls._notify_update(job.job_id)

        tasks = [
            process_single_page(idx, page_info)
            for idx, page_info in enumerate(extracted_pages)
        ]
        await asyncio.gather(*tasks)

        # Assemble full combined document
        total_time = round(time.time() - start_all, 2)
        job.total_processing_time = total_time
        
        all_errors = all(p.status == "ERROR" for p in job.pages)
        job.status = "FAILED" if all_errors and len(job.pages) > 0 else "COMPLETED"

        cls._rebuild_combined_markdown(job)
        cls._notify_update(job.job_id)

    @classmethod
    def _rebuild_combined_markdown(cls, job: BatchJob):
        doc_parts = [f"# {job.filename}\n_Processed with {job.engine} in {job.total_processing_time}s (Filter: {job.scan_filter})_\n"]
        for p in job.pages:
            doc_parts.append(f"\n---\n## Page {p.page_number}\n")
            if p.status == "COMPLETED":
                doc_parts.append(p.transcription_markdown)
            else:
                doc_parts.append(f"> [Error on page {p.page_number}: {p.error_message}]")
        job.combined_markdown = "\n".join(doc_parts)

    @classmethod
    async def rescan_single_page(
        cls,
        job_id: str,
        page_number: int,
        corners: Optional[List[List[float]]] = None,
        scan_filter: str = "magic_color",
        api_key: Optional[str] = None,
        custom_prompt: Optional[str] = None
    ) -> PageStatus:
        """
        Allows interactive re-cropping and re-filtering of any individual page!
        """
        job = cls.get_job(job_id)
        if not job:
            raise ValueError("Job not found")

        page_status = next((p for p in job.pages if p.page_number == page_number), None)
        if not page_status:
            raise ValueError(f"Page {page_number} not found")

        job_dir = PROCESSED_DIR / job_id
        # Derive original file path on disk
        raw_filename = f"page_{page_number:03d}.jpg"
        raw_path = job_dir / raw_filename

        enhanced_filename = f"scanned_{page_number:03d}.jpg"
        enhanced_path = job_dir / enhanced_filename

        page_status.status = "PREPROCESSING"
        page_status.scan_filter = scan_filter
        if corners is not None:
            page_status.corners = corners
        cls._notify_update(job_id)

        loop = asyncio.get_event_loop()
        enhanced_out, meta = await loop.run_in_executor(
            None,
            DocumentScanner.process_scan,
            raw_path,
            enhanced_path,
            page_status.corners,
            scan_filter,
            True
        )

        page_status.processed_file = f"/data/processed/{job_id}/{enhanced_filename}"
        page_status.preprocessing_meta = meta

        # Re-run OCR
        page_status.status = "TRANSCRIBING"
        cls._notify_update(job_id)

        resolved_key = api_key or settings.GEMINI_API_KEY
        if job.engine == "gemini":
            result = await loop.run_in_executor(
                None,
                VisionOCREngine.transcribe_page,
                enhanced_out,
                resolved_key,
                job.model_name,
                custom_prompt
            )
        else:
            result = await loop.run_in_executor(
                None,
                LocalEasyOCREngine.transcribe_page,
                enhanced_out
            )

        page_status.status = "COMPLETED"
        page_status.transcription_markdown = result.get("transcription_markdown", "")
        page_status.summary = result.get("summary", "")
        page_status.confidence_rating = result.get("confidence_rating", "HIGH")
        page_status.estimated_confidence_percent = result.get("estimated_confidence_percent", 90)
        page_status.handwriting_style = result.get("handwriting_style", "")
        page_status.document_type = result.get("document_type", "")
        page_status.key_entities = result.get("key_entities", [])
        page_status.processing_time_sec = result.get("processing_time_sec", 0.0)
        page_status.char_count = result.get("char_count", 0)
        page_status.word_count = result.get("word_count", 0)

        cls._rebuild_combined_markdown(job)
        cls._notify_update(job_id)
        return page_status

    @classmethod
    def _notify_update(cls, job_id: str):
        if job_id in cls._listeners:
            for q in cls._listeners[job_id]:
                try:
                    q.put_nowait(True)
                except Exception:
                    pass

    @classmethod
    async def subscribe(cls, job_id: str) -> asyncio.Queue:
        q = asyncio.Queue()
        if job_id not in cls._listeners:
            cls._listeners[job_id] = []
        cls._listeners[job_id].append(q)
        return q

    @classmethod
    def unsubscribe(cls, job_id: str, q: asyncio.Queue):
        if job_id in cls._listeners and q in cls._listeners[job_id]:
            cls._listeners[job_id].remove(q)
