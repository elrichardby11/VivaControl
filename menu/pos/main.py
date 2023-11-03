import tkinter as tk
import cx_Oracle
import time
from pos import PoS


def main():

    try:
        conexion=cx_Oracle.connect(
        user="Juan_Rodriguez",
        password="Mn3rP7oBsKxL#",
        dsn="XE")
    except Exception as err:
        print("Error en la conexion a la base: ", err) #mensaje de error
        print("Contacta con los desarrolladores. ")
        exit()
    else:
        print("Conectado a la base correctamente!", conexion.version) #mensaje de exito
        print("Bienvenido a la gestion de la base de datos")
        print("")
        print("-------------------------------------------")
        print("---------- G E S T O C K - 1.0.0 ----------")
        print("-------------------------------------------")
        print("")

        time.sleep(3)
        
        root = tk.Tk()
        app = PoS(root)
        app.update_time()  # Iniciar la actualización del tiempo
        root.mainloop()


if __name__ == "__main__":
    main()
