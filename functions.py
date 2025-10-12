# Import libraries at the top of the file
import pdfplumber
import pytesseract
import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
import pandas as pd

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

