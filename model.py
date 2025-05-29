from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD

# Definir namespaces
MOVIE = Namespace("http://example.org/movie/")
GENRE = Namespace("http://example.org/genre/")
DIRECTOR = Namespace("http://example.org/director/")
ACTOR = Namespace("http://example.org/actor/")

class MovieModel:
    def __init__(self):
        self.g = Graph()
        
        # Registrar namespaces
        self.g.bind("movie", MOVIE)
        self.g.bind("genre", GENRE)
        self.g.bind("director", DIRECTOR)
        self.g.bind("actor", ACTOR)
    
    def agregar_pelicula(self, titulo, anio, sinopsis, imagen_url):
        """Agrega una película al grafo RDF"""
        # Generar un ID único para la película basado en el título
        id = titulo.lower().replace(" ", "_").replace(":", "").replace("-", "_")
        pelicula_uri = URIRef(MOVIE + id)
        
        self.g.add((pelicula_uri, RDF.type, MOVIE.Movie))
        self.g.add((pelicula_uri, MOVIE.title, Literal(titulo, datatype=XSD.string)))
        self.g.add((pelicula_uri, MOVIE.year, Literal(anio, datatype=XSD.integer)))
        self.g.add((pelicula_uri, MOVIE.synopsis, Literal(sinopsis, datatype=XSD.string)))
        self.g.add((pelicula_uri, MOVIE.image, Literal(imagen_url, datatype=XSD.anyURI)))
        
        return pelicula_uri
    
    def agregar_genero(self, pelicula_uri, genero):
        """Asocia un género a una película"""
        genero_uri = URIRef(GENRE + genero.lower().replace(" ", "_"))
        
        self.g.add((genero_uri, RDF.type, MOVIE.Genre))
        self.g.add((genero_uri, RDFS.label, Literal(genero, datatype=XSD.string)))
        self.g.add((pelicula_uri, MOVIE.hasGenre, genero_uri))
    
    def agregar_director(self, pelicula_uri, nombre):
        """Asocia un director a una película"""
        director_id = nombre.lower().replace(" ", "_")
        director_uri = URIRef(DIRECTOR + director_id)
        
        self.g.add((director_uri, RDF.type, MOVIE.Director))
        self.g.add((director_uri, RDFS.label, Literal(nombre, datatype=XSD.string)))
        self.g.add((pelicula_uri, MOVIE.hasDirector, director_uri))
    
    def agregar_actor(self, pelicula_uri, nombre):
        """Asocia un actor a una película"""
        actor_id = nombre.lower().replace(" ", "_")
        actor_uri = URIRef(ACTOR + actor_id)
        
        self.g.add((actor_uri, RDF.type, MOVIE.Actor))
        self.g.add((actor_uri, RDFS.label, Literal(nombre, datatype=XSD.string)))
        self.g.add((pelicula_uri, MOVIE.hasActor, actor_uri))
    
    def agregar_calificacion(self, pelicula_uri, calificacion):
        """Agrega una calificación a una película (1-5)"""
        self.g.add((pelicula_uri, MOVIE.rating, Literal(calificacion, datatype=XSD.integer)))
    
    def obtener_todas_peliculas(self):
        """Obtiene todas las películas del grafo"""
        peliculas = []
        
        query = """
            SELECT ?id ?titulo ?anio ?imagen
            WHERE {
                ?id rdf:type movie:Movie .
                ?id movie:title ?titulo .
                ?id movie:year ?anio .
                ?id movie:image ?imagen .
            }
        """
        
        for row in self.g.query(query):
            pelicula = {
                'id': str(row.id).split('/')[-1],
                'titulo': str(row.titulo),
                'anio': int(row.anio),
                'imagen': str(row.imagen)
            }
            peliculas.append(pelicula)
            
        return peliculas
    
    def obtener_pelicula(self, id):
        """Obtiene los detalles de una película específica"""
        pelicula_uri = URIRef(MOVIE + id)
        
        # Datos básicos
        titulo = self.g.value(pelicula_uri, MOVIE.title)
        anio = self.g.value(pelicula_uri, MOVIE.year)
        sinopsis = self.g.value(pelicula_uri, MOVIE.synopsis)
        imagen = self.g.value(pelicula_uri, MOVIE.image)
        
        # Géneros
        generos = []
        for genero in self.g.objects(pelicula_uri, MOVIE.hasGenre):
            generos.append(str(self.g.value(genero, RDFS.label)))
        
        # Director
        directores = []
        for director in self.g.objects(pelicula_uri, MOVIE.hasDirector):
            directores.append(str(self.g.value(director, RDFS.label)))
            
        # Actores
        actores = []
        for actor in self.g.objects(pelicula_uri, MOVIE.hasActor):
            actores.append(str(self.g.value(actor, RDFS.label)))
            
        # Calificación
        calificacion = self.obtener_calificacion(id)
            
        return {
            'id': id,
            'titulo': str(titulo) if titulo else "",
            'anio': int(anio) if anio else 0,
            'sinopsis': str(sinopsis) if sinopsis else "",
            'imagen': str(imagen) if imagen else "",
            'generos': generos,
            'directores': directores,
            'actores': actores,
            'calificacion': calificacion
        }
        
    def recomendar_por_genero(self, genero_id):
        """Recomienda películas por género, considerando calificaciones"""
        genero_uri = URIRef(GENRE + genero_id)
        
        # Primero comprobamos si el género existe
        genero_existe = False
        for s, p, o in self.g.triples((genero_uri, RDF.type, MOVIE.Genre)):
            genero_existe = True
            break
            
        if not genero_existe:
            return []
        
        # Consulta mejorada que incluye calificaciones
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX movie: <http://example.org/movie/>
            PREFIX genre: <http://example.org/genre/>
            
            SELECT ?id ?titulo ?anio ?imagen ?rating
            WHERE {
                ?id rdf:type movie:Movie .
                ?id movie:title ?titulo .
                ?id movie:year ?anio .
                ?id movie:image ?imagen .
                ?id movie:hasGenre <""" + str(genero_uri) + """> .
                OPTIONAL {
                    ?id movie:rating ?rating .
                }
            }
        """
        
        peliculas = []
        results = self.g.query(query)
        
        for row in results:
            # Calcular calificación promedio
            calificaciones = []
            pelicula_uri = URIRef(str(row.id))
            for calificacion in self.g.objects(pelicula_uri, MOVIE.rating):
                calificaciones.append(int(calificacion))
            
            promedio_calificacion = sum(calificaciones) / len(calificaciones) if calificaciones else 0
            
            pelicula = {
                'id': str(row.id).split('/')[-1],
                'titulo': str(row.titulo),
                'anio': int(row.anio),
                'imagen': str(row.imagen),
                'calificacion_promedio': round(promedio_calificacion, 1),
                'total_votos': len(calificaciones)
            }
            peliculas.append(pelicula)
        
        # Ordenar por calificación promedio (de mayor a menor)
        peliculas.sort(key=lambda x: x['calificacion_promedio'], reverse=True)
        return peliculas

    def recomendar_por_generos(self, generos_ids):
        """Recomienda películas basadas en múltiples géneros y calificaciones"""
        if not generos_ids:
            return []
            
        # Construir la consulta para múltiples géneros
        generos_conditions = []
        for genero_id in generos_ids:
            genero_uri = URIRef(GENRE + genero_id)
            generos_conditions.append(f"?id movie:hasGenre <{genero_uri}>")
        
        generos_filter = " . ".join(generos_conditions)
        
        query = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX movie: <http://example.org/movie/>
            PREFIX genre: <http://example.org/genre/>
            
            SELECT ?id ?titulo ?anio ?imagen
            WHERE {{
                ?id rdf:type movie:Movie .
                ?id movie:title ?titulo .
                ?id movie:year ?anio .
                ?id movie:image ?imagen .
                {generos_filter}
            }}
        """
        
        peliculas = []
        results = self.g.query(query)
        
        for row in results:
            pelicula_uri = URIRef(str(row.id))
            
            # Obtener géneros de la película
            generos_pelicula = []
            for genero in self.g.objects(pelicula_uri, MOVIE.hasGenre):
                generos_pelicula.append(str(genero).split('/')[-1])
            
            # Calcular calificaciones
            calificaciones = []
            for calificacion in self.g.objects(pelicula_uri, MOVIE.rating):
                calificaciones.append(int(calificacion))
            
            promedio_calificacion = sum(calificaciones) / len(calificaciones) if calificaciones else 0
            
            # Calcular puntuación de relevancia
            # 1. Porcentaje de géneros coincidentes
            generos_coincidentes = len(set(generos_ids) & set(generos_pelicula))
            porcentaje_generos = generos_coincidentes / len(generos_ids)
            
            # 2. Factor de calificación (normalizado a 0-1)
            factor_calificacion = promedio_calificacion / 5.0
            
            # 3. Puntuación final (70% géneros, 30% calificación)
            puntuacion = (porcentaje_generos * 0.7) + (factor_calificacion * 0.3)
            
            pelicula = {
                'id': str(row.id).split('/')[-1],
                'titulo': str(row.titulo),
                'anio': int(row.anio),
                'imagen': str(row.imagen),
                'calificacion_promedio': round(promedio_calificacion, 1),
                'total_votos': len(calificaciones),
                'generos': generos_pelicula,
                'puntuacion_relevancia': round(puntuacion, 2)
            }
            peliculas.append(pelicula)
        
        # Ordenar por puntuación de relevancia
        peliculas.sort(key=lambda x: x['puntuacion_relevancia'], reverse=True)
        return peliculas
        
    def cargar_datos_muestra(self):
        """Carga datos de ejemplo para probar la aplicación"""
        # Película 1
        p1 = self.agregar_pelicula("inception", 2010, 
                                 "Un ladrón que roba secretos corporativos a través del uso de la tecnología de compartir sueños.",
                                 "inception")
        self.agregar_genero(p1, "Ciencia Ficción")
        self.agregar_genero(p1, "Acción")
        self.agregar_director(p1, "Christopher Nolan")
        self.agregar_actor(p1, "Leonardo DiCaprio")
        self.agregar_actor(p1, "Joseph Gordon-Levitt")
        self.agregar_calificacion(p1, 5)
        
        # Película 2
        p2 = self.agregar_pelicula("the_dark_knight", 2008,
                                 "Batman se enfrenta a una nueva amenaza: un criminal conocido como El Joker.",
                                 "the_dark_knight")
        self.agregar_genero(p2, "Acción")
        self.agregar_genero(p2, "Drama")
        self.agregar_director(p2, "Christopher Nolan")
        self.agregar_actor(p2, "Christian Bale")
        self.agregar_actor(p2, "Heath Ledger")
        self.agregar_calificacion(p2, 5)
        
        # Película 3
        p3 = self.agregar_pelicula("pulp_fiction", 1994,
                                 "Las vidas de dos mafiosos, un boxeador, la esposa de un gángster y un par de bandidos se entrelazan.",
                                 "pulp_fiction")
        self.agregar_genero(p3, "Drama")
        self.agregar_genero(p3, "Crimen")
        self.agregar_director(p3, "Quentin Tarantino")
        self.agregar_actor(p3, "John Travolta")
        self.agregar_actor(p3, "Uma Thurman")
        self.agregar_calificacion(p3, 5)
        
        # Película 4
        p4 = self.agregar_pelicula("interstellar", 2014,
                                 "Un grupo de exploradores viaja a través de un agujero de gusano en busca de un nuevo hogar para la humanidad.",
                                 "interstellar")
        self.agregar_genero(p4, "Ciencia Ficción")
        self.agregar_genero(p4, "Aventura")
        self.agregar_director(p4, "Christopher Nolan")
        self.agregar_actor(p4, "Matthew McConaughey")
        self.agregar_actor(p4, "Anne Hathaway")
        self.agregar_calificacion(p4, 5)
        
        # Película 5
        p5 = self.agregar_pelicula("coco", 2017,
                                 "Miguel sueña con ser un músico pero su familia lo prohíbe. Desesperado por demostrar su talento, se encuentra en la Tierra de los Muertos.",
                                 "coco")
        self.agregar_genero(p5, "Animación")
        self.agregar_genero(p5, "Aventura")
        self.agregar_genero(p5, "Familiar")
        self.agregar_director(p5, "Lee Unkrich")
        self.agregar_director(p5, "Adrian Molina")
        self.agregar_actor(p5, "Anthony Gonzalez")
        self.agregar_actor(p5, "Gael García Bernal")
        self.agregar_calificacion(p5, 5)

        # Película 6
        p6 = self.agregar_pelicula("parasite", 2019,
                                 "Una familia pobre idea un plan para infiltrarse como empleados en el hogar de una familia rica.",
                                 "parasite")
        self.agregar_genero(p6, "Drama")
        self.agregar_genero(p6, "Thriller")
        self.agregar_genero(p6, "Comedy")
        self.agregar_director(p6, "Bong Joon Ho")
        self.agregar_actor(p6, "Song Kang-ho")
        self.agregar_actor(p6, "Lee Sun-kyun")
        self.agregar_actor(p6, "Choi Woo-sik")
        self.agregar_actor(p6, "Park So-dam")
        self.agregar_calificacion(p6, 5)

        # Película 7
        p7 = self.agregar_pelicula("spider_man_into_the_spider_verse", 2018,
                                 "Miles Morales se convierte en el Spider-Man de su realidad y se une a otros Spider-People de diferentes dimensiones para detener una amenaza para todas las realidades.",
                                 "spider_man_into_the_spider_verse")
        self.agregar_genero(p7, "Animación")
        self.agregar_genero(p7, "Acción")
        self.agregar_genero(p7, "Aventura")
        self.agregar_genero(p7, "Ciencia Ficción")
        self.agregar_director(p7, "Peter Ramsey")
        self.agregar_actor(p7, "Shameik Moore")
        self.agregar_actor(p7, "Hailee Steinfeld")
        self.agregar_actor(p7, "Mahershala Ali")
        self.agregar_calificacion(p7, 5)

        # Película 8
        p8 = self.agregar_pelicula("arrival", 2016,
                                 "Un experto lingüista es reclutado por el ejército para ayudar a determinar si los extraterrestres recién llegados vienen en paz o son una amenaza.",
                                 "arrival")
        self.agregar_genero(p8, "Ciencia Ficción")
        self.agregar_genero(p8, "Drama")
        self.agregar_genero(p8, "Misterio")
        self.agregar_director(p8, "Denis Villeneuve")
        self.agregar_actor(p8, "Amy Adams")
        self.agregar_actor(p8, "Jeremy Renner")
        self.agregar_actor(p8, "Forest Whitaker")
        self.agregar_calificacion(p8, 5)

    def obtener_calificacion(self, id):
        """Obtiene la calificación actual de una película"""
        pelicula_uri = URIRef(MOVIE + id)
        
        # Obtener todas las calificaciones
        calificaciones = []
        for calificacion in self.g.objects(pelicula_uri, MOVIE.rating):
            calificaciones.append(int(calificacion))
        
        # Calcular el promedio si hay calificaciones
        if calificaciones:
            promedio = sum(calificaciones) / len(calificaciones)
            return {
                'promedio': round(promedio, 1),
                'total_votos': len(calificaciones)
            }
        else:
            return {
                'promedio': 0,
                'total_votos': 0
            }

    def buscar_peliculas_por_texto(self, query_texto):
        """Busca películas por título o sinopsis usando texto libre"""
        if not query_texto:
            return []
            
        # Escapar caracteres especiales en la consulta de texto para la regex SPARQL
        # Aunque regex en SPARQL es más flexible, es bueno ser precavido.
        # Por ahora, asumiremos que la entrada de texto no contiene caracteres SPARQL regex problemáticos
        # y nos enfocaremos en la estructura de la consulta.
        
        query = f"""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX movie: <http://example.org/movie/>
            
            SELECT ?id ?titulo ?anio ?imagen
            WHERE {{
                ?id rdf:type movie:Movie .
                ?id movie:title ?titulo .
                ?id movie:year ?anio .
                ?id movie:image ?imagen .
                OPTIONAL {{ ?id movie:synopsis ?sinopsis . }}
                
                FILTER (regex(str(?titulo), '{query_texto}', "i") || 
                        (BOUND(?sinopsis) && regex(str(?sinopsis), '{query_texto}', "i")))
            }}
        """
        
        peliculas = []
        try:
            results = self.g.query(query)
            for row in results:
                 # Aquí podrías obtener más detalles como géneros, directores, etc. si fuera necesario mostrar en los resultados de búsqueda
                pelicula = {
                    'id': str(row.id).split('/')[-1],
                    'titulo': str(row.titulo),
                    'anio': int(row.anio),
                    'imagen': str(row.imagen),
                    # Puedes añadir calificación promedio si quieres mostrarla en los resultados de búsqueda
                    'calificacion': self.obtener_calificacion(str(row.id).split('/')[-1])
                }
                peliculas.append(pelicula)
                
            # Opcional: ordenar resultados por algún criterio, por ahora no lo haremos
        except Exception as e:
            print(f"Error ejecutando la consulta SPARQL: {e}")
            # Puedes loggear el error o manejarlo de otra manera
            pass # Continuar con lista vacía si hay error

        return peliculas 