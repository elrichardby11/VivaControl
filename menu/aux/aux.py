import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext as st
from tkinter import *
from datetime import datetime
import cx_Oracle

class aux():
    
    def __init__(self, root):
        self.root = root
        self.root.title("VivaControl - Auxiliares")
        self.root.geometry("1280x720")
        self.create_widgets()

        self.resultados = {}
    
    #   Crear Widgets
    def create_widgets(self):

        # Etiqueta de tiempo
        self.time_label = tk.Label(self.root, text="")
        self.time_label.place(relx=0.50, rely=0.025, anchor="center")

        # Etiqueta de búsqueda
        self.scan_label = tk.Label(self.root, text="Ingrese el texto a buscar:")
        self.scan_label.place(relx=0.02, rely=0.075)

        # Campo de entrada
        self.scan_entry = tk.Entry(self.root, width=100)
        self.scan_entry.place(relx=0.02, rely=0.11)
        self.scan_entry.focus()
        self.scan_entry.bind("<Return>", self.search)

        # Botón de búsqueda
        self.button_search = tk.Button(self.root, text=" Buscar ", command=self.search, anchor="center")
        self.button_search.place(relx=0.665, rely=0.103)

        # Botón de limpiar
        self.button_clear = tk.Button(self.root, text=" Limpiar ", command=self.clear)
        self.button_clear.place(relx=0.75, rely=0.103)

        # Etiqueta de modo de búsqueda
        self.scan_label = tk.Label(self.root, text="Seleccione modo de búsqueda:", anchor="center")
        self.scan_label.place(relx=0.02, rely=0.175)

        # Selección de método de búsqueda
        self.type_options = ttk.Combobox(self.root, values=["Rut", "Razon Social"], state="readonly")
        self.type_options.set("Rut")
        self.type_options.place(relx=0.02, rely=0.205, relwidth=0.175)

        # Etiqueta de tipo de auxiliar
        self.scan_label2 = tk.Label(self.root, text="Seleccione tipo de auxiliar:", anchor="center")
        self.scan_label2.place(relx=0.275, rely=0.175)

        # Selección de método de búsqueda
        self.type_options2 = ttk.Combobox(self.root, values=["Todos", "Proveedores", "Clientes", "Empleados", "Socios", "Distribuidores", "Otros"], state="readonly")
        self.type_options2.set("Todos")
        self.type_options2.place(relx=0.275, rely=0.205, relwidth=0.175)

        # Shared variable for radiobuttons
        self.selected_option = tk.IntVar()

        # Etiqueta de tipo activo
        self.scan_label3 = ttk.LabelFrame(self.root, text="Activo:")
        self.scan_label3.place(relx=0.5, rely=0.175, relwidth=0.15, relheight=0.075)

        self.radiobutton_yes = ttk.Radiobutton(self.scan_label3, text="Si", value=0, variable=self.selected_option)
        self.radiobutton_yes.place(relx=0.05, rely=0.05, relwidth=0.45, relheight=0.8)

        self.radiobutton_no = ttk.Radiobutton(self.scan_label3, text="No", value=1, variable=self.selected_option)
        self.radiobutton_no.place(relx=0.5, rely=0.05, relwidth=0.45, relheight=0.8)


        # Etiqueta de error
        self.error_label = tk.Label(self.root, text="", fg="red")
        self.error_label.place(relx=0.5, rely=0.285, anchor="center")

        self.tree = ttk.Treeview(self.root, height=0, columns=("col2", "col3", "col4"))
        self.tree.place(relx=0.02, rely=0.325, relwidth=0.95)
        self.tree.heading("#0", text="Rut", anchor=tk.CENTER)
        self.tree.heading("col2", text="Razón Social", anchor=tk.CENTER)
        self.tree.heading("col3", text="Dirección", anchor=tk.CENTER)
        self.tree.heading("col4", text="Teléfono", anchor=tk.CENTER)
        self.tree.column("#0", width=262)
        self.tree.column("col2", width=262)
        self.tree.column("col3", width=262)
        self.tree.column("col4", width=262)

        # Lista de resultados
        self.list_aux = st.ScrolledText(self.root, wrap=tk.WORD, borderwidth=2, width=140, height=20)
        self.list_aux.place(relx=0.02, rely=0.35, relwidth=0.95)

        # Botones agrupados
        #button_frame = tk.Frame(self.root)
        #button_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        self.button_view = tk.Button(self.root, text="   Ver   ", command=self.view)
        self.button_view.place(relx=0.02, rely=0.9)

        self.button_edit = tk.Button(self.root, text=" Editar ", command=self.edit)
        self.button_edit.place(relx=0.10, rely=0.9)

        self.button_exit = tk.Button(self.root, text="  Salir  ", command=self.exit)
        self.button_exit.place(relx=0.26, rely=0.9)
        
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
            cursor.execute("SELECT RUT_AUXILIAR,DV,RAZON_SOCIAL,DIRECCION, TELEFONO FROM AUXILIAR WHERE RAZON_SOCIAL LIKE :con", con = consulta_con_comodines)
            # Obtener los resultados de la consulta
            results = cursor.fetchall()

            if results != []:
                self.resultados = {}
                for row in results:

                    rut, dv, name, address, phone_number = row

                    # Replace None values with "-"
                    name = name if name is not None else "-"
                    address = address if address is not None else "-"
                    phone_number = phone_number if phone_number is not None else "-"

                    self.resultados[rut] = {"dv": dv, "name": name, "address" : address, "phone_number" : phone_number}
                    self.update_list()

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
            cursor.execute("SELECT RUT_AUXILIAR,DV,RAZON_SOCIAL,DIRECCION, TELEFONO FROM AUXILIAR WHERE RUT_AUXILIAR LIKE :con", con = consulta_con_comodines)
            # Obtener los resultados de la consulta
            results = cursor.fetchall()


            if results != []:
                self.resultados = {}
                for row in results:
                    rut, dv, name, address, phone_number = row

                    # Replace None values with "-"
                    name = name if name is not None else "-"
                    address = address if address is not None else "-"
                    phone_number = phone_number if phone_number is not None else "-"

                    self.resultados[rut] = {"dv": dv, "name": name, "address" : address, "phone_number" : phone_number}
                    self.update_list()

                    # self.list_aux.insert(tk.END,f"{rut:>35}-{dv:<40} {name:^50}")

                self.error_label.config(fg="green", text="Mostrando resultados")

            else:
                self.error_label.config(fg="red", text="Sin resultados")

            # Cerrar la conexión
            connection.close()

        else:
            self.error_label.config(fg="red", text="Por favor, seleccione un metodo de busqueda")


    def update_list(self):        
        self.clear_list()

        self.list_aux.configure(state=tk.NORMAL)

        for rut, info in self.resultados.items():         
            self.list_aux.insert(tk.END,"{:>15}-{:<15} {:<40} {:<50} {:<10}\n".format(str(rut), str(info['dv']), info['name'], info['address'], str(info['phone_number'])))
       
        self.list_aux.configure(state=tk.DISABLED)



    #   Ver Auxiliar
    def view(self):
        pass

    #   Editar Auxiliar
    def edit(self):
        pass

    #   Limpiar Todo
    def clear(self):
        self.scan_entry.delete(0, tk.END)
        self.clear_list()
        self.error_label.config(fg="black", text="")

    #   Limpia Lista
    def clear_list(self):
        self.list_aux.configure(state=tk.NORMAL)
        self.list_aux.delete("1.0", tk.END)
        self.list_aux.configure(state=tk.DISABLED)


    #   Salir del Programa
    def exit(self): 
        self.root.destroy()
