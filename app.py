from flask import Flask
from flask_cors import CORS
from routers.music_routes import music_bp
from routers.download_routes import download_bp
from routers.image_routes import image_bp
import os

# crear los directorios necesarios
directories = ["music", "static", "static/img", "temp"]
for directory in directories:
    if not os.path.exists(directory):
        os.makedirs(directory)

app = Flask(__name__)
CORS(app)

# Registramos los blueprints
app.register_blueprint(music_bp)
app.register_blueprint(download_bp)
app.register_blueprint(image_bp)


# Configuramos CORS
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
