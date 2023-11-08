import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog


class aux():
    
    def __init__(self, root):
        self.root = root
        self.root.title("VivaControl - Auxiliares")
        self.root.geometry("1280x720")
        self.create_widgets()
        
    
    def create_widgets(self):
        barra_superior = tk.Frame(self.root, height=50)
        barra_superior.pack(side="top")
        
        barra_izquierda = tk.Frame(self.root)
        barra_izquierda.pack(side="left")

        barra_derecha = tk.Frame(self.root)
        barra_derecha.pack(side="right")

        self.scan_label = tk.Label(barra_izquierda, text="Ingrese el texto a buscar: ")
        self.scan_label.pack()

        self.scan_entry = tk.Entry(barra_izquierda, width=100)
        self.scan_entry.pack()
        self.scan_entry.focus()

        self.button_search = tk.Button(barra_derecha, text="Buscar", anchor=CENTER, command=self.search)
        self.button_search.pack()

        self.button_clear = tk.Button(barra_derecha, text="Limpiar", anchor=CENTER, command=self.clear)
        self.button_clear.pack()

        self.cart_listbox = tk.Listbox(barra_izquierda,borderwidth=2, relief="ridge",width=100)
        self.cart_listbox.pack()



    def search(self):
        pass

    def clear(self):
        pass


def main():
    root = tk.Tk()
    app = aux(root)
    #app.update_time()  # Iniciar la actualización del tiempo
    root.mainloop()

if __name__ == "__main__":
    main()