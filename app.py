from PyPDF2 import PdfReader
import io
from collections import Counter
import re
import streamlit as st
from pdf2image import convert_from_bytes  # Necesitarás instalar esta librería
import fitz  # PyMuPDF

# Función para procesar el archivo PDF
def procesar_pdf(pdf_file):
    # Leer el archivo PDF
    reader = fitz.open(pdf_file)
    contenido_paginas = []
    
    for page_num in range(reader.page_count):
        page = reader.load_page(page_num)  # Cargar la página
        texto = page.get_text()  # Extraer texto de la página
        contenido_paginas.append(texto)
    
    return contenido_paginas

# Función para convertir el PDF en imágenes
def mostrar_pdf_como_imagen(pdf_file):
    # Abrir el archivo PDF con PyMuPDF
    pdf_document = fitz.open(pdf_file)
    
    # Convertir cada página a imagen
    pdf_images = []
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # Cargar la página
        pix = page.get_pixmap()  # Convertir la página a imagen
        img_byte_array = pix.tobytes("png")  # Convertir la imagen a bytes
        pdf_images.append(img_byte_array)
    
    return pdf_images

# Crear la interfaz de usuario en Streamlit
st.title("Sube tu archivo PDF para procesar")

# Subir archivo PDF
pdf_file = st.file_uploader("Elige un archivo PDF", type="pdf")

# Si el usuario ha subido un archivo
if pdf_file is not None:
    st.write("Archivo subido correctamente")

    # Convertir el archivo PDF en imágenes usando PyMuPDF
    pdf_images = mostrar_pdf_como_imagen(pdf_file)

    # Mostrar el PDF como imágenes
    st.write("### Vista previa del PDF")
    for page_number, img_byte_array in enumerate(pdf_images):
        st.image(img_byte_array, caption=f"Página {page_number + 1}", use_container_width=True)

    # Procesar el contenido del PDF (extraer texto)
    contenido_paginas = procesar_pdf(pdf_file)
    
    # Aquí va tu lógica para procesar el contenido del PDF
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
        if pagina_num != 0:
             st.write(f"### Partes encontradas en el Layout {pagina_num}:")
        
        for i, parte in enumerate(partes):
            # Hacer que cada parte sea un checkbox con una clave única usando el índice 'i'
            if st.checkbox(f"{parte}", key=f"parte_{pagina_num}_{i}"):
                letras_seleccionadas.append(parte)
    
    # Estilo y colores en la tabla de frecuencias
    if st.button("Mostrar Frecuencia de Partes seleccionadas"):
        letras_seleccionadas_frecuencia = Counter(letras_seleccionadas)
        if letras_seleccionadas_frecuencia:
            st.write("### Tabla de Frecuencia de las partes seleccionadas")
            st.dataframe(letras_seleccionadas_frecuencia)
        else:
            st.write("No se ha seleccionado ninguna letra.")
