# Usamos una imagen base de Python
FROM python:3.11-slim

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

# Copiamos los archivos necesarios al contenedor
COPY . /app

# Copiar las carpetas 'music' y 'static/img' dentro del contenedor
COPY music /app/music
COPY static/img /app/static/img

# Instalamos las dependencias de Python dentro del contenedor
RUN pip install --no-cache-dir -r requirements.txt

#todos los permisos
RUN chmod -R 777 /app

# Exponemos el puerto 5000
EXPOSE 5000

# Establecemos el comando para ejecutar la aplicación de Flask
CMD ["python", "app.py"]
