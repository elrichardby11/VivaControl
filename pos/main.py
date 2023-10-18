import tkinter as tk
from pos.pos import PoS

def main():
    root = tk.Tk()
    app = PoS(root)
    app.update_time()  # Iniciar la actualización del tiempo
    root.mainloop()

if __name__ == "__main__":
    main()
