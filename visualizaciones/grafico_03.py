
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from modulos.datos import obtener_datos


def mostrar():
    df = obtener_datos().copy()

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
            Podrás seleccionar cuántos productos mostrar y explorar
            sus resultados durante el periodo 2022-2024.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Preparar datos
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units_sold"] = pd.to_numeric(
        df["units_sold"], errors="coerce"
    )

    df = df.dropna(subset=["date", "sku", "units_sold"])

    if df.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return

    # Filtros
    col1, col2 = st.columns(2)

    anios = sorted(df["date"].dt.year.unique().tolist())

    with col1:
        anio = st.selectbox(
            "Selecciona el año",
            ["Todos"] + anios,
            index=0
        )

    with col2:
        cantidad = st.selectbox(
            "Cantidad de productos",
            [5, 10, 15, 20, 30],
            index=1
        )

    if anio != "Todos":
        df = df[df["date"].dt.year == anio]

    if df.empty:
        st.warning("No hay datos para el periodo seleccionado.")
        return

    # Ranking de productos
    ventas = (
        df.groupby("sku")["units_sold"]
        .sum()
        .sort_values(ascending=False)
        .head(cantidad)
        .sort_values()
    )

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(10, 6))

    barras = ax.barh(
        ventas.index.astype(str),
        ventas.values,
        color="#F4A261",
        height=0.65
    )

    # Etiquetas de valores
    ax.bar_label(
        barras,
        labels=[f"{v:,.0f}" for v in ventas.values],
        padding=5,
        fontsize=9
    )

    periodo = str(anio) if anio != "Todos" else "2022–2024"

    ax.set_title(
        f"Top {len(ventas)} productos por unidades vendidas · {periodo}",
        loc="left",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Unidades vendidas (miles)")
    ax.set_ylabel("Código de producto")

    # Eje X siempre en miles
    ax.xaxis.set_major_formatter(
        FuncFormatter(lambda x, _: f"{x / 1000:.0f}k")
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.25)
    ax.set_axisbelow(True)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.caption(
        "Ranking calculado mediante la suma de unidades vendidas "
        "por producto en el periodo seleccionado."
    )
