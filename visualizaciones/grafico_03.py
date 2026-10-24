import streamlit as st
import pandas as pd
import plotly.express as px

from modulos.datos import obtener_datos


def mostrar():
    df = obtener_datos().copy()

    # Encabezado
    st.markdown("""
    <div class="hero">
        <h1>Ranking de productos</h1>
        <h3>¿Qué productos lideran las ventas?</h3>
        <p>
            Identifica los productos con mayor volumen de ventas,
            compara marcas y categorías y analiza el desempeño
            comercial de cada producto.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Validar columnas necesarias
    necesarias = ["sku", "brand", "category", "units_sold"]

    faltantes = [
        col for col in necesarias
        if col not in df.columns
    ]

    if faltantes:
        st.error(
            f"Faltan columnas necesarias: {', '.join(faltantes)}"
        )
        return

    # Limpiar datos
    df["units_sold"] = pd.to_numeric(
        df["units_sold"],
        errors="coerce"
    )

    df = df.dropna(
        subset=["sku", "units_sold"]
    ).copy()

    df["sku"] = df["sku"].astype(str).str.strip()

    df = df[
        (df["sku"] != "")
        & (df["sku"].str.lower() != "nan")
    ].copy()

    if df.empty:
        st.warning(
            "No hay datos válidos para generar el ranking."
        )
        return

    # Filtros
    st.subheader("Filtros de análisis")

    c1, c2, c3 = st.columns(3)

    marcas = sorted(
        df["brand"].dropna().unique().tolist(),
        key=str
    )

    categorias = sorted(
        df["category"].dropna().unique().tolist(),
        key=str
    )

    with c1:
        marcas_sel = st.multiselect(
            "Marca",
            options=marcas,
            default=marcas,
            key="ranking_marcas"
        )

    with c2:
        categorias_sel = st.multiselect(
            "Categoría",
            options=categorias,
            default=categorias,
            key="ranking_categorias"
        )

    with c3:
        top_n = st.selectbox(
            "Cantidad de productos",
            options=[5, 10, 15, 20, 30],
            index=1,
            key="ranking_top_n"
        )

    # Aplicar filtros
    df_filtrado = df[
        df["brand"].isin(marcas_sel)
        & df["category"].isin(categorias_sel)
    ].copy()

    if df_filtrado.empty:
        st.warning(
            "No hay productos para los filtros seleccionados."
        )
        return

    # Agrupar unidades vendidas por producto
    productos = (
        df_filtrado
        .groupby(
            ["sku", "brand", "category"],
            dropna=False,
            as_index=False
        )
        .agg(
            unidades_vendidas=("units_sold", "sum")
        )
    )

    # Ranking de mayor a menor
    productos = (
        productos
        .sort_values(
            by=["unidades_vendidas", "sku"],
            ascending=[False, True],
            kind="stable"
        )
        .head(top_n)
        .reset_index(drop=True)
    )

    if productos.empty:
        st.warning("No hay productos para mostrar.")
        return

    # Posición del ranking
    productos.insert(
        0,
        "Posición",
        range(1, len(productos) + 1)
    )

    # Indicadores
    total_ranking = productos["unidades_vendidas"].sum()
    producto_lider = productos.iloc[0]

    k1, k2, k3 = st.columns(3)

    k1.metric(
        "Productos en el ranking",
        f"{len(productos)}"
    )

    k2.metric(
        "Unidades vendidas (Top)",
        f"{total_ranking:,.0f}"
    )

    k3.metric(
        "Producto líder",
        str(producto_lider["sku"])
    )

    st.divider()

    # Preparar el gráfico en orden descendente
    productos_grafico = (
        productos
        .sort_values(
            by="unidades_vendidas",
            ascending=False,
            kind="stable"
        )
        .copy()
    )

    productos_grafico["sku"] = (
        productos_grafico["sku"].astype(str)
    )

    # Orden explícito: primero el más vendido
    orden_sku = productos_grafico["sku"].tolist()

    fig = px.bar(
        productos_grafico,
        x="unidades_vendidas",
        y="sku",
        orientation="h",
        color="unidades_vendidas",
        color_continuous_scale=[
            [0.0, "#FFCC80"],
            [0.5, "#FB8C00"],
            [1.0, "#E65100"]
        ],
        text="unidades_vendidas",
        custom_data=["brand", "category"],
        labels={
            "sku": "Código del producto (SKU)",
            "unidades_vendidas": "Unidades vendidas",
            "brand": "Marca",
            "category": "Categoría"
        }
    )

    # Etiquetas y datos al pasar el cursor
    fig.update_traces(
        texttemplate="%{x:,.0f}",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>SKU: %{y}</b>"
            "<br>Marca: %{customdata[0]}"
            "<br>Categoría: %{customdata[1]}"
            "<br>Unidades vendidas: %{x:,.0f}"
            "<extra></extra>"
        )
    )

    # Espacio para las etiquetas numéricas
    max_unidades = productos_grafico[
        "unidades_vendidas"
    ].max()

    limite_x = (
        max_unidades * 1.20
        if max_unidades > 0
        else 1
    )

    # Configuración del gráfico
    fig.update_layout(
        title=dict(
            text=(
                "<b>Ranking de productos por unidades vendidas</b>"
                "<br><sup>De mayor a menor volumen de ventas</sup>"
            ),
            x=0.02,
            xanchor="left",
            font=dict(
                size=20,
                color="#222222"
            )
        ),

        xaxis=dict(
            title="Unidades vendidas",
            range=[0, limite_x],
            rangemode="tozero",
            gridcolor="rgba(150,150,150,0.20)",
            tickfont=dict(
                size=11,
                color="#333333"
            )
        ),

        yaxis=dict(
            title="",
            categoryorder="array",
            categoryarray=orden_sku,
            autorange="reversed",
            automargin=True,
            tickfont=dict(
                size=12,
                color="#222222"
            )
        ),

        font=dict(
            family="Arial",
            size=12,
            color="#222222"
        ),

        margin=dict(
            t=100,
            l=110,
            r=100,
            b=55
        ),

        height=max(
            450,
            len(productos_grafico) * 45
        ),

        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title_text="Unidades vendidas",
        hovermode="closest"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # Tabla detallada del ranking
    with st.expander("Consultar detalle del ranking"):
        detalle = productos[
            [
                "Posición",
                "sku",
                "brand",
                "category",
                "unidades_vendidas"
            ]
        ].copy()

        detalle = detalle.rename(
            columns={
                "sku": "SKU",
                "brand": "Marca",
                "category": "Categoría",
                "unidades_vendidas": "Unidades vendidas"
            }
        )

        st.dataframe(
            detalle,
            use_container_width=True,
            hide_index=True
        )

    st.caption(
        "El ranking se calcula sumando las unidades vendidas "
        "por SKU después de aplicar los filtros. Los productos "
        "se ordenan de mayor a menor volumen."
    )