import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime 
from menu.apps.pos.file_operations import save_to_file
from menu.apps.pos.products import search_products
from menu.apps.pos.locals import locals
from menu.config import color_cuerpo_principal


class PoS():

    #   Configuracion de ventana
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.visible = False

        self.current_cart = {}
        self.locals = locals
        self.previous_local = []

        self.create_widgets()

    #   Crea los botones, textos, etc
    def create_widgets(self):

        self.time_label = tk.Label(self.root, text="", bg=color_cuerpo_principal)
        self.time_label.place(relx=0.5, rely=0.02, anchor="center")

        self.scan_label = tk.Label(self.root, text="Escanea el código del producto:", bg=color_cuerpo_principal)
        self.scan_label.place(relx=0.4, rely=0.07, anchor="center")

        self.scan_entry = tk.Entry(self.root)
        self.scan_entry.place(relx=0.4, rely=0.1, anchor="center")
        self.scan_entry.focus_set()

        self.scan_entry.bind('<Return>', self.add_to_cart)

        self.add_to_cart_button = tk.Button(self.root, text="Agregar al carrito", command=self.add_to_cart)
        self.add_to_cart_button.place(relx=0.5, rely=0.07)

        self.message_label = tk.Label(self.root, text="", fg="black", bg=color_cuerpo_principal)
        self.message_label.config(text="Escanee un producto ", fg="black")
        self.message_label.place(relx=0.4, rely=0.15, anchor="center")
        
        self.cart_label = tk.Label(self.root, text="Carrito: ", bg=color_cuerpo_principal)
        self.cart_label.place(relx=0.4, rely=0.2, anchor="center")

        self.tree = ttk.Treeview(self.root, height=0, columns=("col2", "col3", "col4"))
        self.tree.place(relx=0.015, rely=0.225)
        self.tree.heading("#0", text="Código", anchor=tk.CENTER)
        self.tree.heading("col2", text="Nombre", anchor=tk.CENTER)
        self.tree.heading("col3", text="Cantidad", anchor=tk.CENTER)
        self.tree.heading("col4", text="Precio", anchor=tk.CENTER)
        self.tree.column("#0", width=262)
        self.tree.column("col2", width=262)
        self.tree.column("col3", width=262)
        self.tree.column("col4", width=262)
        
        self.cart_listbox = tk.Listbox(self.root, borderwidth=2, relief="ridge", height=25, width=130)
        self.cart_listbox.place(relx=0.015, rely=0.25)

        self.subtotal_label = tk.Label(self.root, text="Total:    $    0", bg=color_cuerpo_principal)
        self.subtotal_label.place(relx=0.4, rely=0.95, anchor="center")
        
        self.local_label = tk.Label(self.root, text="Selecciona la sucursal:", bg=color_cuerpo_principal)
        self.local_label.place(relx=0.9, rely=0.07, anchor="center")

        self.local_options = ttk.Combobox(self.root, values=locals, state="readonly")
        self.local_options.bind("<FocusOut>", self.add_local_history)
        self.local_options.bind("<<ComboboxSelected>>", self.handle_local_selection)
        self.local_options.place(relx=0.9, rely=0.1, anchor="center")

        self.payment_label = tk.Label(self.root, text="Selecciona el método de pago:", bg=color_cuerpo_principal)
        self.payment_label.place(relx=0.9, rely=0.4, anchor="center")

        self.payment_options = ttk.Combobox(self.root, values=['Efectivo', 'Débito', 'Crédito'], state="readonly")
        self.payment_options.bind("<<ComboboxSelected>>", self.handle_payment_selection)
        self.payment_options.place(relx=0.9, rely=0.43, anchor="center")

        self.message_label2 = tk.Label(self.root, text="Monto en Efectivo: ", fg="black", bg=color_cuerpo_principal)
        self.message_label2.place(relx=0.9, rely=0.5, anchor="center")

        self.scan_entry2 = tk.Entry(self.root, state="disabled")
        self.scan_entry2.place(relx=0.9, rely=0.53, anchor="center")
        self.scan_entry2.bind('<Return>', self.payment)

        self.edit_button = tk.Button(self.root, text="Editar", command=self.edit_quantity)
        self.edit_button.place(relx=0.9, rely=0.6, anchor="center")

        self.remove_button = tk.Button(self.root, text="Eliminar", command=self.remove_product)
        self.remove_button.place(relx=0.9, rely=0.65, anchor="center")

        self.payment_button = tk.Button(self.root, text="Pagar", command=self.payment)
        self.payment_button.place(relx=0.9, rely=0.7, anchor="center")

    #   Actualizar Tiempo
    def update_time(self):
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.time_label.config(text=f"Fecha actual: {current_time}")
        self.root.after(1000, self.update_time)

    #   Actualizar Texto Subtotal
    def update_subtotal(self):

        total_amount = sum(self.products[code]["price"] * quantity for code, quantity in self.current_cart.items())
        self.subtotal_label.config(text=f"Total:{' ' * 186}$ {total_amount}")

    #   Evento Añadir al Carrito        
    def add_to_cart(self, event=None):
        product_code = self.scan_entry.get()
        selected_local = self.local_options.get()

        # Verificar si selecciono local
        if (selected_local) != "":
            self.products = search_products(selected_local[0])
            
            # Verificar si está el codigo en el diccionario de productos
            if product_code in self.products:

                # Verificar si la cantidad del producto sea mayor a 0
                cantidad = self.products[product_code]['quantity']
                if cantidad > 0:
                    
                    # Verficar si el producto ya ha sido agregado al carrito o no
                    if product_code in self.current_cart:
                        if self.current_cart[product_code] >= cantidad:
                            self.message_label.config(text=f"Producto {product_code} fuera de stock ({cantidad})",fg="red")
                        else:

                            # Añade el producto al carrito
                            self.current_cart[product_code] += 1
                            self.message_label.config(text=f"Elemento escaneado: {product_code}", fg="green")
                            self.update_subtotal()
                            self.update_cart_listbox()
                    else:
                        # Añade el producto al carrito
                        self.current_cart[product_code] = 1
                        self.message_label.config(text=f"Elemento escaneado: {product_code}", fg="green")
                        self.update_subtotal()
                        self.update_cart_listbox()
                else:
                    self.message_label.config(text=f"Producto {product_code} fuera de stock ({cantidad})",fg="red")

            else:
                self.message_label.config(text=f"Producto no encontrado {product_code}",fg="red")
            # Borra el contenido del campo Entry
            self.scan_entry.delete(0, tk.END)
        else:
           self.message_label.config(text="Por favor, seleccione un local",fg="red")

    #   Imprime valores del producto en el carrito
    def update_cart_listbox(self):
        self.cart_listbox.delete(0, tk.END)
        for code, quantity in self.current_cart.items():
            product_name = self.products[code]["name"]
            price = self.products[code]["price"]
            self.cart_listbox.insert(tk.END, f"{code:^50}{product_name:^60}{quantity:^63}{price:^65}")

    #   Evento editar cantidad
    def edit_quantity(self):
        selected_index = self.cart_listbox.curselection()
        if selected_index:
            selected_product = list(self.current_cart.keys())[selected_index[0]]
            new_quantity = tk.simpledialog.askinteger("Editar cantidad", "Editar cantidad de "f"{self.products[selected_product]['name']:}")
            if new_quantity is not None:
                if (self.products[selected_product]["quantity"] >= new_quantity) and (new_quantity > 0):
                    self.current_cart[selected_product] = new_quantity
                    self.message_label.config(text=f"Elemento editado: {selected_product}", fg="green")
                    self.update_subtotal()
                    self.update_cart_listbox()
                else:
                    self.message_label.config(text=f"Cantidad invalida, stock ({self.products[selected_product]['quantity']}).", fg="red")
            else:
                self.message_label.config(text="Cantidad invalida.", fg="red")
        else:
            self.message_label.config(text="Por favor, selecciona un producto.", fg="red")

    #   Evento remover producto
    def remove_product(self):
        selected_index = self.cart_listbox.curselection()
        if selected_index:
            selected_product = list(self.current_cart.keys())[selected_index[0]]
            del self.current_cart[selected_product]
            self.message_label.config(text=f"Elemento eliminado: {selected_product}", fg="green")
            self.update_subtotal()
            self.update_cart_listbox()
        else:
            self.message_label.config(text="Por favor, selecciona un producto.", fg="red")

    #   Configuracion para el campo en Efectivo
    def handle_payment_selection(self, event):
        selected_payment_method = self.payment_options.get()
        if selected_payment_method == "Efectivo":
            self.scan_entry2.config(state="normal")
        else:
            # Borra el contenido del campo Entry
            self.scan_entry2.delete(0, tk.END)
            self.scan_entry2.config(state="disabled")

    def add_local_history(self, event):

        selected_local = self.local_options.get()
        self.previous_local.append(selected_local)

    def handle_local_selection(self, event):

        if (self.cart_listbox.size() != 0) and len(self.previous_local) > 2:
            self.message_label.config(text="Vacie el carrito antes de cambiar de sucursal", fg="red")
            previous_selection = self.previous_local.pop()
            self.local_options.set(previous_selection)

    #   Configuracion y condiciones de Metodos de pago
    def payment(self, event=None):
        total_amount = sum(self.products[code]["price"] * quantity for code, quantity in self.current_cart.items())
        local = self.local_options.get()
        if local != "":
            local = str(local)
            local = local.replace(local, local[0])
        else:
            self.message_label.config(text="Por favor, selecciona una sucursal.", fg="red")

        if (total_amount == 0):
            self.message_label.config(text="Por favor, agrega un producto.", fg="red")
            return
        else:
            payment_method = self.payment_options.get()
            if not payment_method:
                self.message_label.config(text="Por favor, selecciona un método de pago.", fg="red")
                return
            
            selected_payment_method = self.payment_options.get()
            if (selected_payment_method == "Efectivo") and (self.scan_entry2.get() != "") and (self.scan_entry2.get().isdigit()):
                payment_quantity = int(self.scan_entry2.get())
                if (not payment_quantity) or (payment_quantity<total_amount):
                    self.message_label.config(text="Por favor, verifica el monto en efectivo.", fg="red")
                else:
                    payment_confirmation = f"Total a pagar: ${total_amount}\nMétodo de pago: {payment_method}\nVuelto: ${payment_quantity-total_amount}"
                    if tk.messagebox.askyesno("Confirmar Pago", payment_confirmation):
                        save_to_file(self, self.current_cart, total_amount, payment_method, payment_quantity, local)
                        self.clear_cart()
                    else:
                        self.message_label.config(text="Pago no confirmado", fg="red")
            elif selected_payment_method == "Efectivo":
                self.message_label.config(text="Por favor, verifica el monto en efectivo.", fg="red")

            else:
                payment_quantity=total_amount
                payment_confirmation = f"Total a pagar: ${total_amount}\nMétodo de pago: {payment_method}"
                if tk.messagebox.askyesno("Confirmar Pago", payment_confirmation):
                    save_to_file(self, self.current_cart, total_amount, payment_method, payment_quantity, local)
                    self.clear_cart()
                else:
                    self.message_label.config(text="Pago no confirmado", fg="red")

    #   Reinicia POS
    def clear_cart(self):
        self.scan_entry.delete(0, tk.END)
        self.current_cart = {}
        self.cart_listbox.delete(0, tk.END)
        self.update_subtotal()
        self.payment_options.set("")
        self.scan_entry2.delete(0, tk.END)
        self.scan_entry2.config(state="disabled")
        self.scan_entry.focus_set()
        self.message_label.config(text="Carrito vacío", fg="black")
  
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