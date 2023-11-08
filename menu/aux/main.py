import tkinter as tk
from aux import aux

def main():

    root = tk.Tk()
    app = aux(root)
#    app.update_time()  # Iniciar la actualización del tiempo
    root.mainloop()


if __name__ == "__main__":
    main()
