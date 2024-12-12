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

        # Dividir la lista de letras en bloques de 10 para la paginación
        bloques_por_pagina = [letras_pagina[i:i + 10] for i in range(0, len(letras_pagina), 10)]
        
        # Paginación
        pagina_actual = st.selectbox(
            f"Selecciona un bloque de letras en la Página {indice + 1}", 
            range(len(bloques_por_pagina)), 
            index=0
        )

        for letra in bloques_por_pagina[pagina_actual]:
            if st.checkbox(f"{letra}", key=f"pagina_{indice}_letra_{letras_pagina.index(letra)}"):
                letras_seleccionadas.append(letra)

        letras_seleccionadas_por_pagina.append(letras_seleccionadas)

    # Mostrar resultados en DataFrame
    contenido_formateado = []  # Lista para almacenar el contenido modificado
    partes = []  # Lista para almacenar las partes capitalizadas
    partes_frecuencia = Counter()  # Diccionario para contar la frecuencia de cada letra

    for pagina in contenido_paginas:
        # Dividir el contenido usando "Kerf" como punto de corte
        partes_pagina = pagina.split("Kerf: ", 1)
        contenido_modificado = partes_pagina[1] if len(partes_pagina) > 1 else ""
        contenido_formateado.append(contenido_modificado)

        # Buscar todas las partes capitalizadas en el contenido modificado
        partes_mayusculas = re.findall(r'[A-Z]', contenido_modificado)
        
        # Añadir las partes capitalizadas a la lista 'partes'
        partes.extend(partes_mayusculas)
        
        # Contar las partes mayúsculas y actualizar el diccionario de frecuencias
        partes_frecuencia.update(partes_mayusculas)

    # Mostrar los resultados en Streamlit
    st.write("### Frecuencia de las partes encontradas:")
    partes_frecuencia_df = {letra: frecuencia for letra, frecuencia in partes_frecuencia.items()}
    st.dataframe(partes_frecuencia_df)

    letras_seleccionadas = []
    
    # Mostrar las partes encontradas en un checklist
    st.write("### Partes encontradas en el contenido:")
    for i, parte in enumerate(partes):
        # Hacer que cada parte sea un checkbox con una clave única usando el índice 'i'
        if st.checkbox(f"{parte}", key=f"parte_{i}"):
            letras_seleccionadas.append(parte)
    
    # Estilo y colores en la tabla de frecuencias
    st.write("### Tabla de Frecuencia de las partes seleccionadas")
    
    if st.button("Mostrar Frecuencia de Partes seleccionadas"):
        letras_seleccionadas_frecuencia = Counter(letras_seleccionadas)
        if letras_seleccionadas_frecuencia:
            st.dataframe(letras_seleccionadas_frecuencia)
        else:
            st.write("No se ha seleccionado ninguna letra.")
