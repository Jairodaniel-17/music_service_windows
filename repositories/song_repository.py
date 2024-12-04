import os
from threading import Lock

from flask.cli import load_dotenv

load_dotenv()

path = os.getenv("MUSIC_PATH")


class SingletonMeta(type):
    """
    Metaclase para implementar el patrón Singleton.
    """

    _instances = {}
    _lock = Lock()  # Para asegurar el acceso seguro en un entorno de subprocesos.

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                # Crea una instancia si no existe.
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class SongRepository(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, "initialized"):  # Evita reinitialización si ya existe.
            self.music_path = os.path.join(os.getcwd(), "music")
            self.static_path = os.path.join(os.getcwd(), "static")
            self.image_path = os.path.join(self.static_path, "img")
            self.temp_path = os.path.join(os.getcwd(), "temp")
            self.initialized = True

    def lista_de_canciones(self):
        try:
            songs = os.listdir(self.music_path)
            return {"songs": songs}
        except FileNotFoundError:
            return {"error": "La carpeta de música no existe."}
