import streamlit as st
import base64
import os
import pdfplumber
import pytesseract
from functions import *
from PyPDF2 import PdfReader


# Set page configuration
st.set_page_config(
    page_title="RPG Character Creator",
    page_icon="⚔️",
    layout="wide"
)

# Function to load and encode local image
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Load the brick wall background image
bg_image_path = "assets/brick_wall.jpg"  # Update this with your actual image filename
bg_image_base64 = get_base64_image(bg_image_path)

# Apply custom background with local image
if bg_image_base64:
    page_bg_img = f'''
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_image_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    
    .main .block-container {{
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    </style>
    '''
else:
    # Fallback CSS background if image not found
    page_bg_img = '''
    <style>
    .stApp {
        background: linear-gradient(135deg, #c4714b 0%, #a8613e 25%, #b56a45 50%, #9e5937 75%, #c4714b 100%);
    }
    
    .main .block-container {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    '''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Main content
st.title("Bem-vindo ao Criador de Personagens RPG!")
st.write("Crie seu próprio personagem de RPG com atributos e habilidades personalizáveis.")

# Add a dropdown menu for RPG systems
rpg_system = st.selectbox(
    "Escolha qual sistema quer usar:",
    ["", "D&D", "Ordem Paranormal"]
)

# Display the selected option if a valid system is chosen
if rpg_system != "Escolha qual sistema quer usar:" and rpg_system != "":
    st.write(f"Você selecionou: {rpg_system}")

# Handle file processing based on dropdown selection
if rpg_system == "D&D":
    st.write("Vamos começar a criar esse personagem de D&D!")

    # Define file paths
    files_to_process = [
        "assets/D&D.pdf"
    ]

    # Class selection
    character_class = st.selectbox(
        "Selecione sua classe de personagem:",
        ["", "Bárbaro", "Bardo", "Clérigo", "Druida", "Feiticeiro", "Guardião", "Guerreiro", "Ladrão", "Mago",
         "Monge", "Paladino"]
    )

    if character_class != "" and character_class != "Selecione sua classe de personagem:":
        st.write(f"Você selecionou: {character_class}\n")
        search_term = character_class.lower()
        st.write(f"Essa é a tabela de traços da classe escolhida:")

        # Extract and display the basic traits table
        traits_table = basic_traits_table_extraction("assets/D&D.pdf", search_term)
        if traits_table:
            for row in traits_table:
                st.write(row)
        else:
            st.write("Tabela de traços não encontrada.")

    # Origin Selection
    


# Entry point for the Python RPG Character Creator

def main():
    print("Welcome to the Python RPG Character Creator!")

if __name__ == "__main__":
    main()