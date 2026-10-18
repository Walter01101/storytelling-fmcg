
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Storytelling de ventas FMCG",
    page_icon="📊",
    layout="wide"
)

st.title("Ventas de productos de consumo masivo")
st.subheader("Polonia | 2022–2024")

st.markdown("""
Este dashboard analiza la evolución de las ventas,
las categorías de productos y los canales de distribución
para descubrir patrones y comunicar hallazgos mediante datos.
""")

st.divider()

# Cargar dataset
df = pd.read_csv("datos/fmcg_2022_2024.csv")

# Indicadores generales
st.subheader("Exploración del dataset")

col1, col2 = st.columns(2)

with col1:
    st.metric("Registros", f"{len(df):,}")

with col2:
    st.metric("Columnas", len(df.columns))

# Vista previa
st.subheader("Vista previa de los datos")
st.dataframe(df.head(10), use_container_width=True)

st.caption("Fuente: dataset FMCG Daily Sales Data (2022–2024), Kaggle.")
