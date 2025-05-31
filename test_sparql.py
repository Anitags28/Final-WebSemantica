from SPARQLWrapper import SPARQLWrapper, JSON

# URL del endpoint de consultas SPARQL de tu dataset Fuseki
fuseki_url = "http://localhost:3030/peliculas/sparql"

sparql = SPARQLWrapper(fuseki_url)
sparql.setQuery("""
    SELECT * WHERE {
        ?s ?p ?o
    } LIMIT 5
""")
sparql.setReturnFormat(JSON)

results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(f"{result['s']['value']} -- {result['p']['value']} -- {result['o']['value']}")

