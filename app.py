def procesar_pdf(pdf_file):
    # Leer el archivo PDF
    reader = PdfReader(pdf_file)
    contenido_paginas = []
    for page in reader.pages:
        texto = page.extract_text()
        contenido_paginas.append(texto)
    return contenido_paginas

# Función para convertir el PDF a base64
def convertir_pdf_a_base64(pdf_file):
    pdf_bytes = pdf_file.read()
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    return base64_pdf

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
    
    # Mostrar el PDF en un visor embebido
    st.write("### Visualización del PDF:")
    pdf_base64 = convertir_pdf_a_base64(pdf_file)
    pdf_display = f'<embed src="data:application/pdf;base64,{pdf_base64}" width="700" height="900" type="application/pdf">'
    st.components.v1.html(pdf_display, height=900)
