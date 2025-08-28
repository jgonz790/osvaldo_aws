import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configurar estilo de graficos
plt.style.use('default')
sns.set_palette("husl")

print("=== ANALISIS EXPLORATORIO CONFLICTO UCRANIA-RUSIA 2022 ===")
print("Datos de perdidas rusas de equipamiento y personal\n")

# Cargar los datos
print("1. CARGANDO DATOS...")
equipment_df = pd.read_csv('russia_losses_equipment.csv')
corrections_df = pd.read_csv('russia_losses_equipment_correction.csv') 
personnel_df = pd.read_csv('russia_losses_personnel.csv')

print(f"- Equipamiento: {equipment_df.shape[0]} filas, {equipment_df.shape[1]} columnas")
print(f"- Correcciones: {corrections_df.shape[0]} filas, {corrections_df.shape[1]} columnas")
print(f"- Personal: {personnel_df.shape[0]} filas, {personnel_df.shape[1]} columnas")

print("\n2. EXPLORANDO ESTRUCTURA DE DATOS")
print("\n--- DATASET EQUIPAMIENTO ---")
print("Columnas:", list(equipment_df.columns))
print("\nPrimeras 5 filas:")
print(equipment_df.head())
print("\nTipos de datos:")
print(equipment_df.dtypes)
print("\nValores nulos:")
print(equipment_df.isnull().sum())

print("\n--- DATASET PERSONAL ---") 
print("Columnas:", list(personnel_df.columns))
print("\nPrimeras 5 filas:")
print(personnel_df.head())
print("\nTipos de datos:")
print(personnel_df.dtypes)
print("\nValores nulos:")
print(personnel_df.isnull().sum())

print("\n--- DATASET CORRECCIONES ---")
print("Columnas:", list(corrections_df.columns))
print("\nPrimeras 5 filas:")
print(corrections_df.head())

print("\n3. ESTADISTICAS DESCRIPTIVAS")
print("\n--- EQUIPAMIENTO ---")
numeric_cols_eq = equipment_df.select_dtypes(include=[np.number]).columns
print(equipment_df[numeric_cols_eq].describe())

print("\n--- PERSONAL ---")
numeric_cols_pers = personnel_df.select_dtypes(include=[np.number]).columns
print(personnel_df[numeric_cols_pers].describe())

print("\n4. PROBLEMAS DE CALIDAD DETECTADOS")
print("\nProblemas encontrados:")

# Verificar fechas
if 'date' in equipment_df.columns:
    print("- Formato de fechas en equipamiento:", equipment_df['date'].dtype)
if 'date' in personnel_df.columns:
    print("- Formato de fechas en personal:", personnel_df['date'].dtype)

# Buscar valores negativos
print("\nValores negativos en equipamiento:")
for col in numeric_cols_eq:
    negative_count = (equipment_df[col] < 0).sum()
    if negative_count > 0:
        print(f"  {col}: {negative_count} valores negativos")

print("\nValores negativos en personal:")
for col in numeric_cols_pers:
    negative_count = (personnel_df[col] < 0).sum()
    if negative_count > 0:
        print(f"  {col}: {negative_count} valores negativos")

# Duplicados
print(f"\nFilas duplicadas equipamiento: {equipment_df.duplicated().sum()}")
print(f"Filas duplicadas personal: {personnel_df.duplicated().sum()}")

print("\n5. ANALISIS TEMPORAL")
# Convertir fechas si es necesario
if 'date' in equipment_df.columns:
    equipment_df['date'] = pd.to_datetime(equipment_df['date'])
if 'date' in personnel_df.columns:
    personnel_df['date'] = pd.to_datetime(personnel_df['date'])

# Rangos de fechas
if 'date' in equipment_df.columns:
    print(f"Periodo equipamiento: {equipment_df['date'].min()} a {equipment_df['date'].max()}")
if 'date' in personnel_df.columns:
    print(f"Periodo personal: {personnel_df['date'].min()} a {personnel_df['date'].max()}")

print("\n6. TRANSFORMACIONES ETL NECESARIAS")
print("\nTransformaciones identificadas:")
print("1. Convertir columna 'date' a formato datetime")
print("2. Validar y limpiar valores negativos o anomalos")
print("3. Estandarizar nombres de columnas")
print("4. Crear columnas calculadas de totales")
print("5. Normalizar formatos de datos numericos")
print("6. Aplicar correcciones del dataset de correcciones")
print("7. Crear indices temporales para agregaciones")

print("\n7. CORRELACIONES PRINCIPALES")
if len(numeric_cols_eq) > 1:
    print("\nMatriz correlacion equipamiento (primeras 5 variables):")
    corr_matrix = equipment_df[numeric_cols_eq[:5]].corr()
    print(corr_matrix)

if len(numeric_cols_pers) > 1:
    print("\nMatriz correlacion personal:")
    corr_matrix_pers = personnel_df[numeric_cols_pers].corr()
    print(corr_matrix_pers)

print("\n8. PREPARACION PARA DASHBOARD")
print("\nVisualizaciones recomendadas:")
print("- Serie temporal de perdidas totales diarias")
print("- Top 10 tipos de equipamiento mas perdidos")
print("- Correlacion equipamiento vs personal")
print("- Tendencias mensuales y semanales")
print("- Mapas de calor de intensidad temporal")
print("- Metricas acumuladas vs diarias")

print("\n9. RESUMEN EJECUTIVO")
total_equipment_losses = equipment_df[numeric_cols_eq].sum().sum() if len(numeric_cols_eq) > 0 else 0
total_personnel_losses = personnel_df[numeric_cols_pers].sum().sum() if len(numeric_cols_pers) > 0 else 0

print(f"Total perdidas equipamiento (aprox): {total_equipment_losses:,.0f}")
print(f"Total perdidas personal (aprox): {total_personnel_losses:,.0f}")
print(f"Dias analizados equipamiento: {len(equipment_df)}")
print(f"Dias analizados personal: {len(personnel_df)}")

print("\n=== ANALISIS COMPLETADO ===")
print("Los datos estan listos para procesamiento ETL y creacion del dashboard")