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

# Hide specific pages from the Streamlit sidebar (keeps files in repo but not listed)
try:
    pages = st.experimental_get_pages()
    # Filter out any page whose source path ends with the given filename
    filtered = {k: v for k, v in pages.items() if not getattr(v, 'path', k).endswith('pages/OP_Origem.py')}
    if len(filtered) != len(pages):
        st.experimental_set_pages(filtered)
except Exception:
    # experimental_get_pages may not be available in older Streamlit versions
    pass


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
    layout="wide",
    initial_sidebar_state="collapsed",
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

# Hide the Streamlit left sidebar visually across pages
st.markdown(
    """
    <style>
    div[data-testid="stSidebar"] { display: none !important; }
    button[aria-label="Toggle sidebar"] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Also remove the sidebar node using a small JS snippet (components.html) to be robust
try:
    components.html(
        """
        <script>
        (function(){
            const selectors = ['div[data-testid="stSidebar"]', 'div[data-testid="stSidebarNav"]', 'aside', 'section[role="complementary"]'];
            for (const sel of selectors) {
                const el = document.querySelector(sel);
                if (el) { el.remove(); }
            }
            const toggles = document.querySelectorAll('button[aria-label="Toggle sidebar"], button[title="Toggle sidebar"]');
            toggles.forEach(t => t.remove());
        })();
        </script>
        """,
        height=0,
    )
except Exception:
    # components.html may not work in some environments; CSS fallback remains
    pass

# Expand the main content container so columns can use full browser width
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 100% !important;
        width: 100% !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main content (centered)
st.markdown(
    """
    <div style='text-align:center'>
        <h1>Bem-vindo ao Criador de Personagens RPG!</h1>
        <p>Crie seu próprio personagem de RPG com atributos e habilidades personalizáveis.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

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
        # Opens DnD Character Creator page
        st.button('Abrir D&D', on_click=_go_dnd, key='btn_dnd')
    with col_b:
        # Opens Ordem Paranormal Character Creator page
        st.button('Abrir Ordem Paranormal', on_click=_go_op, key='btn_op')

    st.markdown('</div>', unsafe_allow_html=True)

    # Handle navigation after button clicks using session state
    if 'navigate_to' in st.session_state and st.session_state.navigate_to:
        page_to_navigate = st.session_state.navigate_to
        st.session_state.navigate_to = None  # Clear the flag
        try:
            pages = st.experimental_get_pages()
            # If a file path (endswith .py) was stored, try to find the registered page key
            if isinstance(page_to_navigate, str) and page_to_navigate.endswith('.py'):
                for key, page in pages.items():
                    if getattr(page, 'path', '').endswith(page_to_navigate):
                        page_to_navigate = key
                        break
        except Exception:
            # experimental_get_pages may not exist on older Streamlit versions
            pass
        st.switch_page(page_to_navigate)

# Note: navigation to pages is handled by Streamlit when the browser navigates to
# the page route (e.g. /DnD or /OrdemParanormal). We avoid executing page scripts
# from main so the landing page content is not shown together with a page.

# Entry point for the Python RPG Character Creator

def main():
    print("Welcome to the Python RPG Character Creator!")

if __name__ == "__main__":
    main()
