import streamlit as st
from functions import *
from opfunctions import *

def _go_home():
    st.session_state.navigate_to = "main.py"

st.title('Ordem Paranormal — Criador de Personagens')

# In multipage navigation, we don't need to check query params
# The page is accessed when the user navigates to /OrdemParanormal
st.write("Vamos começar a criar esse personagem de Ordem Paranormal!\n")

nex_value = nex_selector()
if nex_value and nex_value != "":
    attrs = atts_selector(5, labels=["Força", "Agilidade", "Intelecto", "Presença", "Vigor"])
    select_origin()

st.button('← Voltar ao início', on_click=_go_home)

# Handle navigation after button clicks using session state
if 'navigate_to' in st.session_state and st.session_state.navigate_to:
    page_to_navigate = st.session_state.navigate_to
    st.session_state.navigate_to = None  # Clear the flag
    st.switch_page(page_to_navigate)
