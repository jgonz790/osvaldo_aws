#!/usr/bin/env python
# coding: utf-8

# # Análisis de Datos de Spotify
# **Nombre:** Osvaldo González  
# **Fecha:** 21 de Agosto, 2025  
# **Curso:** Xideral AWS - Análisis de Datos

# ## Importar librerías necesarias

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ## Cargar el dataset

# In[2]:


# Cargar el archivo CSV de Spotify
df = pd.read_csv('data.csv')
print("Dataset cargado exitosamente!")


# In[3]:


# Mostrar información básica del dataset
print("Forma del dataset:", df.shape)
print("\nPrimeras 5 filas:")
df.head()


# In[4]:


# Información general del dataset
df.info()


# In[5]:


# Estadísticas descriptivas
df.describe()


# ## Análisis Exploratorio

# In[6]:


# Verificar valores únicos en la columna 'liked'
print("Valores únicos en 'liked':")
print(df['liked'].value_counts())


# In[7]:


# Crear gráfico de barras para las preferencias
plt.figure(figsize=(8, 6))
likes_counts = df['liked'].value_counts()
plt.bar(['No me gusta (0)', 'Me gusta (1)'], likes_counts.values, color=['red', 'green'])
plt.title('Distribución de Preferencias Musicales')
plt.ylabel('Número de canciones')
plt.show()


# In[8]:


# Calcular porcentajes
total_songs = len(df)
likes = df['liked'].sum()
dislikes = total_songs - likes

print(f"Total de canciones: {total_songs}")
print(f"Me gusta: {likes} canciones ({likes/total_songs*100:.1f}%)")
print(f"No me gusta: {dislikes} canciones ({dislikes/total_songs*100:.1f}%)")


# ## Análisis de características musicales

# In[9]:


# Analizar la característica 'danceability'
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
df[df['liked']==1]['danceability'].hist(alpha=0.7, label='Me gusta', color='green', bins=20)
df[df['liked']==0]['danceability'].hist(alpha=0.7, label='No me gusta', color='red', bins=20)
plt.xlabel('Danceability')
plt.ylabel('Frecuencia')
plt.title('Distribución de Danceability')
plt.legend()

plt.subplot(1, 2, 2)
df[df['liked']==1]['energy'].hist(alpha=0.7, label='Me gusta', color='green', bins=20)
df[df['liked']==0]['energy'].hist(alpha=0.7, label='No me gusta', color='red', bins=20)
plt.xlabel('Energy')
plt.ylabel('Frecuencia')
plt.title('Distribución de Energy')
plt.legend()

plt.tight_layout()
plt.show()


# In[10]:


# Calcular promedios por preferencia
print("Promedio de características por preferencia:")
print("\nDanceability:")
print(f"Me gusta: {df[df['liked']==1]['danceability'].mean():.3f}")
print(f"No me gusta: {df[df['liked']==0]['danceability'].mean():.3f}")

print("\nEnergy:")
print(f"Me gusta: {df[df['liked']==1]['energy'].mean():.3f}")
print(f"No me gusta: {df[df['liked']==0]['energy'].mean():.3f}")


# In[11]:


# Analizar más características
características = ['valence', 'acousticness', 'instrumentalness', 'speechiness']

plt.figure(figsize=(12, 8))
for i, característica in enumerate(características, 1):
    plt.subplot(2, 2, i)
    df[df['liked']==1][característica].hist(alpha=0.7, label='Me gusta', color='green', bins=15)
    df[df['liked']==0][característica].hist(alpha=0.7, label='No me gusta', color='red', bins=15)
    plt.xlabel(característica.capitalize())
    plt.ylabel('Frecuencia')
    plt.title(f'Distribución de {característica.capitalize()}')
    plt.legend()

plt.tight_layout()
plt.show()


# In[12]:


# Calcular promedios para todas las características
for característica in características:
    me_gusta = df[df['liked']==1][característica].mean()
    no_me_gusta = df[df['liked']==0][característica].mean()
    diferencia = me_gusta - no_me_gusta
    
    print(f"\n{característica.capitalize()}:")
    print(f"Me gusta: {me_gusta:.3f}")
    print(f"No me gusta: {no_me_gusta:.3f}")
    print(f"Diferencia: {diferencia:+.3f}")


# ## Análisis de Tempo y Duración

# In[13]:


# Convertir duración a minutos para mejor comprensión
df['duration_min'] = df['duration_ms'] / 60000

print("Análisis de duración:")
print(f"Duración promedio (me gusta): {df[df['liked']==1]['duration_min'].mean():.2f} minutos")
print(f"Duración promedio (no me gusta): {df[df['liked']==0]['duration_min'].mean():.2f} minutos")


# In[14]:


# Gráficos de tempo y duración
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
df[df['liked']==1]['tempo'].hist(alpha=0.7, label='Me gusta', color='green', bins=20)
df[df['liked']==0]['tempo'].hist(alpha=0.7, label='No me gusta', color='red', bins=20)
plt.xlabel('Tempo (BPM)')
plt.ylabel('Frecuencia')
plt.title('Distribución de Tempo')
plt.legend()

plt.subplot(1, 2, 2)
df[df['liked']==1]['duration_min'].hist(alpha=0.7, label='Me gusta', color='green', bins=20)
df[df['liked']==0]['duration_min'].hist(alpha=0.7, label='No me gusta', color='red', bins=20)
plt.xlabel('Duración (minutos)')
plt.ylabel('Frecuencia')
plt.title('Distribución de Duración')
plt.legend()

plt.tight_layout()
plt.show()


# In[15]:


# Estadísticas de tempo
print("Análisis de tempo:")
print(f"Tempo promedio (me gusta): {df[df['liked']==1]['tempo'].mean():.1f} BPM")
print(f"Tempo promedio (no me gusta): {df[df['liked']==0]['tempo'].mean():.1f} BPM")


# ## Conclusiones

# In[16]:


print("=== CONCLUSIONES DEL ANÁLISIS ===")
print("\n1. DISTRIBUCIÓN GENERAL:")
print(f"   - Analicé {len(df)} canciones")
print(f"   - {df['liked'].sum()} me gustan ({df['liked'].sum()/len(df)*100:.1f}%)")
print(f"   - {len(df)-df['liked'].sum()} no me gustan ({(len(df)-df['liked'].sum())/len(df)*100:.1f}%)")

print("\n2. CARACTERÍSTICAS QUE MÁS ME GUSTAN:")
dance_diff = df[df['liked']==1]['danceability'].mean() - df[df['liked']==0]['danceability'].mean()
energy_diff = df[df['liked']==1]['energy'].mean() - df[df['liked']==0]['energy'].mean()
valence_diff = df[df['liked']==1]['valence'].mean() - df[df['liked']==0]['valence'].mean()

print(f"   - Danceability: +{dance_diff:.3f} (me gustan las canciones más bailables)")
print(f"   - Energy: +{energy_diff:.3f} (prefiero canciones con más energía)")
print(f"   - Valence: +{valence_diff:.3f} (me gusta la música más positiva)")

print("\n3. CARACTERÍSTICAS QUE MENOS ME GUSTAN:")
acoustic_diff = df[df['liked']==1]['acousticness'].mean() - df[df['liked']==0]['acousticness'].mean()
instrumental_diff = df[df['liked']==1]['instrumentalness'].mean() - df[df['liked']==0]['instrumentalness'].mean()

print(f"   - Acousticness: {acoustic_diff:.3f} (prefiero música menos acústica)")
print(f"   - Instrumentalness: {instrumental_diff:.3f} (prefiero canciones con vocales)")

print("\n4. PREFERENCIAS DE TEMPO Y DURACIÓN:")
tempo_liked = df[df['liked']==1]['tempo'].mean()
tempo_disliked = df[df['liked']==0]['tempo'].mean()
duration_liked = df[df['liked']==1]['duration_min'].mean()
duration_disliked = df[df['liked']==0]['duration_min'].mean()

print(f"   - Prefiero tempo más rápido: {tempo_liked:.1f} BPM vs {tempo_disliked:.1f} BPM")
print(f"   - Prefiero canciones más cortas: {duration_liked:.2f} min vs {duration_disliked:.2f} min")


# ## Gráfico final resumen

# In[17]:


# Crear un gráfico final que resuma las principales diferencias
características_principales = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness']
diferencias = []

for car in características_principales:
    diff = df[df['liked']==1][car].mean() - df[df['liked']==0][car].mean()
    diferencias.append(diff)

plt.figure(figsize=(10, 6))
colores = ['green' if x > 0 else 'red' for x in diferencias]
plt.bar(características_principales, diferencias, color=colores)
plt.title('Diferencias en Características Musicales\n(Verde: Me gusta más, Rojo: Me gusta menos)')
plt.ylabel('Diferencia promedio')
plt.xticks(rotation=45)
plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
plt.tight_layout()
plt.show()

print("¡Análisis completado!")