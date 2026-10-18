
import streamlit as st

def mostrar():
    st.title("🛒 Ventas por categoría")

    st.markdown("""
    ### ¿Qué categorías concentran más unidades vendidas?

    Compararemos las unidades vendidas de cada categoría para
    identificar cuáles tienen mayor participación y cuáles
    registran menores volúmenes de ventas.

    El gráfico permitirá seleccionar categorías y comparar
    sus resultados para comprender mejor la composición
    de las ventas durante el periodo 2022–2024.
    """)

    st.info("Próximamente: gráfico interactivo de ventas por categoría.")
