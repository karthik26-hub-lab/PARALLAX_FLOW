import json
import zipfile
import io
from pathlib import Path
from typing import Optional
from backend.services.job_manager import BatchJob
from backend.config import PROCESSED_DIR

class ExportService:
    """
    Exports processed multi-page OCR jobs into multiple production formats:
    Markdown, Plain Text, Structured JSON, and ZIP bundle.
    """

    @staticmethod
    def to_markdown(job: BatchJob, single_page: Optional[int] = None) -> str:
        if single_page is not None:
            for p in job.pages:
                if p.page_number == single_page:
                    return f"# {job.filename} - Page {p.page_number}\n\n{p.transcription_markdown}"
            return ""
        return job.combined_markdown

    @staticmethod
    def to_plain_text(job: BatchJob, single_page: Optional[int] = None) -> str:
        md = ExportService.to_markdown(job, single_page=single_page)
        # Strip simple markdown markers for raw plain text
        import re
        txt = re.sub(r'#+\s*', '', md)
        txt = re.sub(r'\*\*(.*?)\*\*', r'\1', txt)
        txt = re.sub(r'\*(.*?)\*', r'\1', txt)
        txt = re.sub(r'~~(.*?)~~', r'\1', txt)
        txt = re.sub(r'`(.*?)`', r'\1', txt)
        return txt

    @staticmethod
    def to_structured_json(job: BatchJob) -> str:
        return job.model_dump_json(indent=2)

    @staticmethod
    def create_export_zip(job: BatchJob) -> bytes:
        """
        Creates a comprehensive ZIP bundle containing:
        - full_transcription.md
        - full_transcription.txt
        - document_data.json
        - pages/page_001.md, page_002.md...
        - images/enhanced_001.jpg, enhanced_002.jpg...
        """
        buf = io.BytesIO()
        job_dir = PROCESSED_DIR / job.job_id

        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
            # Combined text files
            zf.writestr("transcription.md", ExportService.to_markdown(job))
            zf.writestr("transcription.txt", ExportService.to_plain_text(job))
            zf.writestr("metadata.json", ExportService.to_structured_json(job))

            # Page by page text and enhanced images
            for p in job.pages:
                zf.writestr(f"pages/page_{p.page_number:03d}.md", p.transcription_markdown)
                if p.processed_file:
                    local_img = job_dir / f"enhanced_{p.page_number:03d}.jpg"
                    if local_img.exists():
                        zf.write(local_img, arcname=f"images/page_{p.page_number:03d}_enhanced.jpg")

        buf.seek(0)
        return buf.getvalue()
