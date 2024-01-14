from datetime import datetime
import cx_Oracle
from dotenv import load_dotenv
import os

def insert_data(self, cart_info):

    load_dotenv() # Load database

    current_cart = cart_info.get("current_cart", {})
    total_amount = cart_info.get("total_amount", 0)
    local = cart_info.get("local", "local")
    total_amount_law = cart_info.get("total_amount_law", None)

    local = local.replace(local, local[0])
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
                j = 1

                # Ejecutar la consulta para saber todas las compras de un producto
                cursor.execute(f"SELECT D.ID_MOV, D.CANTIDAD, D.COSTE_UNITARIO FROM DETALLE_MOV D JOIN MOVIMIENTO M ON M.ID_MOVIMIENTO = D.ID_MOV WHERE (D.ID_SUCURSAL = {local} AND M.ID_TIPO_MOVIMIENTO = 1) AND D.ID_PROD = {code} ORDER BY D.ID_MOV")
                compras = {row[0]: {"cantidad": row[1], "precio_coste": row[2]} for row in cursor.fetchall()}

                # Obtener la cantidad total vendida de ese producto
                cursor.execute(f"SELECT SUM(CANTIDAD) FROM DETALLE_MOV D JOIN MOVIMIENTO M ON M.ID_MOVIMIENTO = D.ID_MOV WHERE (D.ID_SUCURSAL = {local} AND M.ID_TIPO_MOVIMIENTO = 2) AND D.ID_PROD = {code}")
                ventas = cursor.fetchone()[0] or 0

                contador = 0

                for i in compras:

                    # Si la cantidad comprada es mayor o igual a la cantidad vendida quiere decir que el precio coste es ese
                    if (((compras[i]["cantidad"]) + contador) >= ventas) and (quantity <= (compras[i]["cantidad"] + contador) - ventas):
                        precio_coste = compras[i]["precio_coste"]
                        query = "INSERT INTO DETALLE_MOV (ID_MOV, ID_PROD, ID_SUCURSAL, CANTIDAD, PRECIO_UNITARIO, COSTE_UNITARIO) VALUES (:id_mov, :id_pro, :id_suc, :cant, :precio, :coste)"
                        cursor.execute(query, id_mov = new_id, id_pro = code, id_suc = local, cant = quantity, precio = precio, coste = precio_coste)
                        con.commit()
                        break
                    
                    # Si la cantidad comprada es mayor o igual a la cantidad vendida y la cantidad vendida es mayor a la cantidad disponible
                    elif (((compras[i]["cantidad"]) + contador) >= ventas) and (quantity > (compras[i]["cantidad"] + contador) - ventas):
                        
                        detalle_inicial = False

                        ventas_restantes = ventas
                        for id_compra, compra_info in compras.items():
                            cantidad_vendida2 = min(compra_info["cantidad"], ventas_restantes)
                            ventas_restantes -= cantidad_vendida2
                            compra_info["cantidad"] -= cantidad_vendida2
                            
                        # Crear un diccionario actualizado restando las ventas
                        compras_actualizadas = {}

                        cantidad_restante = quantity
                        for id_compra, compra_info in compras.items():
                            if cantidad_restante > 0 and compra_info["cantidad"] > 0:
                                cantidad_seleccionada = compra_info["cantidad"]

                                compras_actualizadas[id_compra] = {
                                
                                "cantidad": cantidad_seleccionada,
                                "precio_coste": compra_info["precio_coste"]
                                }

                                cantidad_restante -= cantidad_seleccionada

                        # Reemplazar el diccionario original con el diccionario actualizado
                        compras = compras_actualizadas


                        for indice, (id_compra, compra_info) in enumerate(compras.items()): # Cambiar esto por los actuales precios costes
                            cantidad_compra, costo_unitario = compra_info["cantidad"], compra_info["precio_coste"]


                            cantidad_vendida = min(cantidad_compra, quantity)

                            precio_coste = costo_unitario

                            # Consulta para saber si se añadió el registro de ajuste en Movimiento
                            cursor.execute(f"SELECT id_movimiento FROM MOVIMIENTO where id_movimiento = {new_id+j}")
                            resultado = cursor.fetchone()
                            
                            #resultado = resultado[0]

                            if resultado is None:

                                # Inserta datos en Movimiento ajuste precio coste
                                query = "INSERT INTO MOVIMIENTO (ID_MOVIMIENTO, FECHA, ID_TIPO_MOVIMIENTO, PERIODO, CSTATE_MOVIMIENTO, RUT_AUXILIAR, PRECIO_TOTAL) VALUES (:id, TO_DATE(:fecha, 'dd/mm/yyyy'), :tipo, :periodo, :state, :rut, :precio)"
                                cursor.execute(query, id=new_id+j, fecha=fecha, tipo=tipo_mov, periodo=periodo, state=state, rut=rut, precio=0)
                                con.commit()

                            if not detalle_inicial:

                                # Insertar detalle para el movimiento inicial por primera vez
                                query = "INSERT INTO DETALLE_MOV (ID_MOV, ID_PROD, ID_SUCURSAL, CANTIDAD, PRECIO_UNITARIO, COSTE_UNITARIO) VALUES (:id_mov, :id_pro, :id_suc, :cant, :precio, :coste)"
                                cursor.execute(query, id_mov=new_id, id_pro=code, id_suc=local, cant=cantidad_vendida, precio=precio, coste=precio_coste)
                                con.commit()
                                detalle_inicial = True
                                j -= 1

                            else:
                                # Insertar detalle para el movimiento actual
                                query = "INSERT INTO DETALLE_MOV (ID_MOV, ID_PROD, ID_SUCURSAL, CANTIDAD, PRECIO_UNITARIO, COSTE_UNITARIO) VALUES (:id_mov, :id_pro, :id_suc, :cant, :precio, :coste)"
                                cursor.execute(query, id_mov=new_id+j, id_pro=code, id_suc=local, cant=cantidad_vendida, precio=precio, coste=precio_coste)
                                con.commit()

                            quantity -= cantidad_vendida
                            j += 1

                        break

                    contador += (compras[i]["cantidad"])
