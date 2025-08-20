# Análisis de Datos de Netflix 📊

Este proyecto realiza un análisis exploratorio completo del dataset de Netflix Shows disponible en Kaggle.

## 📋 Descripción del Proyecto

El análisis incluye:
- ✅ Limpieza y preprocesamiento de datos
- ✅ Análisis exploratorio de datos (EDA)
- ✅ Visualizaciones interactivas
- ✅ Insights y conclusiones

## 📁 Estructura del Proyecto

```
├── netflix_data_analysis.ipynb    # Notebook principal con análisis completo
├── netflix_titles.csv             # Dataset original
├── netflix_titles_cleaned.csv     # Dataset limpio (generado)
├── requirements.txt               # Dependencias de Python
└── README.md                      # Este archivo
```

## 🔧 Instalación y Configuración

### Prerrequisitos
- Python 3.7+
- Jupyter Notebook

### Instalación de dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar el análisis
```bash
jupyter notebook netflix_data_analysis.ipynb
```

## 📊 Dataset

**Fuente:** [Netflix Shows Dataset - Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)

**Características del dataset:**
- **Filas:** ~8,800 títulos
- **Columnas:** 12 atributos
- **Período:** Contenido hasta 2021
- **Tipos:** Películas y Series TV

### Columnas del dataset:
- `show_id`: ID único
- `type`: Película o Serie TV
- `title`: Título del contenido
- `director`: Director(es)
- `cast`: Reparto principal
- `country`: País de origen
- `date_added`: Fecha de agregado a Netflix
- `release_year`: Año de lanzamiento
- `rating`: Clasificación por edad
- `duration`: Duración (minutos para películas, temporadas para series)
- `listed_in`: Géneros/categorías
- `description`: Descripción del contenido

## 🔍 Principales Insights

### 1. Distribución de Contenido
- **Películas:** ~70% del catálogo
- **Series TV:** ~30% del catálogo

### 2. Tendencias Temporales
- Crecimiento exponencial de contenido desde 2015
- Pico de contenido agregado en 2019-2020

### 3. Geografía del Contenido
- **Estados Unidos** lidera la producción
- Representación de **80+ países**
- Creciente diversidad internacional

### 4. Géneros Populares
- Dramas Internacionales
- Comedias
- Documentales
- Thrillers

### 5. Duración y Temporadas
- **Películas:** Promedio de 100 minutos
- **Series:** Promedio de 1-2 temporadas

## 🛠️ Tecnologías Utilizadas

- **Python 3.13+**
- **Pandas** - Manipulación de datos
- **NumPy** - Computación numérica
- **Matplotlib & Seaborn** - Visualizaciones estáticas
- **Plotly** - Visualizaciones interactivas
- **Jupyter Notebook** - Entorno de desarrollo

## 📈 Visualizaciones Incluidas

1. **Gráficos de distribución** de tipos de contenido
2. **Tendencias temporales** de agregado de contenido
3. **Mapas de calor** de actividad mensual
4. **Análisis geográfico** por países
5. **Distribución de géneros** y clasificaciones
6. **Análisis de duración** por tipo de contenido

## 🎯 Casos de Uso

Este análisis puede ser útil para:
- Estrategias de contenido para plataformas de streaming
- Investigación de mercado en entretenimiento
- Análisis de tendencias en consumo de medios
- Proyectos educativos de ciencia de datos

## 👨‍💻 Autor

**Osvaldo**
- GitHub: [Tu perfil de GitHub]
- Proyecto creado en: Agosto 2025

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios importantes:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Contacto

Si tienes preguntas o sugerencias sobre este proyecto, no dudes en contactarme.

---

⭐ Si este proyecto te fue útil, ¡considera darle una estrella!