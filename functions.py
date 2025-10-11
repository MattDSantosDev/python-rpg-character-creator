# Import libraries at the top of the file
import pdfplumber
import pytesseract
import streamlit as st
from pypdf import PdfReader

# Functionality to use PDF bookmarks as a search range
def search_with_bookmarks(pdf_path, search_term):
    reader = PdfReader(pdf_path)
    bookmarks = reader.get_outlines()

    results = []
    for bookmark in bookmarks:
        page_number = bookmark.page_number
        page = reader.pages[page_number]
        text = page.extract_text()

        if search_term.lower() in text.lower():
            results.append((bookmark.title, page_number + 1))
    return results


# Functionality to use PDF headers/titles as a search method
def search_with_headers(pdf_path, search_term):
    reader = PdfReader(pdf_path)

    results = []
    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()

        # Assuming headers/titles are in the first few lines of the page
        header_lines = text.splitlines()[:3]  # Adjust the number of lines as needed
        for header in header_lines:
            if search_term.lower() in header.lower():
                results.append((header, page_number + 1))
    return results

# Basic Traits Table Extraction
def basic_traits_table_extraction(pdf_path, search_term):
    reader = PdfReader(pdf_path)
    bookmark_page = search_with_bookmarks(pdf_path, search_term)
    class_page = bookmark_page[0]
    
    with pdfplumber.open(pdf_path) as pdf:
        # Access the specific page using the bookmark_page variable
        page = pdf.pages[class_page[1] - 1]  # Subtract 1 because page numbers are zero-indexed in pdfplumber
        
        # Extract tables from the page
        tables = page.extract_tables()
        
        # Check if tables exist and extract the first one
        if tables:
            first_table = tables[0]
            return first_table
        else:
            return None