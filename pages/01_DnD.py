import streamlit as st
from functions import *
from dndfunctions import *

# Hide the Streamlit left sidebar visually for this page
st.markdown(
    """
    <style>
    div[data-testid="stSidebar"] { display: none !important; }
    button[aria-label="Toggle sidebar"] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

def _go_home():
    st.session_state.navigate_to = "main.py"

st.title('D&D — Criador de Personagens')

# In multipage navigation, we don't need to check query params
# The page is accessed when the user navigates to /DnD
st.write("Vamos começar a criar esse personagem de D&D!\n")

# Call existing D&D flow
choose_dnd_class()

st.button('← Voltar ao início', on_click=_go_home)

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
        pass
    st.switch_page(page_to_navigate)
