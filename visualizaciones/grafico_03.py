
import streamlit as st

def mostrar():
    st.title("🏆 Ranking de productos")

    st.markdown("""
    ### ¿Qué productos lideran las ventas?

    Compararemos las unidades vendidas por código de producto
    para identificar cuáles tienen mayor demanda y cuáles
    registran menores volúmenes de ventas.

    El gráfico permitirá seleccionar cuántos productos mostrar
    y explorar sus resultados durante el periodo 2022-2024.
    """)

    st.info("Próximamente: ranking interactivo de productos.")
