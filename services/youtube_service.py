import os
import yt_dlp as youtube_dl
from repositories.song_repository import SongRepository
from services.file_service import FileService


class YouTubeService:
    def __init__(self):
        self.file_service = FileService()
        self.song_repository = SongRepository()

    def download_song(self, url, max_songs=1) -> str:
        """
        Descarga la canción de YouTube y la guarda en la carpeta de música.
        :param url: URL del video de YouTube.
        :param max_songs: Número máximo de canciones a descargar.
        :return: Mensaje de éxito.
        """
        try:
            ydl_opts = {
                "format": "m4a/bestaudio/best",
                "outtmpl": os.path.join(self.song_repository.temp_path, "%(title)s.%(ext)s"),
                "playlistend": max_songs,
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)

            if "entries" in info_dict:
                for entry in info_dict.get("entries", []):
                    self._process_video(entry, info_dict)
            else:
                self._process_video(info_dict)

            return "Se descargó la canción: " + info_dict.get("title")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            raise Exception(f"Error inesperado: {str(e)}")

    def _process_video(self, entry, info_dict=None):
        """
        Procesa el archivo de audio y la miniatura del video.
        """
        titulo = entry.get("title", None)
        safe_name = self.file_service.clean_filename(titulo)
        original_file_path = os.path.join(self.song_repository.temp_path, f"{titulo}.m4a")
        file_path = os.path.join(self.song_repository.temp_path, f"{safe_name}.m4a")

        try:
            os.rename(original_file_path, file_path)
            self.process_thumbnail_and_move_file(entry, info_dict, safe_name, file_path)

        except Exception as e:
            print(f"Error inesperado al procesar el archivo: {str(e)}")

            try:
                safe_file_name = None
                safe_file_path = None
                for filename in os.listdir(self.song_repository.temp_path):
                    if filename.endswith(".m4a"):
                        original_file_path = os.path.join(self.song_repository.temp_path, filename)
                        safe_file_name = self.file_service.clean_filename(filename)
                        safe_file_path = os.path.join(self.song_repository.temp_path, f"{safe_file_name}.m4a")
                        os.rename(original_file_path, safe_file_path)
                        break

                if safe_file_name and safe_file_path:
                    self.process_thumbnail_and_move_file(entry, info_dict, safe_file_name, safe_file_path)
                else:
                    print("No se pudo encontrar un archivo m4a para renombrar.")

            except Exception as rename_error:
                print(f"Error al renombrar archivo .m4a: {str(rename_error)}")
                print("Limpiando carpeta temporal...")
                for filename in os.listdir(self.song_repository.temp_path):
                    file_path = os.path.join(self.song_repository.temp_path, filename)
                    try:
                        os.remove(file_path)
                        print(f"Archivo eliminado: {file_path}")
                    except Exception as delete_error:
                        print(f"Error al eliminar archivo {file_path}: {str(delete_error)}")

                raise Exception("No se pudo procesar el archivo después de intentar renombrar y limpiar la carpeta temporal.")

    def process_thumbnail_and_move_file(self, entry, info_dict, safe_name, file_path):
        """
        Procesa la miniatura del video (si existe) y mueve el archivo renombrado a la carpeta de música.
        """
        safe_name = self.file_service.clean_filename(safe_name)
        logo = entry.get("thumbnail", None)
        if not logo and info_dict:
            logo = info_dict.get("thumbnail", None)

        if logo:
            self.file_service.save_img_change_name(safe_name, logo)
        else:
            print("No se encontró miniatura para este video.")

        mp3_path = os.path.join(self.song_repository.music_path, f"{safe_name}.mp3")
        if os.path.exists(file_path):
            os.rename(file_path, mp3_path)
            print(f"Archivo {safe_name}.m4a renombrado a .mp3 y guardado en {mp3_path}")
        else:
            # print(f"Error: El archivo {file_path} no se encontró.")
            raise FileNotFoundError(f"El archivo de audio {file_path} no fue encontrado.")
