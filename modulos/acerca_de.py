
import streamlit as st


def mostrar():
    st.title("Acerca del proyecto")

    st.markdown("""
    Este proyecto académico aplica storytelling con datos
    mediante visualizaciones conectadas para analizar las
    ventas de productos de consumo masivo en Polonia
    durante el periodo 2022–2024.
    """)

    st.divider()

    st.header("Información académica")

    st.write("**Trabajo:** Storytelling con visualizaciones")
    st.write("**Curso:** Matemáticas para Ciencia de Datos")
    st.write("**Docente:** [Nombre del docente]")
    st.write("**Universidad:** Universidad Nacional del Altiplano – Puno")

    st.divider()

    st.header("Integrantes")

    st.write("1. [Nombre del integrante 1]")
    st.write("2. [Nombre del integrante 2]")
    st.write("3. [Nombre del integrante 3]")

    st.divider()

    st.caption(
        "Dataset: FMCG Daily Sales Data (2022–2024), Kaggle."
    )
