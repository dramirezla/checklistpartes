!pip install PyPDF2
#!pip install ipywidgets


#from ipywidgets import Checkbox, VBox, Button, Output
# from IPython.display import display
from PyPDF2 import PdfReader
import re
from collections import Counter

# Cambia el nombre al nombre de tu archivo cargado
nombre_archivo1 = "Complejo.pdf"

# Cargar el PDF
reader1 = PdfReader(nombre_archivo1)

# Extraer contenido página por página
contenido_paginas1= []
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
    #letras_mayusculas1 = re.findall(r'[A-Z]:', contenido_modificado)
    #letras_mayusculas = re.findall(r'[A-Z][A-Z]:', contenido_modificado)

    # Añadir las letras capitalizadas a la lista 'partes'
    partes.extend(letras_mayusculas)
    #partes.extend(letras_mayusculas)

    # Contar las letras mayúsculas y actualizar el diccionario de frecuencias
    letras_frecuencia.update(letras_mayusculas)
    #letras_frecuencia.update(letras_mayusculas)


    # Mostrar el contenido modificado
    print("")
    print(contenido_modificado)

# Mostrar la frecuencia de las letras mayúsculas
print("\nFrecuencia de partes encontradas:")
for letra, frecuencia in letras_frecuencia.items():
    print(f"{letra}: {frecuencia}")

# Mostrar las partes  encontradas
print("\nPartes encontradas:")
print(partes)
