# test_models.py
import unittest
from rdflib.namespace import RDF, XSD
from rdflib import Literal
from model import crear_pelicula, EX
class TestModeloPeliculas(unittest.TestCase):
    def test_crear_pelicula(self):
        titulo = "Matrix"
        director = "Lana Wachowski"
        año = 1999
        genero = "Action"

        g = crear_pelicula(titulo, director, año, genero)

        uri = EX["matrix"]
        self.assertIn((uri, RDF.type, EX.Movie), g)
        self.assertIn((uri, EX.title, Literal(titulo, datatype=XSD.string)), g)
        self.assertIn((uri, EX.director, Literal(director, datatype=XSD.string)), g)
        self.assertIn((uri, EX.year, Literal(año, datatype=XSD.gYear)), g)
        self.assertIn((uri, EX.genre, Literal(genero, datatype=XSD.string)), g)

if __name__ == '__main__':
    unittest.main()
