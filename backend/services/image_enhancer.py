import cv2
import numpy as np
from PIL import Image
from pathlib import Path
from typing import Tuple, Optional

class ImageEnhancer:
    """
    Production-grade preprocessing pipeline specifically optimized for
    handwritten documents, notebook pages, and scanned papers.
    """

    @staticmethod
    def remove_shadows(img_bgr: np.ndarray) -> np.ndarray:
        """
        Removes uneven lighting, glare, and phone shadows from handwritten photos
        using morphological background subtraction.
        """
        # Split into RGB channels to handle color-ink notebooks gracefully
        rgb_planes = cv2.split(img_bgr)
        result_planes = []
        for plane in rgb_planes:
            dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
            bg_img = cv2.medianBlur(dilated_img, 21)
            diff_img = 255 - cv2.absdiff(plane, bg_img)
            norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
            result_planes.append(norm_img)
        return cv2.merge(result_planes)

    @staticmethod
    def enhance_contrast(img_bgr: np.ndarray, clip_limit: float = 2.5) -> np.ndarray:
        """
        Enhances handwritten stroke contrast using CLAHE (Contrast Limited
        Adaptive Histogram Equalization) in LAB color space.
        """
        lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl, a, b))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    @staticmethod
    def detect_skew_angle(img_gray: np.ndarray) -> float:
        """
        Calculates skew angle of handwritten text lines using Hough Line Transform
        or contour bounding boxes.
        """
        # Apply threshold to isolate ink strokes
        thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        # Dilate horizontally to connect handwritten words into lines
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
        dilated = cv2.dilate(thresh, kernel, iterations=2)
        
        # Find contours of lines
        contours, _ = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        angles = []
        for c in contours:
            area = cv2.contourArea(c)
            if area < 1000:
                continue
            min_area_rect = cv2.minAreaRect(c)
            angle = min_area_rect[-1]
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle
            if abs(angle) < 45:  # Only accept reasonable skews
                angles.append(angle)
        
        if not angles:
            return 0.0
        return float(np.median(angles))

    @staticmethod
    def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
        """Rotates image around its center while expanding canvas to prevent clipping."""
        if abs(angle) < 0.5:
            return image
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        cos = np.abs(M[0, 0])
        sin = np.abs(M[0, 1])
        new_w = int((h * sin) + (w * cos))
        new_h = int((h * cos) + (w * sin))
        M[0, 2] += (new_w / 2) - center[0]
        M[1, 2] += (new_h / 2) - center[1]
        return cv2.warpAffine(image, M, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    @classmethod
    def process_handwritten_image(
        cls,
        image_path: Path,
        output_path: Path,
        auto_deskew: bool = True,
        remove_shadow: bool = True,
        boost_contrast: bool = True,
        denoise: bool = True
    ) -> Tuple[Path, dict]:
        """
        Executes full preprocessing pipeline and saves optimized image.
        Returns output path and preprocessing metadata.
        """
        # Read image
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Could not load image at {image_path}")

        meta = {
            "original_width": img.shape[1],
            "original_height": img.shape[0],
            "skew_angle": 0.0,
            "shadow_removed": remove_shadow,
            "contrast_boosted": boost_contrast
        }

        # 1. Shadow removal
        if remove_shadow:
            img = cls.remove_shadows(img)

        # 2. Contrast Enhancement
        if boost_contrast:
            img = cls.enhance_contrast(img)

        # 3. Denoising
        if denoise:
            # Fast bilateral filter preserves sharp ink edges while smoothing noise
            img = cv2.bilateralFilter(img, d=5, sigmaColor=50, sigmaSpace=50)

        # 4. Auto-deskew
        if auto_deskew:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            angle = cls.detect_skew_angle(gray)
            meta["skew_angle"] = round(angle, 2)
            if abs(angle) >= 0.5:
                img = cls.rotate_image(img, angle)

        meta["processed_width"] = img.shape[1]
        meta["processed_height"] = img.shape[0]

        # Save enhanced image
        output_path.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output_path), img, [cv2.IMWRITE_JPEG_QUALITY, 95])

        return output_path, meta
