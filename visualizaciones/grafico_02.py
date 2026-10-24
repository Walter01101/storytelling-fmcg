
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from modulos.datos import obtener_datos


def mostrar():
    df = obtener_datos().copy()

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
            El gráfico permitirá comparar los resultados y comprender
            mejor la composición de las ventas durante el periodo 2022-2024.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Preparar datos
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units_sold"] = pd.to_numeric(
        df["units_sold"], errors="coerce"
    )

    df = df.dropna(subset=["date", "category", "units_sold"])

    # Filtro por año
    anios = sorted(df["date"].dt.year.unique().tolist())

    anio = st.selectbox(
        "Selecciona el año",
        ["Todos"] + anios,
        index=0
    )

    if anio != "Todos":
        df = df[df["date"].dt.year == anio]

    if df.empty:
        st.warning("No hay datos para el periodo seleccionado.")
        return

    # Agrupar ventas por categoría
    ventas = (
        df.groupby("category")["units_sold"]
        .sum()
        .sort_values()
    )

    # Crear gráfico
    fig, ax = plt.subplots(figsize=(10, 5))

    barras = ax.barh(
        ventas.index,
        ventas.values,
        color="#2A9D8F",
        height=0.65
    )

    # Etiquetas al final de cada barra
    ax.bar_label(
        barras,
        labels=[f"{v:,.0f}" for v in ventas.values],
        padding=5,
        fontsize=9
    )

    periodo = str(anio) if anio != "Todos" else "2022–2024"

    ax.set_title(
        f"Unidades vendidas por categoría · {periodo}",
        loc="left",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Unidades vendidas (miles)")
    ax.set_ylabel("")

    # Eje X expresado siempre en miles
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
        "Las barras representan la suma de unidades vendidas "
        "por categoría para el periodo seleccionado."
    )
