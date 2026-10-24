import streamlit as st
import pandas as pd
import plotly.express as px

from modulos.datos import obtener_datos


def mostrar():
    df = obtener_datos().copy()

    st.markdown("""
    <div class="hero">
        <h1>Ventas por categoría</h1>
        <h3>¿Qué categorías generan más unidades vendidas?</h3>
        <p>
            Compara el volumen de ventas de cada categoría,
            identifica las más importantes y analiza su participación
            en las ventas totales.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Validar columnas
    necesarias = ["category", "units_sold", "channel"]

    if not all(col in df.columns for col in necesarias):
        st.error("Faltan columnas necesarias para generar la visualización.")
        return

    # Limpiar datos
    df["units_sold"] = pd.to_numeric(
        df["units_sold"], errors="coerce"
    )

    df = df.dropna(subset=["category", "units_sold", "channel"])

    if df.empty:
        st.warning("No hay datos válidos para mostrar.")
        return

    # Filtro por canal
    canales = sorted(df["channel"].unique())

    canal_seleccionado = st.selectbox(
        "Selecciona el canal comercial",
        ["Todos"] + canales,
        key="ventas_categoria_canal"
    )

    if canal_seleccionado != "Todos":
        df = df[df["channel"] == canal_seleccionado]

    if df.empty:
        st.warning("No hay datos para el canal seleccionado.")
        return

    # Agrupar unidades vendidas por categoría
    ventas = (
        df.groupby("category", as_index=False)["units_sold"]
        .sum()
        .sort_values("units_sold", ascending=True)
    )

    total_ventas = ventas["units_sold"].sum()

    if total_ventas == 0:
        st.warning("El total de unidades vendidas es cero.")
        return

    # Calcular participación
    ventas["participacion"] = (
        ventas["units_sold"] / total_ventas * 100
    )

    # Indicadores KPI
    categoria_lider = ventas.loc[
        ventas["units_sold"].idxmax(), "category"
    ]

    unidades_lider = ventas["units_sold"].max()

    participacion_lider = (
        unidades_lider / total_ventas * 100
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Unidades vendidas",
        f"{total_ventas:,.0f}"
    )

    c2.metric(
        "Categorías",
        f"{len(ventas)}"
    )

    c3.metric(
        "Participación líder",
        f"{participacion_lider:.1f}%",
        help=f"Categoría líder: {categoria_lider}"
    )

    # Gráfico de barras horizontales
    fig = px.bar(
        ventas,
        x="units_sold",
        y="category",
        orientation="h",
        text="units_sold",
        custom_data=["participacion"],
        labels={
            "units_sold": "Unidades vendidas",
            "category": "Categoría"
        }
    )

    # Color naranja uniforme
    fig.update_traces(
        marker_color="#F4A261",
        texttemplate="%{x:,.0f}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b>"
            "<br>Unidades vendidas: %{x:,.0f}"
            "<br>Participación: %{customdata[0]:.2f}%"
            "<extra></extra>"
        )
    )

    # Diseño visual
    fig.update_layout(
        title=dict(
            text=(
                "<b>Ventas por categoría</b>"
                "<br><sup>Distribución del volumen de ventas</sup>"
            ),
            x=0.02,
            xanchor="left",
            font=dict(size=20, color="#174A70")
        ),
        xaxis=dict(
            title=dict(
                text="Unidades vendidas",
                font=dict(size=13, color="#333333")
            ),
            tickfont=dict(size=12, color="#333333"),
            showgrid=True,
            gridcolor="rgba(150,150,150,0.20)",
            rangemode="tozero"
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=14, color="#222222"),
            automargin=True,
            showticklabels=True
        ),
        font=dict(
            family="Arial",
            size=13,
            color="#222222"
        ),
        margin=dict(t=100, l=150, r=70, b=50),
        height=max(400, len(ventas) * 65),
        paper_bgcolor="white",
        plot_bgcolor="white",
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Tabla complementaria
    with st.expander("Ver detalle de ventas por categoría"):
        detalle = ventas.sort_values(
            "units_sold", ascending=False
        ).copy()

        detalle["participacion"] = detalle["participacion"].map(
            lambda x: f"{x:.2f}%"
        )

        detalle = detalle.rename(columns={
            "category": "Categoría",
            "units_sold": "Unidades vendidas",
            "participacion": "Participación"
        })

        st.dataframe(
            detalle,
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        "Las ventas se calculan como la suma de units_sold "
        "por categoría, considerando el canal seleccionado."
    )