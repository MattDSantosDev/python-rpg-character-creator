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
/* tighten streamlit button padding for a tighter layout */
button[data-baseweb="button"] {
    padding: 6px 8px !important;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

# Custom CSS to make text stand out
st.markdown("<style>body { color: white; background-color: #2E2E2E; }</style>", unsafe_allow_html=True)

# Main content
st.title("Bem-vindo ao Criador de Personagens RPG!")
st.write("Crie seu próprio personagem de RPG com atributos e habilidades personalizáveis.")

# Add a dropdown menu for RPG systems inside a centered, narrow column
st.markdown(
    """
    <style>
    /* constrain the container that holds the selectbox */
    .narrow-selectbox .stSelectbox {
        max-width: 320px;
        margin-left: auto;
        margin-right: auto;
    }
    /* additional fallback: target the widget label container */
    .narrow-selectbox .stSelectbox > div {
        max-width: 320px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# place the selectbox in a centered column so it visually appears narrow
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown('<div class="narrow-selectbox">', unsafe_allow_html=True)
    rpg_system = st.selectbox(
        "Escolha qual sistema quer usar:",
        ["", "D&D", "Ordem Paranormal"]
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Handle file processing based on dropdown selection
if rpg_system == "D&D":
    st.write("Vamos começar a criar esse personagem de D&D!\n")

    # Call the D&D class chooser and capture the returned values
    choose_dnd_class()

elif rpg_system == "Ordem Paranormal":
    st.write("Vamos começar a criar esse personagem de Ordem Paranormal!\n")
    nex_value = nex_selector()
    if nex_value and nex_value != "":        # only proceed if user selected something
        # render attributes only once and proceed to origin selection
        attrs = atts_selector(5, labels=["Força", "Agilidade", "Intelecto", "Presença", "Vigor"])
        select_origin()

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