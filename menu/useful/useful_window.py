def centrar_ventana(ventana, aplicacion_ancho, aplicacion_largo):
    ventana.update_idletasks()
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_largo = ventana.winfo_screenheight()
    x = int(pantalla_ancho - aplicacion_ancho) // 2
    y = int(pantalla_largo - aplicacion_largo) // 2
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")