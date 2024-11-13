from flask import Blueprint, render_template, send_from_directory
from repositories.song_repository import SongRepository

music_bp = Blueprint("music", __name__)

# Servicio de repositorio
song_repository = SongRepository()


@music_bp.route("/")
def root():
    canciones = song_repository.lista_de_canciones()
    bienvenida = "Bienvenido querido usuario, puedes descargar y escuchar tus canciones de YouTube"
    return render_template(
        "index.html", songs=canciones["songs"], bienvenida=bienvenida
    )


@music_bp.route("/music/<path:filename>")
def music(filename):
    return send_from_directory(song_repository.music_path, filename)
