from ast import Return
from turtle import bgcolor, color

from matplotlib.pyplot import legend
import config
import telegram
from telegram import *
from telegram.ext import * 
from telegram.error import RetryAfter, TimedOut 
from requests import *
import os
import logging
import requests
from requests.auth import HTTPDigestAuth
from datetime import datetime, timedelta
from dateutil import tz
from spida.models import ValoresVisualizados10D
from django.db.models import F
import pandas as pd
import plotly.graph_objects as go
import time
import pytz

from rvra.models import EstGamYRadioyodos


#https://api.telegram.org/bot5221854475:AAE1sPLyC_4jO0ltBoS9_7hwzKXZm0_eVKI/getUpdates

nombre_modulo = os.path.splitext(os.path.basename(__file__))[0]
logger = logging.getLogger(nombre_modulo)
my_token = '5221854475:AAE1sPLyC_4jO0ltBoS9_7hwzKXZm0_eVKI' #token Telegram
id_telegram = '530544321' #id bot


'''def enviar_mensaje(chat_id, mensaje, disable_notify, info_mensaje, config, token=my_token):
    result = None
    try:
        tzInfo = pytz.timezone('Europe/Madrid')
        fecha_hora_actual = datetime.now().astimezone(tzInfo)
        h1 = config['hora_ini_notificaciones_off'].split(':')#Hora inicio modo silencioso
        h2 = config['hora_fin_notificaciones_off'].split(':')#Hora fin modo silencioso
        fecha_hora_ini_notificaciones_off = fecha_hora_actual.replace(hour=int(h1[0]), minute=int(h1[1]), second=int(h1[2]))
        fecha_hora_fin_notificaciones_off = fecha_hora_actual.replace(hour=int(h2[0]), minute=int(h2[1]), second=int(h2[2]))
        if fecha_hora_ini_notificaciones_off>fecha_hora_fin_notificaciones_off:
            fecha_hora_ini_notificaciones_off = fecha_hora_ini_notificaciones_off + timedelta(days=-1)

        bot = Bot(token=token)
        #Envio el mensaje sin notificacion si así lo indico y ademas la hora actual se encuentra en el rango establecido
        if disable_notify == 1 and fecha_hora_actual >= fecha_hora_ini_notificaciones_off and fecha_hora_actual <= fecha_hora_fin_notificaciones_off:
            silenciar = True
        else: #Envio el mensaje con notificacion
            silenciar = False
        if disable_notify == 2: #Envio el mensaje sin notificacion sea la hora que sea
            silenciar = True
        #bot.copy_message()
        respuesta = bot.send_message(chat_id=chat_id, text=mensaje, disable_notification=silenciar, parse_mode='HTML')
        print("RESPUESTA", respuesta)
        
        if  info_mensaje.confirmar==1: # Si tengo que confirmar el mensaje lo edito y le añado el boton
            print("NECESARIO CONFIRMACION")
            
            #url_confirmacion = config['url_confirmacion'] \
            #                +'?a='+ str(info_mensaje.id_area) \
            #                +'&c='+ str(chat_id) \
            #                +'&m='+ str(result)
            
            parameters = str({"a":str(info_mensaje.id_area),"c":str(chat_id),"m": str(respuesta.message_id)})
            url_confirmacion = config['url_confirmacion'] \
                            +'?i='+ parameters
            
            buttonsMenu = [[InlineKeyboardButton("\U0001F4F2 Confirmar", url=url_confirmacion)]]
            keyboard_markup_confirmar = InlineKeyboardMarkup(buttonsMenu)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=respuesta.message_id, reply_markup=keyboard_markup_confirmar)
        
        result = respuesta
              
    except (RetryAfter, TimedOut) as e:
        result = None
        logger.error("RetryAfter, TimedOut: Se ha producido un error al enviar un mensaje. Excepcion: %s",  e, exc_info=True)
    except Exception as e:
        result = None
        logger.error("Se ha producido un error al enviar un mensaje. Excepcion: %s",  e, exc_info=True)
    finally:
        return result

def enviar_captura_videovigilancia(men, chat_id, token=my_token):
    try:
        codEstacion = str(men.id_estacion)[-2:]
        user = 'Spida'
        password = 'Spida2018'
        urlPicture = 'http://spida'+codEstacion+'.selfip.net:90/ISAPI/Streaming/channels/1/picture' 
        r=requests.get(urlPicture, auth=HTTPDigestAuth(user, password), verify=False, timeout=2)

        if r.status_code!=200:
            user = 'admin'
            r=requests.get(urlPicture, auth=HTTPDigestAuth(user, password), verify=False, timeout=2)
        if r.status_code==200:            
            urlPreview = 'http://spida'+codEstacion+'.selfip.net:90/ISAPI/Streaming/channels/102/httppreview' 
            buttonsMenu = [[InlineKeyboardButton("\U0001F3A5 Video Cámara", url=urlPreview)]]
            keyboard_markup = InlineKeyboardMarkup(buttonsMenu)

            tries = 0
            max_tries = 10
            retry_delay = 10
            while tries < max_tries:
                try:
                    bot = Bot(token=my_token)
                    bot.send_photo(chat_id=chat_id, photo=r.content, reply_markup=keyboard_markup)
                except (RetryAfter, TimedOut) as e:
                    time.sleep(retry_delay)
                    tries += 1
                else:
                    break
    except requests.exceptions.Timeout:
        logger.warning("Agotado el tiempo de espera para enviar la ultima imagen de la camara de videovigilancia de %s con url %s.",men.estacion, urlPicture, exc_info=True)
    except Exception as e:
        logger.error("Se ha producido un error al enviar la ultima imagen de la camara de videovigilancia de %s. Excepcion: %s",men.estacion, e, exc_info=True)


def enviar_grafico_spida(men, chat_id, token=my_token):

    try:
        print("MENSAJE", men)
        #Obtengo la fecha a partir de la cual debo obtener los datos para ser representados
        fechahoraUTC_lim = datetime.utcnow() - timedelta(hours=24)
        UTCzone = tz.tzutc()
        fechahoraUTC_lim = fechahoraUTC_lim.replace(tzinfo=UTCzone)

        #Obtengo los datos de la base de datos
        datos = ValoresVisualizados10D.objects.using('spida'
                ).filter(id_estacion=men.id_estacion,
                        id_canal=men.id_canal,
                        fecha_hora_utc__gt=fechahoraUTC_lim
                ).annotate(canal = F('id_canal__nombre'), 
                            unidades = F('id_canal__unidades'),
                            estacion = F('id_estacion__nombre')
                ).values('fecha_hora_local', 'valor', 'canal', 'unidades', 'estacion')

        print("ULTIMOS VALORES")
        print(datos)

        if datos.count()>0: #Si hay datos genero el grafico
            
            #Obtengo los datos ordenados por fecha
            df_datos = pd.DataFrame(datos)
            df_datos['fecha_hora_local'] = pd.to_datetime(df_datos["fecha_hora_local"], errors='ignore').dt.tz_localize(None)
            df_datos = df_datos.sort_values(by=['fecha_hora_local'])
            
            #Genero el grafico
            layout = go.Layout(autosize=True, xaxis=dict(title='Fecha/Hora'), yaxis=dict(title=df_datos.iloc[0]['canal'])) #, autorange = True, type="category"
            data = go.Scatter(x=df_datos['fecha_hora_local'], y=df_datos['valor'], mode='lines+markers')
            fig = go.Figure(layout=layout)#, data=data
            fig.update_layout(title_text=df_datos.iloc[0]['estacion']+'<br><sup>'+df_datos.iloc[0]['canal']+' ('+ df_datos.iloc[0]['unidades']+')</sup>', 
                            title_x=0.5, 
                            title_xanchor='center',
                            xaxis_showgrid=False, 
                            yaxis_showgrid=False) #, plot_bgcolor='rgba(255,0,0,1)'
            #Añado la serie al grafico
            fig.add_trace(data)
            #Añado una etiqueta con el ultimo valor
            fig.add_annotation(x=df_datos['fecha_hora_local'][df_datos.index[-1]], 
                    y=df_datos['valor'][df_datos.index[-1]],
                    text=  str(df_datos['valor'][df_datos.index[-1]])+' '+df_datos.iloc[0]['unidades'] + ', ' +str(df_datos['fecha_hora_local'][df_datos.index[-1]].strftime('%H:%M'))+' h',
                    showarrow=True,
                    arrowhead=1)

            
            if men.id_canal == 100: #Para spida y nivel de río pinto los umbrales
                df_umbrales = getUmbrales(men)
                if len(df_umbrales)>0:
                    #fig.add_traces(go.Scatter(x = [df_datos['fecha_hora_local'][df_datos.index[-1]]],
                    #                            y = [df_datos['valor'][df_datos.index[-1]]],
                    #                            mode="text",
                    #                            #marker_symbol = 'line-ns',
                    #                            #marker_line_width=2, marker_size=20,
                    #                            text = ['(Desbordamiento '+str(df_umbrales.iloc[0]['N3']) + ' m)'],
                    #                            textposition = 'bottom center'
                    #                        )
                    #                )
                    fig.add_annotation(#dict(font=dict(color='red'),
                            x=df_datos['fecha_hora_local'][df_datos.index[-1]], 
                            y=df_datos['valor'][df_datos.index[-1]],
                            text=  '(Desbordamiento '+str(df_umbrales.iloc[0]['N3']) + ' m)',
                            showarrow=False,
                            #arrowhead=2)
                            yshift=-10)

                    #Obtengo los limites del grafico
                    full_fig = fig.full_figure_for_development()
                    dimension_x = full_fig.layout.xaxis.range
                    dimension_y = full_fig.layout.yaxis.range

    
                    #min_value = df_datos['valor'].min()
                    #if min_value > 0:
                    #    min_value = 0
                    #else:
                    #    min_value = dimension_y[0]
                    #fig.update_layout(shapes= [dict(opacity= 0.3,
                                                    layer='below',
                                                    xref= 'x',
                                                    yref= 'y',
                                                    fillcolor= 'green',
                                                    x0= dimension_x[0],
                                                    y0= 0,
                                                    x1= dimension_x[1],
                                                    y1= df_umbrales.iloc[0]['N1'],
                                                    type= 'rect',
                                                    line = dict(width= 0) #color= 'rgba(128, 0, 128, 1)',
                                                ),
                                                dict(opacity= 0.3,
                                                    layer='below',
                                                    xref= 'x',
                                                    yref= 'y',
                                                    fillcolor= 'yellow',
                                                    x0= dimension_x[0],
                                                    y0= df_umbrales.iloc[0]['N1'],
                                                    x1= dimension_x[1],
                                                    y1= df_umbrales.iloc[0]['N2'],
                                                    type= 'rect',
                                                    line = dict(width= 0)
                                                ),
                                                dict(opacity= 0.3,
                                                    layer='below',
                                                    xref= 'x',
                                                    yref= 'y',
                                                    fillcolor= 'orange',
                                                    x0= dimension_x[0],
                                                    y0= df_umbrales.iloc[0]['N2'],
                                                    x1= dimension_x[1],
                                                    y1= df_umbrales.iloc[0]['N3'],
                                                    type= 'rect',
                                                    line = dict(width= 0)
                                                ),
                                                dict(opacity= 0.3,
                                                    layer='below',
                                                    xref= 'x',
                                                    yref= 'y',
                                                    fillcolor= 'red',
                                                    x0= dimension_x[0],
                                                    y0= df_umbrales.iloc[0]['N3'],
                                                    x1= dimension_x[1],
                                                    y1= 20,
                                                    type= 'rect',
                                                    line = dict(width= 0)
                                                )],
                                        xaxis=dict(range=[dimension_x[0], dimension_x[1]]),
                                        yaxis=dict(range=[dimension_y[1], dimension_y[1]]))


            #Represento umbrales en el caso de nivel de rio (Si los hay)
            #if men.id_canal == 100:
            #    df_umbrales = getUmbrales(men)
            #    if len(df_umbrales)>0:
            #        fig.add_hrect(y0=0, y1=df_umbrales.iloc[0]['N1'], line_width=0, fillcolor="green", opacity=0.2)
            #        fig.add_hrect(y0=df_umbrales.iloc[0]['N1'], y1=df_umbrales.iloc[0]['N2'], line_width=0, fillcolor="yellow", opacity=0.5)
            #        fig.add_hrect(y0=df_umbrales.iloc[0]['N2'], y1=df_umbrales.iloc[0]['N3'], line_width=0, fillcolor="orange", opacity=0.2)
            #        fig.add_hrect(y0=df_umbrales.iloc[0]['N3'], y1=10, line_width=0, fillcolor="red", opacity=0.2)

            #grafico = py.plot(fig, filename = str(id_estacion)+'-'+str(id_canal))
            #img_bytes = py.image.get(fig, format = 'png', scale = 2)
            grafico = 'https://google.es'
            img_bytes = fig.to_image(format = "png", scale = 2)

            buttonsMenu = [[InlineKeyboardButton("\U0001F4C8 Monitorizar", url=grafico)]]
            keyboard_markup = InlineKeyboardMarkup(buttonsMenu)

            tries = 0
            max_tries = 10
            retry_delay = 10
            while tries < max_tries:
                try:
                    bot = Bot(token=token)
                    bot.send_photo(chat_id=chat_id, photo=img_bytes) #, reply_markup=keyboard_markup
                except (RetryAfter, TimedOut) as e:
                    time.sleep(retry_delay)
                    tries += 1
                else:
                    break

    except Exception as e:
        logger.error("Se ha producido un error al enviar el grafico de %s de la estacion de %s. Excepcion: %s",men.id_canal, men.estacion, e, exc_info=True)

def enviar_grafico_rvra(men, chat_id, token=my_token):

    try:
        print("MENSAJE", men)
        #Obtengo la fecha a partir de la cual debo obtener los datos para ser representados
        fechahoraLocal_lim = datetime.now() - timedelta(hours=24)

        #Obtengo los datos de la base de datos
        datos = EstGamYRadioyodos.objects.using('rvra'
                ).filter(estaciones_id=men.id_estacion,
                        canales_id=men.id_canal,
                        fecha_hora__gt=fechahoraLocal_lim
                ).annotate(canal = F('canales_id__nombre'), 
                            unidades = F('canales_id__unidades'),
                            estacion = F('estaciones_id__nombre'),
                            fecha_hora_local = F('fecha_hora')
                ).values('fecha_hora_local', 'valor', 'canal', 'unidades', 'estacion')

        print("ULTIMOS VALORES")
        print(datos)

        if datos.count()>0: #Si hay datos genero el grafico
            
            #Obtengo los datos ordenados por fecha
            df_datos = pd.DataFrame(datos)
            df_datos['fecha_hora_local'] = pd.to_datetime(df_datos["fecha_hora_local"], errors='ignore').dt.tz_localize(None)
            df_datos = df_datos.sort_values(by=['fecha_hora_local'])
            
            #Genero el grafico
            layout = go.Layout(autosize=True, xaxis=dict(title='Fecha/Hora'), yaxis=dict(title=df_datos.iloc[0]['canal'])) #, autorange = True, type="category"
            data = go.Scatter(x=df_datos['fecha_hora_local'], y=df_datos['valor'], mode='lines+markers')
            fig = go.Figure(layout=layout)#, data=data
            fig.update_layout(title_text=df_datos.iloc[0]['estacion']+'<br><sup>'+df_datos.iloc[0]['canal']+' ('+ df_datos.iloc[0]['unidades']+')</sup>', 
                            title_x=0.5, 
                            title_xanchor='center',
                            xaxis_showgrid=False, 
                            yaxis_showgrid=False) #, plot_bgcolor='rgba(255,0,0,1)'
            #Añado la serie al grafico
            fig.add_trace(data)
            #Añado una etiqueta con el ultimo valor
            fig.add_annotation(x=df_datos['fecha_hora_local'][df_datos.index[-1]], 
                    y=df_datos['valor'][df_datos.index[-1]],
                    text=  str(df_datos['valor'][df_datos.index[-1]])+' '+df_datos.iloc[0]['unidades'] + ', ' +str(df_datos['fecha_hora_local'][df_datos.index[-1]].strftime('%H:%M'))+' h',
                    showarrow=True,
                    arrowhead=1)

            
            if men.id_canal == 1: #Para spida y nivel de río pinto los umbrales
                df_umbrales = getUmbralesRarex(men)
                if len(df_umbrales)>0:

                    #Obtengo los limites del grafico
                    full_fig = fig.full_figure_for_development()
                    dimension_x = full_fig.layout.xaxis.range
                    dimension_y = full_fig.layout.yaxis.range

    
                    min_value = df_datos['valor'].min()
                    if min_value > 0:
                        min_value = 0
                    else:
                        min_value = dimension_y[0]
                    fig.update_layout(shapes= [dict(opacity= 0.3,
                                                    layer='below',
                                                    xref= 'x',
                                                    yref= 'y',
                                                    fillcolor= 'green',
                                                    x0= dimension_x[0],
                                                    y0= 0,
                                                    x1= dimension_x[1],
                                                    y1= df_umbrales.iloc[0]['N1'],
                                                    type= 'rect',
                                                    line = dict(width= 0) #color= 'rgba(128, 0, 128, 1)',
                                                ),
                                                dict(opacity= 0.3,
                                                    layer='below',
                                                    xref= 'x',
                                                    yref= 'y',
                                                    fillcolor= 'yellow',
                                                    x0= dimension_x[0],
                                                    y0= df_umbrales.iloc[0]['N1'],
                                                    x1= dimension_x[1],
                                                    y1= df_umbrales.iloc[0]['N2'],
                                                    type= 'rect',
                                                    line = dict(width= 0)
                                                ),
                                                dict(opacity= 0.3,
                                                    layer='below',
                                                    xref= 'x',
                                                    yref= 'y',
                                                    fillcolor= 'orange',
                                                    x0= dimension_x[0],
                                                    y0= df_umbrales.iloc[0]['N2'],
                                                    x1= dimension_x[1],
                                                    y1= df_umbrales.iloc[0]['N3'],
                                                    type= 'rect',
                                                    line = dict(width= 0)
                                                ),
                                                dict(opacity= 0.3,
                                                    layer='below',
                                                    xref= 'x',
                                                    yref= 'y',
                                                    fillcolor= 'red',
                                                    x0= dimension_x[0],
                                                    y0= df_umbrales.iloc[0]['N3'],
                                                    x1= dimension_x[1],
                                                    y1= 10,
                                                    type= 'rect',
                                                    line = dict(width= 0)
                                                )],
                                        xaxis=dict(range=[dimension_x[0], dimension_x[1]]),
                                        yaxis=dict(range=[min_value, dimension_y[1]]))


            #Represento umbrales en el caso de nivel de rio (Si los hay)
            #if men.id_canal == 100:
            #    df_umbrales = getUmbrales(men)
            #    if len(df_umbrales)>0:
            #        fig.add_hrect(y0=0, y1=df_umbrales.iloc[0]['N1'], line_width=0, fillcolor="green", opacity=0.2)
            #        fig.add_hrect(y0=df_umbrales.iloc[0]['N1'], y1=df_umbrales.iloc[0]['N2'], line_width=0, fillcolor="yellow", opacity=0.5)
            #        fig.add_hrect(y0=df_umbrales.iloc[0]['N2'], y1=df_umbrales.iloc[0]['N3'], line_width=0, fillcolor="orange", opacity=0.2)
            #        fig.add_hrect(y0=df_umbrales.iloc[0]['N3'], y1=10, line_width=0, fillcolor="red", opacity=0.2)

            #grafico = py.plot(fig, filename = str(id_estacion)+'-'+str(id_canal))
            #img_bytes = py.image.get(fig, format = 'png', scale = 2)
            grafico = 'https://google.es'
            img_bytes = fig.to_image(format = "png", scale = 2)

            buttonsMenu = [[InlineKeyboardButton("\U0001F4C8 Monitorizar", url=grafico)]]
            keyboard_markup = InlineKeyboardMarkup(buttonsMenu)

            tries = 0
            max_tries = 10
            retry_delay = 10
            while tries < max_tries:
                try:
                    bot = Bot(token=token)
                    bot.send_photo(chat_id=chat_id, photo=img_bytes) #, reply_markup=keyboard_markup
                except (RetryAfter, TimedOut) as e:
                    time.sleep(retry_delay)
                    tries += 1
                else:
                    break

    except Exception as e:
        logger.error("Se ha producido un error al enviar el grafico de %s de la estacion de %s. Excepcion: %s",men.id_canal, men.estacion, e, exc_info=True)
'''

def enviar_documento_local(path, nameFile, chat_id=id_telegram, token=my_token):
    tries = 0
    max_tries = 10
    retry_delay = 10
    while tries < max_tries:
        try:
            bot = telegram.Bot(token=token)
            bot.send_document(chat_id=chat_id, document=open(path, 'rb'), filename=nameFile)
        except (RetryAfter, TimedOut) as e:
            logger.error("RetryAfter, TimedOut: Se ha producido un error al enviar el documento %s. Excepcion: %s", path, e, exc_info=True)
            time.sleep(retry_delay)
            tries += 1
        except Exception as e:
            logger.error("Se ha producido un error al enviar el documento %s. Excepcion: %s", path, e, exc_info=True)
        else:
            break


def crear_enlace_invitacion(chat_id, info_usuario, token=my_token):
    result = None
    try:
        #info_usuario debe tener el formato <nombre>|<id_user_web>|+34<telefono>
        bot = Bot(token=token)
        new_link=bot.create_chat_invite_link(chat_id=chat_id, name=info_usuario, expire_date= datetime.now()+timedelta(days=1), creates_join_request=True)
        result = new_link

        #Info
        '''
        {'expire_date': 1650921129, 
        'creator': {'id': 5221854475, 
                    'first_name': 'Mensajes-ALERTA2', 
                    'username': 'MensajesAlerta2Bot', 
                    'is_bot': True}, 
        'is_revoked': False, 
        'name': 'PAULA:+34697989192', 
        'creates_join_request': True, 
        'invite_link': 'https://t.me/+q2QK9q4vO2ZkZjVk', 
        'is_primary': False}'''
        
    except Exception as e:
        logger.error("Se ha producido un error al crear un nuevo link de invitacion a un canal. Excepcion: %s",  e, exc_info=True)
    return result

def main():
    #chat_id = -1001587896744 #Spida
    chat_id = -1001749964853
    info_usuario = "San|50|+34610141776"
    new_link = crear_enlace_invitacion(chat_id, info_usuario, my_token)
    print("LINK", new_link)


            



