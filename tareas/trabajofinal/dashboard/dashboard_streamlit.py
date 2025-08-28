
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import boto3
import json
import io
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Pipeline Conflicto Ucrania-Rusia 2022",
    page_icon="⚔️",
    layout="wide"
)

@st.cache_data
def load_data_from_s3():
    s3 = boto3.client('s3')
    bucket_name = 'xideralaws-curso-osvaldo'

    try:
        # Cargar datos consolidados
        response = s3.get_object(
            Bucket=bucket_name,
            Key='ukraine-war-project/processed-data/weekly_consolidated.parquet'
        )
        df_consolidated = pd.read_parquet(io.BytesIO(response['Body'].read()))

        # Cargar métricas
        response = s3.get_object(
            Bucket=bucket_name,
            Key='ukraine-war-project/aggregated-data/dashboard_metrics.json'
        )
        metrics = json.loads(response['Body'].read().decode('utf-8'))

        return df_consolidated, metrics
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return None, None

# Título principal
st.title("📊 Pipeline de Datos - Conflicto Ucrania-Rusia 2022")
st.markdown("### Proyecto Integrador AWS - Análisis de Datos de Conflicto")

# Cargar datos
df_consolidated, metrics = load_data_from_s3()

if df_consolidated is not None:
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Personal Perdido",
            value=f"{metrics['total_personnel_lost']:,}"
        )

    with col2:
        st.metric(
            label="Total Equipamiento Perdido", 
            value=f"{metrics['total_equipment_lost']:,}"
        )

    with col3:
        st.metric(
            label="Promedio Diario Personal",
            value=f"{metrics['avg_daily_personnel']:.0f}"
        )

    with col4:
        st.metric(
            label="Día Pico Personal",
            value=f"{metrics['peak_day_personnel']:,}"
        )

    # Gráficos principales
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tendencia Semanal de Personal")
        fig = px.line(
            df_consolidated, 
            x='week', 
            y=['personnel', 'POW'],
            title="Personal vs Prisioneros por Semana"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Equipamiento por Tipo")
        equipment_cols = ['aircraft', 'helicopter', 'tank', 'APC', 'field_artillery', 'drone']
        equipment_totals = df_consolidated[equipment_cols].sum()

        fig = px.bar(
            x=equipment_totals.values,
            y=equipment_totals.index,
            orientation='h',
            title="Total de Equipamiento Perdido"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tabla de datos
    st.subheader("Datos Consolidados Semanales")
    st.dataframe(df_consolidated, use_container_width=True)

    # Información del pipeline
    st.sidebar.header("Información del Pipeline")
    st.sidebar.info(
        f"""
        **Última actualización:** {metrics['analysis_date'][:19]}

        **Fuente de datos:** S3 Bucket
        **Procesamiento:** Lambda + EC2
        **Visualización:** Streamlit

        **Componentes del pipeline:**
        - Ingesta de datos raw
        - Procesamiento ETL
        - Agregaciones semanales
        - Dashboard interactivo
        """
    )
else:
    st.error("No se pudieron cargar los datos del pipeline")
