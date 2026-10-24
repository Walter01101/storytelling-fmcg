
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from modulos.datos import obtener_datos

def mostrar():
    df = obtener_datos()

        
    st.markdown("""
    <div class="hero">
        <h1>Promociones y ventas</h1>
        <p>
            ¿Cómo varían las ventas mensuales según las promociones?
        </p>
        <p>
            Comparamos la distribución de las unidades vendidas con promoción
            y sin promoción a lo largo del año.
        </p>
    </div>
    """, unsafe_allow_html=True)


    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units_sold"] = pd.to_numeric(
        df["units_sold"], errors="coerce"
    )
    df["promotion_flag"] = pd.to_numeric(
        df["promotion_flag"], errors="coerce"
    )

    df = df.dropna(
        subset=["date", "units_sold", "promotion_flag", "category"]
    )

    col1, col2 = st.columns(2)

    with col1:
        anios = sorted(df["date"].dt.year.unique().tolist())
        anio = st.selectbox(
            "Selecciona el año",
            anios,
            index=anios.index(2024) if 2024 in anios else len(anios) - 1
        )

    with col2:
        categorias = ["Todas"] + sorted(
            df["category"].unique().tolist()
        )
        categoria = st.selectbox("Categoría", categorias)

    df = df[df["date"].dt.year == anio]

    if categoria != "Todas":
        df = df[df["category"] == categoria]

    df["mes"] = df["date"].dt.month

    meses = [
        "Ene", "Feb", "Mar", "Abr", "May", "Jun",
        "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"
    ]

    posiciones = np.arange(1, 13)
    datos_sin = []
    datos_con = []

    for mes in posiciones:
        datos_mes = df[df["mes"] == mes]

        datos_sin.append(
            datos_mes.loc[
                datos_mes["promotion_flag"] == 0, "units_sold"
            ].values
        )

        datos_con.append(
            datos_mes.loc[
                datos_mes["promotion_flag"] == 1, "units_sold"
            ].values
        )

    fig, ax = plt.subplots(figsize=(13, 5))

    posiciones_sin = posiciones - 0.18
    posiciones_con = posiciones + 0.18

    datos_sin_validos = [
        (pos, datos) for pos, datos in zip(posiciones_sin, datos_sin)
        if len(datos) > 0
    ]
    datos_con_validos = [
        (pos, datos) for pos, datos in zip(posiciones_con, datos_con)
        if len(datos) > 0
    ]

    if datos_sin_validos:
        cajas_sin = ax.boxplot(
            [datos for pos, datos in datos_sin_validos],
            positions=[pos for pos, datos in datos_sin_validos],
            widths=0.30,
            patch_artist=True,
            showfliers=True,    #no mostrar datos atipicos = False
            flierprops={
                "marker": "o",
                "markerfacecolor": "#FFFFFF",
                "markeredgecolor": "#0033CC",
                "markersize": 5
            }
        )
        for caja in cajas_sin["boxes"]:
            caja.set_facecolor("#6C8EBF")

    if datos_con_validos:
        cajas_con = ax.boxplot(
            [datos for pos, datos in datos_con_validos],
            positions=[pos for pos, datos in datos_con_validos],
            widths=0.30,
            patch_artist=True,
            showfliers=True,
            flierprops={
                "marker": "o",
                "markerfacecolor": "#FFD166",
                "markeredgecolor": "#D7191C",
                "markersize": 5
            }
        )
        for caja in cajas_con["boxes"]:
            caja.set_facecolor("#F39C46")

    ax.set_title(
        f"Distribución mensual de ventas según promoción - {anio}",
        loc="left",
        fontsize=13,
        fontweight="bold"
    )
    ax.set_xlabel("Mes")
    ax.set_ylabel("Unidades vendidas por registro")
    ax.set_xticks(posiciones)
    ax.set_xticklabels(meses)
    ax.set_xlim(0.5, 12.5)
    ax.grid(axis="y", linestyle="--", alpha=0.25)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    from matplotlib.patches import Patch

    ax.legend(
        handles=[
            Patch(facecolor="#6C8EBF", label="Sin promoción"),
            Patch(facecolor="#F39C46", label="Con promoción")
        ],
        frameon=False
    )

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    st.caption(
        "Cada caja representa la distribución de las ventas por registro "
        "en un mes. Las cajas no muestran ventas totales mensuales."
    )
