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
    
    # Procesar el archivo PDF
    contenido_paginas = procesar_pdf(pdf_file)
    contenido_por_pagina = []
    letras_por_pagina = []
    letras_seleccionadas_por_pagina = []

    # Procesar cada página
    for pagina in contenido_paginas:
        # Dividir usando "Kerf" como punto de corte
        partes_pagina = pagina.split("Kerf: ", 1)
        contenido_modificado = partes_pagina[1] if len(partes_pagina) > 1 else ""
        contenido_por_pagina.append(contenido_modificado)

        # Buscar letras mayúsculas
        letras_mayusculas = re.findall(r'[A-Z]', contenido_modificado)
        letras_por_pagina.append(letras_mayusculas)

    # Mostrar checkboxes separadas por página
    st.write("### Selecciona las partes encontradas por página:")
    for indice, letras_pagina in enumerate(letras_por_pagina):
        st.write(f"**Página {indice + 1}**")
        letras_seleccionadas = []

        for i, letra in enumerate(letras_pagina):
            # Checkbox única para cada letra
            if st.checkbox(f"{letra}", key=f"pagina_{indice}_letra_{i}"):
                letras_seleccionadas.append(letra)

        letras_seleccionadas_por_pagina.append(letras_seleccionadas)

    # Mostrar resumen de selección
    st.write("### Resumen de letras seleccionadas:")
    for indice, letras_seleccionadas in enumerate(letras_seleccionadas_por_pagina):
        if letras_seleccionadas:
            st.write(f"Página {indice + 1}: {', '.join(letras_seleccionadas)}")
        else:
            st.write(f"Página {indice + 1}: No se seleccionaron letras.")
