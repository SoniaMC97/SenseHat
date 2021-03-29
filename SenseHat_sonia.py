import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from sense_emu import SenseHat
import  queue
import threading

class Aplicacion:

    periodo_inicial = 1000

    def __init__(self):
        self.sense = SenseHat()
        
        self.medir = True

        self.queue=queue.Queue() 

        self.periodo = self.periodo_inicial

        self.ventana = tk.Tk() 
        self.ventana.title("Practica GUI SenseHat")

        #Creamos las opciones
        menubar1 = tk.Menu(self.ventana)
        self.ventana.config(menu=menubar1)
        opciones1 = tk.Menu(menubar1)
        opciones1.add_command(label="Configurar Periodo", command=self.cambiar_periodo)
        menubar1.add_cascade(label="Opciones", menu=opciones1)  


        #Creamos la ventana Monitorizacion
        self.cuaderno1 = ttk.Notebook(self.ventana)
        self.pagina1 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina1, text = "Monitorizacion")

        self.labelframe1=ttk.LabelFrame(self.pagina1, text="Control")        
        self.labelframe1.grid(column=0, row=1, padx=5, pady=10)        
        self.control()

        self.labelframe2=ttk.LabelFrame(self.pagina1, text="Medidas")        
        self.labelframe2.grid(column=0, row=2, padx=5, pady=10)        
        self.medidas()
        
        self.labelframe3=ttk.LabelFrame(self.pagina1, text="Historico")        
        self.labelframe3.grid(column=0, row=3, padx=5, pady=10)        
        self.historico()

        #Creamos la ventana Gráfico
        self.pagina2 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina2, text = "Gráfica")

        self.cuaderno1.grid(column = 0, row = 0, sticky='WE')


        Worker(self.queue).start()
        self.ventana.after(self.periodo, self.process_queue)
        self.ventana.mainloop()

    def cambiar_periodo(self):
        dialogo1 = DialogoPeriodo(self.ventana)
        self.periodo = dialogo1.modificar()
        print("periodo: ", self.periodo)
        self.label1_1.config(text = str(self.periodo))


    def control(self):
        #Crear boton
        self.boton=tk.Button(self.labelframe1, text="Parar", command = self.cambiar_1, bg = "red")
        self.boton.grid(column=1, row=0)

        #Crear cuadro de texto
        self.label1=ttk.Label(self.labelframe1, text="Periodo:")
        self.label1.grid(column=0, row=1)

        self.label1_1=ttk.Label(self.labelframe1, text = str(self.periodo))
        self.label1_1.grid(column=2, row=1)

    def cambiar_1(self):
        if(self.medir == True):
            self.boton.config(text = "Comenzar", bg = "green")
            self.medir = False
        else:
            self.boton.config(text = "Parar", bg = "red")
            self.medir = True

    def medidas(self):
        #Creamos entry para 
        self.dato=tk.StringVar(self.labelframe2, value = "0.0")
        
        self.entry1=tk.Entry(self.labelframe2, width=10, textvariable=self.dato)
        self.entry1.grid(column=1, row=0)

        #Creamos Radiobutton
        self.seleccion=tk.IntVar()
        self.seleccion.set(1)
        
        self.radio1=ttk.Radiobutton(self.labelframe2, text="Temperatura", variable=self.seleccion, value=1)
        self.radio1.grid(column=0, row=1)
        
        self.radio2=ttk.Radiobutton(self.labelframe2, text="Presion", variable=self.seleccion, value=2)
        self.radio2.grid(column=1, row=1)
        
        self.radio3=ttk.Radiobutton(self.labelframe2, text="Humedad", variable=self.seleccion, value=3)
        self.radio3.grid(column=2, row=1)

    def historico(self):
        self.scroll1 = tk.Scrollbar(self.labelframe3, orient=tk.VERTICAL)
        self.tree = ttk.Treeview(self.labelframe3, yscrollcommand=self.scroll1.set)
        self.tree.grid()
        
        self.scroll1.configure(command=self.tree.yview)         
        self.scroll1.grid(column=1, row=0, sticky='NS')    # NS de norte a sur


        self.tree['columns'] = ('size', 'modified', 'owner')

        # self.tree.column('size', width=100, anchor='center')
        self.tree.heading('#0', text='#Num')
        self.tree.heading('size', text='Valor')
        self.tree.heading('modified', text='Fecha/Hora')
        self.tree.heading('owner', text='Tipo')

        #Creamos 3 botones 
        self.boton1=tk.Button(self.labelframe3, text="Limpiar")#, command=self.calcularcuadrado)
        self.boton1.grid(column=0, row=1)

        #self.boton2=tk.Button(self.labelframe3, text="Calcular Media")#, command=self.calcularcuadrado)
        #self.boton2.grid(column=0, row=1)

        #self.boton3=tk.Button(self.labelframe3, text="Exportar")#, command=self.calcularcuadrado)
        #self.boton3.grid(column=0, row=1)

    def process_queue(self):
        try:
            if(self.medir == True):
                res = self.queue.get(0)
                #Pongo el resultado en el Cuadro de texto
                self.dato=tk.StringVar(self.labelframe2, value = str(res))
                self.entry1.config(textvariable=self.dato)

        except queue.Empty:
            self.ventana.after(self.periodo, self.process_queue)

    
    
    #def llamada_medir(self):
        #Si el boton está en parar mide
        

        #Si está en comenzar no mide

class Worker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        try:
            temp = self.sense.temp
            pres = self.sense.pressure
            hum = self.sense.humidity
            
            while self.medir == True:
                #Si está marcado temperatura ponemos en la cola la temperatura
                if self.seleccion.get() == 1:
                    self.queue.put(temp)
                #Si está marcado presion, ponemos la presion en la cola
                elif self.seleccion.get() == 2:
                    self.queue.put(pres)
                #Si está marcado humedad, ponemos la humedad en la cola
                else:
                    self.queue.put(hum)

        except:
            self.queue.put("Error")

class DialogoPeriodo:
    def __init__(self, ventanaprincipal):
        self.dialogo=tk.Toplevel(ventanaprincipal)
        self.label1=ttk.Label(self.dialogo, text="Indique Periodo:")
        self.label1.grid(column=0, row=0, padx=5, pady=5)

        self.dato1=tk.StringVar()
        self.entry1=ttk.Entry(self.dialogo, textvariable=self.dato1)
        self.entry1.grid(column=1, row=0, padx=5, pady=5)
        self.entry1.focus()
       
        self.boton1=ttk.Button(self.dialogo, text="Confirmar", command=self.confirmar)
        self.boton1.grid(column=1, row=2, padx=5, pady=5)
        self.dialogo.protocol("WM_DELETE_WINDOW", self.confirmar)
        self.dialogo.resizable(0,0)
        self.dialogo.grab_set()

    def modificar(self):
        self.dialogo.wait_window()
        return self.dato1.get()

    def confirmar(self):
        self.dialogo.destroy()
    

aplicacion1 = Aplicacion()