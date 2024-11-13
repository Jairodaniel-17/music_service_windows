import zipfile
import os
from repositories.song_repository import SongRepository


class ZipService:
    def __init__(self):
        self.song_repository = SongRepository()

    def create_zip(self, source_dirs):
        zip_filename = os.path.join(
            self.song_repository.temp_path, "songs_and_logos.zip"
        )
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for source_dir in source_dirs:
                for root, _, files in os.walk(source_dir):
                    for file in files:
                        arcname = os.path.relpath(os.path.join(root, file), source_dir)
                        zipf.write(os.path.join(root, file), arcname=arcname)
        return "songs_and_logos.zip"
