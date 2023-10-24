import tkinter
import customtkinter
from PIL import ImageTk,Image

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green


app = customtkinter.CTk()  #creating cutstom tkinter window
app.geometry("600x440")
app.title('Login')



def button_function():
    app.destroy()            # destroy current window and creating new one 
    w = customtkinter.CTk()  
    w.geometry("1280x720")
    w.title('Welcome')
    l1=customtkinter.CTkLabel(master=w, text="Home Page",font=('Century Gothic',60))
    l1.place(relx=0.5, rely=0.5,  anchor=tkinter.CENTER)
    w.mainloop()
    


img1=ImageTk.PhotoImage(Image.open("./login/assets/pattern.png"))
l1=customtkinter.CTkLabel(master=app,image=img1)
l1.pack()

#creating custom frame
frame=customtkinter.CTkFrame(master=l1, width=320, height=330, corner_radius=15)
frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

l2=customtkinter.CTkLabel(master=frame, text="Inicio Sesión",font=('Century Gothic',20))
l2.place(x=105, y=45)

entry1=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Nombre de Usuario')
entry1.place(x=50, y=110)

entry2=customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Contraseña', show="*")
entry2.place(x=50, y=165)

l3=customtkinter.CTkLabel(master=frame, text="Contraseña Olvidada?",font=('Century Gothic',12))
l3.place(x=155,y=195)

#Create custom button
button1 = customtkinter.CTkButton(master=frame, width=220, text="Iniciar Sesión", command=button_function, corner_radius=6)
button1.place(x=50, y=240)

# You can easily integrate authentication system 
app.mainloop()