from pathlib import Path
from backend.services.document_scanner import DocumentScanner
import cv2

def test():
    sample_img = Path("backend/sample_data/sample_handwritten_notebook.pdf")
    from backend.services.pdf_processor import MultiPageProcessor
    out_dir = Path("backend/data/test_scan")
    pages = MultiPageProcessor.extract_pages_from_file(sample_img, out_dir, dpi=150)
    
    first_page = Path(pages[0]["file_path"])
    print(f"Testing on {first_page}")
    
    img = cv2.imread(str(first_page))
    corners = DocumentScanner.detect_document_corners(img)
    print(f"Detected corners: {corners}")
    
    out_magic = out_dir / "test_magic.jpg"
    DocumentScanner.process_scan(first_page, out_magic, corners=corners, filter_type="magic_color")
    print(f"Magic color saved to {out_magic}")

    out_bw = out_dir / "test_bw.jpg"
    DocumentScanner.process_scan(first_page, out_bw, corners=corners, filter_type="clean_bw")
    print(f"Clean B&W saved to {out_bw}")

if __name__ == "__main__":
    test()
