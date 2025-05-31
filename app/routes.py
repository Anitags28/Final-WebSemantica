from flask import Blueprint, jsonify
from app.rdf_loader import cargar_datos
from app.sparql_client import obtener_peliculas

bp = Blueprint('main', __name__)

@bp.route('/cargar')
def cargar():
    cargar_datos()
    return "Datos RDF cargados en Fuseki."

@bp.route('/peliculas')
def mostrar_peliculas():
    peliculas = obtener_peliculas()
    return jsonify(peliculas)
