import streamlit as st
from assets.OP_Origens import descricao_origens

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

def _go_op():
    st.session_state.navigate_to = "pages/02_OrdemParanormal.py"

# Title centered (use a centered header without a narrow 3-column wrapper)
st.markdown("""
<h1 style='text-align:center'>Ordem Paranormal — Criador de Personagens</h1>
<p style='text-align:center;margin-top:-0.5rem'>Vamos ver um resumo das origens!</p>
""", unsafe_allow_html=True)

# Origins resume expanders
items = list(descricao_origens.items())
col1_items = items[0::3]   # indexes 0,3,6,...
col2_items = items[1::3]   # indexes 1,4,7,...
col3_items = items[2::3]   # indexes 2,5,8,...

c1, c2, c3 = st.columns(3)

with c1:
    for k, v in col1_items:
        with st.expander(k):
            st.write(v)

with c2:
    for k, v in col2_items:
        with st.expander(k):
            st.write(v)

with c3:
    for k, v in col3_items:
        with st.expander(k):
            st.write(v)

# Origin selection
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.write("\nAgora, escolha a origem do seu personagem:\n")
    origin_choice = st.selectbox(
        "Escolha a origem",
        ["Nenhuma"] + list(descricao_origens.keys()),
        index=0,
        key="origin_choice"
    )

# Navigation buttons
c1, c2, c3 = st.columns([1, 1, 8])
with c1:
    st.button('← Voltar ao início', on_click=_go_home)
with c2:
    st.button('← Voltar à Ordem Paranormal', on_click=_go_op)

# Navigation handler
if 'navigate_to' in st.session_state and st.session_state.navigate_to:
    page_to_navigate = st.session_state.navigate_to
    st.session_state.navigate_to = None
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