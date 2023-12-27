import tkinter as tk
import customtkinter
from PIL import ImageTk, Image
from dotenv import load_dotenv
import os
import ast
from menu.forms import form_main_design as form
import menu.useful.useful_window as util_ventana

class Login:

    def __init__(self, root):
        self.root = root

        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
 
        self.root.title('VivaControl - Login')
        util_ventana.centrar_ventana(self.root, 600, 440)

        load_dotenv() # Load user and passwords

        self.widgets()

    def widgets(self):
        self.img1 = Image.open("./assets/pattern.png")
        self.photo = ImageTk.PhotoImage(self.img1)
        self.l1 = tk.Label(master=self.root, image=self.photo)
        self.l1.pack()

        # Creating custom frame
        self.frame = customtkinter.CTkFrame(master=self.l1, width=320, height=330, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.l2 = customtkinter.CTkLabel(master=self.frame, text="Inicio Sesión", font=('Century Gothic', 20))
        self.l2.place(x=105, y=45)

        self.text_var = tk.StringVar(value="")
        
        self.label2 = customtkinter.CTkLabel(master=self.frame,
                                    textvariable=self.text_var,
                                    font=('Century Gothic', 10),
                                    width=220,
                                    height=25,
                                    text_color="black",
                                    fg_color="transparent",
                                    corner_radius=5)
        self.label2.place(x=160, y=90, anchor=tk.CENTER)

        self.nombre_de_usuario = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Nombre de Usuario')
        self.nombre_de_usuario.place(x=50, y=115)

        self.contrasena = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Contraseña', show="*")
        self.contrasena.place(x=50, y=170)

        # Events press Enter
        self.nombre_de_usuario.bind('<Return>', self.verificar_credenciales)
        self.contrasena.bind('<Return>', self.verificar_credenciales)

        self.l4 = customtkinter.CTkLabel(master=self.frame, text="Contraseña Olvidada?", font=('Century Gothic', 12))
        self.l4.place(x=155, y=200)

        # Create custom button
        self.button1 = customtkinter.CTkButton(master=self.frame, width=220, text="Iniciar Sesión", command= self.verificar_credenciales, corner_radius=6)
        self.button1.place(x=50, y=245)

    def button_function(self, event=None):
        self.root.destroy()  # destroy current window
        app = form.FormMainDesign()
        app.mainloop()

    def verificar_credenciales(self, event=None):
        usuario = self.nombre_de_usuario.get()
        contrasena = self.contrasena.get()

        users_and_passwords_str = os.environ.get("USERS_AND_PASSWORDS", "")
        users_and_passwords = ast.literal_eval(users_and_passwords_str)
    
        credentials_correct = any(user == usuario and password == contrasena for user, password in users_and_passwords)

        if credentials_correct:
            self.button_function(self)
        else:
            self.text_var.set("Credenciales Incorrectas.")
            self.label2.configure(textvariable=self.text_var, fg_color=("#ffa372", "gray75"))

def main():
    root = tk.Tk()
    login = Login(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()