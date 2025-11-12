import streamlit as st
from functions import *
from dndfunctions import *

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
    st.switch_page(page_to_navigate)
