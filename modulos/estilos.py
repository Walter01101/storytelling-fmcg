
import streamlit as st


def cargar_estilos():
    st.markdown("""
    <style>
    /* Contenido principal */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Encabezado principal: azul */
    .hero {
        background: linear-gradient(120deg, #123B65, #1D5D91);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        color: #FFFFFF;
        font-size: 2.25rem;
        margin-bottom: 0.5rem;
    }

    .hero h3 {
        color: #FFFFFF;
    }

    .hero p {
        color: #E0F2FE;
        font-size: 1.05rem;
        margin-bottom: 0;
    }

    /* Títulos de sección */
    .section-title {
        color: #123B65;
        font-size: 1.45rem;
        font-weight: 700;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    /* Tarjetas informativas */
    .info-card {
        background: #F0F6FC;
        border-left: 5px solid #1D5D91;
        padding: 1.1rem 1.2rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        min-height: 125px;
    }

    .info-card h4 {
        color: #123B65;
        margin: 0 0 0.5rem 0;
        font-size: 1.05rem;
    }

    .info-card p {
        color: #334155;
        margin: 0;
        font-size: 0.95rem;
    }

    /* Fuente de datos */
    .source-card {
        background: #EDF4FA;
        border: 1px solid #C5D9EB;
        padding: 1.2rem;
        border-radius: 10px;
        color: #123B65;
    }

    /* Pie de página */
    .footer {
        text-align: center;
        color: #64748B;
        font-size: 0.85rem;
        padding-top: 1rem;
    }

    /* Menú lateral */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
    }

    [data-testid="stSidebar"] h3 {
        color: #123B65;
        font-size: 1.15rem;
    }

    [data-testid="stSidebar"] hr {
        border-color: #D5E3ED;
    }

    /* Botones del menú */
    [data-testid="stSidebar"] .stButton button {
        border-radius: 8px;
        font-size: 0.92rem;
        box-shadow: none;
    }

    /* Opciones no seleccionadas */
    [data-testid="stSidebar"] .stButton button[kind="secondary"] {
        background-color: #F5F8FC;
        color: #123B65;
        border: 1px solid #D0DDE9;
    }

    [data-testid="stSidebar"] .stButton button[kind="secondary"]:hover {
        background-color: #E5EEF8;
        color: #123B65;
        border-color: #1D5D91;
    }

    /* Opción activa: azul */
    [data-testid="stSidebar"] .stButton button[kind="primary"],
    [data-testid="stSidebar"] .stButton button[kind="primary"]:hover,
    [data-testid="stSidebar"] .stButton button[kind="primary"]:focus {
        background-color: #123B65 !important;
        color: #FFFFFF !important;
        border: 1px solid #123B65 !important;
        border-radius: 8px;
        font-weight: 600;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
