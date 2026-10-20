
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from modulos.datos import obtener_datos


def mostrar():
    df = obtener_datos().copy()

    st.title("🏪 Ventas por canal")

    st.markdown("""
    ### ¿Cómo se distribuyen las ventas entre categorías y canales?

    Este gráfico muestra el flujo de unidades vendidas desde cada
    categoría de productos hacia los canales comerciales durante
    el periodo 2022-2024.
    """)

    # Preparar datos
    df["units_sold"] = pd.to_numeric(
        df["units_sold"], errors="coerce"
    )
    df = df.dropna(
        subset=["category", "channel", "units_sold"]
    )

    # Agrupar ventas por categoría y canal
    datos = df.groupby(
        ["category", "channel"],
        as_index=False
    )["units_sold"].sum()

    categorias = sorted(df["category"].unique())
    canales = sorted(df["channel"].unique())
    nodos = categorias + canales

    # Colores de categorías
    colores_categoria = {
        "Yogur": "#F4A261",
        "Leche": "#E76F51",
        "Comida preparada": "#2A9D8F",
        "Barra de cereal": "#9B5DE5",
        "Jugo": "#5777E5"
    }

    # Colores de canales
    colores_canales = {
        "Tiendas de descuento": "#35C9D8",
        "Comercio electrónico": "#F57CA7",
        "Tiendas minoristas": "#B8E994"
    }

    # Asignar colores incluso si aparece una categoría nueva
    color_predeterminado = "#95A5A6"

    colores_nodos = (
        [
            colores_categoria.get(c, color_predeterminado)
            for c in categorias
        ]
        + [
            colores_canales.get(c, color_predeterminado)
            for c in canales
        ]
    )

    # Índices de origen y destino
    indice_categoria = {
        valor: i for i, valor in enumerate(categorias)
    }

    indice_canal = {
        valor: i + len(categorias)
        for i, valor in enumerate(canales)
    }

    origen = datos["category"].map(indice_categoria)
    destino = datos["channel"].map(indice_canal)

    # Convertir colores hexadecimales a RGBA
    def rgba(hex_color, alpha=0.35):
        hex_color = hex_color.lstrip("#")
        r, g, b = (
            int(hex_color[i:i + 2], 16)
            for i in (0, 2, 4)
        )
        return f"rgba({r},{g},{b},{alpha})"

    colores_flujo = [
        rgba(colores_categoria.get(c, color_predeterminado))
        for c in datos["category"]
    ]

    # Crear gráfico Sankey
    fig = go.Figure(
        go.Sankey(
            arrangement="snap",
            node=dict(
                label=nodos,
                color=colores_nodos,
                pad=20,
                thickness=20,
                line=dict(
                    color="rgba(50,50,50,0.25)",
                    width=0.5
                )
            ),
            link=dict(
                source=origen.tolist(),
                target=destino.tolist(),
                value=datos["units_sold"].tolist(),
                color=colores_flujo,
                hovertemplate=(
                    "%{source.label} → %{target.label}"
                    "<br>Unidades vendidas: %{value:,.0f}"
                    "<extra></extra>"
                )
            )
        )
    )

    # Título y diseño
    fig.update_layout(
        title=dict(
            text=(
                "<b>Flujo de ventas por categoría y canal</b>"
                "<br><sup style='color:gray'>"
                "Distribución de las unidades vendidas por categoría "
                "y canal comercial, periodo 2022-2024"
                "</sup>"
            ),
            x=0.02,
            xanchor="left",
            y=0.97,
            font=dict(size=20, color="#222222")
        ),
        font=dict(size=12),
        margin=dict(t=100, l=30, r=30, b=25),
        height=550,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "El ancho de cada flujo representa las unidades vendidas. "
        "Los valores corresponden a la suma del periodo analizado."
    )
