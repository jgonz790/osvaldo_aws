import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Configuracion de graficos
plt.style.use('default')
sns.set_palette("Set2")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

print("=== GENERANDO VISUALIZACIONES ===")

def crear_graficos_temporales(df_equipment, df_personnel):
    """Crea graficos de series temporales"""
    print("Creando graficos temporales...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('ANALISIS TEMPORAL - PERDIDAS RUSAS 2022', fontsize=16, fontweight='bold')
    
    # Grafico 1: Equipamiento por dia
    if 'date' in df_equipment.columns and 'total_equipment' in df_equipment.columns:
        axes[0,0].plot(df_equipment['date'], df_equipment['total_equipment'], 
                      color='red', linewidth=2, alpha=0.7)
        axes[0,0].set_title('Perdidas Diarias de Equipamiento')
        axes[0,0].set_ylabel('Unidades Perdidas')
        axes[0,0].tick_params(axis='x', rotation=45)
        axes[0,0].grid(True, alpha=0.3)
    
    # Grafico 2: Personal por dia
    if 'date' in df_personnel.columns:
        personnel_numeric = df_personnel.select_dtypes(include=[np.number])
        if len(personnel_numeric.columns) > 0:
            total_personnel = personnel_numeric.sum(axis=1)
            axes[0,1].plot(df_personnel['date'], total_personnel, 
                          color='darkred', linewidth=2, alpha=0.7)
            axes[0,1].set_title('Perdidas Diarias de Personal')
            axes[0,1].set_ylabel('Personal Perdido')
            axes[0,1].tick_params(axis='x', rotation=45)
            axes[0,1].grid(True, alpha=0.3)
    
    # Grafico 3: Tendencia semanal equipamiento
    if 'date' in df_equipment.columns and 'total_equipment' in df_equipment.columns:
        df_equipment['week'] = df_equipment['date'].dt.isocalendar().week
        weekly_eq = df_equipment.groupby('week')['total_equipment'].sum()
        axes[1,0].bar(weekly_eq.index, weekly_eq.values, color='orange', alpha=0.7)
        axes[1,0].set_title('Perdidas Semanales de Equipamiento')
        axes[1,0].set_xlabel('Semana del Año')
        axes[1,0].set_ylabel('Total Equipamiento')
    
    # Grafico 4: Acumulado vs Diario
    if 'date' in df_equipment.columns and 'total_equipment' in df_equipment.columns:
        cumulative = df_equipment['total_equipment'].cumsum()
        axes[1,1].plot(df_equipment['date'], cumulative, 
                      color='green', linewidth=3, label='Acumulado')
        axes[1,1].plot(df_equipment['date'], df_equipment['total_equipment'], 
                      color='blue', alpha=0.5, label='Diario')
        axes[1,1].set_title('Perdidas Acumuladas vs Diarias')
        axes[1,1].set_xlabel('Fecha')
        axes[1,1].set_ylabel('Equipamiento')
        axes[1,1].legend()
        axes[1,1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('analisis_temporal.png', dpi=300, bbox_inches='tight')
    print("Guardado: analisis_temporal.png")
    plt.show()

def crear_graficos_equipamiento(df_equipment):
    """Crea graficos especificos de equipamiento"""
    print("Creando graficos de equipamiento...")
    
    # Top equipamiento perdido
    equipment_cols = df_equipment.select_dtypes(include=[np.number]).columns
    equipment_cols = [col for col in equipment_cols if col not in ['day', 'total_equipment']]
    
    if len(equipment_cols) > 0:
        totals = df_equipment[equipment_cols].sum().sort_values(ascending=False)
        top_10 = totals.head(10)
        
        plt.figure(figsize=(12, 8))
        bars = plt.bar(range(len(top_10)), top_10.values, color='crimson', alpha=0.7)
        plt.title('TOP 10 EQUIPAMIENTO MAS PERDIDO', fontsize=14, fontweight='bold')
        plt.xlabel('Tipo de Equipamiento')
        plt.ylabel('Total Perdidas')
        plt.xticks(range(len(top_10)), top_10.index, rotation=45, ha='right')
        
        # Añadir valores en las barras
        for i, bar in enumerate(bars):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{int(top_10.values[i]):,}', ha='center', va='bottom')
        
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('top_equipamiento.png', dpi=300, bbox_inches='tight')
        print("Guardado: top_equipamiento.png")
        plt.show()

def crear_mapas_calor(df_equipment, df_personnel):
    """Crea mapas de calor de correlaciones"""
    print("Creando mapas de calor...")
    
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    
    # Mapa de calor equipamiento
    equipment_numeric = df_equipment.select_dtypes(include=[np.number])
    if len(equipment_numeric.columns) > 1:
        # Tomar solo las primeras 10 columnas para visualizacion
        corr_eq = equipment_numeric.iloc[:, :10].corr()
        
        sns.heatmap(corr_eq, annot=True, cmap='RdYlBu_r', center=0, 
                   square=True, ax=axes[0], fmt='.2f', cbar_kws={'shrink': .8})
        axes[0].set_title('CORRELACIONES EQUIPAMIENTO', fontsize=12, fontweight='bold')
    
    # Mapa de calor personal
    personnel_numeric = df_personnel.select_dtypes(include=[np.number])
    if len(personnel_numeric.columns) > 1:
        corr_pers = personnel_numeric.corr()
        
        sns.heatmap(corr_pers, annot=True, cmap='RdYlBu_r', center=0, 
                   square=True, ax=axes[1], fmt='.2f', cbar_kws={'shrink': .8})
        axes[1].set_title('CORRELACIONES PERSONAL', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('correlaciones_heatmap.png', dpi=300, bbox_inches='tight')
    print("Guardado: correlaciones_heatmap.png")
    plt.show()

def crear_dashboard_resumen(df_equipment, df_personnel):
    """Crea un dashboard resumen con metricas clave"""
    print("Creando dashboard resumen...")
    
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Titulo principal
    fig.suptitle('DASHBOARD RESUMEN - CONFLICTO UCRANIA-RUSIA 2022', 
                fontsize=18, fontweight='bold', y=0.95)
    
    # Metricas principales (texto)
    ax_metrics = fig.add_subplot(gs[0, :])
    ax_metrics.axis('off')
    
    # Calcular metricas
    total_eq = df_equipment.select_dtypes(include=[np.number]).sum().sum()
    total_pers = df_personnel.select_dtypes(include=[np.number]).sum().sum()
    dias_conflicto = len(df_equipment)
    
    metrics_text = f"""
    METRICAS PRINCIPALES:
    • Total Equipamiento Perdido: {total_eq:,.0f} unidades
    • Total Personal Perdido: {total_pers:,.0f} personas  
    • Dias de Conflicto Analizados: {dias_conflicto} dias
    • Promedio Diario Equipamiento: {total_eq/dias_conflicto:,.0f} unidades/dia
    • Promedio Diario Personal: {total_pers/dias_conflicto:,.0f} personas/dia
    """
    
    ax_metrics.text(0.02, 0.5, metrics_text, fontsize=12, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.5),
                   verticalalignment='center')
    
    # Graficos del dashboard
    # 1. Tendencia equipamiento
    ax1 = fig.add_subplot(gs[1, 0])
    if 'total_equipment' in df_equipment.columns:
        ax1.plot(df_equipment['total_equipment'], color='red', linewidth=2)
        ax1.set_title('Tendencia Equipamiento')
        ax1.set_ylabel('Unidades')
        ax1.grid(True, alpha=0.3)
    
    # 2. Tendencia personal
    ax2 = fig.add_subplot(gs[1, 1])
    personnel_total = df_personnel.select_dtypes(include=[np.number]).sum(axis=1)
    ax2.plot(personnel_total, color='darkred', linewidth=2)
    ax2.set_title('Tendencia Personal')
    ax2.set_ylabel('Personas')
    ax2.grid(True, alpha=0.3)
    
    # 3. Comparacion acumulada
    ax3 = fig.add_subplot(gs[1, 2])
    if 'total_equipment' in df_equipment.columns:
        eq_cumsum = df_equipment['total_equipment'].cumsum()
        pers_cumsum = personnel_total.cumsum()
        
        ax3_twin = ax3.twinx()
        ax3.plot(eq_cumsum, color='red', label='Equipamiento')
        ax3_twin.plot(pers_cumsum, color='darkred', label='Personal')
        ax3.set_title('Perdidas Acumuladas')
        ax3.legend(loc='upper left')
        ax3_twin.legend(loc='upper right')
    
    # 4. Distribucion semanal
    ax4 = fig.add_subplot(gs[2, :2])
    if 'date' in df_equipment.columns:
        df_equipment['weekday'] = df_equipment['date'].dt.day_name()
        weekday_eq = df_equipment.groupby('weekday')['total_equipment'].mean()
        ax4.bar(weekday_eq.index, weekday_eq.values, color='orange', alpha=0.7)
        ax4.set_title('Promedio por Dia de la Semana')
        ax4.tick_params(axis='x', rotation=45)
    
    # 5. Top 5 equipamiento
    ax5 = fig.add_subplot(gs[2, 2])
    equipment_cols = [col for col in df_equipment.select_dtypes(include=[np.number]).columns 
                     if col not in ['day', 'total_equipment']]
    if len(equipment_cols) > 0:
        top_5 = df_equipment[equipment_cols].sum().nlargest(5)
        ax5.pie(top_5.values, labels=top_5.index, autopct='%1.1f%%', startangle=90)
        ax5.set_title('Top 5 Equipamiento')
    
    plt.savefig('dashboard_resumen.png', dpi=300, bbox_inches='tight')
    print("Guardado: dashboard_resumen.png")
    plt.show()

def main():
    """Función principal para generar todas las visualizaciones"""
    try:
        print("Cargando datos limpios...")
        df_equipment = pd.read_csv('equipment_clean.csv')
        df_personnel = pd.read_csv('personnel_clean.csv')
        
        # Convertir fechas
        if 'date' in df_equipment.columns:
            df_equipment['date'] = pd.to_datetime(df_equipment['date'])
        if 'date' in df_personnel.columns:
            df_personnel['date'] = pd.to_datetime(df_personnel['date'])
        
        print(f"Equipamiento: {len(df_equipment)} registros")
        print(f"Personal: {len(df_personnel)} registros")
        
        # Generar visualizaciones
        crear_graficos_temporales(df_equipment, df_personnel)
        crear_graficos_equipamiento(df_equipment)
        crear_mapas_calor(df_equipment, df_personnel)
        crear_dashboard_resumen(df_equipment, df_personnel)
        
        print("\n=== TODAS LAS VISUALIZACIONES GENERADAS ===")
        print("Archivos creados:")
        print("- analisis_temporal.png")
        print("- top_equipamiento.png") 
        print("- correlaciones_heatmap.png")
        print("- dashboard_resumen.png")
        
    except FileNotFoundError:
        print("Error: No se encuentran los archivos limpios.")
        print("Ejecuta primero limpieza_datos.py")
    except Exception as e:
        print(f"Error generando visualizaciones: {e}")

if __name__ == "__main__":
    main()