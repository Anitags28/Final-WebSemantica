#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, flash
import rdflib
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import RDFS, XSD
from model import MovieModel, MOVIE, GENRE

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_flash'  # Necesario para los mensajes flash

# Inicializar el modelo
movie_model = MovieModel()

@app.route('/')
def index():
    # Obtener todas las películas para mostrarlas en la página principal
    peliculas = movie_model.obtener_todas_peliculas()
    return render_template('index.html', peliculas=peliculas)

@app.route('/peliculas')
def peliculas():
    # Obtener todas las películas
    peliculas = movie_model.obtener_todas_peliculas()
    return render_template('peliculas.html', peliculas=peliculas)

@app.route('/pelicula/<id>')
def pelicula(id):
    # Obtener detalles de una película específica
    detalles = movie_model.obtener_pelicula(id)
    return render_template('pelicula.html', pelicula=detalles)

@app.route('/genero/<genero_id>')
def peliculas_por_genero(genero_id):
    # Obtener películas de un género específico
    peliculas = movie_model.recomendar_por_genero(genero_id)
    return render_template('peliculas_genero.html', peliculas=peliculas, genero_id=genero_id)

@app.route('/recomendar', methods=['GET', 'POST'])
def recomendar():
    if request.method == 'POST':
        # Obtener géneros seleccionados del formulario
        generos_seleccionados = request.form.getlist('generos')
        
        # Verificar que se seleccionó al menos un género
        if not generos_seleccionados:
            generos = []
            for s, p, o in movie_model.g.triples((None, RDF.type, MOVIE.Genre)):
                genero_id = str(s).split('/')[-1]
                label = str(movie_model.g.value(s, RDFS.label))
                generos.append({'id': genero_id, 'nombre': label})
            return render_template('preferencias.html', generos=generos, 
                                error="Por favor, selecciona al menos un género.")
        
        # Lógica simple de recomendación basada en géneros seleccionados
        recomendaciones = []
        for genero_id in generos_seleccionados:
            peliculas_genero = movie_model.recomendar_por_genero(genero_id)
            for pelicula in peliculas_genero:
                # Evitar duplicados comparando por ID
                if not any(p['id'] == pelicula['id'] for p in recomendaciones):
                    recomendaciones.append(pelicula)
        
        return render_template('recomendaciones.html', recomendaciones=recomendaciones,
                              generos_seleccionados=generos_seleccionados)
    
    # GET: Obtener todos los géneros disponibles
    generos = []
    for s, p, o in movie_model.g.triples((None, RDF.type, MOVIE.Genre)):
        genero_id = str(s).split('/')[-1]
        label = str(movie_model.g.value(s, RDFS.label))
        generos.append({'id': genero_id, 'nombre': label})
    
    return render_template('preferencias.html', generos=generos)

@app.route('/calificar/<id>', methods=['POST'])
def calificar(id):
    if request.method == 'POST':
        calificacion = int(request.form.get('calificacion', 0))
        if 1 <= calificacion <= 5:
            pelicula_uri = URIRef(MOVIE + id)
            movie_model.agregar_calificacion(pelicula_uri, calificacion)
            # Obtener el título de la película para mostrar en el mensaje
            titulo = str(movie_model.g.value(pelicula_uri, MOVIE.title))
            flash(f'Has calificado "{titulo}" con {calificacion} estrellas. Gracias por tu opinion.', 'success')

        else:
            flash(f'Por favor, selecciona una calificación válida (1-5)', 'warning')
    
    return redirect(url_for('pelicula', id=id))

if __name__ == '__main__':
    # Cargar datos de muestra
    movie_model.cargar_datos_muestra()
    app.run(debug=True) 