import streamlit as st

from modulos.datos import cargar_datos
from modulos.estilos import cargar_estilos


def mostrar():
    df = cargar_datos()

    # Aplicar estilos
    cargar_estilos()

    # Encabezado principal
    st.markdown("""
    <div class="hero">
        <h1>Ventas de productos de consumo masivo</h1>
        <p>Polonia · Periodo 2022-2024</p>
        <p>
            Exploramos tendencias, categorías y canales comerciales
            para descubrir hallazgos mediante visualización de datos
            en el mercado polaco.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Contexto de Polonia
    st.markdown(
        '<div class="section-title">Polonia en contexto</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>👥 Población</h4>
            <h3>≈ 37,5 millones</h3>
            <p>Habitantes aproximadamente.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>🏙️ Capital</h4>
            <h3>Varsovia</h3>
            <p>Principal centro político y económico.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-card">
            <h4>📍 Ubicación</h4>
            <h3>Europa central</h3>
            <p>País miembro de la Unión Europea.</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="info-card">
            <h4>🌦️ Clima</h4>
            <h3>Templado</h3>
            <p>Inviernos fríos y veranos generalmente cálidos.</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Cultura, gastronomía y regiones
    st.markdown(
        '<div class="section-title">Cultura y hábitos de consumo</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>🍲 Gastronomía polaca</h4>
            <p>
                Entre los platos tradicionales destacan los pierogi
                (empanadillas rellenas), bigos (guiso de col y carne),
                żurek (sopa fermentada de centeno) y kotlet schabowy
                (chuleta empanizada).
            </p>
            <p>
                Las sopas, las patatas, los panes y los productos
                lácteos forman parte de su tradición culinaria.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>🌍 Regiones y clima</h4>
            <p>
                Polonia presenta paisajes diversos: costa báltica
                al norte, extensas llanuras en el centro y zonas
                montañosas al sur.
            </p>
            <p>
                Las estaciones influyen en la demanda de alimentos:
                los productos frescos, las bebidas y los alimentos
                reconfortantes pueden mostrar patrones estacionales.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.caption(
        "El norte, centro y sur se presentan como referencias geográficas "
        "generales, no como las únicas divisiones administrativas oficiales."
    )

    st.divider()

    # Resumen de los datos
    st.markdown(
        '<div class="section-title">Resumen de los datos</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Registros analizados", f"{len(df):,}")

    with col2:
        st.metric("Variables", len(df.columns))

    with col3:
        categorias = (
            df["category"].nunique()
            if "category" in df.columns
            else 0
        )
        st.metric("Categorías", categorias)

    with st.expander("Consultar estructura de los datos"):
        st.write("Columnas disponibles:")
        st.write(df.columns.tolist())

    st.divider()

    # Público y objetivo
    st.markdown(
        '<div class="section-title">Acerca del análisis</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>Público objetivo</h4>
            <p>
                Estudiantes y profesionales de negocios, marketing
                y ciencia de datos interesados en comprender
                el comportamiento comercial mediante visualizaciones.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>Objetivo del análisis</h4>
            <p>
                Examinar la evolución de las ventas, comparar
                categorías y canales, e identificar patrones
                temporales y relaciones con las promociones.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Visualizaciones
    st.markdown(
        '<div class="section-title">Explora las visualizaciones</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Seis perspectivas para descubrir cómo se comportan "
        "las ventas durante el periodo analizado."
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("""
        <div class="info-card">
            <h4>01. Evolución de ventas</h4>
            <p>¿Cómo evolucionan las ventas a lo largo de 2022-2024?</p>
        </div>

        <div class="info-card">
            <h4>02. Ventas por categoría</h4>
            <p>¿Qué categorías tienen mayor participación en las ventas?</p>
        </div>

        <div class="info-card">
            <h4>03. Ranking de productos</h4>
            <p>¿Cuáles son los productos más vendidos?</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-card">
            <h4>04. Ventas por canal</h4>
            <p>¿Qué canales concentran más unidades vendidas?</p>
        </div>

        <div class="info-card">
            <h4>05. Patrones temporales</h4>
            <p>¿Qué tendencias y variaciones se observan según el periodo?</p>
        </div>

        <div class="info-card">
            <h4>06. Promociones y ventas</h4>
            <p>¿Cómo varían las ventas cuando hay promociones?</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Fuente de datos
    st.markdown(
        '<div class="section-title">Fuente de datos</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="source-card">
        <strong>Dataset:</strong> FMCG Daily Sales Data (2022-2024)<br>
        <strong>País:</strong> Polonia<br>
        <strong>Periodo:</strong> 2022-2024
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "[Consultar dataset original en Kaggle]"
        "(https://www.kaggle.com/datasets/beatafaron/fmcg-daily-sales-data-to-2022-2024)"
    )

    st.markdown("""
    <div class="footer">
        Proyecto académico · Visualización y storytelling con datos
    </div>
    """, unsafe_allow_html=True)