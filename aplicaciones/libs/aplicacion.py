from ast import arg
from webbrowser import BackgroundBrowser
import config
from concurrent.futures import thread
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import askyesno
from PIL import Image, ImageTk
from matplotlib.pyplot import title
from datetime import datetime, timedelta
import time
from numpy import append
import schedule
import threading
import pandas as pd
import os
import pytz
import queue
from aplicaciones.libs.config_files import QueueHandler, TextHandler, readConfig, setup_logger
from spida.models import MonitorizaApps
import ctypes
import sys
import schedule
import math
import tkinter.scrolledtext as st
import logging
from tkinter import filedialog

#https://stackoverflow.com/questions/38676617/tkinter-show-splash-screen-and-hide-main-screen-until-init-has-finished
class Splash(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Splash")

        ## required to make window show before the program gets to the mainloop
        self.update()


class MainApplication(tk.Tk):
    def __init__(self, root, title, icon, image, programa, nombre_ejecutable, nombre_app):
        
        # Inicializo el fichero .log
        pathLog = readConfig(name_section='PathNameLogs')['path_local'] #obtengo el path donde se almacenara el fichero .log
        nameLog = 'app'+title.replace(" ","")
        logger = setup_logger(nameLog, pathLog)


        #splash = Splash(root)
        self.nombre_ejecutable = nombre_ejecutable
        self.nombre_app = nombre_app
        
        self.root = root
        self.root.title(title)
        self.root.after(0, self.clock_time)
        self.root.iconbitmap('aplicaciones/static/img/' + icon + '.ico')
        self.root.option_add("*tearOff", False) # This is always a good idea
        self.root.geometry("600x500")
        self.root.columnconfigure(index=0, weight=1)
        self.root.columnconfigure(index=1, weight=1)
        self.root.columnconfigure(index=2, weight=1)
        self.root.rowconfigure(index=0, weight=1)
        self.root.rowconfigure(index=1, weight=1)
        self.root.rowconfigure(index=2, weight=1)
        self.root.rowconfigure(index=3, weight=1)
        self.sizegrip = ttk.Sizegrip(root)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))# Create a style
        self.style = ttk.Style(root)

        # Import the tcl file
        self.root.tk.call("source", "aplicaciones/static/proxttk-dark.tcl")

        # Set the theme with the theme_use method
        self.style.theme_use("proxttk-dark")

        # Ventana Consola 
        self.winConsole = Toplevel(self.root)
        self.winConsole.title("Consola - " + self.root.title())
        self.winConsole.geometry("800x550")
        self.winConsole.grid_rowconfigure(0, weight=1)
        self.winConsole.grid_columnconfigure(0, weight=1)
        self.winConsole.protocol("WM_DELETE_WINDOW", self.closeConsole)
        self.winConsole.iconbitmap('aplicaciones/static/img/consola.ico')
        self.winConsole.withdraw()

        # Menu superior
        menubarFile = Menu(root)
        self.winConsole.config(menu=menubarFile)

        # Menu -- File (Archivo Config)
        self.filemenu = Menu(menubarFile, tearoff=0)
        
        self.iconView= Image.open("aplicaciones/static/img/vista_previa.png")  # Color: #45B1D3
        self.iconView= self.iconView.resize((15,15), Image.ANTIALIAS)
        self.iconView = ImageTk.PhotoImage(self.iconView)
        self.filemenu.add_command(label="Vista previa", background="white", foreground="black", command=self.previewViewFileConsole, image=self.iconView, compound='left')
        self.iconSave= Image.open("aplicaciones/static/img/save.png")  # Color: #45B1D3
        self.iconSave= self.iconSave.resize((15,15), Image.ANTIALIAS)
        self.iconSave = ImageTk.PhotoImage(self.iconSave)
        self.filemenu.add_command(label="Guardar como", background="white", foreground="black", command=self.saveFileConsole, image=self.iconSave, compound='left')
        menubarFile.add_cascade(label="Archivo", menu=self.filemenu)
        
        # Add text widget to display logging info
        self.console_text =  st.ScrolledText(self.winConsole, state='disabled')
        self.console_text.configure(font='colortube')
        self.console_text.grid(row=0, column=0, sticky='nsew')
        self.console_text.tag_config('INFO', foreground='lightgreen', font=('Arial', 10))
        self.console_text.tag_config('DEBUG', foreground='gray', font=('Arial', 10))
        self.console_text.tag_config('WARNING', foreground='orange', font=('Arial', 10))
        self.console_text.tag_config('ERROR', foreground='red', font=('Arial', 10))
        self.console_text.tag_config('NOTSET', foreground='blue', font=('Arial', 10))
        self.console_text.tag_config('CRITICAL', foreground='red', font=('Arial', 10), underline=1)
        

        '''# Create textLogger
        self.text_handler = TextHandler(self.console_text)
        formatter = logging.Formatter('%(asctime)s: %(message)s', "%d-%b-%y %H:%M:%S")
        self.text_handler.setFormatter(formatter)
        # Add the handler to logger      
        logger.addHandler(self.text_handler)'''

        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(levelname)8s - %(asctime)s - %(name)s - %(funcName)s : %(message)s', "%d-%b-%y %H:%M:%S")
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        self.winConsole.after(100, self.poll_log_queue)


        # Ventana Configuracion 
        self.winConfig = Toplevel(self.root)
        self.winConfig.withdraw()
        self.winConfig.title("Configuración - " + self.root.title())
        self.winConfig.geometry("600x550")
        self.winConfig.grid_rowconfigure(0, weight=1)
        self.winConfig.grid_columnconfigure(0, weight=1)
        self.winConfig.protocol("WM_DELETE_WINDOW", self.closeConfig)
        self.winConfig.iconbitmap('aplicaciones/static/img/configuracion.ico')
        

        # Add text widget to display logging info
        self.config_text =  st.ScrolledText(self.winConfig)
        self.config_text.configure(font=('Arial', 11), foreground='white')
        self.config_text.grid(row=0, column=0, sticky='nsew')

        # Menu superior
        menubarConfiguracion = Menu(root)
        self.winConfig.config(menu=menubarConfiguracion)

        # Menu -- File (Archivo Config)
        self.configmenu = Menu(menubarFile, tearoff=0)
        self.configmenu.add_command(label="Guardar", background="white", foreground="black", command=self.updateConfigFile, image=self.iconSave, compound='left')
        menubarConfiguracion.add_cascade(label="Archivo", menu=self.configmenu)

        # Menu superior
        menubar = Menu(root)
        self.root.config(menu=menubar)

        # Menu -- Aplicacion
        self.appmenu = Menu(menubar, tearoff=0)

        self.iconPlay= Image.open("aplicaciones/static/img/play.png")  # Color: #45B1D3
        self.iconPlay= self.iconPlay.resize((15,15), Image.ANTIALIAS)
        self.iconPlay = ImageTk.PhotoImage(self.iconPlay)
        self.appmenu.add_command(label="Ejecutar", state="disabled", background="white", foreground="black", command=(lambda arg=programa : self.StartApp(arg)), image=self.iconPlay, compound='left')
        
        self.iconPause= Image.open("aplicaciones/static/img/pause.png")
        self.iconPause= self.iconPause.resize((15,15), Image.ANTIALIAS)
        self.iconPause = ImageTk.PhotoImage(self.iconPause)
        self.appmenu.add_command(label="Detener", background="white", foreground="black", command=self.StopApp, image=self.iconPause, compound='left', state="active")

        self.iconReboot= Image.open("aplicaciones/static/img/reboot.png")
        self.iconReboot= self.iconReboot.resize((15,15), Image.ANTIALIAS)
        self.iconReboot = ImageTk.PhotoImage(self.iconReboot)
        self.appmenu.add_command(label="Reiniciar", background="white", foreground="black", command= (lambda : self.MessageBoxYesNo('Reiniciar '+self.root.title(), '¿Estás seguro de que desea reiniciar la aplicación ' + self.root.title() + '?', self.RestartApp)), image=self.iconReboot, compound='left')
        
        self.appmenu.add_separator(background='white')
        
        self.iconReset= Image.open("aplicaciones/static/img/close.png")
        self.iconReset= self.iconReset.resize((15,15), Image.ANTIALIAS)
        self.iconReset = ImageTk.PhotoImage(self.iconReset)
        self.appmenu.add_command(label="Salir", background="white", foreground="black", command=(lambda : self.MessageBoxYesNo('Salir', '¿Estás seguro de que desea salir de la aplicación ' + self.root.title() + '?', self.CloseApp)), image=self.iconReset, compound='left')
        menubar.add_cascade(label="Aplicacion", menu=self.appmenu)

        # Menu -- Edicion
        editmenu = Menu(menubar, tearoff=0)
        
        self.iconConfiguration= Image.open("aplicaciones/static/img/config.png")
        self.iconConfiguration= self.iconConfiguration.resize((15,15), Image.ANTIALIAS)
        self.iconConfiguration = ImageTk.PhotoImage(self.iconConfiguration)
        editmenu.add_command(label="Configuracion", background="white", foreground="black", image=self.iconConfiguration, compound='left', command=self.showConfig)
        
        self.iconConsola= Image.open("aplicaciones/static/img/consola.png")
        self.iconConsola= self.iconConsola.resize((15,15), Image.ANTIALIAS)
        self.iconConsola = ImageTk.PhotoImage(self.iconConsola)
        editmenu.add_command(label="Consola", background="white", foreground="black", image=self.iconConsola, compound='left', command=self.showConsole)
        
        menubar.add_cascade(label="Editar", menu=editmenu)
        
        # Menu -- Procesos
        self.procesosmenu = Menu(menubar, tearoff=0)
        
        # Obtengo los procesos registrados en la BBDD para esta aplicacions
        self.procesos = self.getProcesos()

        for proceso in self.procesos.itertuples():
            self.createSubMenuProceso(proceso.nombre_proceso, 1 if proceso.ejecutar!= 0 else 0)
        
        menubar.add_cascade(label="Procesos", menu=self.procesosmenu)
        
        # Load frame
        self.frame = ttk.Frame(root, padding=(10,0,0,10))
        self.frame.grid(row=0, column=1, padx=0, pady=(10,10), sticky="nsew", rowspan=3)
        self.frame.columnconfigure(index=0, weight=1)

        #Imagen de la portada
        self.img= Image.open("aplicaciones/static/img/" + image)
        self.img= self.img.resize((380,205), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.label_img= Label(self.frame, image=self.img, height=205, anchor="center") #relief="solid",
        self.label_img.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        #Fecha/Hora actual
        self.fecha_hora_actual = StringVar()
        self.label_date_time = ttk.Label(self.frame, textvariable=self.fecha_hora_actual, font="colortube" ,justify="center",foreground="white")
        self.label_date_time.grid(row=1, column=0, pady=10, columnspan=2)

        # Tiempo restante para actualizar
        self.tiempo_restante = StringVar()
        self.tiempo_restante.set("Tiempo restante para actualizar: - seg")
        self.label_tiempo_restante = ttk.Label(self.frame, textvariable=self.tiempo_restante, font="colortube" ,justify="center",foreground="white")
        self.label_tiempo_restante.grid(row=2, column=0, pady=10, columnspan=2)

        # Fecha/Hora Ultima ejecucion
        self.ultima_ejecucion = StringVar()
        self.label_ultima_ejecucion = ttk.Label(self.frame, textvariable=self.ultima_ejecucion, font="colortube" ,justify="center",foreground="white")
        self.label_ultima_ejecucion.grid(row=3, column=0, pady=10, columnspan=2)

        # Mensajes proceso de ejecucion
        self.estado = StringVar()
        self.estado.set("Pendiente de su próxima ejecución ...")
        self.txt_estado = ttk.Entry(self.frame, textvariable=self.estado, state="readonly")
        self.txt_estado.grid(row=4, column=0, padx=0, pady=(10,0), sticky="nsew") 
        self.txt_estado.configure(wrap=None)

        # Iconos estado proceso de ejecucion
        self.iconChecked = Image.open("aplicaciones/static/img/checked.png")
        self.iconChecked = self.iconChecked.resize((30,30), Image.ANTIALIAS)
        self.iconChecked = ImageTk.PhotoImage(self.iconChecked)
        self.iconStop = Image.open("aplicaciones/static/img/stop.png")
        self.iconStop = self.iconStop.resize((30,30), Image.ANTIALIAS)
        self.iconStop = ImageTk.PhotoImage(self.iconStop)
        self.iconRun = Image.open("aplicaciones/static/img/spinner.png")
        self.iconRun = self.iconRun.resize((30,30), Image.ANTIALIAS)
        self.iconRun = ImageTk.PhotoImage(self.iconRun)
        self.iconError = Image.open("aplicaciones/static/img/error.png")
        self.iconError = self.iconError.resize((30,30), Image.ANTIALIAS)
        self.iconError = ImageTk.PhotoImage(self.iconError)
        self.label_icon_estado= Label(self.frame, image=self.iconChecked, text="Hola")
        self.label_icon_estado.grid(row=4, column=1, padx=(10,0), pady=(10,0))

        # Boton detener aplicacion
        self.boton_detener = ttk.Button(self.frame, text="DETENER",style="ToggleButton", command=self.StopApp)
        self.boton_detener.grid(row=6, column=0, padx=0, pady=(20,5), sticky='nsew', columnspan=2)

        '''# Boton ejecutar aplicacion
        self.boton_ejecutar = ttk.Button(self.frame, text="EJECUTAR",style="ToggleButton", command= (lambda arg=programa : self.StartApp(arg)))
        self.boton_ejecutar.grid(row=7, column=0, padx=0, pady=(5,0), sticky='nsew',columnspan=2)
        self.boton_ejecutar.state(["disabled"]) 

        # Boton reiniciar aplicacion
        self.reiniciar = ttk.Button(self.frame, text="REINICIAR",style="ToggleButton", command= (lambda : self.MessageBoxYesNo('Reiniciar '+self.root.title(), '¿Estás seguro de que desea reiniciar la aplicación ' + self.root.title() + '?', self.RestartApp)))
        self.reiniciar.grid(row=8, column=0, padx=0, pady=(10,0), sticky='nsew',columnspan=2)'''


        # Ejecuto el programa principal 
        self.thread_programa = threading.Thread(target=programa, args=[self])
        self.thread_programa.setDaemon(True)
        self.thread_programa.start()

        # Ejecuto la monitorizacion de los procesos 
        # @cambio elimino para que no haga aviso de la aplicion no funcionando
        self.thread_procesos = threading.Thread(target=self.RefreshEstadoProcesos)
        self.thread_procesos.setDaemon(True)
        self.thread_procesos.start()

        #schedule.every(1).seconds.do(self.poll_log_queue)

    def saveFileConsole(self):
        file = filedialog.asksaveasfile(initialfile=self.nombre_app.replace(" ",'_')+'_Log_'+datetime.now().strftime("%Y%m%d_%H%M%S"),
                                    title="Guardar fichero como",
                                    defaultextension='.txt',
                                    filetypes=[
                                        ("Text file",".txt")
                                    ])
        if file is None:
            return
        # get the text
        text_console = self.console_text.get("1.0", tk.END)
        filetext = str(text_console)
        pathFile = file.name
        with open(pathFile, 'w', encoding='utf-8') as f:
            f.write(filetext) 

        MsgBox = tk.messagebox.askquestion('Abrir fichero','¿Deseas abrir el fichero guardado?',icon = 'question')
        # Abro el fichero
        if MsgBox == 'yes':
            os.startfile(pathFile)
    
    def previewViewFileConsole(self):
        text_console = self.console_text.get("1.0", tk.END)
        pathFile = self.nombre_app.replace(" ",'_')+'_Log.txt'
        with open(pathFile, 'w', encoding='utf-8') as f:
            f.write(text_console)
        
            # Abro el fichero
            if f!=None:
                os.startfile(pathFile)
            
    def updateConfigFile(self):

        MsgBox = tk.messagebox.askquestion('Actualizar','¿Estás seguro de que desea actualizar el fichero de configuracion de la aplicación '+self.nombre_app+'?.\n\nSi aceptas continuar se reiniciará la aplicación con los cambios efectuados.',icon = 'question')
            
        # Reinicio la app
        if MsgBox == 'yes':
            nueva_configuracion = self.config_text.get("1.0", tk.END)
            with open('config.ini', 'w') as f:
                f.write(nueva_configuracion)
            self.RestartApp()
        else:
            self.closeConfig()
        

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.console_text.configure(state='normal')
        self.console_text.insert(tk.END, msg + '\n', record.levelname)
        self.console_text.configure(state='disabled')
        if int(self.console_text.index('end').split('.')[0])>=10000:
            self.console_text.delete(1.0, tk.END)
        # Autoscroll to the bottom
        self.console_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.winConsole.after(100, self.poll_log_queue)

    def createSubMenuProceso(self, nombre_proceso, checked):
        nombre_proceso = nombre_proceso.replace(':', '_')
        intVar = IntVar(value = checked)
        exec('self.var_%s = intVar' % (nombre_proceso))
        self.procesosmenu.add_checkbutton(label= nombre_proceso, background="white", foreground="black", variable=eval('self.var_'+ nombre_proceso), command=lambda arg = nombre_proceso :self.checkProceso(arg))

    def closeConsole(self):
        self.winConsole.withdraw()
    
    def showConsole(self):
        self.winConsole.deiconify()
    
    def closeConfig(self):
        self.winConfig.withdraw()
    
    def showConfig(self):
        configFile = open('config.ini', 'r')
        data = configFile.read()
        self.config_text.delete('1.0', tk.END)
        self.config_text.insert(tk.END, data)
        configFile.close()
        self.winConfig.deiconify()

    def exitsVariable(self, nombre_proceso):
        nombre_proceso=nombre_proceso.replace(':', '_')
        try:
            var = eval('self.var_'+nombre_proceso)
            value = var.get()
            if value!=1:
                return  False  #existe pestaña pero no se tiene que ejecutar
            else:
                return  True #existe pestaña y se tiene que ejecutar
        except:
            self.createSubMenuProceso(nombre_proceso, 1) # Creo una nueva pestaña en el menu
            return  True #No existe pestaña y se tiene que ejecutar

    
    def checkProceso(self, nombre_proceso):

        nombre_proceso=nombre_proceso.replace(':', '_')
        
        var =  eval('self.var_'+ nombre_proceso)

        # Detengo el proceso
        if var.get() == 0:
            update = MonitorizaApps.objects.using('spida').filter(nombre_proceso=nombre_proceso).update(ejecutar=0)
            if update:
                schedule.clear(nombre_proceso)
            else:
                var.set(1)

        # Si lo quiero volver a activar...
        else:
            MsgBox = tk.messagebox.askquestion('Reiniciar '+self.root.title(),'Para reactivar el proceso '+ nombre_proceso +' es necesario reiniciar la aplicación '+ self.nombre_app +'. ¿Estás seguro de que deseas continuar?',icon = 'question')
            
            # Reinicio la app
            if MsgBox == 'yes':
                update = MonitorizaApps.objects.using('spida').filter(nombre_proceso=nombre_proceso).update(ejecutar=1)
                if update:
                    self.RestartApp()
                else:
                    var.set(0)
            # Lo dejo tal y como esta 
            else:
                var.set(0)
                
            #self.MessageBoxYesNo('Reiniciar '+self.root.title(), 'Para reactivar un proceso es necesario reiniciar la aplicación '+ self.nombre_app +'. ¿Estás seguro de que deseas continuar?', self.RestartApp)

    def clock_time(self):
        fecha_hora = datetime.now().strftime("%d %b, %Y %H:%M:%S")
        self.fecha_hora_actual.set(fecha_hora)
        self.root.after(1000, self.clock_time) 
    
    def StopApp(self):
        schedule.clear()
        self.tiempo_restante.set("Tiempo restante para actualizar: - seg")
        self.label_icon_estado.configure(image=self.iconStop)
        self.estado.set("Aplicación detenida ...")
        #self.boton_ejecutar.state(["!disabled"])
        self.boton_detener.state(["disabled"]) 
        self.appmenu.entryconfig("Ejecutar", state="normal")
        self.appmenu.entryconfig("Detener", state="disabled")

    def StartApp(self, programa):
        self.label_icon_estado.configure(image=self.iconChecked)
        self.estado.set("Pendiente de su próxima ejecución ...")
        #self.boton_ejecutar.state(["disabled"])
        self.boton_detener.state(["!disabled"]) 
        self.appmenu.entryconfig("Ejecutar", state="disabled")
        self.appmenu.entryconfig("Detener", state="normal")
        self.thread_programa = threading.Thread(target=programa, args=[self])
        self.thread_programa.setDaemon(True)
        self.thread_programa.start()

    def CloseApp(self):
        self.root.destroy()
    
    def RestartApp(self):
        os.execl(sys.executable, sys.executable, *sys.argv)

    def MessageBoxYesNo(self, titulo, mensaje, accion):
        answer = askyesno(title=titulo,
                    message=mensaje)
        if answer:
            accion()
    
    def RefreshEstadoProcesos(self):
        
        while True:
            schedule.run_pending()
            time.sleep(1)
            
            if schedule.idle_seconds() is not None:
                MonitorizaProcesos(self.nombre_app, self.nombre_ejecutable)
                self.tiempo_restante.set("Tiempo restante para ejecutar: %s seg" % math.ceil(schedule.idle_seconds())) 
    
    def OpenNewThread(self, target, args = None):
        # Ejecuto el programa principal 
        if args==None:
            self.thread_programa = threading.Thread(target=target, args=[self])
        else:
            self.thread_programa = threading.Thread(target=target, args=args)
        self.thread_programa.setDaemon(True)
        self.thread_programa.start()

    def getProcesos(self):

        procesos = MonitorizaApps.objects.using("spida").filter(nombre=self.nombre_app).values()

        if procesos.count()>0:
            return pd.DataFrame(procesos)
        else:
            return pd.DataFrame()




'''Comprueba que solo haya una instancia de la aplicacion abierta'''
def instance_check(name_app):
    U32DLL = ctypes.WinDLL('user32')
    # get the handle of any window matching 'APP_NAME'
    hwnd = U32DLL.FindWindowW(None, name_app)
    if hwnd:  # if a matching window exists...
        # focus the existing window
        U32DLL.ShowWindow(hwnd, 5)
        U32DLL.SetForegroundWindow(hwnd)
        # bail
        sys.exit(0)
    return True


def getNombreProceso(job):
    s= str(job.job_func.args)
    start = 'function'
    end = ' at'
    idx1 = s.index(start)
    idx2 = s.index(end)   
    name_proceso = s[idx1 + len(start) + 1: idx2]
    return name_proceso

def MonitorizaProcesos(nombre_app, nombre_ejecutable):

    try:
        #Obtengo todos los trabajos que se estan ejecutando
        all_jobs = schedule.get_jobs(nombre_ejecutable)
        df_jobs = pd.DataFrame(all_jobs, columns=['job'])
        df_jobs['nombre_ejecutable'] = nombre_ejecutable #df_jobs.apply(lambda row: os.path.splitext(os.path.basename(__file__))[0], axis = 1)
        
        df_jobs['nombre_proceso'] = df_jobs.apply(lambda row: getNombreProceso(row['job']) if row['job'].at_time==None or row['job'].at_time.strftime("%H:%M") == "00:00" else getNombreProceso(row['job']) + '__' + row['job'].at_time.strftime("%H:%M:%S"), axis = 1)
        df_jobs['segundos_ejecucion'] = df_jobs.apply(lambda row: row['job'].period.total_seconds(), axis = 1)
        df_jobs['ultima_ejecucion_utc'] = df_jobs.apply(lambda row: row['job'].last_run.astimezone(pytz.utc) if row['job'].last_run!=None else None, axis = 1)
        df_jobs['ultima_ejecucion_utc'] = (df_jobs['ultima_ejecucion_utc'].astype(str).replace({'NaT': None}))
        df_jobs['proxima_ejecucion_utc'] = df_jobs.apply(lambda row: row['job'].next_run.astimezone(pytz.utc) if row['job'].next_run!=None else None, axis = 1)
        
        #print(df_jobs)        

        for proceso in df_jobs.itertuples():
            if proceso.ultima_ejecucion_utc!=None and proceso.ultima_ejecucion_utc!='None':
                info = {'nombre': nombre_app, 'segundos_ejecucion': proceso.segundos_ejecucion, 'proxima_ejecucion_utc': proceso.proxima_ejecucion_utc, 'ultima_ejecucion_utc': proceso.ultima_ejecucion_utc}
            else:
                info = {'nombre': nombre_app, 'segundos_ejecucion': proceso.segundos_ejecucion, 'proxima_ejecucion_utc': proceso.proxima_ejecucion_utc}

            update_estado_app = MonitorizaApps.objects.using("spida"
                        ).filter(nombre_ejecutable = proceso.nombre_ejecutable, 
                                 nombre_proceso = proceso.nombre_proceso
                        ).update(**info)
            
            if not update_estado_app:
                if proceso.ultima_ejecucion_utc!=None and proceso.ultima_ejecucion_utc!='None':
                    info = {'num_periodos_alarma':2,
                            'nombre': nombre_app,
                            'nombre_ejecutable': proceso.nombre_ejecutable,
                            'nombre_proceso': proceso.nombre_proceso,
                            'segundos_ejecucion': proceso.segundos_ejecucion, 
                            'proxima_ejecucion_utc': proceso.proxima_ejecucion_utc,
                            'ultima_ejecucion_utc': proceso.ultima_ejecucion_utc}
                else:
                    info = {'num_periodos_alarma':2,
                            'nombre': 'Monitoriza Spida',
                            'nombre_ejecutable': proceso.nombre_ejecutable,
                            'nombre_proceso': proceso.nombre_proceso,
                            'segundos_ejecucion': proceso.segundos_ejecucion, 
                            'proxima_ejecucion_utc': proceso.proxima_ejecucion_utc}
                
                MonitorizaApps.objects.using("spida").create(**info)
    
    except Exception as e:
        print("ERROR Monitoriza Procesos", e)
        #global logger
        #logger.error("Se ha producido un error en la monitorizacion del estado de los procesos. Excepcion: %s", e, exc_info=True)


def run_threaded(job_func, args_func = None):
    if args_func==None: # Para funciones que no tiene parametros de entrada 
        job_thread = threading.Thread(target=job_func)
    else: # Para funciones que tienen parametros de entrada 
        job_thread = threading.Thread(target=job_func, args=args_func)
    job_thread.start()


def run_threaded_only_one(job_func, args_func = None):
    name_threads = []
    for thread in threading.enumerate(): 
        name_threads.append(thread.name)
    
    # Solo creo el nuevo hilo si no se esta ejecutando ya uno
    if job_func.__name__ not in name_threads:
        if args_func==None: # Para funciones que no tiene parametros de entrada 
            job_thread = threading.Thread(target=job_func, name=job_func.__name__)
        else: # Para funciones que tienen parametros de entrada 
            job_thread = threading.Thread(target=job_func, name=job_func.__name__, args=args_func)

        job_thread.start()

def round_minutes(dt, resolution, direction = 'up'): #'up', 'down'
    new_minute = (dt.minute // resolution + (1 if direction == 'up' else 0)) * resolution
    fecha_hora = dt + timedelta(minutes=new_minute - dt.minute)
    return fecha_hora.replace(second=0, microsecond=0)

def worker_main(jobqueue):
    while 1:
        #Cuando necesito introducir parametros de entrada en una funcion
        job_func, job_args = jobqueue.get()
        job_func(*job_args)
        jobqueue.task_done()





