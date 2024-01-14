import cx_Oracle
from dotenv import load_dotenv
import os

def search_products(*args):

    load_dotenv() # Load database

    if args is not None:
        args = str(args)
        args = args.replace(args, args[2])

    connection_str = f"{os.getenv('NAME_DATABASE')}/{os.getenv('PASSWORD_DATABASE')}@XE"

    with cx_Oracle.connect(connection_str) as con:

        # Crear un cursor
        with con.cursor() as cursor:

            # Ejecutar la consulta SQL
            cursor.execute(f"SELECT ID_PRODUCTO, NOMBRE, PRECIO, CANTIDAD FROM PRODUCTO JOIN SUCURSAL_PRODUCTO ON SUCURSAL_PRODUCTO.ID_PROD = PRODUCTO.ID_PRODUCTO WHERE ID_SUCURSAL = {args}")
                    
            # Obtener los resultados de la consulta
            results = cursor.fetchall()

    # Crear un diccionario para almacenar los datos
    products = {}

    # Procesar los resultados
    for row in results:
        id_producto, nombre, precio, cantidad = row
        
        if id_producto not in products:
        
            # Si el producto no está en el diccionario, lo agrega con su precio de venta actual
            products[id_producto] = {"name": nombre, "price": precio, "quantity": cantidad}
        else:
        
            # Si el producto ya está en el diccionario, actualiza el precio de venta si es más reciente y cantidad
            products[id_producto]["price"] = precio
            products[id_producto]["quantity"] = cantidad

    # El diccionario 'products' ahora contiene los datos con el precio de venta más reciente

    # Crea un nuevo diccionario con claves convertidas a texto
    products = {str(key): value for key, value in products.items()}
    return products
