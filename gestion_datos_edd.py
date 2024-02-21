import config

import time
from aplicaciones.libs.aplicacion import MainApplication, instance_check, run_threaded, run_threaded_only_one
from aplicaciones.libs.config_files import readConfig, setup_logger
import schedule
import queue
import tkinter as tk
from tkinter import *
import math
import os
from rvra.models import *

from aplicaciones.apps.envio_datos_edd import *

# REQUIERE VISUAL C++ https://www.microsoft.com/en-in/download/details.aspx?id=48145
# pyinstaller gestion_datos_edd.py --onedir --icon=gestion_edd.ico --noconsole --name gestion_datos_edd

def ProgramaPrincipal(self):
    
     # Inicializo el fichero .log
    pathLog = readConfig(name_section='PathNameLogs')['path_local'] #obtengo el path donde se almacenara el fichero .log
    nameLog = ProgramaPrincipal.__name__
    logger = setup_logger(nameLog, pathLog)

    #schedule.every(int(configFile['copia_db'])).minute.at(":00").do(run_threaded_only_one, copiarDB, (self, configFile, logger)).tag(nombre_modulo, copiarDB.__name__)

    horas_EnvioNuevoTLE = str(configFile["ejec_carga_tle"]).split(',')
    for h in horas_EnvioNuevoTLE:
        schedule.every().day.at(h.replace(' ', '')).do(run_threaded, cargaTLE, (self, configFile, logger)).tag(nombre_modulo, cargaTLE.__name__+'__'+h.replace(' ', ''))

    schedule.every().day.at(str(configFile["backup_bd"])).do(run_threaded, backupConfig, (self, configFile, logger)).tag(nombre_modulo, backupConfig.__name__)
    schedule.every().day.at(str(configFile["comprobacion_factory"])).do(run_threaded, comprobarFactorY, (self, configFile, logger)).tag(nombre_modulo, comprobarFactorY.__name__)
    #schedule.run_all()

#https://stackoverflow.com/questions/36688596/how-to-pass-arguments-when-execute-jobs-in-parallel-with-a-shared-job-queue-usin
#https://stackoverflow.com/questions/14694408/runtimeerror-main-thread-is-not-in-main-loop

NAME_APP = 'GESTION DATOS EDD'

if instance_check(NAME_APP):  # if no other instance is found...
    nombre_modulo=os.path.splitext(os.path.basename(__file__))[0]
    configFile = readConfig(name_section='EnvioDatosEDD', filename='config.ini')

    root = tk.Tk()
    jobqueue = queue.Queue()   
    app = MainApplication(root, title = 'GESTION DATOS EDD', icon = 'gestion_edd', image = 'gestion_edd_transparente.png', programa = ProgramaPrincipal, nombre_ejecutable=nombre_modulo, nombre_app='Gestion Datos EDD')

root.mainloop()
