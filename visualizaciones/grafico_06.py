
import streamlit as st

def mostrar():
    st.title("🎯 Promociones y ventas")

    st.markdown("""
    ### ¿Cómo se relacionan las promociones con las ventas?

    Compararemos las unidades vendidas en días con promoción
    y sin promoción para identificar posibles diferencias
    en el comportamiento de las ventas.

    El gráfico permitirá filtrar los resultados y comparar
    ambos grupos durante el periodo 2022–2024.
    """)

    st.info("Próximamente: gráfico interactivo de promociones y ventas.")
