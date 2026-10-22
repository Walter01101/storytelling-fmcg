
import streamlit as st

def mostrar():
    
    st.markdown("""
    <div class="hero">
        <h1>Ranking de productos</h1>
        <h3>¿Qué productos lideran las ventas?</h3>
        <p>
            Compararemos las unidades vendidas por código de producto
            para identificar cuáles tienen mayor demanda y cuáles
            registran menores volúmenes de ventas.
        </p>
        <p>
            El gráfico permitirá seleccionar cuántos productos mostrar
            y explorar sus resultados durante el periodo 2022-2024.
        </p>
    </div>
    """, unsafe_allow_html=True)


    st.info("Próximamente: ranking interactivo de productos.")
