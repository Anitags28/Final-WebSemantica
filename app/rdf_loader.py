# rdf_loader.py
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, XSD
import requests

EX = Namespace("http://example.org/movie/")

def cargar_datos():
    g = Graph()
    g.bind("ex", EX)

    # Película de ejemplo
    pelicula = URIRef(EX["inception"])
    g.add((pelicula, RDF.type, EX.Movie))
    g.add((pelicula, EX.title, Literal("Inception", datatype=XSD.string)))
    g.add((pelicula, EX.director, Literal("Christopher Nolan", datatype=XSD.string)))
    g.add((pelicula, EX.year, Literal(2010, datatype=XSD.gYear)))
    g.add((pelicula, EX.genre, Literal("Sci-Fi", datatype=XSD.string)))

    data = g.serialize(format='turtle')

    fuseki_url = "http://localhost:3030/peliculas/data"
    headers = {"Content-Type": "text/turtle"}

    response = requests.post(fuseki_url, data=data, headers=headers)

    if response.status_code == 200:
        print("✅ Datos cargados exitosamente en Fuseki.")
    else:
        print("❌ Error al cargar datos:", response.status_code)
        print(response.text)
