import tkinter as tk
from tkinter import messagebox
from pos import PoS

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("300x150")

        self.username_label = tk.Label(self.root, text="Usuario:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        self.password_label = tk.Label(self.root, text="Contraseña:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.root, show="*")  # Muestra asteriscos en lugar de la contraseña
        self.password_entry.pack()

        self.login_button = tk.Button(self.root, text="Iniciar Sesión", command=self.check_login)
        self.login_button.pack()

    def check_login(self):
        # Verifica las credenciales (nombre de usuario y contraseña)
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "usuario" and password == "contraseña":
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso.")       
            self.root.destroy()  # Cierra la ventana de inicio de sesión
            PoS(self.root)  # Abre la ventana de POS desde el archivo PoS.py        
        else:
            messagebox.showerror("Error", "Credenciales incorrectas. Por favor, inténtalo de nuevo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
