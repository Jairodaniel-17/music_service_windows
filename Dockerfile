# Usamos una imagen base de Python
FROM python:3.9-slim

# Instalamos las dependencias necesarias, como ffmpeg
RUN apt-get update && \
    apt-get install -y \
    ffmpeg \
    libsndfile1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo requirements.txt al contenedor
COPY requirements.txt /app/

# Instalamos las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código de la aplicación al contenedor
COPY . /app/

# Asignamos permisos a todos los archivos y directorios
RUN chmod -R 755 /app

# Exponemos el puerto en el que la app de Flask se ejecutará
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["python", "app.py"]
