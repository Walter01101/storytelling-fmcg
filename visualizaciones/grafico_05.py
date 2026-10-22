
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import calendar

from modulos.datos import obtener_datos


def mostrar():
    df = obtener_datos()

    
    st.markdown("""
    <div class="hero">
        <h1>Patrones temporales</h1>
        <h3>¿Qué días registran mayores ventas?</h3>
        <p>
            El calendario de calor permite explorar las unidades vendidas
            diariamente e identificar días con mayor o menor actividad.
            Filtra por año y categoría para comparar el comportamiento temporal.
        </p>
    </div>
    """, unsafe_allow_html=True)


    # Preparar datos
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units_sold"] = pd.to_numeric(
        df["units_sold"], errors="coerce"
    )
    df = df.dropna(subset=["date", "units_sold", "category"])

    # Filtros
    anios = sorted(df["date"].dt.year.unique().tolist())
    categorias = ["Todas"] + sorted(df["category"].unique().tolist())

    if not anios or not categorias:
        st.warning("No hay datos disponibles para mostrar.")
        return

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            anio = st.selectbox(
                "Selecciona el año",
                anios,
                index=anios.index(2024) if 2024 in anios else len(anios) - 1
            )

        with col2:
            categoria = st.selectbox(
                "Selecciona la categoría",
                categorias
            )

    datos = df[df["date"].dt.year == anio]

    if categoria != "Todas":
        datos = datos[datos["category"] == categoria]


    # Sumar ventas por día
    ventas_dia = datos.groupby(
        datos["date"].dt.normalize()
    )["units_sold"].sum()

    if ventas_dia.empty:
        st.warning("No existen datos para los filtros seleccionados.")
        return

    # Escala de colores
    vmin = ventas_dia.min()
    vmax = ventas_dia.max()

    if vmin == vmax:
        vmax = vmin + 1

    normalizar = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    colormap = plt.get_cmap("YlOrRd")

    # Calendario
    calendar.setfirstweekday(calendar.MONDAY)

    meses = [
        "ENERO", "FEBRERO", "MARZO",
        "ABRIL", "MAYO", "JUNIO",
        "JULIO", "AGOSTO", "SEPTIEMBRE",
        "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
    ]

    dias_semana = ["L", "M", "X", "J", "V", "S", "D"]

    fig, ejes = plt.subplots(4, 3, figsize=(16, 11))
    fig.patch.set_facecolor("white")

    for mes, ax in enumerate(ejes.flat, start=1):
        ax.set_xlim(0, 7)
        ax.set_ylim(0, 7)
        ax.invert_yaxis()
        ax.axis("off")

        ax.add_patch(plt.Rectangle(
            (0, 0), 7, 0.75,
            facecolor="#DCE5EC", edgecolor="white"
        ))

        ax.text(
            3.5, 0.38, meses[mes - 1],
            ha="center", va="center",
            fontsize=11, fontweight="bold",
            color="#0B1735"
        )

        for col, dia_semana in enumerate(dias_semana):
            ax.add_patch(plt.Rectangle(
                (col, 0.75), 1, 0.55,
                facecolor="#EEF2F6", edgecolor="white"
            ))

            ax.text(
                col + 0.5, 1.02, dia_semana,
                ha="center", va="center",
                fontsize=9, color="#52657A"
            )

        semanas = calendar.monthcalendar(anio, mes)

        for fila, semana in enumerate(semanas):
            for col, dia in enumerate(semana):
                y = 1.30 + fila * 0.95

                if dia == 0:
                    color = "#EEF2F6"
                    texto = ""
                else:
                    fecha = pd.Timestamp(anio, mes, dia)
                    valor = ventas_dia.get(fecha, np.nan)

                    color = (
                        "#EEF2F6"
                        if pd.isna(valor)
                        else colormap(normalizar(valor))
                    )
                    texto = str(dia)

                ax.add_patch(plt.Rectangle(
                    (col, y), 1, 0.95,
                    facecolor=color,
                    edgecolor="white",
                    linewidth=1.2
                ))

                if texto:
                    ax.text(
                        col + 0.5, y + 0.475, texto,
                        ha="center", va="center",
                        fontsize=8, color="#172033"
                    )

    fig.text(
        0.04, 0.965,
        "Calendario de calor de ventas",
        fontsize=21, fontweight="bold",
        color="#0B1735", ha="left"
    )

    nombre_categoria = (
        "Todas las categorías" if categoria == "Todas" else categoria
    )

    fig.text(
        0.04, 0.935,
        f"Unidades vendidas por día · {anio} · {nombre_categoria}",
        fontsize=12, color="#60758B", ha="left"
    )

    plt.subplots_adjust(
        left=0.04, right=0.98,
        top=0.83, bottom=0.035,
        hspace=0.14, wspace=0.05
    )

    mapeable = mpl.cm.ScalarMappable(
        norm=normalizar, cmap=colormap
    )
    mapeable.set_array([])

    cax = fig.add_axes([0.70, 0.875, 0.28, 0.018])

    barra = fig.colorbar(
        mapeable, cax=cax, orientation="horizontal"
    )
    barra.set_label("Unidades vendidas", fontsize=9)
    barra.ax.tick_params(labelsize=8, pad=3)

    # st.pyplot(fig, use_container_width=True)
    st.pyplot(fig, use_container_width=False)
    plt.close(fig)

    st.caption(
        "Los días sin registros aparecen en gris; no necesariamente "
        "representan ventas iguales a cero."
    )
