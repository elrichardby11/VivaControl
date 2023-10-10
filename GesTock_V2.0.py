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

        self.cart_label = tk.Label(self.root, text="Carrito:")
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
        self.time_label.config(text=f"Hora actual: {current_time}")
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
        filename = now.strftime("%Y-%m-%d_%H-%M-%S.txt")
        with open(filename, "w") as file:
            file.write(f"Fecha y Hora: {now}\n")
            file.write("Productos comprados:\n")
            for code, quantity in self.current_cart.items():
                product_name = self.products[code]["name"]
                file.write(f"{product_name} - Cantidad: {quantity}\n")
            file.write(f"Total: ${total_amount}\n")
            file.write(f"Método de pago: {payment_method}\n")
        
        print(f"Registro guardado en {filename}")

def main():
    root = tk.Tk()
    app = MiniMarketApp(root)

    app.update_time()  # Iniciar la actualización del tiempo
    root.mainloop()

if __name__ == "__main__":
    main()
