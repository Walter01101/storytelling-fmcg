import streamlit as st
from modulos.datos import cargar_datos


def mostrar():
    df = cargar_datos()

    st.title("Ventas de productos de consumo masivo")
    st.subheader("Polonia | 2022-2024")

    st.markdown("""
    Analizamos las ventas de productos de consumo masivo para
    descubrir tendencias, comparar categorías y canales, y
    comunicar hallazgos mediante storytelling con datos.
    """)

    st.divider()

    # Indicadores generales
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Registros", f"{len(df):,}")

    with col2:
        st.metric("Columnas", len(df.columns))

    with col3:
        if "sku" in df.columns:
            st.metric("Categorías", df["category"].nunique())
        else:
            st.error("No se encontró la columna sku.")

    # Diagnóstico temporal
    with st.expander("Diagnóstico de datos"):
        st.write("Columnas leídas:", df.columns.tolist())

    st.divider()

    st.header("Público objetivo")

    st.write("""
    Este trabajo está dirigido a estudiantes y profesionales de
    negocios, marketing y ciencia de datos interesados en analizar
    el comportamiento de las ventas mediante visualizaciones
    sencillas e interactivas.
    """)

    st.header("Objetivo del análisis")

    st.write("""
    Analizar la evolución de las ventas de productos de consumo
    masivo en Polonia durante 2022-2024, identificando diferencias
    entre categorías y canales comerciales, así como patrones
    temporales relevantes.
    """)

    st.header("Fuente de datos")

    st.write("""
    **Dataset:** FMCG Daily Sales Data (2022–2024)  
    **País:** Polonia  
    **Periodo:** 2022–2024
    """)

    st.markdown(
        "[Consultar dataset original en Kaggle]"
        "(https://www.kaggle.com/datasets/beatafaron/fmcg-daily-sales-data-to-2022-2024)"
    )

    st.header("Explora las visualizaciones")

    col1, col2 = st.columns(2)

    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 1. Evolución de ventas")
        st.write("¿Cómo cambian las ventas mensuales entre 2022 y 2024?")

        st.subheader("🛒 2. Ventas por categoría")
        st.write("¿Qué categorías concentran más unidades vendidas?")

        st.subheader("🏆 3. Ranking de productos")
        st.write("¿Qué productos lideran las ventas?")

    with col2:
        st.subheader("🏪 4. Ventas por canal")
        st.write("¿Cómo se distribuyen las ventas entre Retail, E-commerce y Discount?")

        st.subheader("📅 5. Patrones temporales")
        st.write("¿Qué meses y años presentan mayores ventas?")

        st.subheader("🎯 6. Promociones y ventas")
        st.write("¿Cómo se relacionan las promociones con las unidades vendidas?")


    st.divider()

    st.caption(
        "Fuente: FMCG Daily Sales Data (2022–2024), Kaggle."
    )
