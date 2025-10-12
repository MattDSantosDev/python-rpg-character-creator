import pdfplumber
import pytesseract
import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
import pandas as pd

def choose_dnd_class():
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
        with st.expander("Essa é a tabela de traços da classe escolhida:", expanded=True):
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
            ocr_text = pytesseract.image_to_string(pil_image)

            # Parse OCR text into a table format (basic implementation)
            rows = ocr_text.split("\n")
            tables = [row.split() for row in rows if row.strip()]  # Split rows into columns

        return tables
