from flask import Blueprint, send_from_directory
from repositories.song_repository import SongRepository

image_bp = Blueprint("image", __name__)
song_repository = SongRepository()


@image_bp.route("/static/img/<path:filename>")
def img(filename):
    return send_from_directory(song_repository.image_path, filename)
