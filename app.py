import streamlit as st
from PyPDF2 import PdfReader
import base64
from io import BytesIO
from collections import Counter
import re
import os

# Función para procesar el archivo PDF
# Función para procesar el archivo PDF
def procesar_pdf(pdf_file):
    # Leer el archivo PDF
    reader = PdfReader(pdf_file)
    contenido_paginas = []
    for page in reader.pages:
        texto = page.extract_text()
        contenido_paginas.append(texto)
    return contenido_paginas

# Interfaz de Streamlit
st.title("Procesador y Visualizador de PDF")

# Subir archivo PDF
pdf_file = st.file_uploader("Sube tu archivo PDF", type="pdf")

if pdf_file is not None:
    st.write("### Archivo subido correctamente")
    
    # Procesar el contenido del PDF
    contenido_paginas = procesar_pdf(pdf_file)
    st.write("### Contenido extraído del PDF:")
    for i, pagina in enumerate(contenido_paginas):
        st.write(f"**Página {i + 1}:**")
        st.text(pagina)
    
    # Guardar el archivo temporalmente
    temp_file_path = "temp_uploaded_file.pdf"
    with open(temp_file_path, "wb") as f:
        f.write(pdf_file.read())
    
    # Mostrar el PDF en un iframe
    st.write("### Visualización del PDF:")
    pdf_display = f'<iframe src="{temp_file_path}" width="700" height="900" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
    
    # Eliminar el archivo temporal cuando sea necesario
    if st.button("Eliminar archivo temporal"):
        os.remove(temp_file_path)
        st.write("Archivo temporal eliminado.")
