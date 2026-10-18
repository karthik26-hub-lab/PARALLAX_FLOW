import json
import shutil
import cv2
import numpy as np
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.config import settings, UPLOAD_DIR, PROCESSED_DIR, BASE_DIR
from backend.services.job_manager import JobManager, BatchJob
from backend.services.document_scanner import DocumentScanner
from backend.services.export_service import ExportService
from backend.services.evaluation_job_manager import EvaluationJobManager, EvaluationJob

app = FastAPI(
    title="ParallaxFlow OCR - Production Handwriting Engine",
    description="High-production OCR and Handwritten Text Recognition system for multi-page documents",
    version="1.1.0"
)

# Enable CORS for development and production web frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static file access for document images and thumbnails
app.mount("/data/processed", StaticFiles(directory=str(PROCESSED_DIR)), name="processed_data")

class PageEditRequest(BaseModel):
    transcription_markdown: str

class RescanPageRequest(BaseModel):
    corners: Optional[List[List[float]]] = None
    scan_filter: str = "magic_color"
    custom_prompt: Optional[str] = None

@app.get("/api/config")
async def get_system_config():
    """Returns active backend configuration and available OCR engines."""
    return {
        "appName": settings.APP_NAME,
        "defaultEngine": settings.DEFAULT_ENGINE,
        "hasEnvGeminiKey": bool(settings.GEMINI_API_KEY and len(settings.GEMINI_API_KEY) > 5),
        "availableEngines": [
            {
                "id": "gemini",
                "name": "Gemini Multimodal Vision (High Accuracy)",
                "description": "State-of-the-art accuracy for cursive handwriting, complex notes, strikethroughs, and tables",
                "models": ["gemini-3.5-flash-lite", "gemini-2.5-flash", "gemini-2.5-pro"],
                "requiresKey": True
            },
            {
                "id": "easyocr",
                "name": "EasyOCR Local Engine (100% Offline)",
                "description": "Open-source deep learning OCR running locally on CPU/GPU without cloud API keys",
                "models": ["easyocr-v1"],
                "requiresKey": False
            }
        ],
        "availableFilters": [
            {"id": "magic_color", "name": "Magic Color", "desc": "CamScanner clean white background with vivid ink"},
            {"id": "clean_bw", "name": "Clean B&W", "desc": "High-contrast binary document, zero bleed-through"},
            {"id": "grayscale", "name": "Grayscale Clean", "desc": "Studio even-lighting monochrome scan"},
            {"id": "enhanced", "name": "Contrast Boost", "desc": "Sharpens faint ink strokes with CLAHE"},
            {"id": "original", "name": "Original", "desc": "Raw perspective-flattened capture"}
        ]
    }

@app.post("/api/scan/detect-corners")
async def detect_document_corners(file: UploadFile = File(...)):
    """
    Analyzes an uploaded or camera-captured document image and detects
    the 4 corners of the paper boundary.
    """
    file_bytes = await file.read()
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    h, w = img.shape[:2]
    corners = DocumentScanner.detect_document_corners(img)
    return {
        "width": w,
        "height": h,
        "corners": corners
    }

@app.post("/api/scan/preview")
async def preview_scan_filter(
    file: UploadFile = File(...),
    corners_json: Optional[str] = Form(None),
    filter_type: str = Form("magic_color")
):
    """
    Generates a live preview of perspective warp + selected scan filter.
    Returns processed JPEG image.
    """
    file_bytes = await file.read()
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image file")

    corners = None
    if corners_json:
        try:
            corners = json.loads(corners_json)
        except Exception:
            pass

    if corners:
        warped = DocumentScanner.perspective_warp(img, corners)
    else:
        warped = img

    if filter_type == "magic_color":
        result = DocumentScanner.apply_magic_color(warped)
    elif filter_type == "clean_bw":
        result = DocumentScanner.apply_clean_bw(warped)
    elif filter_type == "grayscale":
        result = DocumentScanner.apply_grayscale_scan(warped)
    elif filter_type == "enhanced":
        lab = cv2.cvtColor(warped, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        l = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8)).apply(l)
        result = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)
    else:
        result = warped

    _, encoded = cv2.imencode(".jpg", result, [cv2.IMWRITE_JPEG_QUALITY, 90])
    return Response(content=encoded.tobytes(), media_type="image/jpeg")

@app.post("/api/upload")
async def upload_document(
    file: UploadFile = File(...),
    engine: str = Form("gemini"),
    model_name: str = Form("gemini-3.5-flash-lite"),
    scan_filter: str = Form("magic_color"),
    auto_warp: bool = Form(True),
    api_key: Optional[str] = Form(None),
    custom_prompt: Optional[str] = Form(None),
    x_api_key: Optional[str] = Header(None)
):
    """
    Ingests multi-page documents (PDF, ZIP, image bundle) and starts
    parallel page extraction job.
    """
    resolved_key = api_key or x_api_key or settings.GEMINI_API_KEY

    if engine == "gemini" and not resolved_key:
        raise HTTPException(
            status_code=400,
            detail="Gemini API Key is required for Vision OCR. Please provide it in settings or choose the local EasyOCR engine."
        )

    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        job = await JobManager.create_job_from_file(
            upload_path=file_path,
            original_filename=file.filename,
            engine=engine,
            model_name=model_name,
            api_key=resolved_key,
            custom_prompt=custom_prompt,
            scan_filter=scan_filter,
            auto_warp=auto_warp
        )
        return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

@app.post("/api/scan/batch")
async def upload_camera_scan_batch(
    files: List[UploadFile] = File(...),
    engine: str = Form("gemini"),
    model_name: str = Form("gemini-3.5-flash-lite"),
    scan_filter: str = Form("magic_color"),
    api_key: Optional[str] = Form(None),
    custom_prompt: Optional[str] = Form(None),
    x_api_key: Optional[str] = Header(None)
):
    """
    Receives an ordered array of camera-scanned page photos and kicks off
    a multi-page OCR job.
    """
    resolved_key = api_key or x_api_key or settings.GEMINI_API_KEY
    if engine == "gemini" and not resolved_key:
        raise HTTPException(status_code=400, detail="Gemini API key is required for Vision OCR.")

    batch_id = f"cam_scan_{cv2.getTickCount()}"
    batch_dir = UPLOAD_DIR / batch_id
    batch_dir.mkdir(parents=True, exist_ok=True)

    # Save pages into zip
    import zipfile
    zip_path = UPLOAD_DIR / f"{batch_id}.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for idx, f in enumerate(files, start=1):
            page_data = await f.read()
            zf.writestr(f"page_{idx:03d}.jpg", page_data)

    job = await JobManager.create_job_from_file(
        upload_path=zip_path,
        original_filename=f"Camera_Scan_{len(files)}_Pages.pdf",
        engine=engine,
        model_name=model_name,
        api_key=resolved_key,
        custom_prompt=custom_prompt,
        scan_filter=scan_filter,
        auto_warp=True
    )
    return job

@app.post("/api/jobs/{job_id}/pages/{page_number}/rescan")
async def rescan_single_page(
    job_id: str,
    page_number: int,
    req: RescanPageRequest,
    x_api_key: Optional[str] = Header(None)
):
    """
    Allows user to re-crop/re-filter an already processed page and re-run OCR!
    """
    try:
        updated_page = await JobManager.rescan_single_page(
            job_id=job_id,
            page_number=page_number,
            corners=req.corners,
            scan_filter=req.scan_filter,
            api_key=x_api_key or settings.GEMINI_API_KEY,
            custom_prompt=req.custom_prompt
        )
        return updated_page
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to rescan page: {str(e)}")

@app.post("/api/sample")
async def process_sample_document(
    engine: str = "easyocr",
    model_name: str = "easyocr-v1",
    scan_filter: str = "magic_color",
    api_key: Optional[str] = None,
    x_api_key: Optional[str] = Header(None)
):
    """Triggers an OCR batch run on the sample 3-page handwritten document."""
    sample_file = BASE_DIR / "backend" / "sample_data" / "sample_handwritten_notebook.pdf"
    if not sample_file.exists():
        from backend.sample_data.create_sample import create_sample_handwritten_pdf
        create_sample_handwritten_pdf(sample_file)

    resolved_key = api_key or x_api_key or settings.GEMINI_API_KEY
    if engine == "gemini" and not resolved_key:
        engine = "easyocr"
        model_name = "easyocr-v1"

    job = await JobManager.create_job_from_file(
        upload_path=sample_file,
        original_filename="sample_handwritten_notebook.pdf",
        engine=engine,
        model_name=model_name,
        api_key=resolved_key,
        scan_filter=scan_filter,
        auto_warp=True
    )
    return job

@app.get("/api/jobs")
async def list_jobs():
    """Lists all OCR batch processing jobs."""
    return JobManager.list_jobs()

@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str):
    """Retrieves full job status and all extracted pages."""
    job = JobManager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.patch("/api/jobs/{job_id}/pages/{page_number}")
async def update_page_transcription(job_id: str, page_number: int, edit: PageEditRequest):
    """Allows human-in-the-loop review and correction of transcribed text."""
    job = JobManager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    target_page = None
    for p in job.pages:
        if p.page_number == page_number:
            target_page = p
            break

    if not target_page:
        raise HTTPException(status_code=404, detail=f"Page {page_number} not found")

    target_page.transcription_markdown = edit.transcription_markdown
    target_page.char_count = len(edit.transcription_markdown)
    target_page.word_count = len(edit.transcription_markdown.split())

    JobManager._rebuild_combined_markdown(job)
    JobManager._notify_update(job_id)
    return target_page

@app.get("/api/jobs/{job_id}/export/{export_format}")
async def export_job(job_id: str, export_format: str, page: Optional[int] = Query(None)):
    """Exports OCR results into MD, TXT, JSON, or ZIP bundle."""
    job = JobManager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    safe_name = Path(job.filename).stem

    if export_format == "md":
        content = ExportService.to_markdown(job, single_page=page)
        filename = f"{safe_name}_page_{page}.md" if page else f"{safe_name}_full.md"
        return Response(content=content, media_type="text/markdown", headers={"Content-Disposition": f'attachment; filename="{filename}"'})

    elif export_format == "txt":
        content = ExportService.to_plain_text(job, single_page=page)
        filename = f"{safe_name}_page_{page}.txt" if page else f"{safe_name}_full.txt"
        return Response(content=content, media_type="text/plain", headers={"Content-Disposition": f'attachment; filename="{filename}"'})

    elif export_format == "json":
        content = ExportService.to_structured_json(job)
        return Response(content=content, media_type="application/json", headers={"Content-Disposition": f'attachment; filename="{safe_name}_metadata.json"'})

    elif export_format == "zip":
        zip_bytes = ExportService.create_export_zip(job)
        return Response(content=zip_bytes, media_type="application/zip", headers={"Content-Disposition": f'attachment; filename="{safe_name}_ocr_bundle.zip"'})

    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format: {export_format}. Use md, txt, json, or zip.")

# ==========================================
# Automated Exam & Rubric Evaluation Routes
# ==========================================

@app.post("/api/evaluate/demo")
async def trigger_demo_evaluation(
    model_name: str = "gemini-3.5-flash-lite",
    api_key: Optional[str] = None,
    x_api_key: Optional[str] = Header(None)
):
    """
    Triggers an instant evaluation on the benchmark Law Test - 1 exam paper
    using the official step-wise rubric and mandatory keywords.
    """
    resolved_key = api_key or x_api_key or settings.GEMINI_API_KEY
    job = await EvaluationJobManager.create_demo_job(
        api_key=resolved_key,
        model_name=model_name
    )
    return job

@app.post("/api/evaluate/upload")
async def upload_custom_evaluation(
    student_file: UploadFile = File(...),
    rubric_file: UploadFile = File(...),
    title: str = Form("Exam Paper Evaluation"),
    model_name: str = Form("gemini-3.5-flash-lite"),
    ocr_engine: str = Form("gemini"),
    api_key: Optional[str] = Form(None),
    x_api_key: Optional[str] = Header(None)
):
    """
    Ingests a student answer document (PDF or images) along with a Rubric
    spreadsheet (.xlsx or .csv) and launches an automated grading run.
    """
    resolved_key = api_key or x_api_key or settings.GEMINI_API_KEY

    # Save uploaded files
    student_path = UPLOAD_DIR / f"student_{student_file.filename}"
    with open(student_path, "wb") as buf:
        shutil.copyfileobj(student_file.file, buf)

    rubric_path = UPLOAD_DIR / f"rubric_{rubric_file.filename}"
    with open(rubric_path, "wb") as buf:
        shutil.copyfileobj(rubric_file.file, buf)

    try:
        job = await EvaluationJobManager.create_custom_evaluation_job(
            title=title,
            student_file_path=student_path,
            rubric_file_path=rubric_path,
            api_key=resolved_key,
            model_name=model_name,
            ocr_engine=ocr_engine
        )
        return job
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initiate evaluation: {str(e)}")

@app.get("/api/evaluate/jobs")
async def list_evaluation_jobs():
    """Returns list of all evaluation jobs."""
    return EvaluationJobManager.list_jobs()

@app.get("/api/evaluate/jobs/{job_id}")
async def get_evaluation_job(job_id: str):
    """Retrieves detailed question-by-question evaluation report."""
    job = EvaluationJobManager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Evaluation job not found")
    return job

@app.get("/api/evaluate/jobs/{job_id}/export/{export_format}")
async def export_evaluation_report(job_id: str, export_format: str):
    """Exports evaluation marksheet as Markdown, CSV, or JSON."""
    try:
        content = EvaluationJobManager.export_job_report(job_id, export_format)
        if export_format == "json":
            return Response(content=content, media_type="application/json", headers={"Content-Disposition": f'attachment; filename="evaluation_{job_id}.json"'})
        elif export_format == "csv":
            return Response(content=content, media_type="text/csv", headers={"Content-Disposition": f'attachment; filename="evaluation_{job_id}.csv"'})
        else:
            return Response(content=content, media_type="text/markdown", headers={"Content-Disposition": f'attachment; filename="evaluation_{job_id}.md"'})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Serve CA Academy Evaluator static application
CA_EVALUATOR_DIR = BASE_DIR / "ca_evaluator"
if CA_EVALUATOR_DIR.exists():
    app.mount("/ca-evaluator", StaticFiles(directory=str(CA_EVALUATOR_DIR), html=True), name="ca_evaluator")

# Serve frontend production bundle if built
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="frontend")

