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

# Functionality to process D&D files
def process_dd_files():
    st.write("Preparing to process D&D files...")

    # Define file paths
    files_to_process = [
        "assets/D&D.pdf",
        "assets/D&D Tasha.pdf",
        "assets/D&D Xanathar.pdf"
    ]

    # Process files
    for file_path in files_to_process:
        st.write(f"Processing file: {file_path}")

        if file_path == "assets/D&D Tasha.pdf":
            st.write("Performing OCR on D&D Tasha.pdf...")
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = pytesseract.image_to_string(page.to_image())
                    st.write(text)
        else:
            st.write("Extracting text from PDF...")
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    st.write(text)

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

