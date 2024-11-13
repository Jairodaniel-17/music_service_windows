import os


class SongRepository:
    def __init__(self):
        self.music_path = os.path.join(os.getcwd(), "music")
        self.static_path = os.path.join(os.getcwd(), "static")
        self.image_path = os.path.join(self.static_path, "img")
        self.temp_path = os.path.join(os.getcwd(), "temp")

    def lista_de_canciones(self):
        songs = os.listdir(self.music_path)
        return {"songs": songs}
