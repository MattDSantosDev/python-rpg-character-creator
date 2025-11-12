import streamlit as st
import streamlit.components.v1 as components
import urllib.parse as up
import base64
import os
import pdfplumber
import pytesseract
import pandas as pd
from functions import *
from pypdf import PdfReader
from dndfunctions import *
from opfunctions import *
import runpy


# Define page navigation functions at module level
def _go_dnd():
    print("DEBUG: _go_dnd callback called")
    st.session_state.navigate_to = "pages/01_DnD.py"

def _go_op():
    print("DEBUG: _go_op callback called") 
    st.session_state.navigate_to = "pages/02_OrdemParanormal.py"


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

# place system choice as buttons and use query params for shareable navigation
# ensure session key exists
if 'selected_system' not in st.session_state:
    st.session_state['selected_system'] = None

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="narrow-selectbox">', unsafe_allow_html=True)
    st.write('Escolha qual sistema quer usar:')
    
    # Style Streamlit buttons with centered positioning
    st.markdown('''
    <style>
    .stButton>button {
        background-color: #6b6b6b !important;
        color: white !important;
        border-radius: 6px;
        padding: 8px 14px;
        font-weight: 600;
        width: 100% !important;
    }
    .stButton>button:hover { opacity: 0.9; }
    </style>
    ''', unsafe_allow_html=True)

    # Center the buttons in columns
    col_a, col_b = st.columns(2)
    with col_a:
        st.button('Abrir D&D', on_click=_go_dnd, key='btn_dnd')
    with col_b:
        st.button('Abrir Ordem Paranormal', on_click=_go_op, key='btn_op')

    st.markdown('</div>', unsafe_allow_html=True)

    # Handle navigation after button clicks using session state
    if 'navigate_to' in st.session_state and st.session_state.navigate_to:
        page_to_navigate = st.session_state.navigate_to
        st.session_state.navigate_to = None  # Clear the flag
        st.switch_page(page_to_navigate)

# Note: navigation to pages is handled by Streamlit when the browser navigates to
# the page route (e.g. /DnD or /OrdemParanormal). We avoid executing page scripts
# from main so the landing page content is not shown together with a page.

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