import pdfplumber
import pytesseract
import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
import pandas as pd
import re
from typing import Optional, Sequence
from functools import partial

def atts_selector(num_attributes: int = 5, min_value: int = 0, max_value: int = 5) -> Sequence[int]:
    cols = st.columns(num_attributes)
    for i, col in enumerate(cols):
        key = f"box_{i}"
        # initialize to 1 if not present yet
        if key not in st.session_state:
            st.session_state[key] = 1

        with col:
            st.markdown(f"**Box {i+1}**")
            # place decrease button, show value, then increase button
            # use distinct keys for the buttons so Streamlit keeps them independent
            # bind per-column min/max using functools.partial
            col.button("−", key=f"dec_{i}", on_click=partial(dec_with_limit, key, min_value))
            col.write(st.session_state[key])
            col.button("+", key=f"inc_{i}", on_click=partial(inc_with_limit, key, max_value))

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

