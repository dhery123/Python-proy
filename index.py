
from enum import auto
import tkinter as tk
from io import SEEK_CUR
from tkinter import Message, font
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import os

from tkinter import filedialog as FileDialog
import pymongo
from pymongo import MongoClient
from PIL import ImageTk, Image

from tkinter import filedialog as fd 
import shutil

import sys

from pymongo import message



ejemplo_dir = '/home/dhery/TallerGrado/ccc/Admin'
#colores
fondo_aceptar="#a308ba"
fondo_salir="#e80546"
fondInt="#c62f71"

ventana= tk.Tk()
ventana.title("Login")
ventana.geometry("800x400+500+50")
ventana.resizable(width=False, height=False)

fondo = tk.PhotoImage(file="image.png")
fondo1 = tk.Label(ventana, image=fondo).place(x=0, y=0, relwidth=1, relheight=1)
usuario=tk.StringVar()
password=tk.StringVar()

#Int
entrada=tk.Entry(ventana, textvar=usuario,width=22,relief="flat", bg=fondInt)
entrada.place(x=520, y=145)

entrada1=tk.Entry(ventana, textvar=password,width=22,show="*",relief="flat", bg=fondInt)
entrada1.place(x=520, y=217)
entrada.focus()

def login():
    nombre=usuario.get()
    passw = password.get() 
    if nombre== "admin" and passw == "admin":
        main()
    else:
        incorrecta()
def main():
    ventana.destroy()
    os.system("python main.py")
    
def Salir():
    ventana.destroy()
    
def Menus():
    
    ventana.withdraw()
    win=tk.Toplevel()
    win.geometry('300x300+500+50')
    win.resizable(width=False, height=False)
    win.config(background="#64778d")
    
    win.wm_attributes("-alpha",0.1)

    frame = LabelFrame (ventana, text='Menu')
    frame.grid(row = 0, column= 0, columnspan=3, pady= 80)
    Label(frame, text='Introduzca el nombre de la charla: ').grid(row = 1, column = 0)    
    boton2=tk.Button(win,text='autopublicacion', command=autopublicacion)
    boton2.place(x=90,y=40)
    
    boton2=tk.Button(win,text='ChatBot', command=chatbot)
    boton2.place(x=112,y=80)

    boton2=tk.Button(win,text='Citas', command=win.destroy)
    boton2.place(x=124,y=120)

    boton2=tk.Button(win,text='Cerrar Sesion', command=Salir)
    boton2.place(x=96,y=160)

    ventana.mainloop()
def incorrecta():
    messagebox.showwarning("cuidado","Password incorrecto")
keyword=tk.StringVar()
sentence=tk.StringVar()

def chatbot():
    ventana.withdraw()
    win=tk.Toplevel()
    win.geometry('300x300+500+50')
    win.resizable(width=False, height=False) 
    boton2=tk.Button(win,text='Crear chat', command=crearChat)
    boton2.place(x=100,y=80)

    boton2=tk.Button(win,text='Editar chat', command=editarChat)
    boton2.place(x=100,y=120)
    boton2=tk.Button(win,text='Mostrar Registro del chat', command=llamar)
    boton2.place(x=50,y=160)

    

    boton2=tk.Button(win,text='Cancelar', command=win.destroy)
    boton2.place(x=110,y=200)

    ventana.mainloop()   

def crearChat():
    
    ventana.withdraw()
    win=tk.Toplevel()
    win.geometry('400x400+500+50')
    
    text=tk.Label(win, text='Introduzca la palabra clave: ')
    text.place(x=10,y=100)
    entrada=tk.Entry(win, textvar=keyword,width=22,relief="flat")
    entrada.place(x=200, y=100)
    text=tk.Label(win, text='Introduzca la respuesta: ')
    text.place(x=10,y=180)
    entrada=tk.Entry(win, textvar=sentence,width=22,relief="flat")
    entrada.place(x=200, y=180)
    boton=ttk.Button(win, text='guardar charla', command=add_charla)
    boton.place(x=50,y=350)
    
    boton=ttk.Button(win, text='Cancelar', command=win.destroy)
    boton.place(x=270,y=350)
def editarChat():
    
    ventana.withdraw()
    win=tk.Toplevel()
    win.geometry('400x400+500+50')
    
    text=tk.Label(win, text='Introduzca la palabra clave a editar: ')
    text.place(x=10,y=100)
    entrada=tk.Entry(win, textvar=keyword,width=22,relief="flat")
    entrada.place(x=200, y=100)
    text=tk.Label(win, text='Introduzca la nueva respuesta: ')
    text.place(x=10,y=180)
    entrada=tk.Entry(win, textvar=sentence,width=22,relief="flat")
    entrada.place(x=200, y=180)
    
    boton=ttk.Button(win, text='editar charla', command=edit_charla)
    boton.place(x=50,y=350)
    boton=ttk.Button(win, text='Cancelar', command=win.destroy)
    boton.place(x=270,y=350)

def autopublicacion():
    ventana.withdraw()
    win=tk.Toplevel()
    win.geometry('300x660+500+50')
    win.title("Autopublicación")
    win.resizable(width=False, height=False)
    frame1=ttk.LabelFrame(win, text="PUBLICACION :", style = "Red.TLabelframe")        
    frame1.grid(column=0, row=0, padx=3, pady=0)
    
    with open("datos.txt") as f:
        lines = f.read()
        first = lines.split('\n', 1)[0]
    text=tk.Label(frame1, text='Usuario de Facebook: '+first)
    text.grid(column=0, row=0,  padx=0, pady=0,sticky="we")
    img = Image.open("imagen.png")
    
    newImg=img.resize((270,156))
    render= ImageTk.PhotoImage(newImg)
    
    img1 = Label(frame1, image = render)
    img1.image=render
    img1.grid(column=0, row=1,  padx=0, pady=0, sticky="we")

    frame=ttk.LabelFrame(frame1, text="MENSAJE :", style = "Red.TLabelframe")        
    frame.grid(column=0, row=2, padx=1, pady=1)
    text_frame = tk.Frame(frame)
    textArea=tk.Text(text_frame, width=32, height=8)
    
    textArea.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    textScroll=ttk.Scrollbar(text_frame, command=textArea.yview)
    textScroll.pack(fill=tk.Y, side=tk.RIGHT)
    text_frame.grid(column=0, row=0,  padx=0, pady=23, sticky="we")

    textArea.config(yscrollcommand=textScroll.set)
    
    fichero = open('mensaje.txt', 'r')
    contenido = fichero.read()
    textArea.delete(1.0,'end')
    textArea.insert('insert', contenido)
    textArea.config(state=DISABLED)
    boton=ttk.Button(frame, text='Editar', command=lambda:[editMsg(),win.destroy()],width=34)
    boton.place(x=0,y=164)
    
    boton=ttk.Button(win, text='Publicar Ahora', command=Autoposter)
    boton.place(x=90,y=580)
    boton=ttk.Button(win, text='Atras', command=win.destroy)
    boton.place(x=100,y=620)
    
    boton=ttk.Button(win, text='Editar Usuario de Facebook', command=editUs)
    boton.place(x=50,y=460)
    boton=ttk.Button(win, text='Editar Grupos', command=editEnl)
    boton.place(x=90,y=540)
    #boton=ttk.Button(win, text='Editar Mensaje', command=editMensaje)
    #boton.place(x=90,y=450)
    boton=ttk.Button(win, text='Editar Imagen', command=lambda:[editImg(),win.destroy()])
    boton.place(x=90,y=500)




def editMsg():
    os.system("python3 editarMensaje.py")
    return autopublicacion()
def Autoposter():
    os.system("python3 FacebookPoster.py")
def Cron():
    ventana.withdraw()
    win=tk.Toplevel()
    win.geometry('300x300+500+50')
    win.resizable(width=False, height=False)
    button=ttk.Button(win, text='Publicar cada dia', command=dia).grid(row = 0, column=0)
    
    button=ttk.Button(win, text='Publicar una vez a la semana', command=semana).grid(row = 1, column=0 )
    button=ttk.Button(win, text='publicar una vez al mes', command=mes).grid(row = 2, column=0)
    button=ttk.Button(win, text='publicar una vez cada tres meses', command=meses).grid(row = 3, column=0)


   
def dia():
    
    os.system("pwatch -n 86400 python3 FacebookPoster.py") 

def semana():
    a = open("/home/dhery/TallerGrado/ccc/Admin/autopost.txt",'w')
    a.write("Se publicara una vez a la semana")
    os.system("pwatch -n 604800 python3 FacebookPoster.py")

def mes():
    a = open("/home/dhery/TallerGrado/ccc/Admin/autopost.txt",'w')
    a.write("Se publicara una vez al mes")
    os.system("pwatch -n 2.628e+6 python3 FacebookPoster.py")
def meses():
    a = open("/home/dhery/TallerGrado/ccc/Admin/autopost.txt",'w')
    a.write("Se publicara una vez cada 3 meses")
    os.system("pwatch -n 7.884e+6 python3 FacebookPoster.py")


texto=tk.Text()
def editEnl():
    os.system("python3 editarGrupos.py")
def editMensaje():
    os.system("python3 editarMensaje.py")

    
    
usuarioFace=tk.StringVar()
passwordFace=tk.StringVar()
def editUs():
    ventana.withdraw()
    win=tk.Toplevel()
    win.title("Editar Usuario de Facebook")
    win.geometry('390x180+500+50')
     
    frame = LabelFrame (win, text='Register')
    frame.grid(row = 0, column= 0, columnspan=3, pady= 5,padx=5)
    Label(frame, text='Introduzca el Usuario').grid(row = 0, column = 0)
    entrada=tk.Entry(frame, textvar=usuarioFace,width=22,relief="flat").grid(row = 0, column= 1, columnspan=3, pady= 10)
    
    entrada=tk.Entry(frame, textvar=passwordFace,width=22,show="*",relief="flat").grid(row = 1, column= 1, columnspan=3, pady= 10)
    Label(frame, text='Introduzca la contraseña').grid(row = 1, column = 0)

    ttk.Button(win, text='guardar usuario', command=Usss).grid(row = 5, column=0)
    ttk.Button(win, text='Cancelar', command=win.destroy).grid(row = 5, column=2 )
def Usss():
    ObjFichero = open("/home/dhery/TallerGrado/ccc/Admin/datos.txt",'w')
    MiNuevoTexto = usuarioFace.get()+'\n'+passwordFace.get()
    ObjFichero.write(MiNuevoTexto)
    ObjFichero.close()

def add_charla():
    b=keyword.get()
    c=sentence.get()
    
    with os.scandir(ejemplo_dir) as ficheros:
        for fichero in ficheros:
            if fichero.name==b+".js":
                incorrecta()
            else:
                f = open('/home/dhery/TallerGrado/web/Base_de_Datos/botkit-starter-web/skills/'+b+'.js', 'w')
                f.write('module.exports = function(controller){')
                f.write('controller.hears(')
                f.write('"')
                f.write(b)
                f.write('"')
                f.write(',"message_received",function(bot,message){bot.reply(message,')
                f.write('"')
                f.write(c)
                f.write('"')
                f.write(');});')
                
                
                f.write('}')
                f.close() 
def edit_charla():
    b=keyword.get()
    c=sentence.get()
    f = open(b+'.js', 'w')
    f.write('module.exports = function(controller){')
    f.write('controller.hears(')
    f.write('"')
    f.write(b)
    f.write('"')
    f.write(',"message_received",function(bot,message){bot.reply(message,')
    f.write('"')
    f.write(c)
    f.write('"')
    f.write(');});')
                
                
    f.write('}')
    f.close() 
MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000
MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"
MONGO_BASEDATOS="botkit"
MONGO_COLECCION="histories"
def BD():

    win=tk.Toplevel()
    tabla=ttk.Treeview(win,columns=[f"#{n}" for n in range(1, 3)])
    tabla.grid(row=0,column=0,columnspan=1)
    tabla1=ttk.Treeview(win,columns=[f"#{n}" for n in range(1, 3)])
    tabla1.grid(row=1,column=0,columnspan=1)

    cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
    baseDatos=cliente[MONGO_BASEDATOS]
    coleccion=baseDatos[MONGO_COLECCION]
    tabla.column("#0",minwidth=0,width=500, stretch=NO) 
    tabla.heading("#0",text="Mensaje del bot")
    
    tabla.heading("#1",text="Fecha")
    tabla.column("#1",minwidth=0,width=200, stretch=NO) 
    tabla.heading("#2",text="Id")
    tabla.column("#2",minwidth=0,width=400, stretch=NO)
    

    tabla1.column("#0",minwidth=0,width=500, stretch=NO) 
    tabla1.heading("#0",text="Mensajes del usuario")
    
    tabla1.heading("#1",text="Fecha")
    tabla1.column("#1",minwidth=0,width=200, stretch=NO) 
    tabla1.heading("#2",text="Id")
    tabla1.column("#2",minwidth=0,width=400, stretch=NO)
    ejemplo_dir='/home/dhery/TallerGrado/web/Base_de_Datos/botkit-starter-web/skills'

    contenido = os.listdir(ejemplo_dir)
    for fichero in contenido:
                
                if os.path.isfile(os.path.join(ejemplo_dir, fichero)):
                    tabla.insert('',0,text=fichero)


    for documento in coleccion.find({ 'message.type': { '$eq': 'message_received' }}, {'message.text':1,'_id':0,'date':1,'userId':1}):
                a=documento['date']
                s=documento['userId']
                tabla1.insert('',0,text=documento["message"],values=[a,s])
    button=ttk.Button(win, text='Cancelar', command=llamar)
    button.place(x=0,y=0)
    cliente.close()



    
    win.mainloop()

def llamar():
    if __name__ == "__main__":
        app = App()
    #win.geometry('421x423+500+50')
class App:
    def __init__(self):
        self.root = tk.Toplevel()
        self.tabla=ttk.Treeview(self.root,columns=[f"#{n}" for n in range(1, 3)])
        self.tabla.grid(row=0,column=0,columnspan=1)
        
        
        cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
        baseDatos=cliente[MONGO_BASEDATOS]
        coleccion=baseDatos[MONGO_COLECCION]

        self.tabla.column("#0",minwidth=0,width=500, stretch=NO) 
        self.tabla.heading("#0",text="Mensaje del bot")
        
        self.tabla.heading("#1",text="Fecha")
        self.tabla.column("#1",minwidth=0,width=200, stretch=NO) 
        self.tabla.heading("#2",text="Id")
        self.tabla.column("#2",minwidth=0,width=400, stretch=NO)
        

       
        
        for documento in coleccion.find({}, {'message.type':1,'message.text':1,'_id':0,'date':1,'userId':1}).sort('date',1):
                a=documento['date']
                s=documento['message']

                self.tabla.insert('',0,text=documento["userId"],values=[a,s])
        
      
     


        boton=ttk.Button(self.root, text='Buscar mensaje Usuario', command=self.OnDoubleClick)
        boton.place(x=0,y=0)
        
        self.root.mainloop()

    def OnDoubleClick(self):
        
        

        self.root = tk.Toplevel()
        self.Ntabla=ttk.Treeview(self.root,columns=[f"#{n}" for n in range(1, 3)])
        self.Ntabla.grid(row=0,column=0,columnspan=1)
        item1 = self.tabla.selection()[0]
        
        print("botkit", self.tabla.item(item1,"text"))
        
        cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
        baseDatos=cliente[MONGO_BASEDATOS]
        coleccion=baseDatos[MONGO_COLECCION]

        self.Ntabla.column("#0",minwidth=0,width=500, stretch=NO) 
        self.Ntabla.heading("#0",text="Mensaje del bot")
        
        self.Ntabla.heading("#1",text="Fecha")
        self.Ntabla.column("#1",minwidth=0,width=200, stretch=NO) 
        self.Ntabla.heading("#2",text="Id")
        self.Ntabla.column("#2",minwidth=0,width=400, stretch=NO)
        idd=self.tabla.item(item1,"text")
        for documento in coleccion.find({ 'userId': { '$eq': idd }}, {'message.type':1,'message.text':1,'_id':0,'date':1,'userId':1}).sort('date',1):
                a=documento['date']
                s=documento['userId']
                self.Ntabla.insert('',0,text=documento["message"],values=[a,s])

        
        




def editImg():
    name= fd.askopenfilename(filetypes=(('image files', '.png ;.jpg'),))
    shutil.copy(name, "imagen.png")
    return autopublicacion()

    
   
    
       

   
#BUTON
boton= tk.Button(ventana, text="Entrar",command=login, cursor="hand2", bg=fondo_aceptar, width=12, relief="flat", font=("Comic Sans MS",12, "bold"))
boton.place(x=350,y=310)
boton1= tk.Button(ventana, text="Salir",command=Salir, cursor="hand2", bg=fondo_salir, width=12, relief="flat", font=("Comic Sans MS",12, "bold"))
boton1.place(x=600,y=310)



ventana.mainloop()





