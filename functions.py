# Import libraries at the top of the file
import pdfplumber
import pytesseract
import streamlit as st
from pypdf import PdfReader
from PIL import Image
import pandas as pd
import re
from pathlib import Path

# Functionality to use PDF bookmarks as a search range
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

# Functionality to use PDF headers/titles as a search method
def search_with_headers(pdf_path, search_term):
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
    return None  # Return None if the header is not found

def extract_headers_pypdf(pdf_path, header_regex=None):
    pdf_path = Path(pdf_path)
    reader = PdfReader(str(pdf_path))
    header_candidates = []  # (page, line_text)
    # a simple regex for header-like lines (customize)
    if header_regex is None:
        header_regex = re.compile(r'^[A-ZÀ-ÖØ-Ý0-9][A-Z0-9 \-]{2,}$')  # all-caps-ish heuristic

    for pageno, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        # split into non-empty lines
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for idx, line in enumerate(lines):
            # primary heuristic: matches regex (all-caps/short-ish)
            if header_regex.match(line):
                header_candidates.append((pageno, line))
            # secondary heuristic: line ends with ":" or followed by lines that look like table rows
            elif line.endswith(":"):
                header_candidates.append((pageno, line.rstrip(":").strip()))
            else:
                # look ahead: if next lines contain many separators or multiple tokens per line, it's likely a header above a table
                if idx + 1 < len(lines):
                    next_line = lines[idx + 1]
                    if len(next_line.split()) >= 3 and any(c.isdigit() for c in next_line):
                        # heuristic: next line looks tabular (has numbers)
                        header_candidates.append((pageno, line))
    return header_candidates
