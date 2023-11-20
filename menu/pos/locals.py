import cx_Oracle

connection = cx_Oracle.connect("VivaControl/T$g#kP2LMv8X@XE")

# Crear un cursor
cursor = connection.cursor()

# Ejecutar la consulta SQL
cursor.execute("SELECT ID_SUCURSAL, DIRECCION FROM SUCURSAL")
# Obtener los resultados de la consulta
results = cursor.fetchall()

# Cerrar la conexión
connection.close()

# Crear una lista para almacenar los datos
locals = []

for row in results:
    id_sucursal, direccion = row
    row = (str(id_sucursal) + ", " + str(direccion))

    locals.append(row)
