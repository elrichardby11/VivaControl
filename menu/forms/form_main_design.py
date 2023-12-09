import tkinter as tk
from tkinter import font
import subprocess
from config import color_barra_superior, color_cuerpo_principal, color_menu_cursor_encima, color_menu_lateral
import useful.useful_assets as util_img
import useful.useful_window as util_ventana
from forms.form_info_design import FormInfoDesign
import time

class FormMainDesign(tk.Tk):

    def __init__(self):
        super().__init__()
        #self.logo = util_img.leer_imagen("/home/richard/Documentos/VivaControl/01.CODE/assets/VivaControl.png", (560, 136))
        self.perfil = util_img.leer_imagen("/home/richard/Documentos/VivaControl/01.CODE/assets/Profile.png", (100,100))
        self.config_window()
        self.panels()
        self.top_bar_controls()
        self.lateral_menu_controls()

    def config_window(self):
        #Configuracion de la ventana inicial
        self.title("VivaControl - Bienvenido")
        #self.iconbitmap("../01.CODE/assets/VivaControl.png")
        w, h = 1024, 600
        #self.geometry("%dx%d+0+0" % w,h)
        util_ventana.centrar_ventana(self, w, h)

    def panels(self):
        #Crear paneles: barra superior, menu lateral y cuerpo principal
        self.barra_superior = tk.Frame(self, bg=color_barra_superior, height=50)
        self.barra_superior.pack(side=tk.TOP, fill="both")

        self.menu_lateral = tk.Frame(self, bg=color_menu_lateral, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill="both", expand=False)

        self.cuerpo_principal = tk.Frame(self, bg=color_cuerpo_principal)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill="both", expand=True)

    def top_bar_controls(self):
        #Configuracion barra superior
        font_awesome = font.Font(family="FontAwesome", size=12)

        #Etiqueta titulo
        self.labelTitle = tk.Label(self.barra_superior, text="VivaControl")
        self.labelTitle.config(fg="#fff", font=(
           "Roboto", 15), bg=color_barra_superior, pady=10, width=16)
        self.labelTitle.pack(side=tk.LEFT)

        #Boton del menu lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                           command=self.toggle_panel, 
                                           bd=0, bg=color_barra_superior, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        #Etiqueta información
        self.labelTitle = tk.Label(self.barra_superior, text="contacto@vivacontrol.cl")
        self.labelTitle.config(fg="#fff", font=(
           "Roboto", 15), bg=color_barra_superior, padx=10, width=20)
        self.labelTitle.pack(side=tk.RIGHT)

    def lateral_menu_controls(self):
        #Configuracion menu lateral
        width = 20
        height = 2
        font_awesome = font.Font(family="FontAwesome", size=12)

        #Etiqueta de perfil
        self.perfilLabel = tk.Label(self.menu_lateral, image=self.perfil, bg=color_menu_lateral)
        self.perfilLabel.pack(side=tk.TOP, pady=10, padx=2)

        self.buttonPoS = tk.Button(self.menu_lateral)
        self.buttonAux = tk.Button(self.menu_lateral)
        self.buttonProfile = tk.Button(self.menu_lateral)
        self.buttonInfo = tk.Button(self.menu_lateral)
        self.buttonSettings = tk.Button(self.menu_lateral)
        
        buttons_info = [
            ("Punto de Venta", "\uf07a", self.buttonPoS, self.open_pos),
            ("Auxiliares", "\uf0c0", self.buttonAux, self.open_aux),
            ("Perfil", "\uf4ff", self.buttonProfile,  self.open_panel_info),
            (" Info", "\uf05a", self.buttonInfo,  self.open_panel_info),
            (" Ajustes", "\uf013", self.buttonSettings,  self.open_panel_info)
        ]

        for text, icon, button, comando in buttons_info:
            self.config_button_menu(button, text, icon, font_awesome, width, height, comando)

    def config_button_menu(self, button, text, icon, font_awesome, width, height, comando):
        button.config(text=f"   {icon}      {text}", anchor="w", font=font_awesome, bd=0,
                      bg=color_menu_lateral, fg="white", width=width, height=height,
                      command=comando)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        #Asociar eventos enter y leave con la funcion dinamica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        #Cambiar estilo de boton al pasar el raton por encima
        button.config(bg=color_menu_cursor_encima, fg="white")

    def on_leave(self, event, button):
        #Cambiar estilo de boton al pasar el raton por encima
        button.config(bg=color_menu_lateral, fg="white")

    def toggle_panel(self):
        #Alternar visibilidad del panel
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill="y")

    def open_panel_info(self):
        FormInfoDesign()

    def open_pos(self): 

        main_pos = '../01.CODE/menu/pos/main.py'
        try:
            self.proceso = subprocess.Popen(["python3", main_pos])
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar {main_pos}: {e}")

        # Ocultar la ventana temporalmente
        self.withdraw()

        # Verificar el estado del proceso en intervalos regulares
        while True:
            if self.proceso.poll() is not None:
                # El proceso ha terminado, puedes mostrar la ventana
                self.deiconify()
                break

            # Pausa para evitar un uso excesivo de la CPU
            time.sleep(0.2)

    def open_aux(self): 

        main_pos = '../01.CODE/menu/aux/main.py'
        try:
            self.proceso = subprocess.Popen(["python3", main_pos])
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar {main_pos}: {e}")

        # Ocultar la ventana temporalmente
        self.withdraw()

        # Verificar el estado del proceso en intervalos regulares
        while True:
            if self.proceso.poll() is not None:
                # El proceso ha terminado, puedes mostrar la ventana
                self.deiconify()
                break

            # Pausa para evitar un uso excesivo de la CPU
            time.sleep(0.2)

