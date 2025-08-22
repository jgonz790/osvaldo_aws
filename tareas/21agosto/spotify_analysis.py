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
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Configuración de estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_data():
    """Cargar y preparar el dataset de Spotify"""
    df = pd.read_csv('data.csv')
    
    # Crear etiquetas más descriptivas
    df['liked_label'] = df['liked'].map({0: 'No me gusta', 1: 'Me gusta'})
    
    # Convertir duración a minutos
    df['duration_min'] = df['duration_ms'] / 60000
    
    # Categorizar tempo
    df['tempo_category'] = pd.cut(df['tempo'], 
                                 bins=[0, 90, 120, 150, np.inf],
                                 labels=['Lento', 'Moderado', 'Rápido', 'Muy Rápido'])
    
    # Categorizar energía
    df['energy_category'] = pd.cut(df['energy'],
                                  bins=[0, 0.3, 0.7, 1.0],
                                  labels=['Baja', 'Media', 'Alta'])
    
    return df

def basic_statistics(df):
    """Análisis estadístico básico"""
    print("=" * 60)
    print("📊 ANÁLISIS BÁSICO DEL DATASET DE SPOTIFY")
    print("=" * 60)
    
    print(f"🎵 Total de canciones: {len(df)}")
    print(f"📈 Características analizadas: {df.shape[1]}")
    
    # Distribución de preferencias
    liked_counts = df['liked_label'].value_counts()
    print(f"\n💚 Me gusta: {liked_counts['Me gusta']} canciones ({liked_counts['Me gusta']/len(df)*100:.1f}%)")
    print(f"💔 No me gusta: {liked_counts['No me gusta']} canciones ({liked_counts['No me gusta']/len(df)*100:.1f}%)")
    
    # Estadísticas de duración
    print(f"\n⏱️ Duración promedio: {df['duration_min'].mean():.2f} minutos")
    print(f"⏱️ Canción más corta: {df['duration_min'].min():.2f} minutos")
    print(f"⏱️ Canción más larga: {df['duration_min'].max():.2f} minutos")
    
    return df

def analyze_musical_features(df):
    """Análisis de características musicales"""
    print("\n" + "=" * 60)
    print("🎼 ANÁLISIS DE CARACTERÍSTICAS MUSICALES")
    print("=" * 60)
    
    # Características principales
    audio_features = ['danceability', 'energy', 'valence', 'acousticness', 
                     'instrumentalness', 'liveness', 'speechiness']
    
    print("\n📊 Promedio de características por preferencia:")
    feature_comparison = df.groupby('liked_label')[audio_features].mean()
    
    for feature in audio_features:
        liked_avg = feature_comparison.loc['Me gusta', feature]
        disliked_avg = feature_comparison.loc['No me gusta', feature]
        diff = liked_avg - disliked_avg
        
        print(f"\n🎵 {feature.capitalize()}:")
        print(f"   💚 Me gusta: {liked_avg:.3f}")
        print(f"   💔 No me gusta: {disliked_avg:.3f}")
        print(f"   📈 Diferencia: {diff:+.3f}")
    
    return feature_comparison

def create_visualizations(df):
    """Crear visualizaciones interactivas"""
    
    # 1. Distribución de preferencias
    fig1 = px.pie(df, names='liked_label', 
                  title='🎵 Distribución de Preferencias Musicales',
                  color_discrete_map={'Me gusta': '#1DB954', 'No me gusta': '#FF6B6B'})
    fig1.update_layout(font_size=14)
    fig1.write_html('preferencias_distribucion.html')
    
    # 2. Características musicales por preferencia
    audio_features = ['danceability', 'energy', 'valence', 'acousticness']
    
    fig2 = make_subplots(rows=2, cols=2,
                        subplot_titles=[f'{feature.capitalize()}' for feature in audio_features])
    
    for i, feature in enumerate(audio_features):
        row = i // 2 + 1
        col = i % 2 + 1
        
        # Gráfico de violín
        for liked_val, color, name in [(1, '#1DB954', 'Me gusta'), (0, '#FF6B6B', 'No me gusta')]:
            data = df[df['liked'] == liked_val][feature]
            fig2.add_trace(go.Violin(y=data, name=name, 
                                   line_color=color, fillcolor=color, opacity=0.6),
                          row=row, col=col)
    
    fig2.update_layout(title='🎼 Distribución de Características Musicales',
                      showlegend=True, height=600)
    fig2.write_html('caracteristicas_musicales.html')
    
    # 3. Correlación entre características
    audio_features_extended = ['danceability', 'energy', 'valence', 'acousticness', 
                              'instrumentalness', 'liveness', 'speechiness', 'tempo', 'loudness']
    
    corr_matrix = df[audio_features_extended + ['liked']].corr()
    
    fig3 = px.imshow(corr_matrix, 
                     title='🔗 Matriz de Correlación - Características Musicales',
                     color_continuous_scale='RdBu_r',
                     text_auto=True)
    fig3.update_layout(width=800, height=700)
    fig3.write_html('correlacion_matriz.html')
    
    # 4. Scatter plot interactivo
    fig4 = px.scatter(df, x='energy', y='valence', 
                      color='liked_label',
                      size='danceability',
                      hover_data=['tempo', 'acousticness'],
                      title='🎯 Energía vs Valencia (Tamaño = Bailabilidad)',
                      color_discrete_map={'Me gusta': '#1DB954', 'No me gusta': '#FF6B6B'})
    fig4.update_layout(width=800, height=600)
    fig4.write_html('energia_valencia_scatter.html')
    
    # 5. Análisis temporal y de tempo
    fig5 = make_subplots(rows=1, cols=2,
                        subplot_titles=['Distribución de Tempo', 'Duración vs Preferencia'])
    
    # Tempo por preferencia
    for liked_val, color, name in [(1, '#1DB954', 'Me gusta'), (0, '#FF6B6B', 'No me gusta')]:
        data = df[df['liked'] == liked_val]['tempo']
        fig5.add_trace(go.Histogram(x=data, name=name, opacity=0.7,
                                   marker_color=color), row=1, col=1)
    
    # Duración vs preferencia
    fig5.add_trace(go.Box(y=df[df['liked']==1]['duration_min'], name='Me gusta',
                         marker_color='#1DB954'), row=1, col=2)
    fig5.add_trace(go.Box(y=df[df['liked']==0]['duration_min'], name='No me gusta',
                         marker_color='#FF6B6B'), row=1, col=2)
    
    fig5.update_layout(title='⏰ Análisis de Tempo y Duración', height=400)
    fig5.write_html('tempo_duracion_analisis.html')
    
    print("\n✅ Visualizaciones guardadas:")
    print("   📊 preferencias_distribucion.html")
    print("   🎼 caracteristicas_musicales.html") 
    print("   🔗 correlacion_matriz.html")
    print("   🎯 energia_valencia_scatter.html")
    print("   ⏰ tempo_duracion_analisis.html")

def generate_insights(df):
    """Generar insights y conclusiones"""
    print("\n" + "=" * 60)
    print("🧠 INSIGHTS Y CONCLUSIONES")
    print("=" * 60)
    
    # Análisis de características más importantes
    audio_features = ['danceability', 'energy', 'valence', 'acousticness', 
                     'instrumentalness', 'liveness', 'speechiness']
    
    feature_comparison = df.groupby('liked')[audio_features].mean()
    differences = feature_comparison.loc[1] - feature_comparison.loc[0]
    
    # Top características positivas
    top_positive = differences.nlargest(3)
    top_negative = differences.nsmallest(3)
    
    print("🎵 CARACTERÍSTICAS QUE MÁS INFLUYEN EN MIS GUSTOS:")
    print("\n💚 Me gustan más las canciones con mayor:")
    for feature, diff in top_positive.items():
        print(f"   ✓ {feature.capitalize()}: +{diff:.3f}")
    
    print("\n💔 Me gustan menos las canciones con mayor:")
    for feature, diff in top_negative.items():
        print(f"   ✗ {feature.capitalize()}: {diff:.3f}")
    
    # Análisis de tempo y duración
    liked_tempo = df[df['liked']==1]['tempo'].mean()
    disliked_tempo = df[df['liked']==0]['tempo'].mean()
    
    liked_duration = df[df['liked']==1]['duration_min'].mean()
    disliked_duration = df[df['liked']==0]['duration_min'].mean()
    
    print(f"\n🎵 PREFERENCIAS DE TEMPO Y DURACIÓN:")
    print(f"   💚 Tempo promedio (me gusta): {liked_tempo:.1f} BPM")
    print(f"   💔 Tempo promedio (no me gusta): {disliked_tempo:.1f} BPM")
    print(f"   💚 Duración promedio (me gusta): {liked_duration:.2f} min")
    print(f"   💔 Duración promedio (no me gusta): {disliked_duration:.2f} min")
    
    # Perfil musical
    print(f"\n🎯 MI PERFIL MUSICAL:")
    energy_pref = df[df['liked']==1]['energy'].mean()
    valence_pref = df[df['liked']==1]['valence'].mean()
    dance_pref = df[df['liked']==1]['danceability'].mean()
    
    print(f"   ⚡ Nivel de energía preferido: {energy_pref:.2f} ({get_energy_level(energy_pref)})")
    print(f"   😊 Nivel de positividad preferido: {valence_pref:.2f} ({get_valence_level(valence_pref)})")
    print(f"   💃 Nivel de bailabilidad preferido: {dance_pref:.2f} ({get_dance_level(dance_pref)})")

def get_energy_level(energy):
    if energy < 0.3:
        return "Relajado"
    elif energy < 0.7:
        return "Moderado"
    else:
        return "Enérgico"

def get_valence_level(valence):
    if valence < 0.3:
        return "Melancólico"
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
    print("🎵 INICIANDO ANÁLISIS DE DATOS DE SPOTIFY")
    print("=" * 60)
    
    # Cargar datos
    df = load_data()
    
    # Análisis básico
    df = basic_statistics(df)
    
    # Análisis de características musicales
    feature_comparison = analyze_musical_features(df)
    
    # Crear visualizaciones
    create_visualizations(df)
    
    # Generar insights
    generate_insights(df)
    
    print("\n" + "=" * 60)
    print("✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
    print("📊 Revisa los archivos HTML generados para ver las visualizaciones")
    print("=" * 60)

if __name__ == "__main__":
    main()