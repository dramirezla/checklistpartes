import streamlit as st
from PyPDF2 import PdfReader
import base64
from io import BytesIO
from collections import Counter
import re
import os

# Función para procesar el archivo PDF
# Procesamiento de PDF
def procesar_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    contenido_paginas = []
    for page in reader.pages:
        contenido_paginas.append(page.extract_text())
    return contenido_paginas

# Configuración de la interfaz
st.title("Procesador y Visualizador de PDF")

pdf_file = st.file_uploader("Sube un archivo PDF", type="pdf")

if pdf_file is not None:
    st.write("### Archivo subido correctamente")
    
    contenido_paginas = procesar_pdf(pdf_file)
    for i, pagina in enumerate(contenido_paginas):
        st.write(f"**Página {i + 1}:**")
        st.text(pagina)
    
    # Guardar temporalmente el archivo
    with open("archivo.pdf", "wb") as f:
        f.write(pdf_file.read())
    
    # Mostrar el PDF mediante iframe
    st.markdown(
        f'<iframe src="/archivo.pdf" width="700" height="900" type="application/pdf"></iframe>',
        unsafe_allow_html=True,
    )
