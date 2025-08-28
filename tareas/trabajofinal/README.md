# Proyecto Final - Pipeline de Datos Conflicto Ucrania-Rusia 2022

## Descripción
Este proyecto analiza datos de pérdidas rusas durante el conflicto con Ucrania en 2022, implementando un pipeline de datos híbrido usando servicios de AWS.

## Datasets
- `russia_losses_equipment.csv` - Pérdidas diarias de equipamiento (1,277 filas, 19 columnas)
- `russia_losses_personnel.csv` - Pérdidas diarias de personal (1,277 filas, 5 columnas)  
- `russia_losses_equipment_correction.csv` - Correcciones de datos (26 filas, 16 columnas)

## Estructura del Proyecto

```
trabajofinal/
├── data-analysis/          # Análisis exploratorio
│   ├── analisis_exploratorio.py
│   ├── limpieza_datos.py
│   └── visualizaciones.py
├── lambda-functions/       # Funciones AWS Lambda
├── ec2-scripts/           # Scripts para EC2 y Spark
├── architecture/          # Diagramas de arquitectura
├── dashboard/             # Dashboard Streamlit
├── requirements.txt       # Dependencias Python
└── README.md             # Este archivo
```

## Análisis Realizado

### 1. Análisis Exploratorio
- Exploración de estructura de datos
- Identificación de problemas de calidad
- Estadísticas descriptivas
- Análisis de correlaciones

### 2. Limpieza de Datos
- Conversión de tipos de datos
- Tratamiento de valores nulos y negativos
- Aplicación de correcciones
- Generación de métricas agregadas

### 3. Visualizaciones
- Series temporales de pérdidas
- Top equipamiento más perdido
- Mapas de calor de correlaciones
- Dashboard resumen con métricas clave

## Como Usar

### Análisis Local
1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar análisis exploratorio:
```bash
cd data-analysis
python analisis_exploratorio.py
```

3. Limpiar datos:
```bash
python limpieza_datos.py
```

4. Generar visualizaciones:
```bash
python visualizaciones.py
```

## Arquitectura AWS (Próximamente)
- **S3**: Almacenamiento de datos raw y procesados
- **Lambda**: Funciones de ingesta, limpieza y agregación
- **EC2**: Orquestación y procesamiento con Spark
- **Streamlit**: Dashboard interactivo

## Resultados Principales
- Total equipamiento perdido identificado
- Patrones temporales de pérdidas
- Correlaciones entre tipos de equipamiento
- Tendencias semanales y mensuales

## Próximos Pasos
1. Implementar funciones Lambda
2. Configurar jobs de Spark en EC2
3. Crear dashboard interactivo
4. Documentar arquitectura AWS

## Notas Técnicas
- Los datos han sido validados y limpiados
- Se aplicaron correcciones del dataset oficial
- Las visualizaciones están optimizadas para análisis
- El código está preparado para escalamiento en AWS