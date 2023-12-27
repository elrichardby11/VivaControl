import cx_Oracle

def search_products(*args):

    if args is not None:
        args = str(args)
        args = args.replace(args, args[2])

    # Conectar a la base de datos Oracle
    connection = cx_Oracle.connect("VivaControl/T$g#kP2LMv8X@XE")

    # Crear un cursor
    cursor = connection.cursor()

    # Ejecutar la consulta SQL
    cursor.execute(f"SELECT ID_PRODUCTO, NOMBRE, PRECIO FROM PRODUCTO JOIN SUCURSAL_PRODUCTO ON SUCURSAL_PRODUCTO.ID_PROD = PRODUCTO.ID_PRODUCTO WHERE ID_SUCURSAL = {args}")
    # Obtener los resultados de la consulta
    results = cursor.fetchall()

    # Cerrar la conexión
    connection.close()

    # Crear un diccionario para almacenar los datos
    products = {}

    # Procesar los resultados
    for row in results:
        id_producto, nombre, precio = row
        
        if id_producto not in products:
        
            # Si el producto no está en el diccionario, lo agrega con su precio de venta actual
            products[id_producto] = {"name": nombre, "price": precio}
        else:
        
            # Si el producto ya está en el diccionario, actualiza el precio de venta si es más reciente
            products[id_producto]["price"] = precio

    # El diccionario 'products' ahora contiene los datos con el precio de venta más reciente

    # Crea un nuevo diccionario con claves convertidas a texto
    products = {str(key): value for key, value in products.items()}
    return products
