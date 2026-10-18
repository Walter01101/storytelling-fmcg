
import streamlit as st

def mostrar():
    st.title("📈 Evolución de ventas")

    st.markdown("""
    ### ¿Cómo han evolucionado las ventas entre 2022 y 2024?

    Analizaremos la evolución mensual de las unidades vendidas
    para identificar tendencias, variaciones y periodos con
    mayores o menores ventas.

    El gráfico permitirá filtrar por año y explorar los datos
    para comparar el comportamiento de las ventas a lo largo
    del tiempo.
    """)

    st.info("Próximamente: gráfico interactivo de ventas mensuales.")
