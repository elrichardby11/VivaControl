import cx_Oracle
from dotenv import load_dotenv
import os

load_dotenv() # Load database

con = cx_Oracle.connect(f"{os.getenv('NAME_DATABASE')}/{os.getenv('PASSWORD_DATABASE')}@XE")

# Crear un cursor
cursor = con.cursor()

# Ejecutar la consulta SQL
cursor.execute("SELECT ID_SUCURSAL, DIRECCION FROM SUCURSAL")
# Obtener los resultados de la consulta
results = cursor.fetchall()

# Cerrar la conexión
con.close()

# Crear una lista para almacenar los datos
locals = []

for row in results:
    id_sucursal, direccion = row
    row = (str(id_sucursal) + ", " + str(direccion))

    locals.append(row)
