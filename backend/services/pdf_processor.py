import fitz  # PyMuPDF
from PIL import Image
import zipfile
from pathlib import Path
from typing import List, Dict, Any
import shutil

class MultiPageProcessor:
    """
    Extracts individual high-resolution page images from PDFs, ZIP archives,
    or image sequences for multi-page handwritten document processing.
    """

    SUPPORTED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}

    @classmethod
    def extract_pages_from_file(cls, file_path: Path, output_dir: Path, dpi: int = 300) -> List[Dict[str, Any]]:
        """
        Takes any input file (PDF, ZIP, or single image) and decomposes it
        into a sequentially numbered list of page image files.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        ext = file_path.suffix.lower()

        if ext == ".pdf":
            return cls._extract_from_pdf(file_path, output_dir, dpi=dpi)
        elif ext == ".zip":
            return cls._extract_from_zip(file_path, output_dir)
        elif ext in cls.SUPPORTED_IMAGE_EXTS:
            return cls._extract_from_single_image(file_path, output_dir)
        else:
            raise ValueError(f"Unsupported file format: {ext}. Supported: PDF, ZIP, PNG, JPG, JPEG, WEBP, TIFF")

    @classmethod
    def _extract_from_pdf(cls, pdf_path: Path, output_dir: Path, dpi: int = 300) -> List[Dict[str, Any]]:
        pages = []
        doc = fitz.open(str(pdf_path))
        # Calculate zoom matrix for requested DPI (72 is standard base DPI)
        zoom = dpi / 72.0
        mat = fitz.Matrix(zoom, zoom)

        for page_idx in range(len(doc)):
            page_num = page_idx + 1
            page = doc.load_page(page_idx)
            # Render page to high-res pixmap
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            page_filename = f"page_{page_num:03d}.jpg"
            page_path = output_dir / page_filename
            pix.save(str(page_path))

            # Create lightweight thumbnail for fast UI previews
            thumb_filename = f"thumb_{page_num:03d}.jpg"
            thumb_path = output_dir / thumb_filename
            thumb_mat = fitz.Matrix(0.3, 0.3)
            thumb_pix = page.get_pixmap(matrix=thumb_mat, alpha=False)
            thumb_pix.save(str(thumb_path))

            pages.append({
                "page_number": page_num,
                "file_path": str(page_path),
                "thumbnail_path": str(thumb_path),
                "filename": page_filename,
                "width": pix.width,
                "height": pix.height,
                "dpi": dpi
            })

        doc.close()
        return pages

    @classmethod
    def _extract_from_zip(cls, zip_path: Path, output_dir: Path) -> List[Dict[str, Any]]:
        pages = []
        temp_dir = output_dir / "_zip_temp"
        temp_dir.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(str(zip_path), 'r') as zip_ref:
            zip_ref.extractall(str(temp_dir))

        # Collect image files in alphabetical order
        extracted_files = sorted(
            [f for f in temp_dir.rglob("*") if f.suffix.lower() in cls.SUPPORTED_IMAGE_EXTS and not f.name.startswith(".")],
            key=lambda x: x.name
        )

        for idx, src_file in enumerate(extracted_files, start=1):
            dest_filename = f"page_{idx:03d}.jpg"
            dest_path = output_dir / dest_filename
            
            # Standardize and save as high-quality JPEG
            with Image.open(src_file) as img:
                rgb_img = img.convert("RGB")
                rgb_img.save(dest_path, "JPEG", quality=95)
                width, height = rgb_img.size

                # Thumbnail
                thumb_path = output_dir / f"thumb_{idx:03d}.jpg"
                thumb_img = rgb_img.copy()
                thumb_img.thumbnail((300, 400))
                thumb_img.save(thumb_path, "JPEG", quality=85)

            pages.append({
                "page_number": idx,
                "file_path": str(dest_path),
                "thumbnail_path": str(thumb_path),
                "filename": dest_filename,
                "original_filename": src_file.name,
                "width": width,
                "height": height
            })

        shutil.rmtree(temp_dir, ignore_errors=True)
        return pages

    @classmethod
    def _extract_from_single_image(cls, img_path: Path, output_dir: Path) -> List[Dict[str, Any]]:
        dest_filename = "page_001.jpg"
        dest_path = output_dir / dest_filename

        with Image.open(img_path) as img:
            rgb_img = img.convert("RGB")
            rgb_img.save(dest_path, "JPEG", quality=95)
            width, height = rgb_img.size

            # Thumbnail
            thumb_path = output_dir / "thumb_001.jpg"
            thumb_img = rgb_img.copy()
            thumb_img.thumbnail((300, 400))
            thumb_img.save(thumb_path, "JPEG", quality=85)

        return [{
            "page_number": 1,
            "file_path": str(dest_path),
            "thumbnail_path": str(thumb_path),
            "filename": dest_filename,
            "original_filename": img_path.name,
            "width": width,
            "height": height
        }]
