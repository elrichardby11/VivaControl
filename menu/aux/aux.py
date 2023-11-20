import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime
import cx_Oracle

class aux():
    
    def __init__(self, root):
        self.root = root
        self.root.title("VivaControl - Auxiliares")
        self.root.geometry("1280x720")
        self.create_widgets()
    
    #   Crear Widgets
    def create_widgets(self):

        # Etiqueta de estetica
        self.frame_label = tk.Label(self.root, text="")
        self.frame_label.grid(row=0, column=0, padx=0, pady=10, sticky="w")

        # Etiqueta de tiempo
        self.time_label = tk.Label(self.root, text="")
        self.time_label.grid(row=0, column=0)

        # Etiqueta de búsqueda
        self.scan_label = tk.Label(self.root, text="Ingrese el texto a buscar:")
        self.scan_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Campo de entrada
        self.scan_entry = tk.Entry(self.root, width=125)
        self.scan_entry.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="w")
        self.scan_entry.focus()
        self.scan_entry.bind("<Return>", self.search)

        # Botón de búsqueda
        self.button_search = tk.Button(self.root, text="Buscar", command=self.search)
        self.button_search.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="w")

        # Etiqueta de modo de búsqueda
        self.scan_label = tk.Label(self.root, text="Seleccione modo de búsqueda:")
        self.scan_label.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")

        # Selección de método de búsqueda
        self.type_options = ttk.Combobox(self.root, values=["Razon Social", "Rut"], state="readonly")
        self.type_options.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="w")

        # Etiqueta de error
        self.error_label = tk.Label(self.root, text="", fg="red")
        self.error_label.grid(row=5, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")

        # Lista de resultados
        self.list_aux = tk.Listbox(self.root, borderwidth=2, relief="ridge", width=140, height=20)
        self.list_aux.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Botones agrupados
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.button_view = tk.Button(button_frame, text="   Ver   ", command=self.view)
        self.button_view.pack(side="left", padx=10)

        self.button_edit = tk.Button(button_frame, text=" Editar ", command=self.edit)
        self.button_edit.pack(side="left", padx=10)

        self.button_clear = tk.Button(button_frame, text=" Limpiar ", command=self.clear)
        self.button_clear.pack(side="left", padx=10)

        self.button_exit = tk.Button(self.root, text="  Salir  ", command=self.exit)
        self.button_exit.grid(row=8, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="w")
        
    #   Actualizar tiempo
    def update_time(self):
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.time_label.config(text=f"Fecha actual: {current_time}")
        self.root.after(1000, self.update_time)

    #   Buscar Auxiliar
    def search(self, event=None):
        search_method = self.type_options.get()
        if search_method == "Razon Social":
            consulta = (self.scan_entry.get().upper())
            consulta_con_comodines = f'%{consulta}%'
            self.clear_list()
                
            # Conectar a la base de datos Oracle
            connection = cx_Oracle.connect("VivaControl/T$g#kP2LMv8X@XE")

            # Crear un cursor
            cursor = connection.cursor()

            # Ejecutar la consulta SQL
            cursor.execute("SELECT * FROM AUXILIAR WHERE RAZON_SOCIAL LIKE :con", con = consulta_con_comodines)
            # Obtener los resultados de la consulta
            results = cursor.fetchall()

            if results != []:
                for row in results:
                    self.list_aux.insert(tk.END, row)
                self.error_label.config(fg="green", text="Mostrando resultados")
                
            else:
                self.error_label.config(fg="red", text="Sin resultados")

            # Cerrar la conexión
            connection.close()


        elif search_method == "Rut":                
            consulta = (self.scan_entry.get())
            consulta_con_comodines = f'{(consulta)}%'
            self.clear_list()
            
            # Conectar a la base de datos Oracle
            connection = cx_Oracle.connect("VivaControl/T$g#kP2LMv8X@XE")

            # Crear un cursor
            cursor = connection.cursor()

            # Ejecutar la consulta SQL
            cursor.execute("SELECT * FROM AUXILIAR WHERE RUT_AUXILIAR LIKE :con", con = consulta_con_comodines)
            # Obtener los resultados de la consulta
            results = cursor.fetchall()

            if results != []:
                for row in results:
                    self.list_aux.insert(tk.END, row)
                self.error_label.config(fg="green", text="Mostrando resultados")
                
            else:
                self.error_label.config(fg="red", text="Sin resultados")

            # Cerrar la conexión
            connection.close()

        else:
            self.error_label.config(fg="red", text="Por favor, seleccione un metodo de busqueda")

    #   Ver Auxiliar
    def view(self):
        pass

    #   Editar Auxiliar
    def edit(self):
        pass

    #   Limpiar Todo
    def clear(self):
        self.scan_entry.delete(0, tk.END)
        self.list_aux.delete(0, tk.END)
        self.error_label.config(fg="black", text="")

    #   Limpia Lista
    def clear_list(self):
        self.list_aux.delete(0, tk.END)

    #   Salir del Programa
    def exit(self): 
        self.root.destroy()
