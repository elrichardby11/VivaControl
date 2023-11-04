import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime 
from file_operations import save_to_file
from products import products

class PoS():
    def __init__(self, root):
        self.root = root
        self.root.title("VivaControl - Punto de Venta")
        img = tk.PhotoImage(file='./assets/VivaControl.png')
        self.root.iconphoto(False,img)
        self.root.geometry("1280x400")
        self.products = products
        self.current_cart = {}
        self.create_widgets()

    def create_widgets(self):

        #Izquierda
        left_frame = tk.Frame(self.root)
        left_frame.pack(side="left")

        self.time_label = tk.Label(left_frame, text="")
        self.time_label.pack()

        self.scan_label = tk.Label(left_frame, text="Escanea el código del producto:")
        self.scan_label.pack()

        self.scan_entry = tk.Entry(left_frame)
        self.scan_entry.pack()
        self.scan_entry.focus_set()

        self.add_to_cart_button = tk.Button(left_frame, text="Agregar al carrito", command=self.add_to_cart)
        self.add_to_cart_button.pack()

        #Evento Pulsar Enter
        self.scan_entry.bind('<Return>', self.add_to_cart)

        self.message_label = tk.Label(left_frame, text="Escanee un producto ", fg="black")
        self.message_label.pack()

        self.cart_label = tk.Label(left_frame, text="Carrito: ")
        self.cart_label.pack()

        #Tabla para mostrar datos en forma de grilla
        #Considerar que grid, también se puede traducir como grilla
        self.tree = ttk.Treeview(left_frame, height=0, columns=("col2","col3", "col4"))
        #self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading("#0", text="Código", anchor=CENTER)
        self.tree.heading("col2", text="Nombre", anchor=CENTER)
        self.tree.heading("col3", text="Cantidad", anchor=CENTER)
        self.tree.heading("col4", text="Precio", anchor=CENTER)
        self.tree.column("#0", width=262)
        self.tree.column("col2", width=262)
        self.tree.column("col3", width=262)
        self.tree.column("col4", width=262)
        self.tree.pack()

        self.cart_listbox = tk.Listbox(left_frame,borderwidth=2, relief="ridge",width=130)
        self.cart_listbox.pack()

        self.subtotal_label = tk.Label(left_frame, text="Total:    $    0")
        self.subtotal_label.pack()

        #Derecha
        right_frame = tk.Frame(self.root)
        right_frame.pack(side="right")

        self.payment_label = tk.Label(right_frame, text="Selecciona el método de pago:")
        self.payment_label.pack()

        self.payment_options = ttk.Combobox(right_frame, values=['Efectivo', 'Débito', 'Crédito'], state="readonly")
        self.payment_options.bind("<<ComboboxSelected>>", self.handle_payment_selection)
        self.payment_options.pack()

        self.message_label2 = tk.Label(right_frame, text="Monto en Efectivo: ", fg="black")
        self.message_label2.pack()

        self.scan_entry2 = tk.Entry(right_frame, state="disabled")
        self.scan_entry2.pack()

        self.scan_entry2.bind('<Return>', self.payment)

        self.edit_button = tk.Button(right_frame, text="Editar", command=self.edit_quantity)
        self.edit_button.pack()

        self.remove_button = tk.Button(right_frame, text="Eliminar", command=self.remove_product)
        self.remove_button.pack()

        self.payment_button = tk.Button(right_frame, text="Pagar", command=self.payment)
        self.payment_button.pack()

    def update_time(self):
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.time_label.config(text=f"Fecha actual: {current_time}")
        self.root.after(1000, self.update_time)

    def update_subtotal(self):

        total_amount = sum(self.products[code]["price"] * quantity for code, quantity in self.current_cart.items())
        self.subtotal_label.config(text=f"Total:{' ' * 186}$ {total_amount}")
        
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

    def update_cart_listbox(self):
        self.cart_listbox.delete(0, tk.END)
        for code, quantity in self.current_cart.items():
            product_name = self.products[code]["name"]
            price = self.products[code]["price"]
            self.cart_listbox.insert(tk.END, f"{code:^50}{product_name:^60}{quantity:^63}{price:^65}")

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

    def handle_payment_selection(self, event):
        selected_payment_method = self.payment_options.get()
        if selected_payment_method == "Efectivo":
            self.scan_entry2.config(state="normal")
        else:
            # Borra el contenido del campo Entry
            self.scan_entry2.delete(0, tk.END)
            self.scan_entry2.config(state="disabled")

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

def main():
    root = tk.Tk()
    app = PoS(root)
    app.update_time()  # Iniciar la actualización del tiempo
    root.mainloop()

if __name__ == "__main__":
    main()