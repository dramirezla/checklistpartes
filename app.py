import streamlit as st
from PyPDF2 import PdfReader
import re
from collections import Counter

# Cambia el nombre al nombre de tu archivo cargado
nombre_archivo1 = "5.50 SUPERCOR BOREAL 15MM 183X244 - ANDRES LOPEZ - SEBASTIAN BEDOYA - VIRTUAL.pdf"

# Cargar el PDF
reader1 = PdfReader(nombre_archivo1)

# Extraer contenido página por página
contenido_paginas1 = []
for x, page in enumerate(reader1.pages):
    texto1 = page.extract_text()
    contenido_paginas1.append(texto1)
    print(f"Texto de la página {x + 1}:\n{texto1}\n{'-'*50}")

contenido_paginas1.remove(contenido_paginas1[0])

# Cambia el nombre al nombre de tu archivo cargado
nombre_archivo = "despiece ejemplo.pdf"

# Cargar el PDF
reader = PdfReader(nombre_archivo)

# Extraer contenido página por página
contenido_paginas = []
for i, page in enumerate(reader.pages):
    texto = page.extract_text()
    contenido_paginas.append(texto)
    print(f"Texto de la página {i + 1}:\n{texto}\n{'-'*50}")

# `contenido_paginas` tiene todo el contenido dividido por páginas

# Elimino la primera pagina que es la que tiene la lista de partes
contenido_paginas.remove(contenido_paginas[0])

contenido_formateado = []  # Lista para almacenar el contenido modificado
partes = []  # Lista para almacenar las letras capitalizadas
letras_frecuencia = Counter()  # Diccionario para contar la frecuencia de cada letra

for pagina in contenido_paginas:
    # Dividir el contenido usando "Kerf" como punto de corte
    partes_pagina = pagina.split("Kerf: ", 1)  # Dividir en dos partes; antes y después de "Kerf"

    # Obtener todo el contenido después de "Kerf"
    contenido_modificado = partes_pagina[1] if len(partes_pagina) > 1 else ""
    contenido_formateado.append(contenido_modificado)

    # Buscar todas las letras capitalizadas en el contenido modificado
    letras_mayusculas = re.findall(r'[A-Z]', contenido_modificado)

    # Añadir las letras capitalizadas a la lista 'partes'
    partes.extend(letras_mayusculas)

    # Contar las letras mayúsculas y actualizar el diccionario de frecuencias
    letras_frecuencia.update(letras_mayusculas)

# Mostrar los resultados en Streamlit

# Mostrar la frecuencia de las letras mayúsculas de forma simplificada
st.write("### Frecuencia de las letras mayúsculas encontradas:")
letras_frecuencia_df = {letra: frecuencia for letra, frecuencia in letras_frecuencia.items()}
st.dataframe(letras_frecuencia_df)

# Mostrar las partes encontradas en un checklist
st.write("### Letras capitalizadas encontradas en el contenido:")
for i, parte in enumerate(partes):
    # Hacer que cada parte sea un checkbox con una clave única usando el índice 'i'
    if st.checkbox(f"¿Contiene la letra: {parte}", key=f"parte_{i}"):
        st.markdown(f"<span style='color: green;'>✔ {parte}</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"<span style='color: red;'>❌ {parte}</span>", unsafe_allow_html=True)

# Estilo y colores en la tabla de frecuencias
st.write("### Tabla de Frecuencia con colores:")
tabla_estilo = f"""
    <style>
        .stDataFrame table {{
            border-collapse: collapse;
            width: 100%;
        }}
        .stDataFrame th, .stDataFrame td {{
            padding: 8px;
            text-align: left;
            border: 1px solid #ddd;
        }}
        .stDataFrame tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
        .stDataFrame th {{
            background-color: #4CAF50;
            color: white;
        }}
        .stDataFrame td {{
            background-color: #f9f9f9;
        }}
    </style>
"""
st.markdown(tabla_estilo, unsafe_allow_html=True)
st.table(letras_frecuencia.items())
