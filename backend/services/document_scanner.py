import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Tuple, List, Dict, Any, Optional

class DocumentScanner:
    """
    Advanced Document Scanning & Perspective Rectification Engine.
    Emulates high-end mobile document scanners (CamScanner / Adobe Scan):
    - 4-corner document boundary detection
    - Perspective warp & flattening (keystone correction)
    - CamScanner-grade scanning filters (Magic Color, Clean B&W, Grayscale)
    - Notebook ruled-line attenuation
    """

    @staticmethod
    def order_points(pts: np.ndarray) -> np.ndarray:
        """
        Orders 4 coordinates in consistent order:
        [top-left, top-right, bottom-right, bottom-left]
        """
        rect = np.zeros((4, 2), dtype="float32")
        pts = pts.reshape(4, 2)

        # Sum: top-left has smallest sum, bottom-right has largest sum
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        # Difference: top-right has smallest diff, bottom-left has largest diff
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    @classmethod
    def detect_document_corners(cls, img_bgr: np.ndarray) -> List[List[float]]:
        """
        Detects the 4 corners of a piece of paper or notebook page against
        a desk / background. Returns list of [x, y] coordinates in clockwise order:
        [TL, TR, BR, BL] normalized to original image dimensions.
        """
        h, w = img_bgr.shape[:2]
        
        # Resize for fast and noise-tolerant contour detection
        target_h = 800
        scale = h / float(target_h)
        resized_w = int(w / scale)
        resized = cv2.resize(img_bgr, (resized_w, target_h))

        # Convert to gray, blur, and find edges
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection using morphological gradient + Canny
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated = cv2.dilate(blurred, kernel)
        edges = cv2.Canny(dilated, 30, 120)

        # Close gaps in contours
        closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)))

        # Find contours
        contours, _ = cv2.findContours(closed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        doc_contour = None
        min_doc_area = (resized_w * target_h) * 0.15  # Document must occupy at least 15% of frame

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)

            if len(approx) == 4 and cv2.contourArea(approx) > min_doc_area:
                # Ensure contour is convex
                if cv2.isContourConvex(approx):
                    doc_contour = approx
                    break

        # Fallback if no exact 4-corner polygon was found: use convex hull or default bounding rect
        if doc_contour is None:
            for c in contours:
                if cv2.contourArea(c) > min_doc_area:
                    hull = cv2.convexHull(c)
                    peri = cv2.arcLength(hull, True)
                    approx = cv2.approxPolyDP(hull, 0.03 * peri, True)
                    if len(approx) == 4:
                        doc_contour = approx
                        break

        if doc_contour is not None:
            pts = doc_contour.reshape(4, 2).astype("float32") * scale
            ordered = cls.order_points(pts)
            return ordered.tolist()

        # Fallback: Default to inset rectangular frame (5% margin from edges)
        margin_x = w * 0.04
        margin_y = h * 0.04
        return [
            [margin_x, margin_y],
            [w - margin_x, margin_y],
            [w - margin_x, h - margin_y],
            [margin_x, h - margin_y]
        ]

    @classmethod
    def perspective_warp(cls, img_bgr: np.ndarray, corners: List[List[float]]) -> np.ndarray:
        """
        Applies 4-point perspective warp (keystone correction) to flatten
        an angled document photo into a clean rectangular top-down page scan.
        """
        pts = np.array(corners, dtype="float32")
        rect = cls.order_points(pts)
        (tl, tr, br, bl) = rect

        # Compute width of new image
        width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        max_w = max(int(width_a), int(width_b))

        # Compute height of new image
        height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        max_h = max(int(height_a), int(height_b))

        # Ensure valid dimensions
        max_w = max(100, max_w)
        max_h = max(100, max_h)

        dst = np.array([
            [0, 0],
            [max_w - 1, 0],
            [max_w - 1, max_h - 1],
            [0, max_h - 1]
        ], dtype="float32")

        # Compute perspective transform matrix and warp
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(img_bgr, M, (max_w, max_h), flags=cv2.INTER_CUBIC)
        return warped

    @staticmethod
    def apply_magic_color(img_bgr: np.ndarray) -> np.ndarray:
        """
        CamScanner-grade 'Magic Color' filter:
        - Whitens yellowed paper background completely
        - Preserves ink colors (blue, black, red, green pens)
        - Removes shadows and creases
        """
        # Split channels
        channels = cv2.split(img_bgr)
        out_channels = []

        for ch in channels:
            # Estimate uneven background illumination with large morphological dilation
            dilated = cv2.dilate(ch, np.ones((11, 11), np.uint8))
            bg = cv2.medianBlur(dilated, 25)
            
            # Avoid division by zero
            bg = np.maximum(bg, 1)

            # Divide foreground by background: foreground / background * 255
            norm = (ch.astype(np.float32) / bg.astype(np.float32)) * 255.0
            norm = np.clip(norm, 0, 255).astype(np.uint8)

            # Stretch contrast slightly
            norm = cv2.normalize(norm, None, alpha=15, beta=255, norm_type=cv2.NORM_MINMAX)
            out_channels.append(norm)

        magic = cv2.merge(out_channels)

        # Enhance saturation slightly for crisp ink
        hsv = cv2.cvtColor(magic, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        s = cv2.multiply(s, 1.25)
        s = np.clip(s, 0, 255).astype(np.uint8)
        # S-curve on V for crisp dark ink
        v = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8)).apply(v)
        enhanced = cv2.cvtColor(cv2.merge([h, s, v]), cv2.COLOR_HSV2BGR)
        return enhanced

    @staticmethod
    def apply_clean_bw(img_bgr: np.ndarray) -> np.ndarray:
        """
        CamScanner-grade 'Clean B&W' filter:
        Produces ultra-crisp binary scan without gray haze or paper textures.
        Ideal for handwritten notes, pencil, and faint ballpoint ink.
        """
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        # Background estimation via morphological closure
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (19, 19))
        bg = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        diff = cv2.absdiff(gray, bg)

        # Normalize diff
        norm = cv2.normalize(diff, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

        # Invert so text is dark on white
        inv = 255 - norm

        # Adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            inv,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            blockSize=25,
            C=12
        )

        # Light median blur to remove single-pixel salt noise while keeping strokes
        cleaned = cv2.medianBlur(thresh, 3)
        return cv2.cvtColor(cleaned, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def apply_grayscale_scan(img_bgr: np.ndarray) -> np.ndarray:
        """
        Clean Grayscale document scan with balanced lighting.
        """
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        return cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)

    @classmethod
    def process_scan(
        cls,
        image_path: Path,
        output_path: Path,
        corners: Optional[List[List[float]]] = None,
        filter_type: str = "magic_color",  # "magic_color", "clean_bw", "grayscale", "enhanced", "original"
        auto_detect_corners: bool = True
    ) -> Tuple[Path, Dict[str, Any]]:
        """
        Full scan pipeline:
        1. Reads raw photograph/scan.
        2. Detects or uses provided 4 corners.
        3. Perspective warps to rectangular flat document.
        4. Applies selected document scan filter.
        5. Saves high-definition scan.
        """
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Could not load image at {image_path}")

        meta: Dict[str, Any] = {
            "original_width": img.shape[1],
            "original_height": img.shape[0],
            "filter_applied": filter_type
        }

        # Step 1: 4-Corner detection & perspective unwarping
        if corners is None and auto_detect_corners:
            detected_pts = cls.detect_document_corners(img)
            meta["corners_detected"] = detected_pts
            corners_to_use = detected_pts
        elif corners is not None:
            corners_to_use = corners
            meta["corners_applied"] = corners
        else:
            corners_to_use = None

        if corners_to_use is not None:
            warped = cls.perspective_warp(img, corners_to_use)
        else:
            warped = img

        # Step 2: Scanner filter
        if filter_type == "magic_color":
            final_img = cls.apply_magic_color(warped)
        elif filter_type == "clean_bw":
            final_img = cls.apply_clean_bw(warped)
        elif filter_type == "grayscale":
            final_img = cls.apply_grayscale_scan(warped)
        elif filter_type == "enhanced":
            # CLAHE contrast
            lab = cv2.cvtColor(warped, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            l = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8)).apply(l)
            final_img = cv2.cvtColor(cv2.merge([l, a, b]), cv2.COLOR_LAB2BGR)
        else:
            final_img = warped

        meta["scanned_width"] = final_img.shape[1]
        meta["scanned_height"] = final_img.shape[0]

        output_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_path), final_img, [cv2.IMWRITE_JPEG_QUALITY, 95])

        return output_path, meta
