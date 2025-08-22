#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análisis de Datos de Spotify - Características Musicales y Preferencias
Autor: Osvaldo González
Fecha: Agosto 2025
Proyecto: Xideral AWS - Análisis de Datos
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly no disponible, usando solo matplotlib y seaborn")

import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo
plt.style.use('default')
sns.set_palette("husl")

def load_data():
    """Cargar y preparar el dataset de Spotify"""
    df = pd.read_csv('data.csv')
    
    # Crear etiquetas más descriptivas
    df['liked_label'] = df['liked'].map({0: 'No me gusta', 1: 'Me gusta'})
    
    # Convertir duración a minutos
    df['duration_min'] = df['duration_ms'] / 60000
    
    return df

def basic_statistics(df):
    """Análisis estadístico básico"""
    print("=" * 60)
    print("ANALISIS BASICO DEL DATASET DE SPOTIFY")
    print("=" * 60)
    
    print(f"Total de canciones: {len(df)}")
    print(f"Caracteristicas analizadas: {df.shape[1]}")
    
    # Distribución de preferencias
    liked_counts = df['liked_label'].value_counts()
    print(f"\nMe gusta: {liked_counts['Me gusta']} canciones ({liked_counts['Me gusta']/len(df)*100:.1f}%)")
    print(f"No me gusta: {liked_counts['No me gusta']} canciones ({liked_counts['No me gusta']/len(df)*100:.1f}%)")
    
    # Estadísticas de duración
    print(f"\nDuracion promedio: {df['duration_min'].mean():.2f} minutos")
    print(f"Cancion mas corta: {df['duration_min'].min():.2f} minutos")
    print(f"Cancion mas larga: {df['duration_min'].max():.2f} minutos")
    
    return df

def analyze_musical_features(df):
    """Análisis de características musicales"""
    print("\n" + "=" * 60)
    print("ANALISIS DE CARACTERISTICAS MUSICALES")
    print("=" * 60)
    
    # Características principales
    audio_features = ['danceability', 'energy', 'valence', 'acousticness', 
                     'instrumentalness', 'liveness', 'speechiness']
    
    print("\nPromedio de caracteristicas por preferencia:")
    feature_comparison = df.groupby('liked_label')[audio_features].mean()
    
    for feature in audio_features:
        liked_avg = feature_comparison.loc['Me gusta', feature]
        disliked_avg = feature_comparison.loc['No me gusta', feature]
        diff = liked_avg - disliked_avg
        
        print(f"\n{feature.capitalize()}:")
        print(f"   Me gusta: {liked_avg:.3f}")
        print(f"   No me gusta: {disliked_avg:.3f}")
        print(f"   Diferencia: {diff:+.3f}")
    
    return feature_comparison

def create_matplotlib_visualizations(df):
    """Crear visualizaciones con matplotlib/seaborn"""
    
    # Configurar el tamaño de la figura
    plt.figure(figsize=(15, 12))
    
    # 1. Distribución de preferencias
    plt.subplot(2, 3, 1)
    liked_counts = df['liked_label'].value_counts()
    colors = ['#FF6B6B', '#1DB954']
    plt.pie(liked_counts.values, labels=liked_counts.index, autopct='%1.1f%%', colors=colors)
    plt.title('Distribucion de Preferencias Musicales')
    
    # 2. Boxplot de características principales
    plt.subplot(2, 3, 2)
    audio_features = ['danceability', 'energy', 'valence', 'acousticness']
    melted_df = df.melt(id_vars=['liked_label'], value_vars=audio_features, 
                       var_name='feature', value_name='value')
    sns.boxplot(data=melted_df, x='feature', y='value', hue='liked_label')
    plt.xticks(rotation=45)
    plt.title('Caracteristicas Musicales por Preferencia')
    
    # 3. Scatter plot Energy vs Valence
    plt.subplot(2, 3, 3)
    for liked_val, color, label in [(1, '#1DB954', 'Me gusta'), (0, '#FF6B6B', 'No me gusta')]:
        data = df[df['liked'] == liked_val]
        plt.scatter(data['energy'], data['valence'], c=color, label=label, alpha=0.6)
    plt.xlabel('Energy')
    plt.ylabel('Valence')
    plt.title('Energia vs Valencia')
    plt.legend()
    
    # 4. Distribución de tempo
    plt.subplot(2, 3, 4)
    for liked_val, color, label in [(1, '#1DB954', 'Me gusta'), (0, '#FF6B6B', 'No me gusta')]:
        data = df[df['liked'] == liked_val]['tempo']
        plt.hist(data, alpha=0.6, label=label, color=color, bins=20)
    plt.xlabel('Tempo (BPM)')
    plt.ylabel('Frecuencia')
    plt.title('Distribucion de Tempo')
    plt.legend()
    
    # 5. Correlación
    plt.subplot(2, 3, 5)
    audio_features_extended = ['danceability', 'energy', 'valence', 'acousticness', 
                              'instrumentalness', 'liveness', 'speechiness', 'liked']
    corr_matrix = df[audio_features_extended].corr()
    sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0, fmt='.2f')
    plt.title('Matriz de Correlacion')
    
    # 6. Duración por preferencia
    plt.subplot(2, 3, 6)
    sns.boxplot(data=df, x='liked_label', y='duration_min')
    plt.title('Duracion por Preferencia')
    plt.ylabel('Duracion (minutos)')
    
    plt.tight_layout()
    plt.savefig('spotify_analysis_complete.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nVisualizacion guardada como: spotify_analysis_complete.png")

def generate_insights(df):
    """Generar insights y conclusiones"""
    print("\n" + "=" * 60)
    print("INSIGHTS Y CONCLUSIONES")
    print("=" * 60)
    
    # Análisis de características más importantes
    audio_features = ['danceability', 'energy', 'valence', 'acousticness', 
                     'instrumentalness', 'liveness', 'speechiness']
    
    feature_comparison = df.groupby('liked')[audio_features].mean()
    differences = feature_comparison.loc[1] - feature_comparison.loc[0]
    
    # Top características positivas
    top_positive = differences.nlargest(3)
    top_negative = differences.nsmallest(3)
    
    print("CARACTERISTICAS QUE MAS INFLUYEN EN MIS GUSTOS:")
    print("\nMe gustan mas las canciones con mayor:")
    for feature, diff in top_positive.items():
        print(f"   {feature.capitalize()}: +{diff:.3f}")
    
    print("\nMe gustan menos las canciones con mayor:")
    for feature, diff in top_negative.items():
        print(f"   {feature.capitalize()}: {diff:.3f}")
    
    # Análisis de tempo y duración
    liked_tempo = df[df['liked']==1]['tempo'].mean()
    disliked_tempo = df[df['liked']==0]['tempo'].mean()
    
    liked_duration = df[df['liked']==1]['duration_min'].mean()
    disliked_duration = df[df['liked']==0]['duration_min'].mean()
    
    print(f"\nPREFERENCIAS DE TEMPO Y DURACION:")
    print(f"   Tempo promedio (me gusta): {liked_tempo:.1f} BPM")
    print(f"   Tempo promedio (no me gusta): {disliked_tempo:.1f} BPM")
    print(f"   Duracion promedio (me gusta): {liked_duration:.2f} min")
    print(f"   Duracion promedio (no me gusta): {disliked_duration:.2f} min")
    
    # Perfil musical
    print(f"\nMI PERFIL MUSICAL:")
    energy_pref = df[df['liked']==1]['energy'].mean()
    valence_pref = df[df['liked']==1]['valence'].mean()
    dance_pref = df[df['liked']==1]['danceability'].mean()
    
    print(f"   Nivel de energia preferido: {energy_pref:.2f} ({get_energy_level(energy_pref)})")
    print(f"   Nivel de positividad preferido: {valence_pref:.2f} ({get_valence_level(valence_pref)})")
    print(f"   Nivel de bailabilidad preferido: {dance_pref:.2f} ({get_dance_level(dance_pref)})")

def get_energy_level(energy):
    if energy < 0.3:
        return "Relajado"
    elif energy < 0.7:
        return "Moderado"
    else:
        return "Energico"

def get_valence_level(valence):
    if valence < 0.3:
        return "Melancolico"
    elif valence < 0.7:
        return "Neutral"
    else:
        return "Alegre"

def get_dance_level(dance):
    if dance < 0.3:
        return "Poco bailable"
    elif dance < 0.7:
        return "Moderadamente bailable"
    else:
        return "Muy bailable"

def main():
    """Función principal"""
    print("INICIANDO ANALISIS DE DATOS DE SPOTIFY")
    print("=" * 60)
    
    # Cargar datos
    df = load_data()
    
    # Análisis básico
    df = basic_statistics(df)
    
    # Análisis de características musicales
    feature_comparison = analyze_musical_features(df)
    
    # Crear visualizaciones
    create_matplotlib_visualizations(df)
    
    # Generar insights
    generate_insights(df)
    
    print("\n" + "=" * 60)
    print("ANALISIS COMPLETADO EXITOSAMENTE")
    print("Revisa el archivo spotify_analysis_complete.png para ver las visualizaciones")
    print("=" * 60)

if __name__ == "__main__":
    main()