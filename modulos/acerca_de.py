
import streamlit as st

from modulos.estilos import cargar_estilos


def mostrar():
    cargar_estilos()

    # Encabezado
    st.markdown("""
    <div class="hero">
        <h1>Acerca del proyecto</h1>
        <p>
            Información académica, integrantes y detalles
            del proyecto de visualización de datos.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Información académica
    st.markdown(
        '<div class="section-title">Información académica</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    **Trabajo académico:** Storytelling con visualizaciones

    **Curso:** Visualización de datos

    **Docente:** Alain Melquiades Alejo Huarachi

    **Universidad:** Universidad Nacional del Altiplano - Puno
    """)

    st.divider()

    # Integrantes
    st.markdown(
        '<div class="section-title">Integrantes</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    **Integrante 01:** Canaza Mamani, Walter

    **Integrante 02:** Ordoñez Candia, Katia Marilia
    """)

    st.divider()

    # Descripción del proyecto
    st.markdown(
        '<div class="section-title">Descripción del proyecto</div>',
        unsafe_allow_html=True
    )

    st.write("""
    Este proyecto académico aplica storytelling con datos
    mediante visualizaciones conectadas para analizar las
    ventas de productos de consumo masivo en Polonia durante
    el periodo 2022–2024.
    """)

    st.divider()

    st.caption(
        "Dataset: FMCG Daily Sales Data (2022-2024), Kaggle."
    )
