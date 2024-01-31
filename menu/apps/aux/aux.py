import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext as st
from tkinter import *
from datetime import datetime
import cx_Oracle
from menu.config import color_cuerpo_principal
from menu.apps.aux.type_aux import types
from dotenv import load_dotenv
import os

class Auxiliares():
    
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.visible = False
        self.create_widgets()
        self.resultados = {}

        load_dotenv() # Load database

    #   Crear Widgets
    def create_widgets(self):

        # Etiqueta de tiempo
        self.time_label = tk.Label(self.root, text="", bg=color_cuerpo_principal)
        self.time_label.place(relx=0.50, rely=0.025, anchor="center")

        # Etiqueta de búsqueda
        self.scan_label = tk.Label(self.root, text="Ingrese el texto a buscar:", bg=color_cuerpo_principal)
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
        self.scan_label = tk.Label(self.root, text="Seleccione modo de búsqueda:", anchor="center", bg=color_cuerpo_principal)
        self.scan_label.place(relx=0.02, rely=0.175)

        # Selección de método de búsqueda
        self.type_options = ttk.Combobox(self.root, values=["Rut", "Razon_Social"], state="readonly")
        self.type_options.set("Rut")
        self.type_options.place(relx=0.02, rely=0.205, relwidth=0.175)

        # Etiqueta de tipo de auxiliar
        self.scan_label2 = tk.Label(self.root, text="Seleccione tipo de auxiliar:", anchor="center", bg=color_cuerpo_principal)
        self.scan_label2.place(relx=0.275, rely=0.175)

        # Selección de método de búsqueda
        self.id_selected = 0
        self.type_options2 = ttk.Combobox(self.root, values=[value for _, value in types], state="readonly")
        self.type_options2.bind("<<ComboboxSelected>>", self.handle_type_aux_selection)
        self.type_options2.set("Todos")
        self.type_options2.place(relx=0.275, rely=0.205, relwidth=0.175)

        # Shared variable for radiobuttons
        self.selected_option = tk.IntVar()
        

        # Etiqueta de tipo activo
        self.scan_label3 = tk.LabelFrame(self.root, text="Activo:", bg=color_cuerpo_principal)
        self.scan_label3.place(relx=0.5, rely=0.175, relwidth=0.15, relheight=0.075)

        self.radiobutton_yes = tk.Radiobutton(self.scan_label3, text="Si", value=0, variable=self.selected_option, bg=color_cuerpo_principal)
        self.radiobutton_yes.place(relx=0.05, rely=0.05, relwidth=0.45, relheight=0.8)

        self.radiobutton_no = tk.Radiobutton(self.scan_label3, text="No", value=1, variable=self.selected_option, bg=color_cuerpo_principal)
        self.radiobutton_no.place(relx=0.5, rely=0.05, relwidth=0.45, relheight=0.8)

        # Etiqueta de error
        self.error_label = tk.Label(self.root, text="", fg="red", bg=color_cuerpo_principal)
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

        self.button_view = tk.Button(self.root, text="   Ver   ", command=self.view)
        self.button_view.place(relx=0.02, rely=0.9)

        self.button_edit = tk.Button(self.root, text=" Editar ", command=self.edit)
        self.button_edit.place(relx=0.10, rely=0.9)
        
    #   Actualizar Tiempo
    def update_time(self):
        try:
            current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.time_label.config(text=f"Fecha actual: {current_time}")
            self.root.after(1000, self.update_time)
        except tk.TclError as e:
            print("error tlc {e}")

    #   Buscar Auxiliar
    def search(self, event=None):

        self.clear_list()

        attributes = self.get_atributes(self.type_options.get().upper(), self.type_options2.get(), self.selected_option.get())

        consulta = (self.scan_entry.get().upper())
        consulta_con_comodines = f'%{consulta}%'

        connection_str = f"{os.getenv('NAME_DATABASE')}/{os.getenv('PASSWORD_DATABASE')}@XE"

        with cx_Oracle.connect(connection_str) as con:

            with con.cursor() as cursor:

                if attributes["type_aux"] == 0:

                    # Ejecutar consulta para todos los tipos de auxiliares
                    cursor.execute(f"SELECT RUT, DV, RAZON_SOCIAL, DIRECCION, TELEFONO FROM AUXILIAR WHERE {attributes['search_method']} LIKE :con AND ACTIVO = :activo", con = consulta_con_comodines, activo = attributes['active'])

                else:

                    # Ejecutar la consulta SQL
                    cursor.execute(f"SELECT RUT, DV, RAZON_SOCIAL, DIRECCION, TELEFONO FROM AUXILIAR WHERE {attributes['search_method']} LIKE :con AND ID_TIPO_AUXILIAR = :tipo AND ACTIVO = :activo", con = consulta_con_comodines, tipo = attributes['type_aux'], activo = attributes['active'])

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

    #   Obtener atributos para busqueda
    def get_atributes(self, search_method, type_aux, active):

        type_aux = self.handle_type_aux_selection()
        active = 0 if active else 1

        attributes = {
            "search_method": search_method,
            "type_aux": type_aux,
            "active": active
        }
        
        return attributes

    #   Manejar tipos auxiliares
    def handle_type_aux_selection(self, event=None):

        # Obtener la tupla completa seleccionada
        selected_tuple = next((tupla for tupla in types if tupla[1] == self.type_options2.get()), 0)

        # Almacenar solo el ID seleccionado
        self.selected_id = selected_tuple[0] if selected_tuple else None

        return self.selected_id

    #   Actualizar Lista
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

    #   Ocultar para Menu
    def ocultar(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.visible = False
    
    #   Mostrar para Menu
    def mostrar(self):
        for widget in self.root.winfo_children():
            widget.place()
        self.visible = True
