import os
import pytest
from dndfunctions import extract_table_page_2, _ensure_tesseract, class_to_file_map


def test_extract_table_page_2_basic():
    """Ensure extract_table_page_2 returns a non-empty table for the included Barbaro PDF.

    The test will be skipped if OCR is intentionally disabled via SKIP_OCR or if
    the environment does not have tesseract available and the function requires it.
    """
    # If CI set SKIP_OCR, skip the test
    if os.environ.get("SKIP_OCR", "0") in ("1", "true", "True"):
        pytest.skip("SKIP_OCR set; skipping OCR-dependent extraction test")

    # If system tesseract is not available, skip (the function will also skip OCR)
    if not _ensure_tesseract():
        pytest.skip("Tesseract not available; skipping OCR-dependent extraction test")

    pdf = class_to_file_map.get("Bárbaro")
    assert pdf is not None

    rows = extract_table_page_2(pdf, ocr_lang="por", ocr_resolution=200)
    assert rows is not None and len(rows) > 0
