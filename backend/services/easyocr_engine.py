import time
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional
import numpy as np

class LocalEasyOCREngine:
    """
    Local Open-Source OCR Engine using EasyOCR.
    Operates 100% offline with zero cloud API keys or internet requirements.
    Thread-safe lazy initialization.
    """
    _reader = None
    _init_lock = threading.Lock()

    @classmethod
    def get_reader(cls):
        if cls._reader is None:
            with cls._init_lock:
                if cls._reader is None:
                    import easyocr
                    # Initialize English reader (supports Latin characters and numbers)
                    # verbose=False reduces terminal noise
                    cls._reader = easyocr.Reader(['en'], gpu=False, verbose=False)
        return cls._reader

    @classmethod
    def transcribe_page(cls, image_path: Path) -> Dict[str, Any]:
        """
        Runs EasyOCR, clusters bounding boxes into lines and paragraphs,
        and returns structured transcription.
        """
        start_time = time.time()
        reader = cls.get_reader()
        
        # Read image text
        results = reader.readtext(str(image_path), paragraph=False)
        elapsed = round(time.time() - start_time, 2)

        if not results:
            return {
                "transcription_markdown": "_No text detected on this page._",
                "summary": "Empty page or undetected text",
                "detected_language": "English",
                "confidence_rating": "LOW",
                "estimated_confidence_percent": 0,
                "handwriting_style": "Undetected",
                "document_type": "Page",
                "key_entities": [],
                "processing_time_sec": elapsed,
                "engine": "EasyOCR (Offline Local)",
                "char_count": 0,
                "word_count": 0,
                "bounding_boxes": []
            }

        # Cluster results into logical lines
        # results format: [ (bbox, text, confidence), ... ]
        items = []
        confidences = []
        for bbox, text, conf in results:
            if not text.strip():
                continue
            # Calculate center Y and min X
            y_coords = [pt[1] for pt in bbox]
            x_coords = [pt[0] for pt in bbox]
            top_y = min(y_coords)
            bottom_y = max(y_coords)
            center_y = (top_y + bottom_y) / 2
            min_x = min(x_coords)
            height = bottom_y - top_y

            items.append({
                "bbox": bbox,
                "text": text.strip(),
                "conf": float(conf),
                "center_y": center_y,
                "min_x": min_x,
                "height": height
            })
            confidences.append(float(conf))

        # Sort items primarily by Y, secondarily by X
        items.sort(key=lambda item: item["center_y"])
        
        # Group into lines
        lines = []
        current_line = []
        current_line_y = None
        line_height_avg = np.mean([item["height"] for item in items]) if items else 20

        for item in items:
            if current_line_y is None:
                current_line = [item]
                current_line_y = item["center_y"]
            elif abs(item["center_y"] - current_line_y) < (line_height_avg * 0.7):
                current_line.append(item)
            else:
                current_line.sort(key=lambda x: x["min_x"])
                lines.append(" ".join(x["text"] for x in current_line))
                current_line = [item]
                current_line_y = item["center_y"]

        if current_line:
            current_line.sort(key=lambda x: x["min_x"])
            lines.append(" ".join(x["text"] for x in current_line))

        full_text = "\n\n".join(lines)
        avg_conf = float(np.mean(confidences)) if confidences else 0.0
        conf_percent = int(round(avg_conf * 100))

        confidence_rating = "HIGH" if conf_percent >= 80 else ("MEDIUM" if conf_percent >= 50 else "LOW")

        return {
            "transcription_markdown": full_text,
            "summary": f"Detected {len(lines)} lines of text using EasyOCR",
            "detected_language": "English",
            "confidence_rating": confidence_rating,
            "estimated_confidence_percent": conf_percent,
            "handwriting_style": "Local HTR / OCR",
            "document_type": "Scanned Document",
            "key_entities": [],
            "processing_time_sec": elapsed,
            "engine": "EasyOCR (Offline Local)",
            "char_count": len(full_text),
            "word_count": len(full_text.split()),
            "lines_count": len(lines)
        }
