import win32.lib.win32serviceutil as win32serviceutil
import win32.win32service as win32service
import win32.win32event as win32event
import win32.servicemanager as servicemanager
import socket
import os
import time


class FlaskAppServiceMusic(win32serviceutil.ServiceFramework):
    _svc_name_ = "FlaskMusicService"
    _svc_display_name_ = "Flask Music Service"
    _svc_description_ = "Servicio para escuchar musica en el navegador de forma local, permite descargar musica de youtubea través de una API en Flask."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.stop_requested = False
        self.log("Servicio inicializado.")

    def log(self, msg):
        servicemanager.LogInfoMsg(str(msg))

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.log("Servicio detenido.")
        win32event.SetEvent(self.hWaitStop)
        self.stop_requested = True

    def SvcDoRun(self):
        self.log("Servicio iniciado.")
        self.main()
        self.log("Servicio terminado.")

    def main(self):
        # Configurar la ruta al directorio donde se encuentra app.py y al entorno virtual
        script_dir = r"E:/flask-musica-final"

        # Ejecutar app.py usando el intérprete de Python del entorno virtual
        command = f'python "{os.path.join(script_dir, "app.py")}"'
        self.log(f"Ejecutando comando: {command}")
        os.system(command)

        # Bucle de espera para mantener el servicio ejecutándose
        while not self.stop_requested:
            # Pausa de 1 segundo en el bucle para evitar el uso elevado de CPU
            time.sleep(1)


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(FlaskAppServiceMusic)
