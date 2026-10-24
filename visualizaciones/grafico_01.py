
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

from modulos.datos import obtener_datos


def mostrar():
    df = obtener_datos().copy()

    st.markdown("""
    <div class="hero">
        <h1>Evolución de ventas</h1>
        <h3>¿Cómo han evolucionado las ventas entre 2022 y 2024?</h3>
        <p>
            Analizaremos la evolución mensual de las unidades vendidas
            para identificar tendencias y variaciones a lo largo del tiempo.
        </p>
        <p>
            El gráfico permitirá filtrar por año y explorar el comportamiento
            de las ventas durante el periodo seleccionado.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Preparar datos
    columna_fecha = "date"
    columna_ventas = "units_sold"

    df[columna_fecha] = pd.to_datetime(
        df[columna_fecha], errors="coerce"
    )
    df[columna_ventas] = pd.to_numeric(
        df[columna_ventas], errors="coerce"
    )
    df = df.dropna(subset=[columna_fecha, columna_ventas])

    # Filtro de año
    anios = sorted(df[columna_fecha].dt.year.unique())

    if len(anios) == 0:
        st.warning("No hay datos disponibles para mostrar.")
        return

    anio = st.selectbox(
        "Selecciona el año",
        anios,
        index=anios.index(2024) if 2024 in anios else len(anios) - 1
    )

    df = df[df[columna_fecha].dt.year == anio].copy()

    # Agrupar ventas por mes
    df["mes"] = df[columna_fecha].dt.month

    ventas_mensuales = (
        df.groupby("mes")[columna_ventas]
        .sum()
        .reindex(range(1, 13), fill_value=0)
    )

    nombres_meses = [
        "Ene", "Feb", "Mar", "Abr", "May", "Jun",
        "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
    ]

    # Gráfico
    fig, ax = plt.subplots(figsize=(11, 5))

    ax.plot(
        range(1, 13),
        ventas_mensuales.values,
        marker="o",
        linewidth=2.5,
        markersize=6,
        color="#2A9D8F"
    )

    ax.fill_between(
        range(1, 13),
        ventas_mensuales.values,
        alpha=0.12,
        color="#2A9D8F"
    )

    ax.set_title(
        f"Evolución mensual de ventas — {anio}",
        loc="left",
        fontsize=15,
        fontweight="bold"
    )
    ax.set_xlabel("Mes")
    ax.set_ylabel("Unidades vendidas")

    # Mostrar el eje Y en miles: 10k, 20k, 30k...
    ax.yaxis.set_major_formatter(
        EngFormatter(unit="", sep="")
    )

    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(nombres_meses)
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.caption(
        "Cada punto representa la suma de unidades vendidas durante un mes."
    )
