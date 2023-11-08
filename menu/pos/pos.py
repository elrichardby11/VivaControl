import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime 
from pos.file_operations import save_to_file
from pos.products import products

class PoS():

    def __init__(self, root, **kwargs):
        self.root = root
        self.root.title("VivaControl - Punto de Venta")
        #self.root.geometry("1280x400")

        self.state = False
        root.attributes("-fullscreen", self.state)  # Configura el modo de pantalla completa

        root.bind("<F11>", self.toggle_fullscreen)  # Atajo de teclado para alternar la pantalla completa
        root.bind("<Escape>", self.quit_fullscreen)  # Atajo de teclado para salir de pantalla completa

        self.products = products
        self.current_cart = {}
        self.create_widgets()

    def create_widgets(self):

        # Izquierda
        left_frame = tk.Frame(self.root)
        left_frame.grid(row=0, column=0, padx=10, pady=50, sticky="nsew")

        self.time_label = tk.Label(left_frame, text="")
        self.time_label.grid(row=0, column=0)

        self.scan_label = tk.Label(left_frame, text="Escanea el código del producto:")
        self.scan_label.grid(row=1, column=0, padx=10, pady=5)

        self.scan_entry = tk.Entry(left_frame)
        self.scan_entry.grid(row=2, column=0, padx=10, pady=0)
        self.scan_entry.focus_set()

        self.add_to_cart_button = tk.Button(left_frame, text="Agregar al carrito", command=self.add_to_cart)
        self.add_to_cart_button.grid(row=3, column=0, padx=10, pady=5)

        self.message_label = tk.Label(left_frame, text="Escanee un producto ", fg="black")
        self.message_label.grid(row=4, column=0, padx=10, pady=5)

        self.cart_label = tk.Label(left_frame, text="Carrito: ")
        self.cart_label.grid(row=5, column=0, padx=10, pady=5)

        self.tree = ttk.Treeview(left_frame, height=0, columns=("col2", "col3", "col4"))
        self.tree.grid(row=6, column=0, padx=10, pady=0)
        self.tree.heading("#0", text="Código", anchor=tk.CENTER)
        self.tree.heading("col2", text="Nombre", anchor=tk.CENTER)
        self.tree.heading("col3", text="Cantidad", anchor=tk.CENTER)
        self.tree.heading("col4", text="Precio", anchor=tk.CENTER)
        self.tree.column("#0", width=262)
        self.tree.column("col2", width=262)
        self.tree.column("col3", width=262)
        self.tree.column("col4", width=262)

        self.cart_listbox = tk.Listbox(left_frame, borderwidth=2, relief="ridge", height=25, width=130)
        self.cart_listbox.grid(row=7, column=0, padx=10, pady=0)

        self.subtotal_label = tk.Label(left_frame, text="Total:    $    0")
        self.subtotal_label.grid(row=8, column=0, padx=10, pady=5)

        # Derecha
        right_frame = tk.Frame(self.root)
        right_frame.grid(row=0, column=1, padx=10, pady=250, sticky="nsew")

        self.payment_label = tk.Label(right_frame, text="Selecciona el método de pago:")
        self.payment_label.grid(row=2, column=0, padx=5)

        self.payment_options = ttk.Combobox(right_frame, values=['Efectivo', 'Débito', 'Crédito'], state="readonly")
        self.payment_options.bind("<<ComboboxSelected>>", self.handle_payment_selection)
        self.payment_options.grid(row=3, column=0, padx=10, pady=5)

        self.message_label2 = tk.Label(right_frame, text="Monto en Efectivo: ", fg="black")
        self.message_label2.grid(row=4, column=0, padx=10, pady=5)

        self.scan_entry2 = tk.Entry(right_frame, state="disabled")
        self.scan_entry2.grid(row=5, column=0, padx=10, pady=5)

        self.edit_button = tk.Button(right_frame, text="Editar", command=self.edit_quantity)
        self.edit_button.grid(row=6, column=0, padx=10, pady=2)

        self.remove_button = tk.Button(right_frame, text="Eliminar", command=self.remove_product)
        self.remove_button.grid(row=7, column=0, padx=10, pady=2)

        self.payment_button = tk.Button(right_frame, text="Pagar", command=self.payment)
        self.payment_button.grid(row=8, column=0, padx=10, pady=2)

        self.close_button = tk.Button(right_frame, text="Salir", command=self.exit)
        self.close_button.grid(row=9, column=0, padx=10, pady=50)

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
        if product_code in self.products:
            if product_code in self.current_cart:
                self.current_cart[product_code] += 1
            else:
                self.current_cart[product_code] = 1

            self.message_label.config(text=f"Elemento escaneado: {product_code}", fg="green")
            self.update_subtotal()
            self.update_cart_listbox()
        else:
            self.message_label.config(text=f"Producto no encontrado {product_code}",fg="red")
        # Borra el contenido del campo Entry
        self.scan_entry.delete(0, tk.END)

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
                self.current_cart[selected_product] = new_quantity
                self.message_label.config(text=f"Elemento editado: {selected_product}", fg="green")
                self.update_subtotal()
                self.update_cart_listbox()
            else:
                pass
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

    #   Configuracion y condiciones de Metodos de pago
    def payment(self, event=None):
        total_amount = sum(self.products[code]["price"] * quantity for code, quantity in self.current_cart.items())
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
                        save_to_file(self, self.current_cart, total_amount, payment_method, payment_quantity)
                        self.clear_cart()
                    else:
                        self.message_label.config(text="Pago no confirmado", fg="red")
            elif selected_payment_method == "Efectivo":
                self.message_label.config(text="Por favor, verifica el monto en efectivo.", fg="red")

            else:
                payment_quantity=total_amount
                payment_confirmation = f"Total a pagar: ${total_amount}\nMétodo de pago: {payment_method}"
                if tk.messagebox.askyesno("Confirmar Pago", payment_confirmation):
                    save_to_file(self, self.current_cart, total_amount, payment_method, payment_quantity)
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

    def exit(self):
        self.root.destroy()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.root.attributes("-fullscreen", self.state)

    def quit_fullscreen(self, event=None):
        self.state = False
        self.root.attributes("-fullscreen", self.state)

    def main():
        root = tk.Tk()
        app = PoS(root) 
        app.update_time() # Programar la primera actualización
        root.mainloop()
