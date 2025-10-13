import os
import pdfplumber
import pytesseract
import shutil
import streamlit as st
from pypdf import PdfReader
from PIL import Image
import pandas as pd
import re
from typing import Optional, Sequence

 # Define a mapping of character classes to their corresponding files
class_to_file_map = {
    "Bárbaro": "assets/D&D-Barbaro.pdf",
    "Bardo": "assets/D&D-Bardo.pdf",
    "Clérigo": "assets/D&D-Clerigo.pdf",
    "Druida": "assets/D&D-Druida.pdf",
    "Feiticeiro": "assets/D&D-Feiticeiro.pdf",
    "Guardião": "assets/D&D-Guardiao.pdf",
    "Guerreiro": "assets/D&D-Guerreiro.pdf",
    "Ladrão": "assets/D&D-Ladino.pdf",
    "Mago": "assets/D&D-Mago.pdf",
    "Monge": "assets/D&D-Monge.pdf",
    "Paladino": "assets/D&D-Paladino.pdf"
    }

def choose_dnd_class():
   
    # Class selection
    character_class = st.selectbox(
        "Selecione sua classe de personagem:",
        ["", "Bárbaro", "Bardo", "Clérigo", "Druida", "Feiticeiro", "Guardião", "Guerreiro", "Ladrão", "Mago",
         "Monge", "Paladino"]
    )

    # If nothing selected yet, return early with mapping so caller can use it
    if not character_class:
        return None, class_to_file_map

    # Proceed if selected and mapping contains the class
    file_to_process = class_to_file_map.get(character_class)
    if not file_to_process:
        st.write("Classe selecionada não encontrada nos arquivos disponíveis.")
        return character_class, class_to_file_map

    st.write(f"Você selecionou: {character_class}\n")
    search_term = character_class.lower()

    traits_table = basic_traits_table_extraction(file_to_process, search_term)

    if not traits_table:
        st.write("No tables found in extraction.")
        return character_class, class_to_file_map

    # traits_table is a list of tables; pick the first table-like object
    table = traits_table[0] if isinstance(traits_table[0], list) and len(traits_table[0]) > 0 and isinstance(traits_table[0][0], list) else traits_table

    # Create separate lists for each column
    trait_col = []
    description_col = []

    # Process each row in the table
    for row in table:
        if isinstance(row, list) and len(row) >= 2:
            trait_col.append(row[0])
            description_col.append(row[1])

    if trait_col and description_col:
        # Create DataFrame with separate columns
        formatted_table = pd.DataFrame({
            "Traço": trait_col,
            "Descrição": description_col
        })
        with st.expander("Essa é a tabela de traços iniciais da classe escolhida:", expanded=True):
            # Use st.dataframe so long text is scrollable and fits inside the expander
            st.dataframe(formatted_table)
    else:
        st.write("No valid data to display in table.")

    return character_class, class_to_file_map

# Basic Traits Table Extraction
def basic_traits_table_extraction(pdf_path, search_term):
    with pdfplumber.open(pdf_path) as pdf:
        # Extract the first page
        first_page = pdf.pages[0]

        # Attempt to extract tables directly
        tables = first_page.extract_tables()

        # Use OCR if no tables are found
        if not tables:
            image = first_page.to_image()
            pil_image = image.original  # Access the original Pillow image object
            if _ensure_tesseract():
                ocr_text = pytesseract.image_to_string(pil_image)

                # Parse OCR text into a table format (basic implementation)
                rows = ocr_text.split("\n")
                tables = [row.split() for row in rows if row.strip()]  # Split rows into columns
            else:
                # Tesseract not available or intentionally skipped; return None so caller can handle
                return None

        return tables

# Extract Table from Page with Index 1

def extract_table_page_2(pdf_path, ocr_lang="por", ocr_resolution=300):
    """Extract tables from page 2 (index 1). If pdfplumber doesn't return tables,
    run OCR and try to slice columns based on header positions (Nível, Bônus..., Características..., Fúrias, Dano, Maestria).
    Returns a list of rows (each row is a list of cell strings) or None on failure.
    """
    with pdfplumber.open(pdf_path) as pdf:
        if len(pdf.pages) < 2:
            return None
        # Extract the second page
        second_page = pdf.pages[1]

        # Attempt to extract tables directly
        tables2 = second_page.extract_tables()

        # If we got a proper table, return it immediately
        if tables2 and len(tables2) > 0:
            return tables2

        # Use OCR if no tables are found
        image = second_page.to_image(resolution=ocr_resolution)
        pil_image = image.original  # Access the original Pillow image object
        if not _ensure_tesseract():
            # Can't run OCR on this runner; return None so the test/workflow can skip OCR-related checks
            return None

        ocr_text = pytesseract.image_to_string(pil_image, lang=ocr_lang)

        # Split into lines and keep only non-empty lines
        lines = [ln.rstrip() for ln in ocr_text.splitlines() if ln.strip()]

        # Try to find a header line containing the expected column headings
        header_keys = ["Nível", "Bônus", "Características", "Fúrias", "Dano", "Maestria"]
        header_line = None
        header_index = None
        for i, ln in enumerate(lines):
            # require at least the three main headings to be present
            if all(k in ln for k in ["Nível", "Bônus", "Características"]):
                header_line = ln
                header_index = i
                break

        if header_line:
            # Determine slice positions from header keywords
            positions = []
            for key in ["Nível", "Bônus", "Características", "Fúrias", "Dano", "Maestria"]:
                pos = header_line.find(key)
                positions.append((pos if pos >= 0 else None, key))

            # If any position is missing, fallback to splitting on multi-space
            if any(p is None for p, _ in positions):
                # fallback
                rows = [re.split(r"\s{2,}", ln.strip()) for ln in lines[header_index + 1 :]]
                return rows if rows else None

            # Sort by position to ensure proper order
            positions = sorted(positions, key=lambda x: x[0])
            starts = [p for p, _ in positions]
            starts.append(None)  # sentinel for slicing end

            rows_out = []
            # include header as first row (optional) - we'll include it so the caller can detect headers
            header_cells = [header_line[starts[i] : starts[i + 1]].strip() if starts[i] is not None else "" for i in range(len(starts) - 1)]
            rows_out.append(header_cells)

            for ln in lines[header_index + 1 :]:
                # slice each line using the header positions
                cells = []
                for i in range(len(starts) - 1):
                    s = starts[i]
                    e = starts[i + 1]
                    if s is None:
                        cell = ln.strip()
                    else:
                        cell = ln[s:e].strip() if e is not None else ln[s:].strip()
                    # collapse whitespace
                    cell = re.sub(r"\s+", " ", cell)
                    cells.append(cell)
                # skip empty rows
                if any(c for c in cells):
                    rows_out.append(cells)

            return rows_out if rows_out else None

        # final fallback: split on 2+ spaces (common OCR column delimiter)
        rows = [re.split(r"\s{2,}", ln.strip()) for ln in lines]
        return rows if rows else None


def _ensure_tesseract():
    """Return True if the system tesseract binary is available.

    Respects the environment variable `SKIP_OCR=1` which CI can set to explicitly
    skip OCR tests on runners where system Tesseract is not available.
    """
    # Allow CI to explicitly opt-out
    if os.environ.get("SKIP_OCR", "0") in ("1", "true", "True"):
        return False

    return shutil.which("tesseract") is not None