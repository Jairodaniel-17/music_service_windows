import os
import re

import requests
import unicodedata
import subprocess
from repositories.song_repository import SongRepository


class FileService:
    def __init__(self):
        self.song_repository = SongRepository()

    def save_img_change_name(self, title, logo):
        """
        Guarda la imagen de miniatura del video de YouTube con un nombre seguro.
        """
        clean_title = self.clean_filename(
            title
        )
        response = requests.get(logo)
        img_path = os.path.join(self.song_repository.image_path, f"{clean_title}.jpg")
        with open(img_path, "wb") as file:
            file.write(response.content)
        return clean_title

    def clean_filename(self, title) -> str:
        """
        Limpia el nombre del archivo reemplazando caracteres no permitidos por otros válidos.
        """
        title_normalized = unicodedata.normalize("NFKD", title)
        forbidden_chars = r"[\"\'/\\:*?<>|,]"
        clean_title = re.sub(forbidden_chars, "", title_normalized)
        clean_title = re.sub(
            r"\s+", "_", clean_title
        )
        clean_title = re.sub(
            r"[^\w\s-]", "", clean_title
        )
        clean_title = re.sub(r"_", " ", clean_title)
        # Limitar la longitud del nombre del archivo para evitar problemas con el sistema de archivos
        max_length = 255
        if len(clean_title) > max_length:
            clean_title = clean_title[
                          :max_length
                          ]

        final_path = os.path.join(self.song_repository.temp_path, clean_title + ".m4a")
        if len(final_path) > 260:
            clean_title = clean_title[
                          : max_length - 10
                          ]
        # quitar m4a del final del nombre del archivo
        clean_title = clean_title.replace("m4a", "")
        return clean_title

    def convert_to_mp3(self, title):
        """
        Convierte el archivo de audio de su formato original a mp3 usando ffmpeg.
        """
        clean_title = self.clean_filename(title)
        temp_path = os.path.join(
            self.song_repository.temp_path, f"{clean_title}.m4a"
        )
        mp3_path = os.path.join(self.song_repository.music_path, f"{clean_title}.mp3")
        if os.path.exists(temp_path):
            if not os.path.exists(mp3_path):
                # Usamos ffmpeg para convertir a mp3
                try:
                    subprocess.run(
                        [
                            "ffmpeg",
                            "-i",
                            temp_path,
                            "-vn",
                            "-ar",
                            "44100",
                            "-ac",
                            "2",
                            "-b:a",
                            "192k",
                            mp3_path,
                        ],
                        check=True,
                    )
                    print(f"Archivo convertido y guardado en {mp3_path}")
                except subprocess.CalledProcessError as e:
                    raise Exception(f"Error al convertir el archivo: {e}")
            else:
                print(f"El archivo MP3 ya existe: {mp3_path}")
        else:
            raise FileNotFoundError(
                f"No se encontró el archivo de audio en {temp_path}"
            )

