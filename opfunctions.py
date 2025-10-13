import pdfplumber
import pytesseract
import streamlit as st
from pypdf import PdfReader
from PIL import Image
import pandas as pd
import re
from typing import Optional, Sequence
from functools import partial
from functions import *


def select_origin():
    #Passo 3
    pdf_paths = ["assets/OP-Origens.pdf","assets/OP-SaH-Origens.pdf"]
    origin = st.selectbox(
        "Selecione a origem do seu personagem:",
        [""] + pdf_paths
    )

'''def select_class():
    #Passo 4

def select_skills():
    #Passo 5

def select_trilha():
    #Passo 6

def nex_increase():
    #Passo 7'''

def nex_selector():
    # place the selectbox in a centered column so it visually appears narrow
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.write("Nível de Exposição\n")
        nex_value = st.selectbox("NEX",["", "05%", "10%", "15%", "20%", "25%", "30%", "35%", "40%", "45%", "50%",
                   "55%", "60%", "65%", "70%", "75%", "80%", "85%", "90%", "95%", "99%"])
        if nex_value >= "05%" and nex_value < "20%":
            st.write("Valor máximo para atributos = 3")
        elif nex_value >= "20%" and nex_value < "50%":
            st.write("Valor máximo para atributos = 4")
        elif nex_value >= "50%" and nex_value < "80%":
            st.write("Valor máximo para atributos = 5")

def atts_selector(num_attributes: int = 5, min_value: int = 0, max_value: int = 5, labels: Optional[Sequence[str]] = None) -> Sequence[int]:
    """Render N attribute columns and return their integer values.

    Args:
        num_attributes: number of columns to render.
        min_value: minimum allowed value for each attribute.
        max_value: maximum allowed value for each attribute.
        labels: optional sequence of strings used as static column headings. If
            shorter than num_attributes it will be padded with default names.

    Returns:
        Sequence[int]: current values for each attribute in order.
    """

    # prepare column headings
    if labels is None:
        labels = [f"Box {i+1}" for i in range(num_attributes)]
    else:
        labels = list(labels)
        if len(labels) < num_attributes:
            labels += [f"Box {i+1}" for i in range(len(labels), num_attributes)]

    cols = st.columns(num_attributes)
    for i, col in enumerate(cols):
        key = f"box_{i}"
        # initialize to 1 if not present yet
        if key not in st.session_state:
            st.session_state[key] = 1

        # create inner columns once and render header + controls so header always shows
        inner = col.columns([0.4, 0.8, 1.0])
        header_html = f"<div style='text-align:center; font-weight:700; margin-bottom:6px'>{labels[i]}</div>"
        inner[1].markdown(header_html, unsafe_allow_html=True)

        # horizontal row: - | value | +
        with inner[0]:
            inner[0].button("➖", key=f"dec_{i}", on_click=partial(dec_with_limit, key, min_value))
        with inner[1]:
            inner[1].markdown(f"<div style='text-align:center; font-size:20px; font-weight:700; color:#6EE7B7'>{st.session_state[key]}</div>", unsafe_allow_html=True)
        with inner[2]:
            inner[2].button("➕", key=f"inc_{i}", on_click=partial(inc_with_limit, key, max_value))

    # return current values as a list
    return [st.session_state[f"box_{i}"] for i in range(num_attributes)]

def inc_with_limit(key, maxv):
    st.session_state[key] = min(maxv, st.session_state.get(key, 1) + 1)


def dec_with_limit(key, minv):
    st.session_state[key] = max(minv, st.session_state.get(key, 1) - 1)

''' 
cols = st.columns(5)
for i, col in enumerate(cols):
    key = f"box_{i}"
    # initialize to 1 if not present yet
    if key not in st.session_state:
        st.session_state[key] = 1

    with col:
        st.markdown(f"**Box {i+1}**")
        # place decrease button, show value, then increase button
        # use distinct keys for the buttons so Streamlit keeps them independent
        col.button("−", key=f"dec_{i}", on_click=dec, args=(key,))
        col.write(st.session_state[key])
        col.button("+", key=f"inc_{i}", on_click=inc, args=(key,))'''

