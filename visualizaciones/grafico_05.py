
import streamlit as st

def mostrar():
    st.title("📅 Patrones temporales")

    st.markdown("""
    ### ¿En qué meses se registran mayores ventas?

    Analizaremos las unidades vendidas por mes y año para
    identificar periodos con mayores o menores ventas y
    explorar posibles patrones temporales.

    El gráfico permitirá comparar los meses y años del
    periodo 2022–2024 mediante un mapa de calor interactivo.
    """)

    st.info("Próximamente: mapa de calor interactivo de ventas mensuales.")
