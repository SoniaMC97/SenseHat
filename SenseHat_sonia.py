import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from sense_emu import SenseHat
import  queue

class Aplicacion:

    periodo_inicial = 1000

    def __init__(self):
        self.sense = SenseHat()
        
        self.medir = True

        self.queue = queue.Queue()

        self.list_max = [105, 1260, 100]   #Valores maximos
        self.periodo = self.periodo_inicial

        #Creamos la ventana
        self.ventana = tk.Tk() 
        self.ventana.title("Practica GUI SenseHat")

        self.labelframe1=ttk.LabelFrame(self.ventana, text="Control")        
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10)        
        self.control()

        self.labelframe2=ttk.LabelFrame(self.ventana, text="Medidas")        
        self.labelframe2.grid(column=0, row=1, padx=5, pady=10)        
        self.medidas()
        
        self.labelframe3=ttk.LabelFrame(self.ventana, text="Historico")        
        self.labelframe3.grid(column=0, row=2, padx=5, pady=10)        
        self.historico()


        self.ventana.mainloop()
    
    def control(self):
        #Crear boton
        self.boton=tk.Button(self.labelframe1, text="Parar")#, command=self.calcularcuadrado)
        self.boton.grid(column=1, row=0)

        #Crear cuadro de texto
        self.label1=ttk.Label(self.labelframe1, text="Periodo:")
        self.label1.grid(column=0, row=1)

        self.label1_1=ttk.Label(self.labelframe1, )
        self.label1_1.grid(column=2, row=1)

    def medidas(self):
        #Creamos entry para 
        self.dato=tk.StringVar(self.labelframe2, value = "0.0")
        
        self.entry1=tk.Entry(self.labelframe2, width=10, textvariable=self.dato)
        self.entry1.grid(column=1, row=0)

        #Creamos Radiobutton
        self.seleccion=tk.IntVar()
        self.seleccion.set(2)
        
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

aplicacion1 = Aplicacion()