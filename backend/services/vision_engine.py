from google import genai
from google.genai import types
from PIL import Image
from pathlib import Path
import json
import time
from typing import Dict, Any, Optional

HANDWRITING_OCR_PROMPT = """You are a world-class production OCR and Handwritten Text Recognition (HTR) specialist.
Analyze this image of a handwritten document page with maximum accuracy.

Tasks:
1. Transcribe ALL handwritten and printed text verbatim.
2. Accurately decipher cursive, messy handwriting, notes, margins, annotations, and corrections.
3. If words are struck through or crossed out, indicate them with ~~strikethrough~~.
4. If there are tables, preserve them in clean Markdown table syntax.
5. If there are numbered lists, formulas, bullet points, or headings, preserve their layout and hierarchy using Markdown.
6. If a word or character is illegible, use `[illegible]` rather than guessing wildly.
7. Return a clean, structured output.

Please format your response strictly as JSON with this schema:
{
  "transcription_markdown": "Full transcribed page content in GitHub Markdown format",
  "summary": "1-2 sentence high-level summary of the page contents",
  "detected_language": "English / etc.",
  "confidence_rating": "HIGH" | "MEDIUM" | "LOW",
  "estimated_confidence_percent": 95,
  "handwriting_style": "Cursive" | "Print" | "Mixed" | "Notes",
  "document_type": "Notebook" | "Letter" | "Form" | "Exam" | "Loose Leaf" | "Other",
  "key_entities": ["key names, topics, or headings found on the page"]
}

Return ONLY valid JSON without wrapping markdown code fences if possible, or standard markdown ```json code blocks.
"""

class VisionOCREngine:
    """
    State-of-the-art Multimodal Vision OCR Engine for handwritten multi-page recognition.
    """

    @classmethod
    def transcribe_page(
        cls,
        image_path: Path,
        api_key: Optional[str] = None,
        model_name: str = "gemini-3.5-flash-lite",
        custom_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transcribes a handwritten image page using Gemini Vision models.
        Defaults to Gemini 3.5 Flash-Lite.
        """
        if not api_key:
            raise ValueError("Gemini API key is required for Vision OCR. Please provide an API key in settings.")

        start_time = time.time()
        client = genai.Client(api_key=api_key)

        prompt = HANDWRITING_OCR_PROMPT
        if custom_instructions and custom_instructions.strip():
            prompt += f"\n\nAdditional User Guidance:\n{custom_instructions.strip()}"

        # Load image bytes
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        mime_type = "image/jpeg"
        if image_path.suffix.lower() == ".png":
            mime_type = "image/png"
        elif image_path.suffix.lower() == ".webp":
            mime_type = "image/webp"

        # Normalize model identifier
        normalized_model = model_name.strip().lower().replace(" ", "-")
        if "3.5" in normalized_model and "flash" in normalized_model:
            normalized_model = "gemini-3.5-flash-lite"

        # Candidate models list with requested model first
        candidate_models = [normalized_model]
        for fallback in ["gemini-2.5-flash-lite", "gemini-2.0-flash-lite", "gemini-2.5-flash"]:
            if fallback not in candidate_models:
                candidate_models.append(fallback)

        response = None
        used_model = normalized_model
        last_error = None

        for target_model in candidate_models:
            try:
                response = client.models.generate_content(
                    model=target_model,
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
                        prompt
                    ],
                    config=types.GenerateContentConfig(
                        temperature=0.1,  # Low temperature for deterministic, accurate transcription
                        response_mime_type="application/json"
                    )
                )
                used_model = target_model
                break
            except Exception as e:
                err_str = str(e)
                last_error = e
                # Only retry if error is model not found / unsupported
                if "404" in err_str or "not found" in err_str.lower() or "invalid model" in err_str.lower():
                    continue
                else:
                    raise e

        if response is None:
            if last_error:
                raise last_error
            raise RuntimeError(f"Failed to generate content with {model_name}")

        elapsed = round(time.time() - start_time, 2)
        raw_text = response.text or ""

        # Parse JSON response
        try:
            # Strip potential ```json markers
            cleaned = raw_text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            data = json.loads(cleaned.strip())
        except Exception:
            # Fallback if raw text wasn't strict JSON
            data = {
                "transcription_markdown": raw_text,
                "summary": "Transcribed handwritten document",
                "detected_language": "Unknown",
                "confidence_rating": "MEDIUM",
                "estimated_confidence_percent": 80,
                "handwriting_style": "Mixed",
                "document_type": "Notes",
                "key_entities": []
            }

        data["processing_time_sec"] = elapsed
        data["engine"] = f"{model_name} (Vision AI)"
        data["char_count"] = len(data.get("transcription_markdown", ""))
        data["word_count"] = len(data.get("transcription_markdown", "").split())
        return data
