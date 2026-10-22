
import streamlit as st

def mostrar():
    
    st.markdown("""
    <div class="hero">
        <h1>Evolución de ventas</h1>
        <h3>¿Cómo han evolucionado las ventas entre 2022 y 2024?</h3>
        <p>
            Analizaremos la evolución mensual de las unidades vendidas
            para identificar tendencias, variaciones y periodos con
            mayores o menores ventas.
        </p>
        <p>
            El gráfico permitirá filtrar por año y explorar los datos
            para comparar el comportamiento de las ventas a lo largo
            del tiempo.
        </p>
    </div>
    """, unsafe_allow_html=True)


    st.info("Próximamente: gráfico interactivo de ventas mensuales.")
