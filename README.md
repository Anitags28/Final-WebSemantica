# RecomendadorPelículas

Un sistema de recomendación de películas basado en tecnologías semánticas, desarrollado con Python, Flask y RDFlib.

## Descripción

Este proyecto implementa un recomendador de películas que utiliza tecnologías de la web semántica (RDF) para modelar y consultar información sobre películas, géneros, directores y actores. La aplicación permite a los usuarios:

- Explorar un catálogo de películas
- Ver detalles de películas específicas
- Calificar películas
- Obtener recomendaciones basadas en preferencias de géneros

## Tecnologías utilizadas

- **Python**: Lenguaje principal de programación
- **Flask**: Framework web ligero para Python
- **RDFlib**: Biblioteca para trabajar con datos RDF en Python
- **Bootstrap**: Framework CSS para el diseño de la interfaz

## Estructura del proyecto

```
RecomendadorPeliculas/
├── app.py                  # Aplicación principal Flask
├── model.py                # Modelo de datos RDF
├── templates/              # Plantillas HTML
│   ├── base.html           # Plantilla base
│   ├── index.html          # Página de inicio
│   ├── peliculas.html      # Catálogo de películas
│   ├── pelicula.html       # Detalles de película
│   ├── peliculas_genero.html  # Películas por género
│   ├── preferencias.html   # Formulario de preferencias
│   └── recomendaciones.html # Resultados de recomendaciones
└── README.md               # Documentación
```

## Instalación y ejecución

1. Asegúrate de tener Python 3.6 o superior instalado

2. Instala las dependencias:
   ```
   pip install flask rdflib
   ```

3. Inicia la aplicación:
   ```
   python app.py
   ```

4. Abre tu navegador y visita: `http://localhost:5000`

## Modelo semántico

El proyecto utiliza RDF (Resource Description Framework) para representar datos sobre películas. El modelo incluye:

- Películas: título, año, sinopsis, imagen
- Géneros: asociados a películas
- Directores: asociados a películas
- Actores: asociados a películas
- Calificaciones: valoraciones de las películas

## Algoritmo de recomendación

El sistema de recomendación actual se basa en las preferencias de género del usuario. A partir de los géneros seleccionados, el sistema consulta el grafo RDF para encontrar películas que coincidan con esos géneros.

## Mejoras futuras

- Implementar un sistema de recomendación más sofisticado
- Añadir autenticación de usuarios para guardar preferencias
- Conectar con una fuente externa de datos de películas (como una API)
- Implementar un sistema de calificación más avanzado
- Mejorar las consultas SPARQL para obtener recomendaciones más precisas

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. 