
from asyncio.windows_events import NULL
from io import TextIOBase
from queue import PriorityQueue
from tkinter import  Tk, Button, Entry, Label, ttk, PhotoImage
from tkinter import  StringVar,Scrollbar,Frame
from tkinter import messagebox
import msvcrt
import os
from os import remove
from tkinter import *
from tkinter import ttk
import tkinter as tk
from typing import ItemsView, Literal, ValuesView
from tkinter import filedialog as fd 
import shutil
import time
import os.path
import pymongo
import threading
from tkcalendar import DateEntry
from datetime import datetime 
from pymongo import MongoClient
from PIL import ImageTk
from PIL import Image as ImagePIL
from arrow import utcnow, get
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import black, purple, white, blue
from reportlab.pdfgen import canvas


path = 'C:\\Users\\dhe_e\\Downloads\\taller\\main.py'
  
dirname = os.path.dirname(path) 

class reportePDF(object):
    
    
    def __init__(self, titulo, cabecera, datos, nombrePDF):
        super(reportePDF, self).__init__()

        self.titulo = titulo
        self.cabecera = cabecera
        self.datos = datos
        self.nombrePDF = nombrePDF

        self.estilos = getSampleStyleSheet()

    @staticmethod
    def _encabezadoPiePagina(canvas, archivoPDF):
        canvas.saveState()
        estilos = getSampleStyleSheet()

        alineacion = ParagraphStyle(name="alineacion", alignment=TA_RIGHT,
                                    parent=estilos["Normal"])
 
        # Encabezado
        encabezadoNombre = Paragraph('CEEDISC "EL SUEÑO DEL COLIBRÍ" ', estilos["Normal"])
        anchura, altura = encabezadoNombre.wrap(archivoPDF.width, archivoPDF.topMargin)
        encabezadoNombre.drawOn(canvas, archivoPDF.leftMargin, 37)

        encabezadoImg = Image('log.jpg', 60 * mm,20 * mm)
        anchura, altura = encabezadoImg.wrap(archivoPDF.width, archivoPDF.topMargin)
        encabezadoImg.drawOn(canvas, archivoPDF.leftMargin, 720)

        fecha = utcnow().to("local").format("dddd, DD - MMMM - YYYY", locale="es")
        fechaReporte = fecha.replace("-", "de")

        encabezadoFecha = Paragraph(fechaReporte, alineacion)
        anchura, altura = encabezadoFecha.wrap(archivoPDF.width, archivoPDF.topMargin)
        encabezadoFecha.drawOn(canvas, archivoPDF.leftMargin, 736)
 
        # Pie de página
        piePagina = Paragraph("Reporte de Citas", estilos["Normal"])
        anchura, altura = piePagina.wrap(archivoPDF.width, archivoPDF.bottomMargin)
        piePagina.drawOn(canvas, archivoPDF.leftMargin, 15 * mm + (0.2 * inch))
 
        # Suelta el lienzo
        canvas.restoreState()

    def convertirDatos(self):

        estiloEncabezado = ParagraphStyle(name="estiloEncabezado", alignment=TA_LEFT,
                                          fontSize=10, textColor=white,
                                          fontName="Helvetica-Bold",
                                          parent=self.estilos["Normal"])

        estiloNormal = self.estilos["Normal"]
        estiloNormal.alignment = TA_LEFT

        claves, nombres = zip(*[[k, n] for k, n in self.cabecera])

        encabezado = [Paragraph(nombre, estiloEncabezado) for nombre in nombres]
        nuevosDatos = [tuple(encabezado)]

        for dato in self.datos:
            nuevosDatos.append([Paragraph(str(dato[clave]), estiloNormal) for clave in claves])
            
        return nuevosDatos
        
    def Exportar(self):

        alineacionTitulo = ParagraphStyle(name="centrar", alignment=TA_CENTER, fontSize=13,
                                          leading=10, textColor=purple,
                                          parent=self.estilos["Heading1"])
        
        self.ancho, self.alto = letter

        convertirDatos = self.convertirDatos()
    
        tabla = Table(convertirDatos, colWidths=(self.ancho-100)/len(self.cabecera), hAlign="CENTER")
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0),(-1, 0), purple),
            ("ALIGN", (0, 0),(0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), # Texto centrado y alineado a la izquierda
            ("INNERGRID", (0, 0), (-1, -1), 0.50, black), # Lineas internas
            ("BOX", (0, 0), (-1, -1), 0.25, black), # Linea (Marco) externa
            ]))

        historia = []
        historia.append(Paragraph(self.titulo, alineacionTitulo))
        historia.append(Spacer(1, 0.16 * inch))
        historia.append(tabla)

        archivoPDF = SimpleDocTemplate(self.nombrePDF, leftMargin=50, rightMargin=50, pagesize=letter,
                                       title="Reporte PDF")
        
        try:
            archivoPDF.build(historia, onFirstPage=self._encabezadoPiePagina,
                             onLaterPages=self._encabezadoPiePagina,
                             canvasmaker=numeracionPaginas)
            
         # +------------------------------------+
            return "Reporte generado con éxito."
         # +------------------------------------+
        except PermissionError:
         # +--------------------------------------------+  
            return "Error inesperado: Permiso denegado."
         # +--------------------------------------------+


# ================== CLASE numeracionPaginas =======================

class numeracionPaginas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """Agregar información de la página a cada página (página x de y)"""
        numeroPaginas = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(numeroPaginas)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
    def draw_page_number(self, conteoPaginas):
        self.drawRightString(204 * mm, 15 * mm + (0.2 * inch),
                             "Página {} de {}".format(self._pageNumber, conteoPaginas))        


# ===================== FUNCIÓN generarReporte =====================
  

class Ventana(Frame):
	def __init__(self, master, *args):
		super().__init__( master,*args)
		
		self.menu = True
		self.color = True

		self.id = StringVar()
		self.frame_inicio = Frame(self.master, bg='#18181b', width=50, height=45)
		self.frame_inicio.grid_propagate(0)
		self.frame_inicio.grid(column=0, row = 0, sticky='nsew')

		
		self.frame_menu = Frame(self.master, bg='#1f1f23', width = 170)
		self.frame_menu.grid_propagate(0)
		self.frame_menu.grid(column=0, row = 1, sticky='nsew')

		self.frame_top = Frame(self.master, bg='#18181b', height = 50)
		self.frame_top.grid(column = 1, row = 0, sticky='nsew')

		self.frame_principal = Frame(self.master, bg='black')
		self.frame_principal.grid(column=1, row=1, sticky='nsew')
		self.master.columnconfigure(1, weight=1)
		self.master.rowconfigure(1, weight=1)
		self.frame_principal.columnconfigure(0, weight=1)
		self.frame_principal.rowconfigure(0, weight=1)
		
		self.widgets()
		

	def pantalla_inicial(self):
		self.paginas.select([self.frame_uno])
	
	def option(self,evento):
		
		self.f1=Frame(self.frame_dos,width=188,height=125,bg='#d9d9d9')
		self.f1.place(x=450,y=490)
	
		def dele(evento):
			self.f1.destroy()
		self.f1.bind('<Leave>',dele)
		#buttons
		def bttn(x,y,text,bcolor,fcolor,cmd):
			myButton1 = Button(self.f1,text=text,
						width=20,
						height=1,
						border=1,
						bg=fcolor,      
							command=cmd)
			myButton1.place(x=x,y=y)
		bttn(0,0,'Editar...','#d9d9d9','#d9d9d9',None)
		bttn(0,30,'Editar Imagen','#d9d9d9','#d9d9d9',self.editImg)

	def d(self,evento):
		def dele(evento):
			self.f1.destroy()
		self.f1.bind("<Leave>",dele)
		
		
	def autopublicacion(self):
		self.paginas.select([self.frame_dos])
		self.frame_dos.columnconfigure(0, weight=1)
		self.frame_dos.columnconfigure(1, weight=1)
		self.frame_dos.rowconfigure(2, weight=1)
	
		frame1=ttk.LabelFrame(self.frame_dos, text="PUBLICACION :", style = "Red.TLabelframe")        
		frame1.place(x=0,y=0)
		fram=ttk.LabelFrame(frame1, text="IMAGEN :", style = "Red.TLabelframe")        
		fram.grid(column=0, row=1,  padx=20, pady=20, sticky="we")

		self.b = Button(self.frame_dos,text="Editar...",
						
						fg='#262626',
						border=1,
						
						activeforeground='#262626',
						width= 20,          
							command=self.option)
		self.b.place(x=450,y=490)
		self.b.bind("<Enter>", self.option)
		self.b.bind("<Leave>", self.d)

		with open("datos.txt") as f:
			lines = f.read()
			first = lines.split('\n', 1)[0]
		
		img = ImagePIL.open("imagen.png")
		
		newImg=img.resize((400,300))
		render= ImageTk.PhotoImage(newImg)
		
		img1 = Label(fram, image = render)
		img1.image=render
		img1.grid(column=0, row=0,  padx=0, pady=0, sticky="we")

		frame=ttk.LabelFrame(frame1, text="MENSAJE :", style = "Red.TLabelframe")        
		frame.grid(column=1, row=1, padx=0, pady=0)
		text_frame = tk.Frame(frame)
		self.textArea=tk.Text(text_frame, width=47, height=21)
		
		self.textArea.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
		textScroll=ttk.Scrollbar(text_frame, command=self.textArea.yview)
		textScroll.pack(fill=tk.Y, side=tk.RIGHT)
		text_frame.grid(column=0, row=0,  padx=0, pady=23, sticky="we")

		self.textArea.config(yscrollcommand=textScroll.set)
		
		fichero = open('mensaje.txt', 'r', encoding='utf-8')
		self.contenido = fichero.read()
		self.textArea.delete(1.0,'end')
		self.textArea.insert('insert', self.contenido)
		
			
		
		

		self.boton=ttk.Button(self.frame_dos, text='Guardar', command=lambda:[self.editMsg()],width=14)
		self.boton.place(x=450,y=415)
		
		boton=ttk.Button(self.frame_dos, text='Publicar Ahora en Facebook', command=self.AutoposterFacebook,width=20)
		boton.place(x=660,y=490)
		boton=ttk.Button(self.frame_dos, text='Publicar Ahora en Twitter', command=self.AutoposterTwitter,width=20)
		boton.place(x=660,y=520)
		boton=ttk.Button(self.frame_dos, text='PUBLICAR AHORA', command=self.publicar,width=20)
		boton.place(x=660,y=550)


	def mensajes(self):
		self.paginas.select([self.frame_tres])
		

	def botkit(self):

		self.paginas.select([self.frame_cuatro])	
		self.frame_cuatro.columnconfigure(0, weight=1)
		self.interfaz_inicial()

        # LABEL PARA MENSAJES DE SALIDA
		self.message = Label(text = '')
		self.message.grid(row = 6, column = 0, columnspan = 5, sticky = W + E, padx = 150)
		# TABLA
		frame2 = LabelFrame(self.frame_cuatro, text=' Arbol de Respuestas: ')
		frame2.grid(row = 7, column = 0, columnspan = 3, padx = 20, pady = 15)

		self.tree = ttk.Treeview(frame2, height = 10, columns=("#1"))
		self.tree.grid(row = 7, column = 0, columnspan = 2, padx = 20, pady = 10)
		self.tree.heading("#0", text="Palabra Clave", anchor = CENTER)         
		self.tree.heading("#1", text="Response", anchor = CENTER)
		# SCROLL VERTICAL TREEVIEW
		scrolvert = Scrollbar(frame2, command = self.tree.yview)
		scrolvert.grid(row=7, column=2, sticky="nsew")
		self.tree.config(yscrollcommand=scrolvert.set)
		# SCROLL HORIZONTAL TREEVIEW
		scrolhoriz = Scrollbar(frame2, command = self.tree.xview, orient='horizontal')
		scrolhoriz.grid(row=12, column=0, columnspan=2, sticky="news")
		self.tree.config(xscrollcommand=scrolhoriz.set)
		ejemplo_dir=dirname+'\\botkit-starter-web\\skills\\'
		car=dirname+'\\botkit-starter-web\\skills\\'
		self.cont=[]
		contenido = os.listdir(ejemplo_dir)
		for fichero in contenido:
			with open(car+fichero, encoding='utf-8', errors='ignore') as f:
				padre = f.readlines()[0].strip()
				
			with open(car+fichero, encoding='utf-8', errors='ignore') as f:
				strkey = f.readlines()[1].strip()
				self.cont.append(strkey)
				
			with open(car+fichero, encoding='utf-8', errors='ignore') as f:
				mensaje = f.readlines()[2].strip()
			for x in range(len('//')):
				padre = padre.replace('//'[x],"")
				
			for x in range(len('//')):
				mensaje = mensaje.replace('//'[x],"")
				
			for x in range(len('//')):
				strkey = strkey.replace('//'[x],"")	
			
			
			if fichero!='message_history.js' and fichero!='_connection_events.js'and fichero!='demo_quick_replies.js'and fichero!='sample_hears.js'and fichero!='super_quit.js' and fichero!='unhandled_messages.js'and fichero!='groserias.js'and padre not in fichero :
				
						#op2 = linecache.getline(car+fichero, 3).strip()
						#op3 = linecache.getline(car+fichero, 4).strip()
						#op4 = linecache.getline(car+fichero, 5).strip()
				self.tree.insert('', 'end', fichero, text=strkey, values=[mensaje,padre,fichero])
				
			if padre in fichero:
				
				self.tree.insert(padre, 'end', fichero, text=strkey, values=[mensaje,padre,fichero])
		
		self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)
		item = self.tree.identify_row(0)
		self.tree.selection_set(item)
		self.tree.focus(item)
		
		boton2=tk.Button(self.frame_cuatro,text='Crear Padre', command=self.crearPadre)
		boton2.grid(row = 13, column = 0, columnspan=2, ipadx = 50, pady = 10)
		boton2=tk.Button(self.frame_cuatro,text='Crear Hijos', command=self.add_Hijos)
		boton2.place(x=127,y=487, widt=180)

		boton2=tk.Button(self.frame_cuatro,text='Eliminar chat', command=self.eliminarChat)
		boton2.place(x=600,y=487, widt=180)

	def salir(self):
		ventana.destroy()

	
	def cita(self):
		
		self.paginas.select([self.frame_siete])
		self.frame_tabla_siete = Frame(self.frame_siete, bg= 'gray90')
		self.frame_tabla_siete.grid(row=0,column=0, sticky='nsew')		
		self.tabla_siete = ttk.Treeview(self.frame_tabla_siete) 
		self.tabla_siete.grid(column=0, row=0, sticky='nsew')
		ladox = ttk.Scrollbar(self.frame_tabla_siete, orient = 'horizontal', command= self.tabla_siete.xview)
		ladox.grid(column=0, row = 1, sticky='ew') 
		ladoy = ttk.Scrollbar(self.frame_tabla_siete, orient ='vertical', command = self.tabla_siete.yview)
		ladoy.grid(column = 1, row = 0, sticky='ns')
		
	
		for documento in self.coletionform.find({}, {'hora':1,'nombre':1,'apellido':1,'email':1,'telf':1,'servicio':1,'fecha_cita':1}).sort('createdAt',1):
					hor=documento['hora']
					no=documento['nombre']
					ap=documento['apellido']
					em=documento['email']
					te=documento['telf']
					se=documento['servicio']
		
					
					self.tabla_siete.insert('',0,text=documento["fecha_cita"],values=[hor,no,ap,em,te,se])
					
				
        

		self.tabla_siete.configure(xscrollcommand = ladox.set, yscrollcommand = ladoy.set)
		self.tabla_siete['columns'] = ('hora','nombre', 'apellido','email','telf','servicio')
		self.tabla_siete.column('#0', minwidth=100, width=50, anchor='w')
		self.tabla_siete.column('hora', minwidth=100, width=100 , anchor='w')
		self.tabla_siete.column('nombre', minwidth=100, width=100 , anchor='w')
		self.tabla_siete.column('apellido', minwidth=100, width=100, anchor='w' )
		self.tabla_siete.column('email', minwidth=100, width=150, anchor='w' )
		self.tabla_siete.column('telf', minwidth=100, width=100, anchor='w' )
		self.tabla_siete.column('servicio', minwidth=100, width=100, anchor='w' )

		self.tabla_siete.heading('#0', text='Fecha')
		self.tabla_siete.heading('hora', text='Hora', anchor ='center')
		self.tabla_siete.heading('nombre', text='Nombres', anchor ='center')
		self.tabla_siete.heading('apellido', text='Apellidos', anchor ='center')
		self.tabla_siete.heading('email', text='Correo', anchor ='center')
		self.tabla_siete.heading('telf', text='Telefono', anchor ='center')
		self.tabla_siete.heading('servicio', text='Servicio', anchor ='center')

		frame = LabelFrame (self.frame_siete, text='Reporte de citas')
		frame.grid(row = 1, column= 0, columnspan=3, pady= 5,padx=5, sticky='w')
		Label(frame, text='Introduzca fecha inicial').grid(row = 0, column = 0)

		Label(frame, text='Introduzca fecha final').grid(row = 1, column = 0)
		ttk.Button(frame, text='  Generar reporte de citas  ', command=lambda:[self.report()] ).grid(row = 3, column= 1, columnspan=3, padx= 13)
		

	
		self.cal =DateEntry(frame,selectmode='day',date_pattern='MM-dd-yyyy',background='darkblue',foreground='white',showweeknumbers=False,firstweekday='sunday')
		self.cal.grid(row = 0, column= 1, columnspan=3, pady= 10)
		self.cal1 =DateEntry(frame,selectmode='day',date_pattern='MM-dd-yyyy',background='darkblue',foreground='white',showweeknumbers=False,firstweekday='sunday')
		self.cal1.grid(row = 1, column= 1, columnspan=3, pady= 10)


		frame1 = LabelFrame (self.frame_siete, text='Reporte de crecimiento')
		frame1.grid(row = 2, column= 0, columnspan=3, pady= 5,padx=5, sticky='w')
		Label(frame1, text='Introduzca fecha inicial').grid(row = 0, column = 0)

		Label(frame1, text='Introduzca fecha final').grid(row = 1, column = 0)
		ttk.Button(frame1, text='Generar reporte de crecimiento', command=self.reportCrecimiento).grid(row = 3, column= 1, columnspan=3, pady= 10)
        

		self.call =DateEntry(frame1,selectmode='day',date_pattern='MM-dd-yyyy',background='darkblue',foreground='white',showweeknumbers=False,firstweekday='sunday')
		self.call.grid(row = 0, column= 1, columnspan=3, pady= 10)
		self.call1 =DateEntry(frame1,selectmode='day',date_pattern='MM-dd-yyyy',background='darkblue',foreground='white',showweeknumbers=False,firstweekday='sunday')
		self.call1.grid(row = 1, column= 1, columnspan=3, pady= 10)
		
	
	def menu_lateral(self):
		self.frame_menu.update()
	
	def widgets(self):
		########################CONEXION DE LA BASE DE DATOS#########################
		MONGO_HOST="localhost"
		MONGO_PUERTO="27017"
		self.MONGO_TIEMPO_FUERA=1000
		self.MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"
		self.MONGO_BASEDATOS="botkit"
		self.MONGO_COLECCION="histories"
		self.MONGO_COLECCIONFORM="formularios"
		cliente=pymongo.MongoClient("mongodb+srv://Dhery:computadora@cluster0.quh68.mongodb.net")
		baseDatos=cliente[self.MONGO_BASEDATOS]
		self.coleccion=baseDatos[self.MONGO_COLECCION]
		self.coletionform = baseDatos[self.MONGO_COLECCIONFORM]

		self.logo = PhotoImage(file ='logo.png')
		
		self.bt_inicio = Button(self.frame_inicio, command = self.pantalla_inicial, text="Inicio", fg='white',cursor="hand2", bg='#464649', width=12, relief="flat", font=("Comic Sans MS",12, "bold"))
		self.bt_inicio.grid(column=0, row=0, padx=5, pady=10)
		
		
		

		#BOTONES Y ETIQUETAS DEL MENU LATERAL 
		
		
		Button(self.frame_menu, text="Autopublicacion",cursor="hand2" ,font=('Arial',8,'bold') 	,fg='white', bg='#3a3a3d',  command=self.autopublicacion, width=23, height=3).grid(column=0, row=2, pady=0,padx=0)
		Button(self.frame_menu, text="Registro de Mensajes" ,cursor="hand2",font=('Arial',8,'bold'), fg='white',bg='#3a3a3d', command =self.mensajes, width=23, height=3 ).grid(column=0, row=4, pady=0,padx=0)
		Button(self.frame_menu,  text="Botkit" ,cursor="hand2",font=('Arial',8,'bold'), fg='white',bg='#3a3a3d', command = self.botkit, width=23, height=3).grid(column=0, row=3, pady=0,padx=0)
		Button(self.frame_menu, text="Citas" ,cursor="hand2",font=('Arial',8,'bold'), fg='white',bg='#3a3a3d', bd=0, command = self.cita, width=23, height=3).grid(column=0, row=5, pady=0,padx=0)		
		Button(self.frame_menu, text="Salir" ,cursor="hand2",font=('Arial',8,'bold'), fg='white',bg='#3a3a3d', bd=0, command = self.salir, width=23, height=3).grid(column=0, row=6, pady=0,padx=0)		

		#############################  CREAR  PAGINAS  ##############################
	
		#CREACCION DE LAS PAGINAS 
		self.paginas = ttk.Notebook(self.frame_principal , style= 'TNotebook') 
		self.paginas.grid(column=0,row=0, sticky='nsew')
		self.frame_uno = Frame(self.paginas, bg='DarkOrchid1')
		self.frame_dos = Frame(self.paginas, bg='#dadada')
		self.frame_tres = Frame(self.paginas, bg='#dadada')
		self.frame_cuatro = Frame(self.paginas, bg='#dadada')
		
		
		self.frame_siete= Frame(self.paginas, bg='#dadada')
		self.paginas.add(self.frame_uno)
		self.paginas.add(self.frame_dos)
		self.paginas.add(self.frame_tres)
		self.paginas.add(self.frame_cuatro)
		
	
		self.paginas.add(self.frame_siete)

		##############################         PAGINAS       #############################################

		######################## FRAME TITULO #################
		self.titulo = Label(self.frame_top,text= 'CENTRO DE ENSEÑANZA Y ESTIMULACION DEL DESARROLLO INTEGRAL EL SUEÑO DEL COLIBRI', bg='black', fg= 'DarkOrchid1', font= ('Imprint MT Shadow', 12, 'bold'))
		self.titulo.pack(expand=1)

		######################## VENTANA PRINCIPAL #################

		Label(self.frame_uno, text= 'Bienvenido', bg='DarkOrchid1', fg= 'white', font= ('Freehand521 BT', 20, 'bold')).pack(expand=1)
		Label(self.frame_uno ,image= self.logo, bg='DarkOrchid1').pack(expand=1)
		
		######################## MOSTRAR TODOS LOS PRODUCTOS DE LA BASE DE DATOS MYSQL #################
		
		#ESTILO DE LAS TABLAS DE DATOS TREEVIEW
		estilo_tabla = ttk.Style()
		estilo_tabla.configure("Treeview", font= ('Helvetica', 10, 'bold'), foreground='black',  background='white')  #, fieldbackground='yellow'
		estilo_tabla.map('Treeview',background=[('selected', 'DarkOrchid1')], foreground=[('selected','black')] )		
		estilo_tabla.configure('Heading',background = 'white', foreground='navy',padding=3, font= ('Arial', 10, 'bold'))
		estilo_tabla.configure('Item',foreground = 'white', focuscolor ='DarkOrchid1')
		estilo_tabla.configure('TScrollbar', arrowcolor = 'DarkOrchid1',bordercolor  ='black', troughcolor= 'DarkOrchid1',background ='white')

		#TABLA SIETE
		
		

		#TABLA TRES mensaje botkit
		
		

		boton=ttk.Button(self.frame_tres, text='Buscar mensaje Usuario', command=self.OnDoubleClick).place(x=0,y=300)
        
		self.frame_tabla_uno = Frame(self.frame_tres, bg= 'gray90')
		self.frame_tabla_uno.grid(columnspan=3, row=2, sticky='nsew')		
		self.tabla_uno = ttk.Treeview(self.frame_tabla_uno) 
		self.tabla_uno.grid(column=0, row=0, sticky='nsew')
		ladox = ttk.Scrollbar(self.frame_tabla_uno, orient = 'horizontal', command= self.tabla_uno.xview)
		ladox.grid(column=0, row = 1, sticky='ew') 
		ladoy = ttk.Scrollbar(self.frame_tabla_uno, orient ='vertical', command = self.tabla_uno.yview)
		ladoy.grid(column = 1, row = 0, sticky='ns')
	
		for documento in self.coleccion.find({}, {'message.text':1,'_id':0,'date':1,'userId':1}).sort('date',1):
					
					a=documento['date']
					s=documento['message']
					self.tabla_uno.insert('',0,text=documento["userId"],values=[a,s])
					
				
        

		self.tabla_uno.configure(xscrollcommand = ladox.set, yscrollcommand = ladoy.set)
		self.tabla_uno['columns'] = ('Fecha', 'Mensaje')
		self.tabla_uno.column('#0', minwidth=250, width=270, anchor='center')
		self.tabla_uno.column('Fecha', minwidth=250, width=270 , anchor='center')
		self.tabla_uno.column('Mensaje', minwidth=800, width=270, anchor='w' )
		

		self.tabla_uno.heading('#0', text='id', anchor ='center')
		self.tabla_uno.heading('Fecha', text='Fecha', anchor ='center')
		self.tabla_uno.heading('Mensaje', text='Mensaje', anchor ='center')
		
		Label(self.frame_cuatro, text = 'BotKit',fg='purple',bg='#dadada', font=('Kaufmann BT',24,'bold')).grid(columnspan= 4,  row=0,sticky='nsew',padx=2)
		Label(self.frame_tres, text = 'Registro de mensajes',fg='purple',bg='#dadada', font=('Kaufmann BT',24,'bold')).grid(columnspan= 4,  row=0,sticky='nsew',padx=2)
		Label(self.frame_siete, text = 'Citas',fg='purple',bg='#dadada', font=('Kaufmann BT',24,'bold')).grid(columnspan= 4,  row=0,sticky='nsew',padx=2)
		
		#TABLA DOS
		

		######################## AJUSTES #################

	 
		
		

	def editMsg(self):
		b=self.textArea.get(1.0,'end-1c')
		caracteres = len(b)
		largo= 280
		if caracteres > largo:
			return self.errorCaracteres(), self.autopublicacion()
		else:
			if 'mensaje.txt' != "":
				self.contenido = self.textArea.get(1.0,'end-1c')
				fichero = open('mensaje.txt', 'w+', encoding='utf-8')
				fichero.write(self.contenido)
				fichero.close()
				
	
	def Autoposter(self):
		os.system("python FacebookPoster.py")
		
	def AutoposterFacebook(self):
		
		x = threading.Thread(target=self.Autoposter)
		x.start()
			# code while computing
		self.espere()
		
		
		
			#self.Twitter()
		
		return self.autopublicacion()
	def Three(self):
		os.system("python TwitterPoster.py")
	def AutoposterTwitter(self):
		
		x = threading.Thread(target=self.Three)
		x.start()
			# code while computing
		self.espere()
		
		
		
			#self.Twitter()
		
		return self.autopublicacion()
	def publicar(self):
		
		x = threading.Thread(target=self.Three)
		x.start()
		y = threading.Thread(target=self.Autoposter)
		y.start()
			# code while computing
		self.espere()
		
		
		
			#self.Twitter()
		
		return self.autopublicacion()
	
	def editEnl(self):
		os.system("python3 editarGrupos.py")
		return self.autopublicacion()
	def report(self):
		self.generarReporte()
		
		self.reportcitas()
		return self.cita()
	def reportCrecimiento(self):
		self.generarReporteC()
		self.reportcitasC()
		
		return self.cita()


	def crearPadre(self):
		win=tk.Toplevel()
		win.geometry('400x400+500+50')
		self.keyword=StringVar()
		self.sentence=StringVar()
		text=tk.Label(win, text='REGISTRO DE PALABRAS')
		text.place(x=140,y=10)
		text=tk.Label(win, text='Introduzca la palabra clave: ')
		text.place(x=10,y=50)
		entrada=tk.Entry(win, textvar=self.keyword,width=22,relief="flat")
		entrada.place(x=200, y=50)
		text=tk.Label(win, text='Introduzca la respuesta: ')
		text.place(x=10,y=100)
		entrada=tk.Entry(win, textvar=self.sentence,width=22,relief="flat")
		entrada.place(x=200, y=100)

		
		boton=ttk.Button(win, text='Guardar charla', command=lambda:[self.add_padre(),win.destroy()])
		boton.place(x=50,y=350)
		
		boton=ttk.Button(win, text='Cancelar', command=win.destroy)
		boton.place(x=270,y=350)
	def add_Hijos(self):
    	
		win=tk.Toplevel()
		win.title("Crear opciones")
		win.geometry('390x180+500+50')
		self.options=IntVar()
		
		
		
		frame = LabelFrame (win, text='Numero de opciones')
		frame.grid(row = 0, column= 0, columnspan=3, pady= 5,padx=5)
		Label(frame, text='Introduzca el Numero de opciones').grid(row = 0, column = 0)
		tk.Entry(frame,textvar=self.options,width=22,relief="flat").grid(row = 0, column= 1, columnspan=3, pady= 10)
	
	
		ttk.Button(win, text='Crear opciones', command=lambda:[self.crearHijos(),self.botkit(),win.destroy()]).grid(row = 5, column=0)
		ttk.Button(win, text='Cancelar', command=win.destroy).grid(row = 5, column=2 )

	def add_padre(self):
		ejemplo_dir = dirname+'\\botkit-starter-web\\skills\\'
		b=self.keyword.get().strip()
		c=self.sentence.get().strip()


		with os.scandir(ejemplo_dir) as ficheros:
			lista = []
			for fichero in ficheros:
				lista.append(fichero.name)
			if lista.count(b+'.js')>=1:
				self.errPalabraClave()
				return self.botkit()
			else:
				file = open(dirname+'\\botkit-starter-web\\skills\\'+b.strip()+'.js', 'w', encoding='utf-8', errors='ignore')
				file.write('//'+'\n')
				file.write('//'+b+'\n')
				file.write('//'+c+'\n')
				file.write('module.exports = function(controller){')
				file.write('controller.hears(')
				file.write('"')
				file.write(b)
				file.write('"')
				file.write(',"message_received",function(bot,message){bot.reply(message,{text:')
				file.write('"'+c+'",\nquick_replies:[\n]},function() { });});}')
				file.close()
					
				
			
		return self.botkit()
	
	def editUs(self):
		
		win=tk.Toplevel()
		win.title("Editar Usuario de Facebook")
		win.geometry('390x180+500+50')
		self.usuarioFace=StringVar()
		self.passwordFace=StringVar()
		frame = LabelFrame (win, text='Register')
		frame.grid(row = 0, column= 0, columnspan=3, pady= 5,padx=5)
		Label(frame, text='Introduzca el Usuario').grid(row = 0, column = 0)
		self.entrada1=tk.Entry(frame,textvar=self.usuarioFace,width=22,relief="flat").grid(row = 0, column= 1, columnspan=3, pady= 10)
		
		self.entrada2=tk.Entry(frame,textvar=self.passwordFace, width=22,show="*",relief="flat").grid(row = 1, column= 1, columnspan=3, pady= 10)
		Label(frame, text='Introduzca la contraseña').grid(row = 1, column = 0)

		ttk.Button(win, text='guardar usuario', command=self.Usss).grid(row = 5, column=0)
		ttk.Button(win, text='Cancelar', command=win.destroy).grid(row = 5, column=2 )

	def Usss(self):
		ObjFichero = open(dirname+"\\Admin\\datos.txt",'w')
		MiNuevoTexto = self.usuarioFace.get()+'\n'+self.passwordFace.get()
		ObjFichero.write(MiNuevoTexto)
		ObjFichero.close()
		self.usuario()

	def crearHijos(self):
		data = self.tree.selection()[0]
		idd=self.tree.item(data,"values")
		padre = self.tree.item(data,"text")
		b=idd[0]
		c=self.options.get()
		contenedor=[]
		for i in range(c):
			contenedor.append("{title: "+'"vacio' +str (i)+'"' +",payload:"+'"vacio' +str (i)+'"' +",},")

		busqueda= 'quick_replies:['
		
		with open(dirname+'\\botkit-starter-web\\skills\\'+idd[2], "rt", encoding='utf-8', errors='ignore') as file:
			x = file.read()
		with open(dirname+'\\botkit-starter-web\\skills\\'+idd[2], "wt") as file:
			Str = "".join(contenedor)
			x = x.replace(busqueda,'quick_replies:['+Str)
			file.write(x)
			file.tell()
			file.seek(0,2)
			file.write('\n')
			file.write('//option'+str(c))
		for i in range(c):
			file = open(dirname+'\\botkit-starter-web\\skills\\'+idd[2]+'hijoNro'+str(i)+'vacio'+'.js', "w")
			file.write('//'+idd[2]+'\n')
			file.write('//Escriba palabra clave'+'\n')
			file.write('//Escriba respuesta a la palabra clave'+'\n')
			file.write('module.exports = function(controller){')
			file.write('controller.hears(')
			file.write('"')
			file.write('Escriba palabra clave')
			file.write('"')
			file.write(',"message_received",function(bot,message){bot.reply(message,{text:')
			file.write('"'+'Escriba respuesta a la palabra clave'+'",\nquick_replies:[\n]},function() { });});}')
			file.close()
			

	def editImg(self):
		name= fd.askopenfilename(filetypes=(('image files', '.png ;.jpg'),))
		if 'img.txt' != "":
			fichero = open('img.txt', 'w+')
			fichero.write(name)
			fichero.close()
			
		shutil.copy(name, "imagen.png")
		return self.autopublicacion()
	
	
	def eliminarChat(self):
		
		data = self.tree.selection()[0]
		idd=self.tree.item(data,"values")


		remove(dirname+'\\botkit-starter-web\\skills\\'+idd[2])
		return self.botkit()

	
	def OnDoubleClick(self):
		self.win=tk.Toplevel()
		self.Ntabla=ttk.Treeview(self.win,columns=[f"#{n}" for n in range(1, 3)])
		self.Ntabla.grid(row=0,column=0,columnspan=1)
		item1 = self.tabla_uno.selection()[0]
		self.Ntabla.column("#0",minwidth=0,width=500, stretch=NO)
		self.Ntabla.heading("#0",text="Mensaje del bot")
		self.Ntabla.heading("#1",text="Fecha")
		self.Ntabla.column("#1",minwidth=0,width=200, stretch=NO) 
		self.Ntabla.heading("#2",text="Id")
		self.Ntabla.column("#2",minwidth=0,width=400, stretch=NO)
		idd=self.tabla_uno.item(item1,"text")
		for documento in self.coleccion.find({ 'userId': { '$eq': idd }}, {'message.type':1,'message.text':1,'_id':0,'date':1,'userId':1}).sort('date',1):
					a=documento['date']
					s=documento['userId']
					self.Ntabla.insert('',0,text=documento["message"],values=[a,s])
		
		
		
	def generarReporte(self):
		dt=self.cal.get_date()
		fechainicio=dt.strftime("%Y-%m-%d")
		dt=self.cal1.get_date()
		fechafin=dt.strftime("%Y-%m-%d")
	
		myclient = pymongo.MongoClient( "mongodb+srv://Dhery:computadora@cluster0.quh68.mongodb.net")
		mydb = myclient["botkit"]
		mycol = mydb["formularios"]
		
		mydoc = mycol.find({"$and":[ {"fecha_cita":{"$gte":fechainicio}}, {"fecha_cita":{"$lte":fechafin}}]})


		contenedor = []
		for x in mydoc:
			contenedor.append(x)
		titulo = "REPORTE DE CITAS"

		cabecera = (
			("nombre", "Nombre"),
			("apellido", "Apellido"),
			("servicio", "Servicio"),
			("fecha_cita", "FECHA CITA"),
			)
			
	
		nombrePDF = "reporteCrecimiento.pdf"

		reporte = reportePDF(titulo, cabecera, contenedor, nombrePDF).Exportar()
		print(reporte)

   
	def leer():
		nombre_archivo = "archivo.txt"
		with open(nombre_archivo, "r") as archivo:
			for linea in archivo:
				print("Aquí hay una línea: ", linea)
		

	def errorCaracteres(self):
		
		messagebox.showwarning("cuidado","Numero de caracteres superados")
	def reportcitas(self):
		messagebox.showinfo(title='Reporte', message='Reporte ya generado')
		os.system("reporteCrecimiento.pdf")
	def reportcitasC(self):
		messagebox.showinfo(title='Reporte', message='Reporte ya generado')
		os.system("reporteCrecimiento.pdf")
	def usuario(self):
		messagebox.showinfo(title='Usuario guardado', message='Registro existoso')
	def errPalabraClave(self):
		messagebox.showinfo(title='Error', message='Ya existe una palabra clave con el mismo nombre')
	def AT(self):
		
		messagebox.showinfo("Publicado correctamente","Publicacion exitosa")
	

	def espere(self):
		
		win=tk.Toplevel()
		win.title("Espere...")
		win.geometry('360x170+500+50')
		win.resizable(width=False, height=False)
		frame = LabelFrame (win, text='Espere Porfavor')
		frame.grid(row = 0, column= 1, columnspan=3, pady= 5,padx=5)
		Label(frame, text='Estamos publicando...').grid(row = 0, column = 1)
		img = ImagePIL.open("waiting.png")
		
		newImg=img.resize((220,130))
		render= ImageTk.PhotoImage(newImg)
		
		img1 = Label(frame, image = render)
		img1.image=render
		img1.grid(column=0, row=0,  padx=0, pady=0, sticky="we")
		def OcultarVentana():
			win.withdraw()
			self.AT()
		win.after(4000, OcultarVentana)
		 
	def _on_tree_select(self, event):
		current_item = self.tree.focus()
		if not current_item:
			return
		data = self.tree.item(current_item)
		nombre = data["text"]
		respuesta = data["values"]
		self.name.delete('0', 'end')
		self.name.insert(0, nombre)
		self.respuesta.delete('0', 'end')
		self.respuesta.insert(0, respuesta[0])		
	def interfaz_inicial(self):
		global frame
		# FRAME CONTENEDOR
		frame = LabelFrame(self.frame_cuatro, text=' Editar: ')
		frame.grid(row = 0, column = 0, columnspan = 3, pady = 15, ipadx = 5, ipady = 5	)	
        # INPUT NAME
		Label(frame, text=' Nombre: ').grid(row = 1, column = 0, padx = 20, pady = 5, sticky = W)
		self.name = UpperEntry(frame, width=45)
		self.name.grid(row = 1, column = 1, sticky = W)
		self.name.focus()
		
		# INPUT STOCK
		Label(frame, text='Response: ').grid(row = 3, column = 0, padx = 20, pady = 5, sticky = W)
		self.respuesta = UpperEntry(frame, width=25)
		self.respuesta.grid(row = 3, column = 1, sticky = W)
		
		# BOTON AGREGAR PRODUCTO
		ttk.Button(frame, text='GUARDAR', command=lambda:[self.guardar(), self.botkit()]).grid(row = 5, columnspan = 2, ipadx=40, pady = 10)

	def guardar(self):
		
		data = self.tree.selection()[0]
		idd=self.tree.item(data,"values")
		Tstrkey = self.tree.item(data,"text")
		b = 'Escriba palabra clave'
		keystr=self.name.get()
		msj=self.respuesta.get()
		
		aa= str(self.cont)
		for x in range(len('//')):
			mensaje = aa.replace('//'[x],"")
		aaa=mensaje.count(keystr)
		if aaa>=1 and keystr!=Tstrkey:
			self.errPalabraClave()
		else:

			with open(dirname+'\\botkit-starter-web\\skills\\'+idd[2], "rt") as file:
				x = file.read()
			if x.count(b)>=1:
				#edicion para opciones nuevas
				with open(dirname+'\\botkit-starter-web\\skills\\'+idd[2], "rt", encoding='utf-8', errors='ignore') as file:
					x = file.read()

				with open(dirname+'\\botkit-starter-web\\skills\\'+idd[2], "wt", encoding='utf-8', errors='ignore') as file:
					x = x.replace(b,keystr)
					file.write(x)
				#response

				with open(dirname+'\\botkit-starter-web\\skills\\'+idd[2], "rt", encoding='utf-8', errors='ignore') as file:
					x = file.read()

				with open(dirname+'\\botkit-starter-web\\skills\\'+idd[2], "wt", encoding='utf-8', errors='ignore') as file:
					x = x.replace('Escriba respuesta a la palabra clave',msj)
					file.write(x)


			else:
				#edicion para opciones con palabra clave
				#palabra clave
				with open(dirname+'\\botkit-starter-web\\skills\\'+idd[2], "rt", encoding='utf-8', errors='ignore') as file:
					x = file.read()

				with open(dirname+'\\botkit-starter-web\\skills\\'+idd[2], "wt", encoding='utf-8', errors='ignore') as file:
					x = x.replace(Tstrkey,keystr)
					file.write(x)
				#response

				with open(dirname+'\\botkit-starter-web\\skills\\'+idd[2], "rt", encoding='utf-8', errors='ignore') as file:
					x = file.read()

				with open(dirname+'\\botkit-starter-web\\skills\\'+idd[2], "wt", encoding='utf-8', errors='ignore') as file:
					x = x.replace(idd[0],msj)
					file.write(x)
			################################ OPCIONES YA REGISTRADAS #################################
			if len (idd[1])!=0:
				with open(dirname+'\\botkit-starter-web\\skills\\'+idd[1], "r" , encoding='utf-8', errors='ignore') as file:
					x = file.read()
				busqueda= 'vacio'
				rango = (int(x[-1]))
				with open(dirname+'\\botkit-starter-web\\skills\\'+idd[1], "rt", encoding='utf-8', errors='ignore') as file:
					z = file.read()
					if z.count(Tstrkey)>=1:
						with open(dirname+'\\botkit-starter-web\\skills\\'+idd[1], "wt", encoding='utf-8', errors='ignore') as file:
							z = z.replace(Tstrkey,keystr)
							file.write(z)
							return
					else:
						for i in range(rango):
							with open(dirname+'\\botkit-starter-web\\skills\\'+idd[1], "rt", encoding='utf-8', errors='ignore') as file:
								y = file.read()
								for i in range(rango):
									if y.count(busqueda+str(i))>=1:
										with open(dirname+'\\botkit-starter-web\\skills\\'+idd[1], "wt", encoding='utf-8', errors='ignore') as file:
											y = y.replace(busqueda+str(i),keystr)
											file.write(y)
										return 
								
	def reporte(self):
		x= self.fechaF.get().strip()
		print(x)
		self.fechaI=StringVar()
		self.fechaF=StringVar()

	def generarReporteC(self):
	
		dt=self.call.get_date()
		fechainicioC=dt.strftime("%Y-%m-%d")
		dt=self.call1.get_date()
		fechafinC=dt.strftime("%Y-%m-%d")
		print(fechainicioC,fechafinC)
		myclient = pymongo.MongoClient( "mongodb+srv://Dhery:computadora@cluster0.quh68.mongodb.net/")
		mydb = myclient["botkit"]
		mycol = mydb["formularios"]
		
		mydoc = mycol.find({"$and":[ {"fecha_cita":{"$gte":fechainicioC}}, {"fecha_cita":{"$lte":fechafinC}}, {"servicio":"registro"}]})

		contenedor = []
		for x in mydoc:
			contenedor.append(x)
		titulo = "REPORTE DE CRECIMIENTO"

		cabecera = (
			("nombre", "Nombre"),
			("apellido", "Apellido"),
			("servicio", "Servicio"),
			("fecha_cita", "FECHA CITA"),
			)
			
	
		nombrePDF = "reporteCrecimiento.pdf"

		reporte = reportePDF(titulo, cabecera, contenedor, nombrePDF).Exportar()
		print(reporte)



	

class UpperEntry(Entry):
    def __init__(self, parent, *args, **kwargs):
        self._var = kwargs.get("textvariable") or StringVar(parent)
        super().__init__(parent, *args, **kwargs)
        self.configure(textvariable=self._var)
        

    def config(self, cnf=None, **kwargs):
        self.configue(cnf, **kwargs)

    def configure(self, cnf=None, **kwargs):
        var = kwargs.get("textvariable")
        if var is not None:
            
            self._var = var
        super().config(cnf, **kwargs)

    def __setitem__(self, key, item):
        if key == "textvariable":
            item.trace_add('write')
            self._var = item
        super.__setitem__(key, item)

 
if __name__ == "__main__":
	ventana = Tk()
	
	ventana.title('')
	ventana.minsize(height= 475, width=795)
	ventana.geometry('1080x700+0+0')
	ventana.call('wm', 'iconphoto', ventana._w, PhotoImage(file='logo.png'))	
	app = Ventana(ventana)
	app.mainloop()