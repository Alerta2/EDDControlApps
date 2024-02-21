
import logging
import configparser
from datetime import datetime, timedelta
import pytz

class gestorLogger():
    def __init__(self):
        self.logger = None
    
    def readConfig(self, name_section, filename='config.ini'):
        """
        It reads the config.ini file and returns the value of the name_section parameter.
        
        :param name_section: The name of the section in the config file
        :param filename: The name of the file to read, defaults to config.ini (optional)
        """
        try:
            # create parser and read ini configuration file
            parser = configparser.ConfigParser()
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
                    self.logger.error("Seccion "+name_section+ " no encontrada en el archivo de configuracion "+filename, exc_info=False)
                    db=None
                    #raise Exception('{0} not found in the {1} file'.format(user, filename))
            else:
                self.logger.error("No se ha podido leer el contenido del archivo de configuracion "+ filename, exc_info=False)
                db=None

        except Exception as e:
            self.logger.error("Fallo al leer el archivo de configuracion "+ filename, exc_info=True)
            db=None

        finally:
            return db

    def LogApp(self, name, configFile='logger.ini'):
        """
        It creates a logger object.
        
        :param name: The name of the logger
        :param configFile: The name of the configuration file, defaults to logger.ini (optional)
        """
        
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
        rutaLog = self.readConfig(name_section='PathNameLogs')['path_local'] #obtengo el path donde se almacenara el fichero .log
    
        logging.config.fileConfig(configFile,disable_existing_loggers=False,defaults={ 'logfilename' : str(rutaLog)+str(name)})  #leo el fichero de configuracion
        self.logger = logging.getLogger(str(name))   #genero un logger con la configuracion con nombre name
        self.logger.info('Tu fichero .log sera almacenado en la ruta %s%s.log',rutaLog,name) #genero el primer mensaje
        self.logger.info('Iniciando Ejecucion App %s a las %s', name, datetime.strftime(datetime.now().astimezone(pytz.timezone("Europe/Madrid")),"%d-%b-%y %H:%M:%S")) #genero el primer mensaje

        return self.logger #devuelvo el logger generado