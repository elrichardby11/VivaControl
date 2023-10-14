import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime   

class PoS:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniMarket - Punto de Venta")
        self.root.geometry("650x540")

        self.products = {
            "7807265064173": {"name": "Producto 1", "price": 1000},
            "7501007528427": {"name": "Producto 2", "price": 1500}
            # Agrega más productos con su información
        }

        self.current_cart = {}
        self.create_widgets()

    def create_widgets(self):
        self.time_label = tk.Label(self.root, text="")
        self.time_label.pack()

        self.scan_label = tk.Label(self.root, text="Escanea el código del producto:")
        self.scan_label.pack()

        self.scan_entry = tk.Entry(self.root)
        self.scan_entry.pack()
        self.scan_entry.focus_set()

        self.add_to_cart_button = tk.Button(self.root, text="Agregar al carrito", command=self.add_to_cart)
        self.add_to_cart_button.pack()

        #Evento Pulsar Enter
        self.scan_entry.bind('<Return>', self.add_to_cart)

        self.message_label = tk.Label(self.root, text="Escanee un producto ", fg="black")
        self.message_label.pack()

        self.cart_label = tk.Label(self.root, text="Carrito: ")
        self.cart_label.pack()

        self.cart_listbox = tk.Listbox(self.root,borderwidth=3, relief="ridge",width=60)
        self.cart_listbox.pack()
        self.subtotal_label = tk.Label(self.root, text="Subtotal:    $    0")
        self.subtotal_label.pack()

        self.edit_button = tk.Button(self.root, text="Editar", command=self.edit_quantity)
        self.edit_button.pack()

        self.remove_button = tk.Button(self.root, text="Eliminar", command=self.remove_product)
        self.remove_button.pack()

        self.payment_button = tk.Button(self.root, text="Pagar", command=self.payment)
        self.payment_button.pack()

        self.payment_label = tk.Label(self.root, text="Selecciona el método de pago:")
        self.payment_label.pack()

        self.payment_options = ttk.Combobox(self.root, values=['Efectivo', 'Débito', 'Crédito'], state="readonly")
        self.payment_options.bind("<<ComboboxSelected>>", self.handle_payment_selection)
        self.payment_options.pack()

        self.message_label2 = tk.Label(self.root, text="Monto en Efectivo: ", fg="black")
        self.message_label2.pack()

        self.scan_entry2 = tk.Entry(self.root, state="disabled")
        self.scan_entry2.pack()

    def update_time(self):
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.time_label.config(text=f"Fecha actual: {current_time}")
        self.root.after(1000, self.update_time)

    def update_subtotal(self):

        total_amount = sum(self.products[code]["price"] * quantity for code, quantity in self.current_cart.items())
        self.subtotal_label.config(text=f"Subtotal:    $    {total_amount:>90}")

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
            self.cart_listbox.insert(tk.END, f"{code} - {product_name:<40} Cant: {quantity} - Precio: {price:<10}")

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

    def remove_product(self):
        selected_index = self.cart_listbox.curselection()
        if selected_index:
            selected_product = list(self.current_cart.keys())[selected_index[0]]
            del self.current_cart[selected_product]
            self.message_label.config(text=f"Elemento eliminado: {selected_product}", fg="green")
            self.update_subtotal()
            self.update_cart_listbox()


    def handle_payment_selection(self, event):
        selected_payment_method = self.payment_options.get()
        if selected_payment_method == "Efectivo":
            self.scan_entry2.config(state="normal")
        else:
            # Borra el contenido del campo Entry
            self.scan_entry2.delete(0, tk.END)
            self.scan_entry2.config(state="disabled")

    def payment(self):
        total_amount = sum(self.products[code]["price"] * quantity for code, quantity in self.current_cart.items())
        if (total_amount == 0):
            self.message_label.config(text="Por favor, selecciona un producto.", fg="red")
            return
        else:
            payment_method = self.payment_options.get()
            if not payment_method:
                self.message_label.config(text="Por favor, selecciona un método de pago.", fg="red")
                return
            
            selected_payment_method = self.payment_options.get()
            if (selected_payment_method == "Efectivo") and (self.scan_entry2.get() != ""):
                payment_quantity = int(self.scan_entry2.get())
                if (not payment_quantity) or (payment_quantity<total_amount):
                    self.message_label.config(text="Por favor, verifica el monto en efectivo.", fg="red")
                else:
                    payment_confirmation = f"Total a pagar: ${total_amount}\nMétodo de pago: {payment_method}\nVuelto: ${payment_quantity-total_amount}"
                    if tk.messagebox.askyesno("Confirmar Pago", payment_confirmation):
                        self.save_to_file(total_amount, payment_method, payment_quantity)
                        self.clear_cart()
                    else:
                        self.message_label.config(text="Pago no confirmado", fg="red")
            elif selected_payment_method == "Efectivo":
                self.message_label.config(text="Por favor, verifica el monto en efectivo.", fg="red")

            else:
                payment_quantity=total_amount
                payment_confirmation = f"Total a pagar: ${total_amount}\nMétodo de pago: {payment_method}"
                if tk.messagebox.askyesno("Confirmar Pago", payment_confirmation):
                    self.save_to_file(total_amount, payment_method, payment_quantity)
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

    def save_to_file(self, total_amount, payment_method, payment_quantity):
        now = datetime.now()
        #Nombre del Archivo
        filename = now.strftime("%Y-%m-%d_%H-%M-%S.txt")
        formatted_date = now.strftime("Fecha: %d-%m-%Y")
        formatted_time = now.strftime("Hora: %H:%M:%S")

        neto = round    (total_amount / 1.19)
        iva = round(total_amount - neto)

        with open(filename, "w") as file:
            file.write(" _____________________________________________________ \n")
            file.write("|                                                     |\n")
            file.write("|RUT: 11.111.111-1                                    |\n")
            file.write("|RAZON SOCIAL: FANTASIA S.A                           |\n")
            file.write("|BLABLA NRO 999 - PISO 2234B                          |\n")
            file.write("|LAS CONDES - SANTIAGO F. -256784321                  |\n")
            file.write("|GIRO: VENTAS AL POR MENOS DE MERCADERIA              |\n")
            file.write("|_____________________________________________________|\n")
            file.write(f" {formatted_date}          {formatted_time}\n")
            file.write(" Boleta Electronica:        123.456.789\n")
            file.write(" CAJA: 2 CAJERO: RICHARD MAZUELOS\n")
            file.write(" D E T A L L E\n")
            file.write(" ---------------\n")
            
            for code, quantity in self.current_cart.items():
                product_code = code
                product_name = self.products[code]["name"]
                price = self.products[code]["price"]
                total_price = quantity * price
                formatted_quantity = format_number(quantity)
                formatted_price = format_number(price)
                formatted_total_price = format_number(total_price)
                if quantity > 1:
                    file.write(f" Codigo: {product_code}\n")
                    file.write(f"{formatted_quantity:>3}X{formatted_price} {product_name:<33}$ {formatted_total_price:>10}\n")
                else:
                    file.write(f" {product_code} {product_name:<28}$ {formatted_total_price:>10}\n")
            file.write(" -----------------------------------------------------\n")
            file.write(f"                             Neto:         $ {format_number(neto):>10}\n")
            file.write(f"                             IVA 19%:      $ {format_number(iva):>10}\n")
            file.write(f"                             TOTAL:        $ {format_number(total_amount):>10}\n")
            file.write(" ---------------------P A G O S-----------------------\n")
            if payment_method == "Efectivo":
                file.write(f" {payment_method}           $ {format_number(payment_quantity):>10}\n")
                file.write(f" Vuelto             $ { format_number(payment_quantity-total_amount):>10}\n")
                file.write(" =====================================================\n")
            else:
                file.write(f" {payment_method:<7}           $ {format_number(total_amount):>10}\n")
                file.write(" Vuelto            $          0\n")
                file.write(" =====================================================\n")

        print(f"Registro guardado en {filename}")


def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")

def main():
    root = tk.Tk()
    app = PoS(root)
    app.update_time()  # Iniciar la actualización del tiempo
    root.mainloop()

if __name__ == "__main__":
    main()