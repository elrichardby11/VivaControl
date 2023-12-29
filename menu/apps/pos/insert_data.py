from datetime import datetime
import cx_Oracle
from dotenv import load_dotenv
import os

def insert_data(self,current_cart, total_amount, local, total_amount_law):

    load_dotenv() # Load database

    connection_str = f"{os.getenv('NAME_DATABASE')}/{os.getenv('PASSWORD_DATABASE')}@XE"
    fecha = datetime.now().strftime("%d/%m/%Y")
    periodo = int(datetime.now().strftime("%Y"))

    with cx_Oracle.connect(connection_str) as con:

        # Crear un cursor
        with con.cursor() as cursor:
    
            # Ejecutar la consulta SQL
            cursor.execute("SELECT MAX(ID_MOVIMIENTO) FROM MOVIMIENTO")
        
            # Obtener los resultados de la consulta
            result = cursor.fetchone()
            max_id = result[0] if result[0] is not None else 0  # Maneja el caso en el que no haya registros
            
            # Incrementa el valor máximo en uno para obtener el nuevo ID
            new_id = max_id + 1
            tipo_mov = 2    # Tipo 2 Venta
            state = 1       # Estado Activo
            rut = 1         # Rut generico Cliente
            precio_total = total_amount if total_amount_law is None else total_amount_law

            # Inserta datos en Movimiento
            query = "INSERT INTO MOVIMIENTO (ID_MOVIMIENTO, FECHA, ID_TIPO_MOVIMIENTO, PERIODO, CSTATE_MOVIMIENTO, RUT_AUXILIAR, PRECIO_TOTAL) VALUES (:id, TO_DATE(:fecha, 'dd/mm/yyyy'), :tipo, :periodo, :state, :rut, :precio)"
            cursor.execute(query, id=new_id, fecha=fecha, tipo=tipo_mov, periodo=periodo, state=state, rut=rut, precio=precio_total)
            con.commit()

            # Ciclo para insertar en detalle de movimiento
            for code, quantity in current_cart.items():
                precio = self.products[code]["price"]
                query = "INSERT INTO DETALLE_MOV (ID_MOV, ID_PROD, ID_SUCURSAL, CANTIDAD, PRECIO_UNITARIO) VALUES (:id_mov, :id_pro, :id_suc, :cant, :precio)"
                cursor.execute(query, id_mov = new_id, id_pro = code, id_suc = local, cant = quantity, precio = precio)
                con.commit()