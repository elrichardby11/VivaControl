import tkinter
import customtkinter
from PIL import ImageTk, Image

class Login:

    def __init__(self, root):
        self.root = root
        customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
        self.root.geometry("600x440")
        self.root.title('Login')
        self.widgets()

    def widgets(self):
        self.img1 = ImageTk.PhotoImage(Image.open("./login/assets/pattern.png"))
        self.l1 = customtkinter.CTkLabel(master=self.root, image=self.img1)
        self.l1.pack()

        # Creating custom frame
        self.frame = customtkinter.CTkFrame(master=self.l1, width=320, height=330, corner_radius=15)
        self.frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

        self.l2 = customtkinter.CTkLabel(master=self.frame, text="Inicio Sesión", font=('Century Gothic', 20))
        self.l2.place(x=105, y=45)

        self.entry1 = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Nombre de Usuario')
        self.entry1.place(x=50, y=110)

        self.entry2 = customtkinter.CTkEntry(master=self.frame, width=220, placeholder_text='Contraseña', show="*")
        self.entry2.place(x=50, y=165)

        # Evento Pulsar Enter
        self.entry2.bind('<Return>', self.button_function)

        self.l3 = customtkinter.CTkLabel(master=self.frame, text="Contraseña Olvidada?", font=('Century Gothic', 12))
        self.l3.place(x=155, y=195)

        # Create custom button
        self.button1 = customtkinter.CTkButton(master=self.frame, width=220, text="Iniciar Sesión", command=self.button_function, corner_radius=6)
        self.button1.place(x=50, y=240)

    def button_function(self, event=None):
        self.root.destroy()  # destroy current window and creating new one
        self.w = customtkinter.CTk()
        self.w.geometry("1280x720")
        self.w.title('Welcome')
        self.l1 = customtkinter.CTkLabel(master=self.w, text="Home Page", font=('Century Gothic', 60))
        self.l1.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
        self.w.mainloop()

def main():
    # You can easily integrate authentication system
    root = tkinter.Tk()
    login = Login(root)
    root.mainloop()
    
if __name__ == "__main__":
    main()
