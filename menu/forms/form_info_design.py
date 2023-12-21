import tkinter as tk
import menu.useful.useful_window as util_ventana

class FormInfoDesign(tk.Toplevel):

    def __init__(self):
        super().__init__()
        self.config_window()
        self.widgets()

    def config_window(self):
        # Configuracion de inicio de ventana
        self.title("Viva Control - Info")
        w, h = 400, 100
        util_ventana.centrar_ventana(self, w, h)

    def widgets(self):
        self.lavelVersion = tk.Label(self, text="Version: 1.0")
        self.lavelVersion.config(fg="#000000", font=(
            "Roboto", 15), pady=10, width=20)
        self.lavelVersion.pack() 
        
        self.lavelVersion = tk.Label(self, text="Autor: Richard Mazuelos")
        self.lavelVersion.config(fg="#000000", font=(
            "Roboto", 15), pady=10, width=20)
        self.lavelVersion.pack()