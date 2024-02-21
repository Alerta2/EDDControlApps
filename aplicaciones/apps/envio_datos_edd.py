from cgitb import reset
import time
from datetime import datetime
from django.db import close_old_connections
from aplicaciones.libs.aplicacion import MainApplication, MonitorizaProcesos, instance_check, run_threaded, run_threaded_only_one
from aplicaciones.libs.config_files import readConfig, setup_logger
from aplicaciones.libs.gestorMensajes import *
from aplicaciones.libs.lib_gestion_cortex import *


def cargaTLE(self, config, logger):
    # Fecha/Hora en la que se inicia la aplicacion
    start_time = time.time()
    
    # Icono que muestra que se está ejecutando el proceso
    self.label_icon_estado.configure(image=self.iconRun)
    

    try:
        logger.info("Solicitando actualización de TLE")
        # Inicializo la actuacion
        envioDatos = LibGestionCortex(logger)
        
        # Ejecuto la actuacion
        envioDatos.enviarFicheroTLE()

    except Exception as e:
        logger.error("Se ha producido un error en el Proceso %s. Excepcion: %s", cargaTLE.__name__, e, exc_info=True)

    finally:
        close_old_connections()
        logger.info('Carga TLE se ha ejecutado en %s segundos' % round((time.time() - start_time),2))
        logger.info('Ultima ejecución a las %s' % datetime.now().strftime("%d %b, %Y %H:%M:%S"))
        self.ultima_ejecucion.set("Ultima ejecución: %s" % datetime.now().strftime("%d %b, %Y %H:%M:%S"))
        self.estado.set("Pendiente de su próxima ejecución ...")

        self.label_icon_estado.configure(image=self.iconChecked)


def comprobacionEDD(self, config, logger):
    # Fecha/Hora en la que se inicia la aplicacion
    start_time = time.time()
    
    # Icono que muestra que se está ejecutando el proceso
    self.label_icon_estado.configure(image=self.iconRun)
    

    try:
        logger.info("nada que comprobar en la EDD aun")
        
    except Exception as e:
        logger.error("Se ha producido un error en el Proceso %s. Excepcion: %s", comprobacionEDD.__name__, e, exc_info=True)

    finally:
        close_old_connections()
        logger.info('Comprobación EDD se ha ejecutado en %s segundos' % round((time.time() - start_time),2))
        logger.info('Ultima ejecución a las %s' % datetime.now().strftime("%d %b, %Y %H:%M:%S"))
        self.ultima_ejecucion.set("Ultima ejecución: %s" % datetime.now().strftime("%d %b, %Y %H:%M:%S"))
        self.estado.set("Pendiente de su próxima ejecución ...")

        self.label_icon_estado.configure(image=self.iconChecked)


def comprobarFactorY(self, config, logger):
    # Fecha/Hora en la que se inicia la aplicacion
    start_time = time.time()
    
    # Icono que muestra que se está ejecutando el proceso
    self.label_icon_estado.configure(image=self.iconRun)

    try:
        logger.info("Solicitando actualización de TLE")
        # Inicializo la actuacion
        envioDatos = LibGestionCortex(logger)

        # Ejecuto la actuacion
        envioDatos.consultarFactorY()
        
    except Exception as e:
        logger.error("Se ha producido un error en el Proceso %s. Excepcion: %s", comprobarFactorY.__name__, e, exc_info=True)

    finally:
        close_old_connections()
        logger.info('Comprobación FactorY se ha ejecutado en %s segundos' % round((time.time() - start_time),2))
        logger.info('Ultima ejecución a las %s' % datetime.now().strftime("%d %b, %Y %H:%M:%S"))
        self.ultima_ejecucion.set("Ultima ejecución: %s" % datetime.now().strftime("%d %b, %Y %H:%M:%S"))
        self.estado.set("Pendiente de su próxima ejecución ...")

        self.label_icon_estado.configure(image=self.iconChecked)


def copiarDB(self, config, logger):
    # Fecha/Hora en la que se inicia la aplicacion
    start_time = time.time()
    
    # Icono que muestra que se está ejecutando el proceso
    self.label_icon_estado.configure(image=self.iconRun)

    try:
        logger.info("Solicitando copia de DB")
        # Inicializo la actuacion
        envioDatos = LibGestionCortex(logger)

        # Ejecuto la actuacion
        envioDatos.obtenerBaseDeDatos()
        
    except Exception as e:
        logger.error("Se ha producido un error en el Proceso %s. Excepcion: %s", copiarDB.__name__, e, exc_info=True)

    finally:
        close_old_connections()
        logger.info('Copia de DB se ha ejecutado en %s segundos' % round((time.time() - start_time),2))
        logger.info('Ultima ejecución a las %s' % datetime.now().strftime("%d %b, %Y %H:%M:%S"))
        self.ultima_ejecucion.set("Ultima ejecución: %s" % datetime.now().strftime("%d %b, %Y %H:%M:%S"))
        self.estado.set("Pendiente de su próxima ejecución ...")

        self.label_icon_estado.configure(image=self.iconChecked)


def backupConfig(self, config, logger):
    # Fecha/Hora en la que se inicia la aplicacion
    start_time = time.time()
    
    # Icono que muestra que se está ejecutando el proceso
    self.label_icon_estado.configure(image=self.iconRun)

    try:
        logger.info("Solicitando copia de los ficheros de configuracion")
        # Inicializo la actuacion
        envioDatos = LibGestionCortex(logger)

        # Ejecuto la actuacion
        envioDatos.copiaSeguridadCortex()
        
    except Exception as e:
        logger.error("Se ha producido un error en el Proceso %s. Excepcion: %s", backupConfig.__name__, e, exc_info=True)

    finally:
        close_old_connections()
        logger.info('Copia de ficheros de configuracion se ha ejecutado en %s segundos' % round((time.time() - start_time),2))
        logger.info('Ultima ejecución a las %s' % datetime.now().strftime("%d %b, %Y %H:%M:%S"))
        self.ultima_ejecucion.set("Ultima ejecución: %s" % datetime.now().strftime("%d %b, %Y %H:%M:%S"))
        self.estado.set("Pendiente de su próxima ejecución ...")

        self.label_icon_estado.configure(image=self.iconChecked)