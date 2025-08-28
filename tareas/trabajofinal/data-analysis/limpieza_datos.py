import pandas as pd
import numpy as np
from datetime import datetime

print("=== LIMPIEZA Y TRANSFORMACION DE DATOS ===")

def limpiar_equipamiento(df):
    """Limpia y transforma datos de equipamiento"""
    print("Limpiando datos de equipamiento...")
    
    # Copiar dataframe
    df_clean = df.copy()
    
    # Convertir fecha
    if 'date' in df_clean.columns:
        df_clean['date'] = pd.to_datetime(df_clean['date'])
    
    # Rellenar valores nulos con 0
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    df_clean[numeric_cols] = df_clean[numeric_cols].fillna(0)
    
    # Convertir negativos a 0 
    for col in numeric_cols:
        df_clean.loc[df_clean[col] < 0, col] = 0
    
    # Crear columna total equipamiento
    equipment_cols = [col for col in numeric_cols if col not in ['day']]
    if equipment_cols:
        df_clean['total_equipment'] = df_clean[equipment_cols].sum(axis=1)
    
    print(f"Filas antes: {len(df)}, Filas despues: {len(df_clean)}")
    return df_clean

def limpiar_personal(df):
    """Limpia y transforma datos de personal"""
    print("Limpiando datos de personal...")
    
    df_clean = df.copy()
    
    # Convertir fecha
    if 'date' in df_clean.columns:
        df_clean['date'] = pd.to_datetime(df_clean['date'])
    
    # Rellenar nulos
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    df_clean[numeric_cols] = df_clean[numeric_cols].fillna(0)
    
    # Limpiar negativos
    for col in numeric_cols:
        df_clean.loc[df_clean[col] < 0, col] = 0
    
    print(f"Filas antes: {len(df)}, Filas despues: {len(df_clean)}")
    return df_clean

def aplicar_correcciones(df_equipment, df_corrections):
    """Aplica correcciones al dataset principal"""
    print("Aplicando correcciones...")
    
    if df_corrections.empty:
        print("No hay correcciones que aplicar")
        return df_equipment
    
    df_corrected = df_equipment.copy()
    corrections_applied = 0
    
    # Aplicar correcciones por fecha si es posible
    if 'date' in df_corrections.columns and 'date' in df_corrected.columns:
        df_corrections['date'] = pd.to_datetime(df_corrections['date'])
        
        for idx, correction in df_corrections.iterrows():
            correction_date = correction['date']
            matching_rows = df_corrected[df_corrected['date'] == correction_date]
            
            if not matching_rows.empty:
                for col in df_corrections.columns:
                    if col != 'date' and col in df_corrected.columns:
                        if pd.notna(correction[col]):
                            df_corrected.loc[df_corrected['date'] == correction_date, col] = correction[col]
                            corrections_applied += 1
    
    print(f"Correcciones aplicadas: {corrections_applied}")
    return df_corrected

def generar_metricas_agregadas(df_equipment, df_personnel):
    """Genera métricas agregadas para el dashboard"""
    print("Generando metricas agregadas...")
    
    metricas = {}
    
    if 'date' in df_equipment.columns:
        # Métricas por mes
        df_equipment['month'] = df_equipment['date'].dt.to_period('M')
        monthly_equipment = df_equipment.groupby('month').sum()
        metricas['monthly_equipment'] = monthly_equipment
        
        # Métricas por semana
        df_equipment['week'] = df_equipment['date'].dt.to_period('W')
        weekly_equipment = df_equipment.groupby('week').sum()
        metricas['weekly_equipment'] = weekly_equipment
    
    if 'date' in df_personnel.columns:
        df_personnel['month'] = df_personnel['date'].dt.to_period('M')
        monthly_personnel = df_personnel.groupby('month').sum()
        metricas['monthly_personnel'] = monthly_personnel
        
        df_personnel['week'] = df_personnel['date'].dt.to_period('W')
        weekly_personnel = df_personnel.groupby('week').sum()
        metricas['weekly_personnel'] = weekly_personnel
    
    return metricas

def main():
    """Función principal de limpieza"""
    print("Iniciando proceso de limpieza...")
    
    try:
        # Cargar datos
        equipment_df = pd.read_csv('russia_losses_equipment.csv')
        corrections_df = pd.read_csv('russia_losses_equipment_correction.csv')
        personnel_df = pd.read_csv('russia_losses_personnel.csv')
        
        print(f"Datos cargados exitosamente")
        
        # Limpiar datos
        equipment_clean = limpiar_equipamiento(equipment_df)
        personnel_clean = limpiar_personal(personnel_df)
        
        # Aplicar correcciones
        equipment_final = aplicar_correcciones(equipment_clean, corrections_df)
        
        # Generar métricas
        metricas = generar_metricas_agregadas(equipment_final, personnel_clean)
        
        # Guardar datos limpios
        equipment_final.to_csv('equipment_clean.csv', index=False)
        personnel_clean.to_csv('personnel_clean.csv', index=False)
        
        print("\nDatos limpios guardados:")
        print("- equipment_clean.csv")
        print("- personnel_clean.csv")
        
        print("\nResumen de limpieza:")
        print(f"Equipamiento: {len(equipment_final)} filas procesadas")
        print(f"Personal: {len(personnel_clean)} filas procesadas")
        
        if 'total_equipment' in equipment_final.columns:
            print(f"Total equipamiento perdido: {equipment_final['total_equipment'].sum():,.0f}")
        
        numeric_pers = personnel_clean.select_dtypes(include=[np.number]).columns
        if len(numeric_pers) > 0:
            print(f"Total personal perdido: {personnel_clean[numeric_pers].sum().sum():,.0f}")
            
        print("\n=== LIMPIEZA COMPLETADA ===")
        
    except FileNotFoundError as e:
        print(f"Error: No se encuentran los archivos CSV: {e}")
        print("Asegurate de que los archivos esten en el directorio actual")
    except Exception as e:
        print(f"Error durante la limpieza: {e}")

if __name__ == "__main__":
    main()