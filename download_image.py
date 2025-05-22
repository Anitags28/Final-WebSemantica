import requests
import os

# URLs de las imágenes y nombres de archivo locales correspondientes
IMAGENES_INFO = {
    "inception": {"url": "https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg", "filename": "inception.jpg"},
    "the_dark_knight": {"url": "https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg", "filename": "the_dark_knight.jpg"},
    "pulp_fiction": {"url": "https://m.media-amazon.com/images/M/MV5BNGNhMDIzZTUtNTBlZi00MTRlLWFjM2ItYzViMjE3YzI5MjljXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg", "filename": "pulp_fiction.jpg"},
    "interstellar": {"url": "https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg", "filename": "interstellar.jpg"},
    "coco": {"url": "https://m.media-amazon.com/images/M/MV5BYjQ5NjM0Y2YtNjZkNC00ZDhkLWJjMWItN2QyNzFkMDE3ZjAxXkEyXkFqcGdeQXVyODIxMzk5NjA@._V1_FMjpg_UX1000_.jpg", "filename": "coco.jpg"},
    "parasite": {"url": "http://www.impawards.com/intl/south_korea/2019/posters/parasite_xlg.jpg", "filename": "parasite.jpg"},
    "spider_man_into_the_spider_verse": {"url": "https://image.tmdb.org/t/p/original/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg", "filename": "spider_man_into_the_spider_verse.jpg"},
    "arrival": {"url": "http://www.impawards.com/2016/posters/arrival_ver15_xlg.jpg", "filename": "arrival.jpg"}
}

def download_images():
    # Crear el directorio si no existe
    os.makedirs("static/images", exist_ok=True)
    
    # Descargar cada imagen
    for movie_id, info in IMAGENES_INFO.items():
        url = info["url"]
        filename = info["filename"]
        filepath = os.path.join("static/images", filename)
        
        # Verificar si el archivo ya existe
        if os.path.exists(filepath):
            print(f"La imagen para {movie_id} ya existe ({filename}). Saltando descarga.")
            continue
            
        try:
            print(f"Descargando imagen para {movie_id} desde {url}...")
            response = requests.get(url, stream=True)
            response.raise_for_status() # Lanzar una excepción para códigos de estado erróneos
            
            # Guardar la imagen en chunks
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Imagen para {movie_id} descargada exitosamente como {filename}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error al descargar la imagen para {movie_id} desde {url}: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado al descargar la imagen para {movie_id}: {e}")

if __name__ == "__main__":
    download_images() 