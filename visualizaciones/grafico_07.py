
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from modulos.datos import obtener_datos
from modulos.estilos import cargar_estilos


def mostrar():
    cargar_estilos()

    df = obtener_datos().copy()

    # Encabezado
    st.markdown("""
    <div class="hero">
        <h1>Evolución dinámica de ventas</h1>
        <p>¿Cómo han evolucionado las ventas entre 2022 y 2024?</p>
        <p>
            Explora la evolución mensual de las unidades vendidas
            por categoría mediante una animación interactiva.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Validar columnas
    requeridas = ["date", "units_sold", "category"]
    faltantes = [c for c in requeridas if c not in df.columns]

    if faltantes:
        st.error(f"Faltan columnas: {', '.join(faltantes)}")
        return

    # Preparar datos
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units_sold"] = pd.to_numeric(
        df["units_sold"], errors="coerce"
    )
    df = df.dropna(subset=requeridas)

    if df.empty:
        st.warning("No hay datos válidos para mostrar.")
        return

    df["category"] = df["category"].astype(str)
    df["mes"] = df["date"].dt.to_period("M").dt.to_timestamp()

    # Filtros
    st.markdown(
        '<div class="section-title">Configura la animación</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    anios_disponibles = sorted(df["date"].dt.year.unique().tolist())

    with col1:
        anios = st.multiselect(
            "Años",
            options=anios_disponibles,
            default=anios_disponibles,
            key="g07_anios"
        )

    with col2:
        categorias_disponibles = sorted(df["category"].unique().tolist())

        categorias = st.multiselect(
            "Categorías",
            options=categorias_disponibles,
            default=categorias_disponibles,
            key="g07_categorias"
        )

    with col3:
        velocidades = {
            "Lenta · 2 segundos": 2000,
            "Normal · 1 segundo": 1000,
            "Rápida · 0.5 segundos": 500
        }

        velocidad = st.selectbox(
            "Velocidad de animación",
            list(velocidades.keys()),
            index=1,
            key="g07_velocidad"
        )

    # Aplicar filtros
    df = df[
        df["date"].dt.year.isin(anios)
        & df["category"].isin(categorias)
    ]

    if df.empty:
        st.warning("Selecciona al menos un año y una categoría.")
        return

    # Agregación mensual
    mensual = (
        df.groupby(["mes", "category"], as_index=False)
        ["units_sold"]
        .sum()
    )

    if mensual.empty:
        st.warning("No hay ventas para los filtros seleccionados.")
        return

    meses = sorted(mensual["mes"].unique())
    categorias = sorted(mensual["category"].unique())

    # Paleta consistente por categoría
    paleta = [
        "#123B65",
        "#087E8B",
        "#1D5D91",
        "#6C8EBF",
        "#F39C46",
        "#8E6BBF",
        "#D95D39",
        "#4C956C",
    ]

    colores = {
        categoria: paleta[i % len(paleta)]
        for i, categoria in enumerate(categorias)
    }

    # Tabla completa: cada categoría tiene un valor por mes.
    # Los meses sin registros se rellenan con cero.
    tabla = (
        mensual.pivot(
            index="mes",
            columns="category",
            values="units_sold"
        )
        .reindex(index=meses, columns=categorias)
        .fillna(0)
    )

    max_ventas = max(1, float(tabla.max().max()) * 1.10)

    # Figura inicial: todas las categorías están presentes.
    fig = go.Figure()

    for categoria in categorias:
        fig.add_trace(
            go.Scatter(
                x=[meses[0]],
                y=[tabla.loc[meses[0], categoria]],
                mode="lines+markers",
                name=categoria,
                line=dict(
                    color=colores[categoria],
                    width=3
                ),
                marker=dict(size=7),
                connectgaps=True
            )
        )

    # Fotogramas: cada uno conserva todo el historial.
    frames = []

    for i, mes_actual in enumerate(meses):
        fechas = meses[:i + 1]

        datos_frame = []

        for categoria in categorias:
            datos_frame.append(
                go.Scatter(
                    x=fechas,
                    y=tabla.loc[fechas, categoria].tolist(),
                    mode="lines+markers",
                    name=categoria,
                    line=dict(
                        color=colores[categoria],
                        width=3
                    ),
                    marker=dict(size=7),
                    connectgaps=True
                )
            )

        frames.append(
            go.Frame(
                name=str(pd.Timestamp(mes_actual).strftime("%Y-%m")),
                data=datos_frame,
                traces=list(range(len(categorias)))
            )
        )

    fig.frames = frames

    # Diseño
    fig.update_layout(
        template="plotly_white",
        height=570,
        margin=dict(l=30, r=25, t=90, b=110),
        title=dict(
            text="Unidades vendidas por categoría y mes",
            x=0,
            font=dict(size=20, color="#123B65")
        ),
        font=dict(
            family="Arial",
            color="#123B65"
        ),
        legend=dict(
            title="Categoría",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            x=0
        ),
        xaxis=dict(
            title="Mes",
            range=[meses[0], meses[-1]],
            tickformat="%b %Y",
            showgrid=False
        ),
        yaxis=dict(
            title="Unidades vendidas",
            range=[0, max_ventas],
            gridcolor="#E5EEF8",
            rangemode="tozero"
        ),
        hovermode="x unified",
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                x=0,
                y=-0.20,
                xanchor="left",
                yanchor="top",
                showactive=False,
                buttons=[
                    dict(
                        label="Reproducir",
                        method="animate",
                        args=[
                            None,
                            {
                                "frame": {
                                    "duration": velocidades[velocidad],
                                    "redraw": True
                                },
                                "transition": {"duration": 200},
                                "fromcurrent": True,
                                "mode": "immediate"
                            }
                        ]
                    ),
                    dict(
                        label="Pausar",
                        method="animate",
                        args=[
                            [None],
                            {
                                "frame": {
                                    "duration": 0,
                                    "redraw": False
                                },
                                "transition": {"duration": 0},
                                "mode": "immediate"
                            }
                        ]
                    )
                ]
            )
        ],
        sliders=[
            dict(
                active=0,
                currentvalue=dict(
                    prefix="Periodo: ",
                    font=dict(size=14, color="#123B65")
                ),
                pad=dict(t=35, b=10),
                steps=[
                    dict(
                        label=pd.Timestamp(mes).strftime("%Y-%m"),
                        method="animate",
                        args=[
                            [pd.Timestamp(mes).strftime("%Y-%m")],
                            {
                                "frame": {
                                    "duration": 0,
                                    "redraw": True
                                },
                                "transition": {"duration": 0},
                                "mode": "immediate"
                            }
                        ]
                    )
                    for mes in meses
                ]
            )
        ]
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="grafico_07_animacion"
    )

    st.caption(
        "Cada línea representa una categoría. La animación añade "
        "un mes en cada paso y mantiene visibles los meses anteriores. "
        "Los valores representan la suma de unidades vendidas por mes."
    )
