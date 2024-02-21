from datetime import datetime
from configparser import ConfigParser
import os
import logging
import logging.config
import tkinter as tk
from aplicaciones.libs.bot_envios import enviar_documento_local

nombre_modulo = os.path.splitext(os.path.basename(__file__))[0]
logger = logging.getLogger(nombre_modulo)

def readConfig(name_section, filename='config.ini'):

    try:
        # create parser and read ini configuration file
        parser = ConfigParser()
        ReadOK=parser.read(filename)

        # get section, default to mysql
        if len(ReadOK)>0:
            db = {}
            if parser.has_section(name_section):
                items = parser.items(name_section)
                for item in items:
                    db[item[0]] = item[1]
                    if item[0] == 'connect_timeout':
                        db[item[0]] = int(item[1])
            else:
                logger.error("Seccion "+name_section+ " no encontrada en el archivo de configuracion "+filename, exc_info=False)
                db=None
                #raise Exception('{0} not found in the {1} file'.format(user, filename))
        else:
            logger.error("No se ha podido leer el contenido del archivo de configuracion "+ filename, exc_info=False)
            db=None

    except Exception as e:
        logger.error("Fallo al leer el archivo de configuracion "+ filename, exc_info=True)
        db=None

    finally:
        return db


def LogApp(name, configFile='logger.ini'):
    
    '''Declara un logger para una App. En la funcion de la App en la primera linea se debe importar: 
        Ejemplo -> logger=LogApp('DatosSpida', 'datos_spida', 'logger.ini')
        
        Ejemplo de mensajes:
            debug -> logger.debug('Ejemplo de un mensaje de depuracion)
            info -> logger.info('Esto es un mensaje informativo)
            warning -> logger.warning('Se ha producido un fallo sin importancia')
            error -> logger.error('No se ha podido establecer conexion con FTP')
            critical -> logger.critical('El registro no existe en la BD') 
        
        OJO!
        1. El parametro de entrada name es igual a -> os.path.splitext(os.path.basename(__file__))[0]
            Para ello añadir en la parte superior del modulo de tu app lo siguiente -> import os 
            '''
    rutaLog = readConfig(name_section='PathNameLogs')['path_local'] #obtengo el path donde se almacenara el fichero .log
  
    logging.config.fileConfig(configFile,disable_existing_loggers=True, defaults={ 'logfilename' : str(rutaLog)+str(name)})  #leo el fichero de configuracion
    logger = logging.getLogger(str(name))   #genero un logger con la configuracion con nombre name
    
    logger.info('Tu fichero .log sera almacenado en la ruta %s%s.log',rutaLog, name) #genero el primer mensaje
    #logger.info('Iniciando Ejecucion App %s a las %s', name, datetime.strftime(datetime.now(),"%d-%b-%y %H:%M:%S")) #genero el primer mensaje

    return logger #devuelvo el logger generado



def setup_logger(logger_name, path_file, level=logging.DEBUG):
    
    formatter = logging.Formatter('%(levelname)8s - %(asctime)s - %(name)s - %(funcName)s - %(message)s', "%d-%b-%y %H:%M:%S")
    
    fileHandlerERROR = logging.FileHandler(path_file+logger_name+'.log', mode='w+')
    fileHandlerERROR.setFormatter(formatter)
    fileHandlerERROR.setLevel(logging.ERROR)
    
    fileHandlerINFO = logging.FileHandler(path_file+logger_name+'INFO.log',mode='w+')
    fileHandlerINFO.setFormatter(formatter)
    fileHandlerINFO.setLevel(logging.INFO)
    
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    if (logger.hasHandlers()): # Para limpiar el archivo
        logger.handlers.clear()

    logger.addHandler(fileHandlerERROR)
    logger.addHandler(fileHandlerINFO)
    logger.addHandler(streamHandler)

    logger.info('Tu fichero .log sera almacenado en la ruta %s',path_file) #genero el primer mensaje
    logger.info('Iniciando Ejecucion App %s a las %s', logger_name, datetime.strftime(datetime.now(),"%d-%b-%y %H:%M:%S")) #genero el primer mensaje
    
    return logger


class TextHandler(logging.Handler):
    # This class allows you to log to a Tkinter Text or ScrolledText widget
    # Adapted from Moshe Kaplan: https://gist.github.com/moshekaplan/c425f861de7bbf28ef06
    
    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        #print("PRUEBA", self, msg, record.levelname, record.asctime, record.funcName)
        #expected_attributes = \
        #    "args,asctime,created,exc_info,filename,funcName,levelname," \
        #    "levelno,lineno,module,msecs,message,msg,name,pathname," \
        #    "process,processName,relativeCreated,stack_info,thread,threadName"

        #for ea in expected_attributes.split(","):
        #    if not hasattr(record, ea):
        #        print("UNEXPECTED: LogRecord does not have the '{}' field!".format(ea))
        def append():
            self.text.configure(state='normal') 
            #print(self.text.index('end').split('.')[0], self.text.index('end-1c').split('.')[0])
            self.text.insert(tk.END, msg + '\n', record.levelname)
            self.text.configure(state='disabled')
            if int(self.text.index('end').split('.')[0])>=1000:
                self.text.delete(1.0, tk.END)
            # Autoscroll to the bottom
            self.text.yview(tk.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue

    It can be used from different threads
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)



def EnviarLog(nombreApp):
    listPathLogs = readConfig(name_section='PathNameLogs')
    rutaLogOrigen = listPathLogs['path_local']

    with open(str(rutaLogOrigen)+str(nombreApp)+'.log') as f:
            txt = f.readlines()
    if len(txt) > 0:
        enviar_documento_local(str(rutaLogOrigen)+str(nombreApp)+'INFO.log', str(nombreApp)+'.log')
        