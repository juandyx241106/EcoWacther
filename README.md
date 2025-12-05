**Instrucciones de ejecución**


  1. Clonar el repositorio.
  2. Crear un entorno virtual.
  3. Instalar dependencias.
  4. Abrir la carpeta "EcoWatcher" y ejecutar app.py
  5. Abrir el navegador de preferencia y poner la URL "http://127.0.0.1:5000"


**Dependencias necesarias**


  1. Flask
  2. SQLAlchemy
  3. pandas
  4. numpy
  5. scikit-learn
  6. joblib


**Estructura del proyecto**

```

EcoWatcher/
├── app.py
│       Archivo principal de la aplicación.
│       Implementa la inicialización de Flask, definición de rutas HTTP,
│       carga del modelo de Machine Learning y coordinación entre
│       los componentes de persistencia, preprocesamiento y visualización.
│
├── requirements.txt
│       Listado completo de dependencias necesarias para la ejecución
│       del proyecto. Permite la reconstrucción del entorno mediante
│       instalación automatizada.
│
├── .gitignore
│       Especificación de archivos y directorios excluidos del control de
│       versiones, incluyendo bases de datos locales, artefactos temporales
│       y configuraciones del entorno.
│
├── data/
│   ├── EcoWatcher.db
│   │       Base de datos SQLite donde se almacenan todas las predicciones
│   │       históricas generadas por el sistema.
│   │
│   ├── bogota_procesado.csv
│   │       Dataset depurado y normalizado, utilizado durante el proceso
│   │       de entrenamiento del modelo.
│   │
│   ├── bogota_sin_procesar.csv
│   │       Fuente original del dataset previo al preprocesamiento.
│   │
│   └── dataset_mejorado.csv
│           Versión extendida o refinada del dataset con correcciones
│           y mejoras de calidad para análisis posteriores.
│
├── modelo/
│   ├── entrenador_de_modelo.py
│   │       Script encargado del entrenamiento del modelo predictivo.
│   │       Incluye generación del artefacto final y evaluación del desempeño.
│   │
│   └── modelo_entrenado.pkl
│           Artefacto del modelo entrenado serializado (joblib),
│           utilizado en las predicciones de la aplicación en tiempo real.
│
├── preprocesamiento_datos/
│   ├── preprocesador_datos.py
│   │       Implementación de las rutinas de preprocesamiento, tales como
│   │       normalización MinMax, limpieza y transformación de características.
│   │
│   └── parametros_normalizados.json
│           Archivo que almacena los parámetros de normalización utilizados
│           para mantener consistencia entre entrenamiento e inferencia.
│
├── database/
│   ├── conexion.py
│   │       Configuración de la conexión a la base de datos SQLite.
│   │       Define el engine, sesiones y parámetros clave del ORM.
│   │
│   └── modelos.py
│           Declaración de los modelos ORM utilizados por SQLAlchemy.
│           Incluye la estructura de la tabla de predicciones.
│
├── sensor/
│   └── simulador.py
│           Módulo de simulación IoT basado en hilos (threading).
│           Genera datos sintéticos de manera periódica y los registra
│           automáticamente en la base de datos.
│
├── static/
│   ├── css/
│   │   ├── index.css
│   │   │       Estilos correspondientes a la interfaz del formulario de predicción.
│   │   │
│   │   └── dashboard.css
│   │           Estilos utilizados por el panel de análisis y visualización histórica.
│   │
│   └── js/
│       ├── index.js
│       │       Lógica de interacción del usuario con el formulario,
│       │       validaciones y flujo de envío.
│       │
│       └── dashboard.js
│               Implementación de la lógica del dashboard: consumo de APIs,
│               renderización de gráficas mediante Chart.js y actualización dinámica.
│
└── templates/
    ├── index.html
    │       Plantilla principal utilizada para capturar datos del usuario
    │       y presentar el resultado de la predicción.
    │
    └── dashboard.html
            Plantilla destinada a la visualización del historial, tendencias,
            alertas ambientales y análisis del EcoScore.
```



  **Descripcionn del proyecto**


EcoWatcher es un sistema que emula el funcionamiento de una plataforma IoT (Internet of Things) orientada al monitoreo ambiental. El programa simula un conjunto de sensores que registran variables ambientales relevantes cada minuto y las envían al sistema para su procesamiento.

Con estos datos, el sistema calcula un EcoScore —un indicador numérico de 0 a 500— que resume el estado ambiental de una zona determinada. El EcoScore permite evaluar condiciones críticas, identificar tendencias y facilitar la toma de decisiones relacionadas con la gestión del entorno.
