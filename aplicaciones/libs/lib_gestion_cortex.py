from rvra.models import *
import pytz
from datetime import datetime, timedelta, date
import ftplib
import os
from aplicaciones.libs.config_files import readConfig
import sqlite3
import shutil
from aplicaciones.libs.gestorMensajes import *

class LibGestionCortex():
    
    def __init__(self, logger):
        self.logger = logger

    def conectarFTP(self):
        print("Conectando con el servidor FTP")
        configFile = readConfig(name_section='FTPEDDConfig', filename='config.ini')
        ftp = ftplib.FTP()
        ftp.connect(host=configFile['host'], port=int(configFile['port']))
        ftp.login(user=configFile['user'], passwd=configFile['passwd'])
        print("Conexión realizada con éxito")
        return ftp


    def enviarFicheroTLE(self):
        self.logger.info("consultarDatosEnviar")

        # Create an FTP connection to the server
        ftp = self.conectarFTP()
        # Download the last TLE satellite file from a remote location
        # using the requests module
        import requests
        print("Intento descargar el fichero TLE")
        last_tle_file = requests.get("https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle")
        print("Fichero descargado con éxito")
        with open("gp.tle", "wb") as f:
            f.write(last_tle_file.content)

        filename = "gp.tle"
        filetocopy = open(filename, "rb")
        print("Procedo al envío del fichero TLE")
        # Upload the file to the FTP server gp.tle
        ftp.storbinary(f"STOR {filename}", filetocopy)
        print("transferencia realizada con éxito...")
        gestorMensajes().enviarMensajeTelegram("Cargado nuevo fichero TLE", "Se ha cargado un nuevo fichero TLE en la Estación de Descarga Directa",'24')
        # Close the FTP connection
        ftp.close()
        print("conexión cerrada")


    def copiaSeguridadCortex(self):
        infoCopias = readConfig(name_section='ficherosBackup')
        #get the current date
        now = datetime.now()
        #get the current date in the format YYYY-MM-DD
        date = now.strftime("%Y-%m-%d")
        if os.path.exists(infoCopias['ruta_save']):
            shutil.make_archive(date+"_save", 'zip', infoCopias['ruta_save'])  

        self.logger.info("consultarDatosEnviar")
        # Create an FTP connection to the server
        ftp = self.conectarFTP()
        local_path = "save"

        if not os.path.exists(local_path):
            os.makedirs(local_path)

        def copiar_ficheros_ftp(ftp, ruta_local, ruta_server):            
            if not os.path.exists(ruta_local):
                os.makedirs(ruta_local)
            ftp.cwd(ruta_server)
            for file in ftp.mlsd():
                if file[1]['type'] == 'file':
                    print("intentando copiar", file[0])
                    if not "W_DB" in file[0]:
                        ftp.retrbinary("RETR " + file[0], open(ruta_local + '/' + file[0], 'wb').write)
                elif file[1]['type'] == 'dir':
                    copiar_ficheros_ftp(ftp, ruta_local+"/"+file[0], file[0])
            ftp.cwd("..")

        listaRutas = eval(infoCopias['rutas'])
        for ruta in listaRutas:
            copiar_ficheros_ftp(ftp, local_path+"/"+ruta, ruta)
        
        gestorMensajes().enviarMensajeTelegram("Copia de seguridad realizada", "Se ha realizado copia en las siguientes ubicaciones:"+str(listaRutas),'24')
        # Close the FTP connection
        ftp.close()
        print("conexión cerrada")


    def obtenerBaseDeDatos(self):
        # Create an FTP connection to the server
        ftp = self.conectarFTP()

        infoDB = readConfig(name_section='ficherosBackup')
        ftp.cwd(infoDB['rutaDB'])
        ftp.retrbinary("RETR " + infoDB['ficheroDB'], open(infoDB['ficheroDB'], 'wb').write)
        
    
    def consultarFactorY(self):
        self.logger.info("Consultando FactorY txt")
        # List all files in a directory using os.listdir
        basepath = 'save/publicapplog'
        fichero = os.listdir(basepath)[len(os.listdir(basepath))-1]

        fechaFichero = date(int(fichero.split("_")[1].split("-")[0]), int(fichero.split("_")[1].split("-")[1]), int(fichero.split("_")[1].split("-")[2].split(".")[0]))

        self.logger.info("Leyendo fichero " + fichero)
        
        f = open(basepath + "/" + fichero, "r")
        analizar = False
        leer = 3
        factor = None
        for linea in f:
            if "TEST_TEST : Y Factor Results" in linea:
                self.logger.info("Localizado Test Y automático")
                analizar = True
            
            if analizar and leer>0:
                if leer == 2:
                    factor = linea.split(" : ")[3].replace("\n","")
                elif leer == 1:
                    if "Test OK" in linea:
                        gestorMensajes().enviarMensajeTelegram("Test de FactorY realizado con éximo", "Se ha detectado un test realizado en la fecha {} y el resultado es positivo con un factor {}".format(fechaFichero,factor),'20')
                    else:
                        gestorMensajes().enviarMensajeTelegram("Test de FactorY realizado erróneo", "Se ha detectado un test realizado en la fecha {} y el resultado es negativo. Necesario revisar el software de la EDD.".format(fechaFichero),'20')
                leer -= 1


    def consultarFactorYDB(self):
        self.logger.info("Consultando FactorY")

        self.obtenerBaseDeDatos()
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Perform the SELECT query
        query = "SELECT EvtDate FROM EVENEMENT WHERE EvtEqtName='#TG_TEST' AND EvtOrigine='#CM_TEST' AND EvtTexte='#TEST_FACTY_RESULTS' ORDER BY EvtCompteur DESC LIMIT 1"
        cursor.execute(query)

        fechaTest = None
        # Iterate through the results
        for row in cursor:
            fechaTest = row[0]

        query = "SELECT * FROM EVENEMENT WHERE EvtDate>'"+fechaTest+"' AND EvtEqtName='#TG_TEST' AND EvtOrigine='#CM_TEST' AND EvtTexte='#TEST_OK';"

        cursor.execute(query)

        if len(cursor.fetchall()) > 0:
            gestorMensajes().enviarMensajeTelegram("Test de FactorY realizado con éximo", "Se ha detectado un test realizado en la fecha {} y el resultado es positivo".format(fechaTest),'20')
        else:
            gestorMensajes().enviarMensajeTelegram("Test de FactorY realizado erróneo", "Se ha detectado un test realizado en la fecha {} y el resultado es negativo. Necesario revisar el software de la EDD.".format(fechaTest),'20')

        # Close the cursor and connection
        cursor.close()
        conn.close()
        