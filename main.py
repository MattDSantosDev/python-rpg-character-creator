import streamlit as st
import base64
import os
import pdfplumber
import pytesseract
import pandas as pd
from functions import *
from pypdf import PdfReader
from dndfunctions import *
from opfunctions import *


# Set page configuration
st.set_page_config(
    page_title="RPG Character Creator",
    page_icon="⚔️",
    layout="wide"
)

# Remove image background and replace it with dark grey color
page_bg_img = '''
<style>
.stApp {
    background-color: #2E2E2E;
}

.main .block-container {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    padding: 2rem;
    margin-top: 2rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Custom CSS to make text stand out
st.markdown("<style>body { color: white; background-color: #2E2E2E; }</style>", unsafe_allow_html=True)

# Main content
st.title("Bem-vindo ao Criador de Personagens RPG!")
st.write("Crie seu próprio personagem de RPG com atributos e habilidades personalizáveis.")

# Add a dropdown menu for RPG systems
rpg_system = st.selectbox(
    "Escolha qual sistema quer usar:",
    ["", "D&D", "Ordem Paranormal"]
)

# Display the selected option if a valid system is chosen
if rpg_system != "Escolha qual sistema quer usar:" and rpg_system != "":
    st.write(f"Você selecionou: {rpg_system}")

# Handle file processing based on dropdown selection
if rpg_system == "D&D":
    st.write("Vamos começar a criar esse personagem de D&D!")

    # Call the D&D class chooser and capture the returned values
    choose_dnd_class()

elif rpg_system == "Ordem Paranormal":
    st.write("Vamos começar a criar esse personagem de Ordem Paranormal!")
    atts_selector()

# Entry point for the Python RPG Character Creator

def main():
    print("Welcome to the Python RPG Character Creator!")

if __name__ == "__main__":
    main()

# Example usage of pdfplumber and pytesseract
# This is a placeholder for future functionality
# You can use pdfplumber to extract text from PDFs and pytesseract for OCR tasks

# Example usage of pypdf
# This is a placeholder for future functionality
# You can use PdfReader to extract text from PDFs