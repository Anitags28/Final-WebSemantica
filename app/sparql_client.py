from SPARQLWrapper import SPARQLWrapper, JSON

def obtener_peliculas():
    endpoint = "http://localhost:3030/peliculas/query"
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery("""
        PREFIX ex: <http://example.org/movie/>

        SELECT ?titulo ?director ?anio ?genero WHERE {
            ?pelicula a ex:Movie ;
                      ex:title ?titulo ;
                      ex:director ?director ;
                      ex:year ?anio ;
                      ex:genre ?genero .
        }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    peliculas = []
    for result in results["results"]["bindings"]:
        peliculas.append({
            "titulo": result["titulo"]["value"],
            "director": result["director"]["value"],
            "anio": result["anio"]["value"],
            "genero": result["genero"]["value"]
        })

    return peliculas
