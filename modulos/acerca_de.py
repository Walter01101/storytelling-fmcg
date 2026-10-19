
import streamlit as st


def mostrar():
    st.title("Acerca del proyecto")

    st.markdown("""
    Este proyecto académico aplica storytelling con datos
    mediante visualizaciones conectadas para analizar las
    ventas de productos de consumo masivo en Polonia
    durante el periodo 2022-2024.
    """)

    st.divider()

    st.header("Información académica")

    st.write("**Trabajo:** Storytelling con visualizaciones")
    st.write("**Curso:** Visualización de datos")
    st.write("**Docente:** Alain Melquiades Alejo Huarachi")
    st.write("**Universidad:** Universidad Nacional del Altiplano - Puno")

    st.divider()

    st.header("Integrantes")

    st.write("1. Canaza Mamani, Walter")
    st.write("2. Ordoñez Candia, Katia Marilia")

    st.divider()

    st.caption(
        "Dataset: FMCG Daily Sales Data (2022-2024), Kaggle."
    )
