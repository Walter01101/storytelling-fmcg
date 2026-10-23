
import streamlit as st

from modulos import presentacion, acerca_de
from modulos.estilos import cargar_estilos

from visualizaciones import (
    grafico_01,
    grafico_02,
    grafico_03,
    grafico_04,
    grafico_05,
    grafico_06,
    grafico_07
)

st.set_page_config(
    page_title="ANÁLISIS DE VENTAS",
    page_icon="📋",
    layout="wide"
)

# Aplicar estilos globales
cargar_estilos()

# Encabezado del menú
st.sidebar.markdown("### ANÁLISIS DE VENTAS")
st.sidebar.caption("Polonia · 2022–2024")
st.sidebar.divider()

# Opciones agrupadas
grupos = {
    "GENERAL": [
        "Presentación"
    ],
    "ANÁLISIS DE VENTAS": [
        "Evolución de ventas",
        "Ventas por categoría",
        "Ranking de productos",
        "Ventas por canal",
        "Patrones temporales",
        "Promociones y ventas",
        "Gráfico dinámico",
    ],
    "PROYECTO": [
        "Acerca de"
    ]
}

# Sección inicial
if "seccion" not in st.session_state:
    st.session_state.seccion = "Presentación"


# Cambiar sección
def cambiar_seccion(opcion):
    st.session_state.seccion = opcion


# Crear menú
for titulo, opciones_grupo in grupos.items():
    st.sidebar.caption(titulo)

    for opcion in opciones_grupo:
        st.sidebar.button(
            opcion,
            key=f"btn_{opcion}",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.seccion == opcion
                else "secondary"
            ),
            on_click=cambiar_seccion,
            args=(opcion,)
        )

    st.sidebar.markdown("")


# Mostrar contenido
seccion = st.session_state.seccion

if seccion == "Presentación":
    presentacion.mostrar()

elif seccion == "Evolución de ventas":
    grafico_01.mostrar()

elif seccion == "Ventas por categoría":
    grafico_02.mostrar()

elif seccion == "Ranking de productos":
    grafico_03.mostrar()

elif seccion == "Ventas por canal":
    grafico_04.mostrar()

elif seccion == "Patrones temporales":
    grafico_05.mostrar()

elif seccion == "Promociones y ventas":
    grafico_06.mostrar()

elif seccion == "Gráfico dinámico":
    grafico_07.mostrar()

elif seccion == "Acerca de":
    acerca_de.mostrar()

else:
    st.title(seccion)
    st.info("Esta visualización está pendiente de desarrollo.")
