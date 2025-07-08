"""
🎯 Objetivo del Tutorial

Crear una app web interactiva en Streamlit que:

Muestre un título, texto y una imagen.
Tenga un slider para seleccionar un número.
Permita subir un archivo.
Genere un gráfico dinámico.
Use una función en Python.

"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Título y texto
st.title("Mi primera app con Streamlit 🎈")
st.write("¡Bienvenido a esta app interactiva con Python y Streamlit!")

# Imagen
st.image("https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png", width=300)

# Slider
valor = st.slider("Selecciona un número", 0, 100, 25)
st.write("El número seleccionado es:", valor)

# Subida de archivos
archivo = st.file_uploader("Sube un archivo CSV", type="csv")

if archivo is not None:
    df = pd.read_csv(archivo)
    st.write("Vista previa de los datos:")
    st.dataframe(df.head())

    # Gráfico de líneas si hay datos numéricos
    columnas_numericas = df.select_dtypes(include=np.number).columns
    if len(columnas_numericas) >= 2:
        st.line_chart(df[columnas_numericas])
    else:
        st.write("No hay suficientes columnas numéricas para graficar.")

# Ejemplo de función personalizada
def cuadrado(x):
    return x ** 2

st.write(f"El cuadrado de {valor} es {cuadrado(valor)}")

# Footer
st.markdown("---")
st.caption("Hecho con 💻 y Streamlit")
