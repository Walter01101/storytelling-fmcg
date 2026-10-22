
import streamlit as st

def mostrar():
    
    st.markdown("""
    <div class="hero">
        <h1>Ventas por categoría</h1>
        <h3>¿Qué categorías concentran más unidades vendidas?</h3>
        <p>
            Compararemos las unidades vendidas de cada categoría para
            identificar cuáles tienen mayor participación y cuáles
            registran menores volúmenes de ventas.
        </p>
        <p>
            El gráfico permitirá seleccionar categorías y comparar
            sus resultados para comprender mejor la composición
            de las ventas durante el periodo 2022-2024.
        </p>
    </div>
    """, unsafe_allow_html=True)


    st.info("Próximamente: gráfico interactivo de ventas por categoría.")
