import asyncio
from pathlib import Path
from backend.services.job_manager import JobManager
from backend.config import settings

async def main():
    sample_pdf = Path("backend/sample_data/sample_handwritten_notebook.pdf")
    print(f"Testing extraction with EasyOCR on {sample_pdf}...")
    
    job = await JobManager.create_job_from_file(
        upload_path=sample_pdf,
        original_filename="sample_handwritten_notebook.pdf",
        engine="easyocr",
        model_name="easyocr-v1",
        auto_deskew=True,
        remove_shadow=True,
        boost_contrast=True
    )
    
    print(f"Job created: {job.job_id}. Pages: {job.total_pages}. Processing...")
    
    # Wait until finished
    while True:
        await asyncio.sleep(1)
        cur = JobManager.get_job(job.job_id)
        print(f"Status: {cur.status} ({cur.completed_pages}/{cur.total_pages} pages)")
        if cur.status in ("COMPLETED", "FAILED"):
            print("\n--- RESULTS ---")
            print(f"Total time: {cur.total_processing_time}s")
            for p in cur.pages:
                print(f"\nPage {p.page_number} ({p.status}):")
                print(f"Confidence: {p.estimated_confidence_percent}% ({p.confidence_rating})")
                print(f"Text snippet: {p.transcription_markdown[:150]}...")
            break

if __name__ == "__main__":
    asyncio.run(main())
