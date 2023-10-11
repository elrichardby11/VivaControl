import tkinter as tk
from tkinter import simpledialog
from datetime import datetime

class MiniMarketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniMarket - Punto de Venta")
        self.root.geometry("650x400")

        self.products = {
            "7807265064173": {"name": "Producto 1", "price": 1000},
            "67890": {"name": "Producto 2", "price": 1500}
            # Agrega más productos con su información
        }

        self.current_cart = {}  # Código de producto: cantidad
        self.create_widgets()

    def create_widgets(self):
        self.time_label = tk.Label(self.root, text="")
        self.time_label.pack()

        self.scan_label = tk.Label(self.root, text="Escanea el código del producto:")
        self.scan_label.pack()

        self.scan_entry = tk.Entry(self.root)
        self.scan_entry.pack()

        self.add_to_cart_button = tk.Button(self.root, text="Agregar al carrito", command=self.add_to_cart)
        self.add_to_cart_button.pack()

        self.cart_label = tk.Label(self.root, text="Carrito: ")
        self.cart_label.pack()

        self.cart_listbox = tk.Listbox(self.root)
        self.cart_listbox.pack()

        self.edit_button = tk.Button(self.root, text="Editar", command=self.edit_quantity)
        self.edit_button.pack()

        self.remove_button = tk.Button(self.root, text="Eliminar", command=self.remove_product)
        self.remove_button.pack()

        self.payment_button = tk.Button(self.root, text="Pagar", command=self.payment)
        self.payment_button.pack()

    def update_time(self):
        current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.time_label.config(text=f"Fecha actual: {current_time}")
        self.root.after(1000, self.update_time)

    def add_to_cart(self):
        product_code = self.scan_entry.get()
        if product_code in self.products:
            if product_code in self.current_cart:
                self.current_cart[product_code] += 1
            else:
                self.current_cart[product_code] = 1

            self.update_cart_listbox()
        else:
            print("Producto no encontrado")

    def update_cart_listbox(self):
        self.cart_listbox.delete(0, tk.END)
        for code, quantity in self.current_cart.items():
            product_name = self.products[code]["name"]
            self.cart_listbox.insert(tk.END, f"{product_name} - Cantidad: {quantity}")

    def update_cart_listbox(self):
        self.cart_listbox.delete(0, tk.END)
        for code, quantity in self.current_cart.items():
            product_name = self.products[code]["name"]
            self.cart_listbox.insert(tk.END, f"{product_name} - Cantidad: {quantity}")

    def edit_quantity(self):
        selected_index = self.cart_listbox.curselection()
        if selected_index:
            selected_product = list(self.current_cart.keys())[selected_index[0]]
            new_quantity = tk.simpledialog.askinteger("Editar cantidad", f"Editar cantidad de {self.products[selected_product]['name']}:")
            if new_quantity is not None:
                self.current_cart[selected_product] = new_quantity
                self.update_cart_listbox()

    def remove_product(self):
        selected_index = self.cart_listbox.curselection()
        if selected_index:
            selected_product = list(self.current_cart.keys())[selected_index[0]]
            del self.current_cart[selected_product]
            self.update_cart_listbox()

    def payment(self):
        total_amount = sum(self.products[code]["price"] * quantity for code, quantity in self.current_cart.items())
        payment_method = tk.simpledialog.askstring("Método de pago", f"Total a pagar: ${total_amount}\nIngrese el método de pago:")
        if payment_method:
            self.save_to_file(total_amount, payment_method)

    def save_to_file(self, total_amount, payment_method):
        now = datetime.now()
        #Nombre del Archivo
        filename = now.strftime("%Y-%m-%d_%H-%M-%S.txt")
        formatted_date = now.strftime("Fecha: %Y-%m-%d")
        formatted_time = now.strftime("Hora: %H:%M:%S")

        neto = round(total_amount / 1.19)
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
            file.write(f"Fecha: {formatted_date}          Hora: {formatted_time}\n")
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
                    file.write(f"Codigo: {product_code}\n")
                    file.write(f"{formatted_quantity:>3}X{formatted_price} {product_name:<33}$ {formatted_total_price:>10}\n")
                else:
                    file.write(f"{product_code} {product_name:<29}$ {formatted_total_price:>10}\n")
            file.write(" -----------------------------------------------------\n")
            file.write(f"                             Neto:         $ {format_number(neto):>10}\n")
            file.write(f"                             IVA 19%:      $ {format_number(iva):>10}\n")
            file.write(f"                             TOTAL:        $ {format_number(total_amount):>10}\n")
            file.write(" ---------------------P A G O S-----------------------\n")
            file.write(f" {payment_method}           $ {format_number(total_amount):>10}\n")
            file.write(" Vuelto             $     0\n")
            file.write(" =====================================================\n")

        print(f"Registro guardado en {filename}")

def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")


def main():
    root = tk.Tk()
    app = MiniMarketApp(root)

    app.update_time()  # Iniciar la actualización del tiempo
    root.mainloop()

if __name__ == "__main__":
    main()
