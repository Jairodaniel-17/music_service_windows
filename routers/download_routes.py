from flask import Blueprint, request, abort, send_from_directory
from services.youtube_service import YouTubeService
from services.zip_service import ZipService
from repositories.song_repository import SongRepository
import os

download_bp = Blueprint("download", __name__)

# Instancias de servicios
youtube_service = YouTubeService()
zip_service = ZipService()
song_repository = SongRepository()


@download_bp.route("/download", methods=["POST"])
def download_song():
    try:
        data = request.json
        if "url" not in data:
            abort(400, "URL no proporcionada")

        new_name = youtube_service.download_song(data["url"])
        return {"message": new_name}
    except Exception as e:
        abort(500, f"Error al descargar la canción: {str(e)}")


@download_bp.route("/download-all")
def download_all():
    try:
        zip_filename = zip_service.create_zip(
            [song_repository.music_path, song_repository.image_path]
        )
        return send_from_directory(
            song_repository.temp_path, zip_filename, as_attachment=True
        )
    except Exception as e:
        abort(500, f"Error al crear el archivo ZIP: {str(e)}")


@download_bp.route("/downloadSong/<string:song_name>")
def download_song_by_name(song_name):
    try:

        song_path = os.path.join(song_repository.music_path, f"{song_name}.mp3")
        if not os.path.exists(song_path):
            abort(404, f"Canción no encontrada: {song_name}")

        return send_from_directory(
            song_repository.music_path, f"{song_name}.mp3", as_attachment=True
        )

    except Exception as e:
        abort(500, f"Error al descargar la canción: {str(e)}")
