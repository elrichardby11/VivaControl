products = {
            "7807265064173": {"name": "Producto 1", "price": 1000},
            "7501007528427": {"name": "Producto 2", "price": 1500}
            # Agrega más productos con su información
        }




import cx_Oracle






"""""""""

# Conectar a la base de datos Oracle
connection = cx_Oracle.connect("Juan_Rodriguez/Mn3rP7oBsKxL#@9501")

# Crear un cursor
cursor = connection.cursor()

# Ejecutar la consulta SQL
cursor.execute("SELECT id_producto, nombre_producto, precio FROM productos;")
# Obtener los resultados de la consulta
results = cursor.fetchall()

# Cerrar la conexión
connection.close()

# Crear un diccionario para almacenar los datos
products = {}

# Procesar los resultados
for row in results:
    id_producto, nombre_producto, precio = row
    
    if id_producto not in products:
    
        # Si el producto no está en el diccionario, lo agrega con su precio de venta actual
        products[id_producto] = {"name": nombre_producto, "price": precio}
    else:
    
        # Si el producto ya está en el diccionario, actualiza el precio de venta si es más reciente
        products[id_producto]["price"] = precio

# El diccionario 'products' ahora contiene los datos con el precio de venta más reciente
print(products)

"""""""""