import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Análisis de Spotify",
    page_icon="🎵",
    layout="wide"
)

# Título principal
st.title("🎵 Dashboard de Análisis de Spotify")
st.markdown("---")

# Función para cargar datos
@st.cache_data
def load_data():
    """Carga los datos desde el archivo CSV local"""
    try:
        df = pd.read_csv('data.csv')
        return df
    except FileNotFoundError:
        st.error("No se encontró el archivo data.csv en el directorio actual.")
        return None

# Cargar datos
df = load_data()

if df is not None:
    # Sidebar para filtros
    st.sidebar.header("📊 Filtros")
    
    # Filtro por canciones que gustan
    liked_filter = st.sidebar.selectbox(
        "Filtrar por preferencia:",
        ["Todas", "Solo canciones que me gustan", "Solo canciones que no me gustan"]
    )
    
    # Aplicar filtros
    if liked_filter == "Solo canciones que me gustan":
        df_filtered = df[df['liked'] == 1]
    elif liked_filter == "Solo canciones que no me gustan":
        df_filtered = df[df['liked'] == 0]
    else:
        df_filtered = df
    
    # KPIs principales
    st.header("📈 Métricas Principales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_songs = len(df_filtered)
        st.metric("Total de Canciones", total_songs)
    
    with col2:
        liked_percentage = (df_filtered['liked'].sum() / len(df_filtered)) * 100 if len(df_filtered) > 0 else 0
        st.metric("% Canciones que Gustan", f"{liked_percentage:.1f}%")
    
    with col3:
        avg_danceability = df_filtered['danceability'].mean() if len(df_filtered) > 0 else 0
        st.metric("Bailabilidad Promedio", f"{avg_danceability:.3f}")
    
    with col4:
        avg_energy = df_filtered['energy'].mean() if len(df_filtered) > 0 else 0
        st.metric("Energía Promedio", f"{avg_energy:.3f}")
    
    # Gráficos
    st.markdown("---")
    st.header("📊 Visualizaciones")
    
    if len(df_filtered) > 0:
        # Primera fila de gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribución de Preferencias")
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            liked_counts = df_filtered['liked'].value_counts()
            colors = ['#ff7f7f', '#7fbf7f']
            ax1.pie(liked_counts.values, labels=['No me gusta', 'Me gusta'], autopct='%1.1f%%', colors=colors)
            ax1.set_title('Distribución de Canciones por Preferencia')
            st.pyplot(fig1)
        
        with col2:
            st.subheader("Distribución de Modos")
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            mode_counts = df_filtered['mode'].value_counts()
            colors = ['#ffb366', '#66b3ff']
            mode_labels = ['Menor', 'Mayor']
            ax2.pie(mode_counts.values, labels=mode_labels, autopct='%1.1f%%', colors=colors)
            ax2.set_title('Distribución de Modos Musicales')
            st.pyplot(fig2)
        
        # Segunda fila de gráficos
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Distribución de Bailabilidad")
            fig3, ax3 = plt.subplots(figsize=(8, 6))
            ax3.hist(df_filtered['danceability'], bins=20, color='skyblue', alpha=0.7, edgecolor='black')
            ax3.set_xlabel('Bailabilidad')
            ax3.set_ylabel('Frecuencia')
            ax3.set_title('Distribución de Bailabilidad')
            ax3.grid(True, alpha=0.3)
            st.pyplot(fig3)
        
        with col4:
            st.subheader("Energía vs Valencia")
            fig4, ax4 = plt.subplots(figsize=(8, 6))
            scatter = ax4.scatter(df_filtered['energy'], df_filtered['valence'], 
                                c=df_filtered['liked'], cmap='RdYlGn', alpha=0.6)
            ax4.set_xlabel('Energía')
            ax4.set_ylabel('Valencia')
            ax4.set_title('Relación entre Energía y Valencia')
            plt.colorbar(scatter, ax=ax4, label='Me gusta (0=No, 1=Sí)')
            st.pyplot(fig4)
        
        # Mapa de correlación
        st.subheader("Mapa de Correlación de Características")
        numeric_cols = ['danceability', 'energy', 'loudness', 'speechiness', 
                       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
        
        fig5, ax5 = plt.subplots(figsize=(12, 8))
        correlation_matrix = df_filtered[numeric_cols].corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax5)
        ax5.set_title('Mapa de Correlación de Características Musicales')
        st.pyplot(fig5)
        
        # Tabla de datos
        st.markdown("---")
        st.header("📋 Datos")
        st.subheader("Muestra de los datos filtrados")
        st.dataframe(df_filtered.head(10))
        
        # Estadísticas descriptivas
        st.subheader("Estadísticas Descriptivas")
        st.dataframe(df_filtered[numeric_cols].describe())
        
    else:
        st.warning("No hay datos para mostrar con los filtros seleccionados.")

else:
    st.error("No se pudieron cargar los datos. Asegúrate de que el archivo 'data.csv' esté en el directorio de la aplicación.")
    
    # Mostrar instrucciones
    st.markdown("### 📝 Instrucciones:")
    st.markdown("""
    1. Asegúrate de que el archivo `data.csv` esté en el mismo directorio que `app.py`
    2. El archivo debe contener las siguientes columnas:
       - danceability, energy, key, loudness, mode, speechiness
       - acousticness, instrumentalness, liveness, valence
       - tempo, duration_ms, time_signature, liked
    3. Ejecuta la aplicación con: `streamlit run app.py`
    """)