import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from modulos.datos import obtener_datos


def mostrar():
    df = obtener_datos().copy()

    st.markdown("""
    <div class="hero">
        <h1>Ventas por canal</h1>
        <h3>¿Cómo se distribuyen las ventas entre categorías y canales?</h3>
        <p>
            Este gráfico muestra el flujo de unidades vendidas desde cada
            categoría de productos hacia los canales comerciales.
            Puedes filtrar por año, categoría y canal.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Preparar datos
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units_sold"] = pd.to_numeric(
        df["units_sold"], errors="coerce"
    )

    df = df.dropna(
        subset=["date", "category", "channel", "units_sold"]
    )

    if df.empty:
        st.warning("No hay datos disponibles para mostrar.")
        return

    # Filtros de selección única
    col1, col2, col3 = st.columns(3)

    anios = sorted(df["date"].dt.year.unique().tolist())
    categorias_disponibles = sorted(df["category"].unique().tolist())
    canales_disponibles = sorted(df["channel"].unique().tolist())

    with col1:
        anio = st.selectbox(
            "Periodo (año)",
            ["Todos"] + anios
        )

    with col2:
        categoria = st.selectbox(
            "Categoría",
            ["Todas"] + categorias_disponibles
        )

    with col3:
        canal = st.selectbox(
            "Canal",
            ["Todos"] + canales_disponibles
        )

    # Aplicar filtros
    if anio != "Todos":
        df = df[df["date"].dt.year == anio]

    if categoria != "Todas":
        df = df[df["category"] == categoria]

    if canal != "Todos":
        df = df[df["channel"] == canal]

    if df.empty:
        st.warning("No hay datos para los filtros seleccionados.")
        return

    # Agrupar ventas por categoría y canal
    datos = (
        df.groupby(["category", "channel"], as_index=False)["units_sold"]
        .sum()
    )

    # ÚNICO CAMBIO: categorías ordenadas de mayor a menor venta
    categorias = (
        datos.groupby("category")["units_sold"]
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )

    canales = sorted(datos["channel"].unique())
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

    # Periodo del título
    periodo = str(anio) if anio != "Todos" else "2022-2024"

    # Diseño del gráfico
    fig.update_layout(
        title=dict(
            text=(
                "<b>Flujo de ventas por categoría y canal</b>"
                f"<br><sup style='color:gray'>Periodo: {periodo}</sup>"
            ),
            x=0.02,
            xanchor="left",
            y=0.95,
            font=dict(size=20, color="#222222")
        ),
        font=dict(size=12),
        margin=dict(t=100, l=30, r=30, b=25),
        height=550,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Resumen
    total = df["units_sold"].sum()

    st.caption(
        f"Total de unidades vendidas con los filtros seleccionados: "
        f"{total:,.0f}."
    )