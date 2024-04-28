import os
import re
from flask import Flask, abort, request, send_from_directory, render_template
from werkzeug.utils import secure_filename
from pytube import YouTube
import unicodedata
import requests
import zipfile
import webbrowser
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Verificar que existen las 4 carpetas necesarias
for folder in ["music", "static", "static/img", "temp"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Carpeta donde guardar las canciones
music_path = os.path.join(os.getcwd(), "music")
static_path = os.path.join(os.getcwd(), "static")
image_path = os.path.join(os.getcwd(), "static/img")
temp_path = os.path.join(os.getcwd(), "temp")


# CORS
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


def lista_de_canciones():
    songs = os.listdir(music_path)
    return {"songs": songs}


@app.route("/")
def root():
    """
    Manejador para el punto de entrada raíz.

    Returns:
        TemplateResponse: La respuesta que contiene la plantilla index.html renderizada.
    """
    # Retorna un diccionario con las canciones, escoger la key "songs"
    canciones = lista_de_canciones()
    # Mensaje de bienvenida en la página principal
    bienvenida = "Bienvenido querido usuario, puedes descargar y escuchar tus canciones de YouTube"
    return render_template(
        "index.html", songs=canciones["songs"], bienvenida=bienvenida
    )


# Prueba con test.html
@app.route("/test")
def test():
    # Retorna un diccionario con las canciones, escoger la key "songs"
    canciones = lista_de_canciones()
    # Mensaje de bienvenida en la página principal
    bienvenida = "Bienvenido mi estimado, aquí puedes descargar y escuchar tus canciones favoritas de YouTube"
    return render_template(
        "index.html", songs=canciones["songs"], bienvenida=bienvenida
    )


# Cambia la ruta de POST a GET
@app.route("/downloadSong/<string:song_name>")
def download_song_by_name(song_name):
    try:
        # Verificar que el archivo exista en la carpeta de música
        song_path = os.path.join(music_path, f"{song_name}.mp3")
        if not os.path.exists(song_path):
            abort(404, f"Canción no encontrada: {song_name}")

        # Devolver el archivo de la canción en modo descarga
        return send_from_directory(music_path, f"{song_name}.mp3", as_attachment=True)

    except Exception as e:
        abort(500, f"Error al descargar la canción: {str(e)}")


def save_img_change_name(titulo, logo):
    titulo_normalizado = unicodedata.normalize("NFKD", titulo)
    # Limpiar el título para usarlo como nombre de archivo
    caracteres_no_permitidos = r"[\"\'/\\:*?<>|,]"
    titulo_limpio = re.sub(caracteres_no_permitidos, "", titulo_normalizado)
    print(titulo_limpio)
    response = requests.get(logo)
    new_name = f"{titulo_limpio}.jpg"
    with open(os.path.join(temp_path, new_name), "wb") as file:
        file.write(response.content)
    return titulo_limpio


class Item:
    def __init__(self, url):
        self.url = url


@app.route("/download", methods=["GET"])
def download_song():
    return {"Api status": "OK"}


# Ruta de descarga de la canción alternativa con mejoras
@app.route("/download", methods=["POST"])
def download_song_two():
    try:
        data = request.json
        item = Item(url=data["url"])

        # Limpiar temporal
        for file in os.listdir(temp_path):
            os.remove(os.path.join(temp_path, file))
        # Obtener la URL de la canción
        url = item.url
        # Obtener el título de la canción
        yt = YouTube(url)
        titulo = yt.title
        # Descargar la canción en la carpeta temp
        yt.streams.filter(only_audio=True).first().download(temp_path)
        # Descargar el logo de la canción (imagen) en la carpeta temp
        logo = yt.thumbnail_url
        new_name = save_img_change_name(titulo, logo)
        # Buscar el archivo descargado en la carpeta temp
        for file in os.listdir(temp_path):
            if file.endswith(".mp4"):
                # Cambiar el nombre de la canción descargada en la carpeta temp
                os.rename(
                    os.path.join(temp_path, file),
                    os.path.join(temp_path, f"{new_name}.mp4"),
                )
        # Convertir a mp3
        for file in os.listdir(temp_path):
            if file.endswith(".mp4"):
                os.rename(
                    os.path.join(temp_path, file),
                    os.path.join(temp_path, file.replace(".mp4", ".mp3")),
                )
        # Mover la canción descargada a la carpeta music
        os.rename(
            os.path.join(temp_path, f"{new_name}.mp3"),
            os.path.join(music_path, f"{new_name}.mp3"),
        )
        # Mover la imagen descargada a la carpeta img
        os.rename(
            os.path.join(temp_path, f"{new_name}.jpg"),
            os.path.join(image_path, f"{new_name}.jpg"),
        )
        return {"message": new_name}

    except Exception as e:
        abort(500, f"Error al descargar la canción: {str(e)}")


def zip_files(zip_filename, source_dirs, arcname_prefix=""):
    with zipfile.ZipFile(zip_filename, "w") as zipf:
        for source_dir in source_dirs:
            for root, _, files in os.walk(source_dir):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), source_dir)
                    arcname = (
                        os.path.join(arcname_prefix, rel_path)
                        if arcname_prefix
                        else rel_path
                    )
                    zipf.write(os.path.join(root, file), arcname=arcname)


# Ruta para descargar todas las canciones y logotipos en un archivo ZIP
@app.route("/download-all")
def download_all():
    try:
        # Crear un archivo ZIP temporal
        zip_filename = os.path.join(temp_path, "songs_and_logos.zip")

        # Comprimir canciones y logotipos en el archivo ZIP
        zip_files(zip_filename, [music_path, image_path], arcname_prefix="")

        # Devolver el archivo ZIP como respuesta
        return send_from_directory(temp_path, "songs_and_logos.zip", as_attachment=True)
    except Exception as e:
        abort(500, f"Error al crear el archivo ZIP: {str(e)}")


# poner disponible el contenido de la carpeta music y static/img
@app.route("/music/<path:filename>")
def music(filename):
    return send_from_directory(music_path, filename)


@app.route("/static/img/<path:filename>")
def img(filename):
    return send_from_directory(image_path, filename)


if __name__ == "__main__":
    app.run(host="localhost", port=50000)

# pyinstaller --onefile --windowed --add-data "static;static" --add-data "templates;templates" --ico=icon.ico app.py
# pyinstaller --onefile --windowed --add-data "static:static" --add-data "templates:templates" --icon=ico.ico app.py
