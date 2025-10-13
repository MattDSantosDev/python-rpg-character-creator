# Import libraries at the top of the file
import pdfplumber
import pytesseract
import streamlit as st
from pypdf import PdfReader
from PIL import Image
import pandas as pd
import re
from pathlib import Path

'''# Functionality to use PDF bookmarks as a search range
def search_with_bookmarks(pdf_path, search_term):
    reader = PdfReader(pdf_path)
    bookmarks = reader.outline

    results = []
    for bookmark in bookmarks:
        # Updated bookmark page number retrieval
        if bookmark.page is not None:
            # Added fallback mechanism for page lookup
            for i, page in enumerate(reader.pages):
                if page == bookmark.page:
                    page_number = i
                    break
            else:
                continue  # Skip if no matching page is found
        else:
            continue  # Skip invalid bookmarks
            
        page = reader.pages[page_number]
        text = page.extract_text()

        if search_term.lower() in text.lower():
            results.append((bookmark.title, page_number + 1))
    return results

# Functionality to use PDF headers/titles as a search method'''
'''def search_with_headers(pdf_path, search_term):
    reader = PdfReader(pdf_path)

    # Fixed `search_with_headers` to use `pdfplumber` for image conversion
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            text = page.extract_text()
            if search_term.lower() in text.lower():
                return page_number + 1  # Pages are 1-indexed

            # Use OCR if text extraction fails
            image = page.to_image()  # Convert page to image
            # Fixed image compatibility for OCR
            pil_image = image.original  # Access the original Pillow image object
            ocr_text = pytesseract.image_to_string(pil_image)
            if search_term.lower() in ocr_text.lower():
                return page_number + 1
    return None  # Return None if the header is not found'''

'''def extract_headers_pypdf(pdf_path, header_regex=None):
    """Extract header-like lines from one PDF or an iterable of PDFs.

    Args:
        pdf_path: str/Path or iterable of paths. If iterable, headers from all
            files will be returned.
        header_regex: optional compiled regex used to detect header-like lines.

    Returns:
        List of tuples (pdf_path_str, page_number, header_line).
    """
    # normalize incoming argument to a list of paths
    if isinstance(pdf_path, (str, Path)):
        paths = [pdf_path]
    else:
        # assume iterable of paths
        paths = list(pdf_path)

    # default header regex (all-caps-ish heuristic)
    if header_regex is None:
        # Allow letters (including common Latin-1 uppercase accents), digits,
        # spaces and hyphen. Place '-' at the end of the class so it doesn't
        # need escaping and avoids SyntaxWarning about invalid escape sequences.
        header_regex = re.compile(r'^[A-ZÀ-ÖØ-Ý0-9][A-Z0-9 -]{2,}$')

    header_candidates = []  # (pdf_path_str, page, line_text)

    for p in paths:
        p_path = Path(p)
        reader = PdfReader(str(p_path))
        for pageno, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            # split into non-empty lines
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            for idx, line in enumerate(lines):
                # primary heuristic: matches regex (all-caps/short-ish)
                if header_regex.match(line):
                    header_candidates.append((str(p_path), pageno, line))
                # secondary heuristic: line ends with ":" or followed by lines that look like table rows
                elif line.endswith(":"):
                    header_candidates.append((str(p_path), pageno, line.rstrip(":").strip()))
                else:
                    # look ahead: if next lines contain many separators or multiple tokens per line, it's likely a header above a table
                    if idx + 1 < len(lines):
                        next_line = lines[idx + 1]
                        if len(next_line.split()) >= 3 and any(c.isdigit() for c in next_line):
                            # heuristic: next line looks tabular (has numbers)
                            header_candidates.append((str(p_path), pageno, line))

    return header_candidates'''
