import pdfplumber
import pytesseract
import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
import pandas as pd

def choose_dnd_class():


        # Class selection
        character_class = st.selectbox(
        "Selecione sua classe de personagem:",
        ["", "Bárbaro", "Bardo", "Clérigo", "Druida", "Feiticeiro", "Guardião", "Guerreiro", "Ladrão", "Mago",
         "Monge", "Paladino"]
        )

        if character_class != "" and character_class != "Selecione sua classe de personagem:":
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
            return character_class, class_to_file_map
    
        if character_class in class_to_file_map:
            # Get the file corresponding to the selected class
            file_to_process = class_to_file_map[character_class]
    
            st.write(f"Você selecionou: {character_class}\n")
            search_term = character_class.lower()
            with st.expander(f"Essa é a tabela de traços da classe escolhida:")
                traits_table = basic_traits_table_extraction(file_to_process, search_term)
    
            if traits_table:
                # traits_table is a list of tables, we want the first table if it exists
                if len(traits_table) > 0 and isinstance(traits_table[0], list):
                    # Get the first table
                    table = traits_table[0] if len(traits_table[0]) > 0 and isinstance(traits_table[0][0], list) else traits_table
                
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
                    st.table(formatted_table)  # Display the table in Streamlit
                else:
                    st.write("No valid data to display in table.")
            else:
                st.write("No tables found in extraction.")
        else:
            st.write("Tabela de traços não encontrada.")


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
