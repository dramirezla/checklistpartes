import streamlit as st
from PyPDF2 import PdfReader
import base64
from io import BytesIO

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

# Función para convertir el archivo a base64 para visualización
def convertir_pdf_a_base64(pdf_file):
    pdf_bytes = pdf_file.read()
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    return base64_pdf

# Crear la interfaz de usuario
st.title("Sube tu archivo PDF para procesar")

# Subir archivo PDF
pdf_file = st.file_uploader("Elige un archivo PDF", type="pdf")

if pdf_file is not None:
    st.write("Archivo subido correctamente")
    
    # Procesar y mostrar el contenido extraído del PDF
    contenido_paginas = procesar_pdf(pdf_file)
    
    st.write("### Contenido extraído:")
    for i, pagina in enumerate(contenido_paginas):
        st.text(f"Página {i + 1}:")
        st.write(pagina)

    # Mostrar el PDF en la interfaz
    st.write("### Visualización del PDF:")
    pdf_base64 = convertir_pdf_a_base64(pdf_file)
    pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="700" height="900" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

    contenido_formateado = []  # Lista para almacenar el contenido modificado
    partes = []  # Lista para almacenar las partes capitalizadas
    partes_frecuencia = Counter()  # Diccionario para contar la frecuencia de cada letra
    
    for pagina in contenido_paginas:
        # Dividir el contenido usando "Kerf" como punto de corte
        partes_pagina = pagina.split("Kerf: ", 1)  # Dividir en dos partes; antes y después de "Kerf"
    
        # Obtener todo el contenido después de "Kerf"
        contenido_modificado = partes_pagina[1] if len(partes_pagina) > 1 else ""
        contenido_formateado.append(contenido_modificado)
    
        # Buscar todas las partes capitalizadas en el contenido modificado
        partes_mayusculas = re.findall(r'[A-Z]', contenido_modificado)
    
        # Añadir las partes capitalizadas a la lista 'partes'
        partes.extend(partes_mayusculas)
    
        # Contar las partes mayúsculas y actualizar el diccionario de frecuencias
        partes_frecuencia.update(partes_mayusculas)
    
    # Mostrar los resultados en Streamlit
    
    # Mostrar la frecuencia de las partes mayúsculas de forma simplificada
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

