import tkinter
import customtkinter
from PIL import ImageTk, Image
import subprocess

class Login:

    def __init__(self, root):
        self.root = root
        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
        self.root.geometry("600x440")
        self.root.title('VivaControl - Login')
        self.widgets()

    def widgets(self):
        self.img1 = ImageTk.PhotoImage(Image.open("./assets/pattern.png"))
        self.l1 = customtkinter.CTkLabel(master=self.root, image=self.img1)
        self.l1.pack()

        # Creating custom frame
        self.frame = customtkinter.CTkFrame(master=self.l1, width=320, height=330, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.l2 = customtkinter.CTkLabel(master=self.frame, text="Inicio Sesión", font=('Century Gothic', 20))
        self.l2.place(x=105, y=45)

        text_var = tkinter.StringVar(value="")
        
        self.label2 = customtkinter.CTkLabel(master=self.frame,
                                    textvariable=text_var,
                                    font=('Century Gothic', 10),
                                    width=220,
                                    height=25,
                                    text_color="black",
                                    fg_color="transparent",
                                    #fg_color=("#ffa372", "gray75"),
                                    corner_radius=5)
        self.label2.place(x=160, y=90, anchor=tkinter.CENTER)

        self.nombre_de_usuario = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Nombre de Usuario')
        self.nombre_de_usuario.place(x=50, y=115)

        self.contrasena = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Contraseña', show="*")
        self.contrasena.place(x=50, y=170)

        # Evento Pulsar Enter
        self.contrasena.bind('<Return>', self.registrar_usuario)

        self.l4 = customtkinter.CTkLabel(master=self.frame, text="Contraseña Olvidada?", font=('Century Gothic', 12))
        self.l4.place(x=155, y=200)

        # Create custom button
        self.button1 = customtkinter.CTkButton(master=self.frame, width=220, text="Iniciar Sesión", command= self.verificar_credenciales, corner_radius=6)
        self.button1.place(x=50, y=245)

    def button_function(self, event=None):

        self.root.destroy()  # destroy current window
        main_pos = '../01.CODE/menu/main.py'
        try:
            subprocess.run(["python3", main_pos], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar {main_pos}: {e}")

    def registrar_usuario(self, event=None):
        self.nombre = self.nombre_de_usuario.get()
        self.password = self.contrasena.get()
        with open('../01.CODE/usuarios.txt', 'a') as archivo:
            archivo.write(f"{self.nombre},{self.password}\n")

    def verificar_credenciales(self):
        nombre_de_usuario = self.nombre_de_usuario.get()
        contrasena_ingresada = self.contrasena.get()
        with open('../01.CODE/usuarios.txt', 'r') as archivo:
            for linea in archivo:
                usuario, contrasena = linea.strip().split(',')
                if usuario == nombre_de_usuario and contrasena == contrasena_ingresada:
                    self.button_function(self)
                else:
                    self.text_var = tkinter.StringVar(value="Credenciales Incorrectas.")
                    self.label2.configure(textvariable=self.text_var, fg_color=("#ffa372", "gray75"))

def main():
    # You can easily integrate authentication system
    root = tkinter.Tk()
    login = Login(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
