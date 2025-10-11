# Import libraries at the top of the file
import pdfplumber
import pytesseract
import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image

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

# Basic Traits Table Extraction
def basic_traits_table_extraction(pdf_path, search_term):
    reader = PdfReader(pdf_path)
    header_page = search_with_headers(pdf_path, search_term)
    
    # Fixed `header_page` usage
    if header_page is None:
        return None  # Return None if no header page is found
    class_page = header_page + 1
    
    # Updated `basic_traits_table_extraction` to extract table from the next page
    if header_page:
        with pdfplumber.open(pdf_path) as pdf:
            next_page = header_page  # Use the next page after the header
            page = pdf.pages[next_page]
            tables = page.extract_tables()

            # Use OCR if no tables are found
            if not tables:
                image = page.to_image()  # Convert page to image
                # Fixed image compatibility for OCR
                pil_image = image.original  # Access the original Pillow image object
                ocr_text = pytesseract.image_to_string(pil_image)
                return parse_table_from_ocr(ocr_text)

            return tables[0]  # Return the first table
    return None  # Return None if no tables are found

# Added `parse_table_from_ocr` function

def parse_table_from_ocr(ocr_text):
    # Example logic to parse table-like data from OCR text
    rows = ocr_text.split("\n")  # Split text into rows
    table = []
    for row in rows:
        columns = row.split()  # Split row into columns (customize as needed)
        table.append(columns)
    return table