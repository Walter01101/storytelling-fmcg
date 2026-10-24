
import streamlit as st
import pandas as pd
import plotly.express as px

from modulos.datos import obtener_datos


def mostrar():
    df = obtener_datos().copy()

    st.markdown("""
    <div class="hero">
        <h1>Evolución de ventas</h1>
        <h3>¿Cómo evolucionan las ventas a lo largo del tiempo?</h3>
        <p>
            Analiza la evolución mensual de las unidades vendidas
            durante el periodo disponible, comparando categorías,
            canales comerciales y regiones.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Validar columnas necesarias
    columnas_necesarias = [
        "date", "units_sold", "category", "channel", "region"
    ]

    faltantes = [
        col for col in columnas_necesarias
        if col not in df.columns
    ]

    if faltantes:
        st.error(
            f"Faltan columnas necesarias: {', '.join(faltantes)}"
        )
        return

    # Preparar datos
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units_sold"] = pd.to_numeric(
        df["units_sold"], errors="coerce"
    )

    df = df.dropna(
        subset=[
            "date", "units_sold", "category", "channel", "region"
        ]
    )

    if df.empty:
        st.warning("No hay datos válidos para mostrar.")
        return

    # Filtros multiselección
    st.subheader("Filtros de análisis")

    c1, c2, c3 = st.columns(3)

    with c1:
        categorias = sorted(df["category"].unique().tolist())

        categorias_sel = st.multiselect(
            "Categoría",
            options=categorias,
            default=categorias,
            key="evolucion_categoria"
        )

    with c2:
        canales = sorted(df["channel"].unique().tolist())

        canales_sel = st.multiselect(
            "Canal",
            options=canales,
            default=canales,
            key="evolucion_canal"
        )

    with c3:
        regiones = sorted(df["region"].unique().tolist())

        regiones_sel = st.multiselect(
            "Región",
            options=regiones,
            default=regiones,
            key="evolucion_region"
        )

    # Aplicar filtros
    df_filtrado = df[
        df["category"].isin(categorias_sel)
        & df["channel"].isin(canales_sel)
        & df["region"].isin(regiones_sel)
    ].copy()

    if df_filtrado.empty:
        st.warning("No hay datos para los filtros seleccionados.")
        return

    # Agrupar ventas por mes
    df_filtrado["mes"] = (
        df_filtrado["date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    ventas_mes = (
        df_filtrado.groupby("mes", as_index=False)["units_sold"]
        .sum()
        .sort_values("mes")
    )

    # Indicadores
    total_ventas = df_filtrado["units_sold"].sum()
    promedio_mensual = ventas_mes["units_sold"].mean()

    k1, k2 = st.columns(2)

    k1.metric(
        "Unidades vendidas",
        f"{total_ventas:,.0f}"
    )

    k2.metric(
        "Promedio mensual",
        f"{promedio_mensual:,.0f}"
    )

    # Gráfico de evolución mensual
    fig = px.line(
        ventas_mes,
        x="mes",
        y="units_sold",
        markers=True,
        labels={
            "mes": "Mes",
            "units_sold": "Unidades vendidas"
        }
    )

    # Línea, puntos y sombreado naranja
    fig.update_traces(
        line=dict(
            color="#F4A261",
            width=3
        ),
        marker=dict(
            color="#F4A261",
            size=7
        ),
        fill="tozeroy",
        fillcolor="rgba(244,162,97,0.15)",
        hovertemplate=(
            "Mes: %{x|%b %Y}"
            "<br>Unidades vendidas: %{y:,.0f}"
            "<extra></extra>"
        )
    )

    # Diseño del gráfico
    fig.update_layout(
        title=dict(
            text=(
                "<b>Evolución mensual de ventas</b>"
                "<br><sup>Unidades vendidas según los filtros seleccionados</sup>"
            ),
            x=0.02,
            xanchor="left",
            font=dict(size=20, color="#174A70")
        ),
        xaxis=dict(
            title="Periodo",
            showgrid=False
        ),
        yaxis=dict(
            title="Unidades vendidas",
            gridcolor="rgba(150,150,150,0.20)",
            rangemode="tozero"
        ),
        font=dict(size=12),
        margin=dict(t=100, l=30, r=30, b=40),
        height=500,
        paper_bgcolor="white",
        plot_bgcolor="white",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "Las unidades vendidas se agregan por mes mediante la suma "
        "de units_sold. Los filtros permiten explorar categorías, "
        "canales y regiones."
    )
