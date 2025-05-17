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
    
    def agregar_pelicula(self, id, titulo, anio, sinopsis, imagen_url):
        """Agrega una película al grafo RDF"""
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
        """Recomienda películas por género"""
        genero_uri = URIRef(GENRE + genero_id)
        
        # Primero comprobamos si el género existe
        genero_existe = False
        for s, p, o in self.g.triples((genero_uri, RDF.type, MOVIE.Genre)):
            genero_existe = True
            break
            
        if not genero_existe:
            return []
        
        # Preparar consulta con prefijos explícitos
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX movie: <http://example.org/movie/>
            PREFIX genre: <http://example.org/genre/>
            
            SELECT ?id ?titulo ?anio ?imagen
            WHERE {
                ?id rdf:type movie:Movie .
                ?id movie:title ?titulo .
                ?id movie:year ?anio .
                ?id movie:image ?imagen .
                ?id movie:hasGenre <""" + str(genero_uri) + """> .
            }
        """
        
        peliculas = []
        results = self.g.query(query)
        
        for row in results:
            pelicula = {
                'id': str(row.id).split('/')[-1],
                'titulo': str(row.titulo),
                'anio': int(row.anio),
                'imagen': str(row.imagen)
            }
            peliculas.append(pelicula)
            
        return peliculas
        
    def cargar_datos_muestra(self):
        """Carga datos de ejemplo para probar la aplicación"""
        # Película 1
        p1 = self.agregar_pelicula("inception", "Inception", 2010, 
                                 "Un ladrón que roba secretos corporativos a través del uso de la tecnología de compartir sueños.",
                                 "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg")
        self.agregar_genero(p1, "Ciencia Ficción")
        self.agregar_genero(p1, "Acción")
        self.agregar_director(p1, "Christopher Nolan")
        self.agregar_actor(p1, "Leonardo DiCaprio")
        self.agregar_actor(p1, "Joseph Gordon-Levitt")
        self.agregar_calificacion(p1, 5)
        
        # Película 2
        p2 = self.agregar_pelicula("the_dark_knight", "The Dark Knight", 2008,
                                 "Batman se enfrenta a una nueva amenaza: un criminal conocido como El Joker.",
                                 "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg")
        self.agregar_genero(p2, "Acción")
        self.agregar_genero(p2, "Drama")
        self.agregar_director(p2, "Christopher Nolan")
        self.agregar_actor(p2, "Christian Bale")
        self.agregar_actor(p2, "Heath Ledger")
        self.agregar_calificacion(p2, 5)
        
        # Película 3
        p3 = self.agregar_pelicula("pulp_fiction", "Pulp Fiction", 1994,
                                 "Las vidas de dos mafiosos, un boxeador, la esposa de un gángster y un par de bandidos se entrelazan.",
                                 "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg")
        self.agregar_genero(p3, "Drama")
        self.agregar_genero(p3, "Crimen")
        self.agregar_director(p3, "Quentin Tarantino")
        self.agregar_actor(p3, "John Travolta")
        self.agregar_actor(p3, "Uma Thurman")
        self.agregar_calificacion(p3, 5)
        
        # Película 4
        p4 = self.agregar_pelicula("interstellar", "Interstellar", 2014,
                                 "Un grupo de exploradores viaja a través de un agujero de gusano en busca de un nuevo hogar para la humanidad.",
                                 "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg")
        self.agregar_genero(p4, "Ciencia Ficción")
        self.agregar_genero(p4, "Aventura")
        self.agregar_director(p4, "Christopher Nolan")
        self.agregar_actor(p4, "Matthew McConaughey")
        self.agregar_actor(p4, "Anne Hathaway")
        self.agregar_calificacion(p4, 5)
        
        # Película 5
        p5 = self.agregar_pelicula("coco", "Coco", 2017,
                                 "Miguel sueña con ser un músico pero su familia lo prohíbe. Desesperado por demostrar su talento, se encuentra en la Tierra de los Muertos.",
                                 "https://m.media-amazon.com/images/M/MV5BYjQ5NjM0Y2YtNjZkNC00ZDhkLWJjMWItN2QyNzFkMDE3ZjAxXkEyXkFqcGdeQXVyODIxMzk5NjA@._V1_FMjpg_UX1000_.jpg")
        self.agregar_genero(p5, "Animación")
        self.agregar_genero(p5, "Aventura")
        self.agregar_genero(p5, "Familiar")
        self.agregar_director(p5, "Lee Unkrich")
        self.agregar_director(p5, "Adrian Molina")
        self.agregar_actor(p5, "Anthony Gonzalez")
        self.agregar_actor(p5, "Gael García Bernal")
        self.agregar_calificacion(p5, 5)
    
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