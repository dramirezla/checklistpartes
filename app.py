from PyPDF2 import PdfReader
import io
from collections import Counter
import re
import streamlit as st


# Función para procesar el archivo PDF
def procesar_pdf(pdf_file):
    # Leer el archivo PDF
    reader = PdfReader(pdf_file)
    contenido_paginas = []
    
    for page in reader.pages:
        texto = page.extract_text()
        contenido_paginas.append(texto)
    
    # Aquí puedes aplicar tu procesamiento de las páginas y extraer la información que necesites
    return contenido_paginas

# Crear la interfaz de usuario
st.title("Sube tu archivo PDF para procesar")

# Subir archivo PDF
pdf_file = st.file_uploader("Elige un archivo PDF", type="pdf")

# Si el usuario ha subido un archivo
if pdf_file is not None:
    st.write("Archivo subido correctamente")

    # Mostrar el contenido del PDF como ejemplo (puedes eliminar esto si no lo deseas)
    contenido_paginas = procesar_pdf(pdf_file)
    
    for i, pagina in enumerate(contenido_paginas):
        print(f"Página {i}:") # layout
        print(pagina)  # Muestra el texto extraído de la página

    # Botón para procesar el PDF (en caso de que se desee realizar alguna acción adicional)
    ##############Logica
    contenido_formateado = []  # Lista para almacenar el contenido modificado
    partes_por_pagina = []  # Lista para almacenar las partes encontradas por cada página
    partes_frecuencia = Counter()  # Diccionario para contar la frecuencia de cada letra
    
    for pagina in contenido_paginas:
        # Inicializamos una lista para almacenar las partes de la página actual
        partes_pagina = []
        
        # Dividir el contenido usando "Kerf" como punto de corte
        partes_pagina_dividida = pagina.split("Kerf: ", 1)  # Dividir en dos partes; antes y después de "Kerf"
    
        # Obtener todo el contenido después de "Kerf"
        contenido_modificado = partes_pagina_dividida[1] if len(partes_pagina_dividida) > 1 else ""
        contenido_formateado.append(contenido_modificado)
    
        # Buscar todas las partes capitalizadas en el contenido modificado
        partes_mayusculas = re.findall(r'[A-Z]', contenido_modificado)
        
        # Añadir las partes capitalizadas a la lista de la página
        partes_pagina.extend(partes_mayusculas)
        
        # Actualizar la frecuencia de las partes mayúsculas
        partes_frecuencia.update(partes_mayusculas)
        
        # Agregar la lista de partes de la página a la lista general
        partes_por_pagina.append(partes_pagina)
    
    # Mostrar los resultados en Streamlit
    
    # Mostrar la frecuencia de las partes mayúsculas de forma simplificada
    st.write("### Frecuencia de las partes encontradas (Layout 0):")
    partes_frecuencia_df = {letra: frecuencia for letra, frecuencia in partes_frecuencia.items()}
    st.dataframe(partes_frecuencia_df)
    
    letras_seleccionadas = []
    
    # Mostrar las partes encontradas en un checklist por página
    for pagina_num, partes in enumerate(partes_por_pagina):
        st.write(f"### Partes encontradas en la Página {pagina_num + 1}:")
        
        for i, parte in enumerate(partes):
            # Hacer que cada parte sea un checkbox con una clave única usando el índice 'i'
            if st.checkbox(f"{parte}", key=f"parte_{pagina_num}_{i}"):
                letras_seleccionadas.append(parte)
    
    # Estilo y colores en la tabla de frecuencias
    st.write("### Tabla de Frecuencia de las partes seleccionadas")
    
    if st.button("Mostrar Frecuencia de Partes seleccionadas"):
        letras_seleccionadas_frecuencia = Counter(letras_seleccionadas)
        if letras_seleccionadas_frecuencia:
            st.dataframe(letras_seleccionadas_frecuencia)
        else:
            st.write("No se ha seleccionado ninguna letra.")
