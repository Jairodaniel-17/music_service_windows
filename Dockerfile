# Usamos una imagen base de Python
FROM python:3.9-slim

# Instalamos las dependencias necesarias, como ffmpeg y git
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    libsndfile1 \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Clonamos el repositorio de GitHub
RUN git clone https://github.com/Jairodaniel-17/music_service_windows.git /app

# Nos aseguramos de estar dentro del directorio del repositorio
WORKDIR /app

# Instalamos las dependencias de Python dentro del contenedor
RUN pip install --no-cache-dir -r requirements.txt

# Exponemos el puerto en el que la app de Flask se ejecutará
EXPOSE 51000

# Establecemos el comando para ejecutar la aplicación de Flask
CMD ["python", "app.py"]
