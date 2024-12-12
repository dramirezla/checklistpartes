import streamlit as st
from PyPDF2 import PdfReader
import io
from collections import Counter
import re

# Función para procesar el archivo PDF
def procesar_pdf(pdf_file):
    # Leer el archivo PDF
    reader = PdfReader(pdf_file)
    contenido_paginas = []
    
    for page in reader.pages:
        texto = page.extract_text()
        contenido_paginas.append(texto)
    
    return contenido_paginas

# Crear la interfaz de usuario
st.title("Sube tu archivo PDF para procesar")

# Subir archivo PDF
pdf_file = st.file_uploader("Elige un archivo PDF", type="pdf")

# Si el usuario ha subido un archivo
if pdf_file is not None:
    st.write("Archivo subido correctamente")

    # Procesar el PDF
    contenido_paginas = procesar_pdf(pdf_file)
    
    # Crear columnas para organizar las casillas de verificación
    num_paginas = len(contenido_paginas)
    columnas = st.columns(num_paginas)
    
    # Lista para almacenar las letras seleccionadas
    letras_seleccionadas = []
    
    # Iterar sobre las páginas y mostrar las casillas de verificación
    for i, pagina in enumerate(contenido_paginas):
        with columnas[i]:
            st.write(f"### Página {i + 1}")
            partes_mayusculas = re.findall(r'[A-Z]', pagina)
            partes_frecuencia = Counter(partes_mayusculas)
            
            # Mostrar las letras encontradas en la página
            for letra, frecuencia in partes_frecuencia.items():
                if st.checkbox(f"{letra} ({frecuencia} veces)", key=f"letra_{i}_{letra}"):
                    letras_seleccionadas.append(letra)
    
    # Mostrar la frecuencia de las letras seleccionadas
    if letras_seleccionadas:
        st.write("### Frecuencia de las letras seleccionadas:")
        letras_seleccionadas_frecuencia = Counter(letras_seleccionadas)
        st.write(letras_seleccionadas_frecuencia)
    else:
        st.write("No se ha seleccionado ninguna letra.")
