import streamlit as st
from functions import *
from opfunctions import *

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

def _go_origem():
    try:
        pages = st.experimental_get_pages()
        target_key = None
        for key, page in pages.items():
            if getattr(page, "path", "").endswith("OP_Origem.py"):
                target_key = key
                break
        if target_key:
            st.session_state.navigate_to = target_key
        else:
            st.session_state.navigate_to = "pages/OP_Origem.py"
    except Exception:
        st.session_state.navigate_to = "pages/OP_Origem.py"

col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.title('Ordem Paranormal — Criador de Personagens\n')

    st.write("Vamos começar pela Classe do seu personagem.\n Escolha uma das opções abaixo:\n")

    class_selection = st.radio(
        "Escolha a classe",
        ["Nenhuma", "Combatente", "Especialista", "Ocultista"],
        index=0,
        key="class_choice",
        horizontal=True  # <-- renders radio options side-by-side
    )

# only show expanders for the selected class
if class_selection == "Nenhuma":
    st.write("Por favor, selecione uma classe para o seu personagem.")
elif class_selection == "Combatente":
    with st.expander("Combatente", expanded=True):
        st.write("O combatente é aquele que se destaca nas batalhas físicas, seja com armas ou combate corpo a corpo.\n")
        # class-specific widgets...
elif class_selection == "Especialista":
    with st.expander("Especialista", expanded=True):
        st.write("O especialista é aquele que possui a capacidade de se adaptar a diversas situações e agir de forma versátil.\n")
elif class_selection == "Ocultista":
    with st.expander("Ocultista", expanded=True):
        st.write("O ocultista é aquele que domina rituais e entende o Outro Lado de maneira mais profunda.\n")

choice = st.session_state.get("class_choice", "Nenhuma")

if choice and choice != "Nenhuma":
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.write(f"Você selecionou **{choice}**. Deseja prosseguir com esta classe?")
    
        st.caption("Revise as opções acima; ao prosseguir os valores serão usados para gerar o personagem.")
        if st.button("Prosseguir", key="btn_proceed", on_click=_go_origem):
            st.session_state["selected_class"] = choice
            st.session_state["proceed_with_class"] = True
            st.success(f"Prosseguindo com {choice}.")

            # optional navigation (uncomment if desired)
            # st.session_state.navigate_to = "main.py"
            # st.experimental_rerun()
    

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
