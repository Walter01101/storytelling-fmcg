
import streamlit as st

def mostrar():
    st.title("🏪 Ventas por canal")

    st.markdown("""
    ### ¿Qué canales concentran más ventas?

    Compararemos las unidades vendidas a través de Retail,
    E-commerce y Discount para identificar qué canales
    registran mayores volúmenes de ventas.

    El gráfico permitirá seleccionar y comparar canales
    durante el periodo 2022–2024.
    """)

    st.info("Próximamente: gráfico interactivo de ventas por canal.")
