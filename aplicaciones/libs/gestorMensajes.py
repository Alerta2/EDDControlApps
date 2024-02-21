from rvra.models import *

from datetime import datetime, timedelta
from django.template.loader import render_to_string
import pytz
from aplicaciones.libs.config_files import readConfig, setup_logger

import traceback
import os

from aplicaciones.libs.gestorLog import *
from aplicaciones.libs.consultasGuardias import *


class gestorMensajes():
    def __init__(self):
        self.mensajesPendientes = []
        nombre_modulo=os.path.splitext(os.path.basename(__file__))[0]
        self.logger = gestorLogger().LogApp(nombre_modulo, 'logger.ini')
        self.testing = False


    # envia una mensaje por telegram. si hay fallo de comunicacion guarda en lista de mensajes pendientes hasta que pueda ser enviado
    # estacion: estacion a la que se le envia el mensaje
    # mensaje: mensaje a enviar
    # descripcion: descripcion del mensaje
    # icono: icono del mensaje
    # estado: estado de la alerta 0, 1, 2, 3 leve -> grave
    # destino: destino del mensaje. 1: grupo rarex, 2: juan baeza
    # parametro: parametro afectado para calcular si se envía con sonido o no en horas intespestivas. Los parametros de control y meteo no general aviso sonoro de 0 a 8 horas
    def enviarMensajeTelegram(self, mensaje, descripcion, icono):
        telegram = readConfig(name_section='EnvioDatosEDD')['telegram']

        horaActual = datetime.now().astimezone(pytz.timezone("Europe/Madrid"))
        silenciar = 0 # no silencia
        if not self.checkHorarioAviso():
            silenciar = 1 # silencia
        try:
            self.logger.info("Intento de envío del mensaje: " + mensaje + ". Silencio: " + str(silenciar))
            self.logger.info("Envio de mensaje " + str(horaActual) + " - " + mensaje + " - " + str(silenciar))
            MensajesTelegram(id_area=1,id_estacion=None,fecha_hora_utc=horaActual,mensaje=mensaje,descripcion=descripcion,icono=icono,estado=1,id_telegram=telegram,silenciar=silenciar).save(using='spd')
        except Exception as e:
            self.logger.error("Fallo de envío del mensaje: " + mensaje + ". Silencio: " + str(silenciar))
            self.logger.error(e)
            self.logger.error(traceback.format_exc())

    # checkea si el valor se debe enviar en función de la hora
    # tipo: tipo de dato monitorizado
    # False: no se debe enviar si la hora de entre 00.00h y 08.00h
    # True: se debe enviar si la hora de entre 08.00h y 00.00h o un valor radiológico a cualquier hora
    def checkHorarioAviso(self):
        hora = datetime.now().astimezone(pytz.timezone("Europe/Madrid")).hour
        if hora < 8:
            return False
        else:
            return True