from datetime import datetime
import cx_Oracle


def save_to_file(self,current_cart, total_amount, payment_method, payment_quantity):

    # Conectar a la base de datos Oracle
    con = cx_Oracle.connect("VivaControl/T$g#kP2LMv8X@XE")

    # Crear un cursor
    cursor = con.cursor()

    # Ejecutar la consulta SQL
    cursor.execute("SELECT MAX(ID_MOVIMIENTO) FROM MOVIMIENTO")

    # Obtener los resultados de la consulta
    result = cursor.fetchone()
    max_id = result[0] if result[0] is not None else 0  # Maneja el caso en el que no haya registros
    # Incrementa el valor máximo en uno para obtener el nuevo ID
    new_id = max_id + 1
    fecha = datetime.now().strftime("%d/%m/%Y")
    tipo_mov = 2
    state = 1
    rut = 1
    query = "INSERT INTO MOVIMIENTO (ID_MOVIMIENTO, FECHA, ID_TIPO_MOVIMIENTO, CSTATE_MOVIMIENTO, RUT_AUXILIAR) VALUES (:id, TO_DATE(:fecha, 'dd/mm/yyyy'), :tipo, :state, :rut)"
    cursor.execute(query, id=new_id, fecha=fecha, tipo=tipo_mov, state=state, rut=rut)
    con.commit()

    for code, quantity in current_cart.items():
        product_code = code
        precio = self.products[code]["price"]
        query = "INSERT INTO DETALLE_MOV (ID_MOV, ID_PROD, CANTIDAD, PRECIO_UNITARIO) VALUES (:id_mov, :id_pro, :cant, :precio)"
        cursor.execute(query, id_mov = new_id, id_pro = code, cant = quantity, precio = precio)
        con.commit()

    now = datetime.now()
    #Nombre del Archivo
    filename = now.strftime("%Y-%m-%d_%H-%M-%S.txt")
    formatted_date = now.strftime("Fecha: %d-%m-%Y")
    formatted_time = now.strftime("Hora: %H:%M:%S")

    neto = round    (total_amount / 1.19)
    iva = round(total_amount - neto)

    with open(filename, "w") as file:
        file.write(" _____________________________________________________ \n")
        file.write("|                                                     |\n")
        file.write("|RUT: 11.111.111-1                                    |\n")
        file.write("|RAZON SOCIAL: FANTASIA S.A                           |\n")
        file.write("|BLABLA NRO 999 - PISO 2234B                          |\n")
        file.write("|LAS CONDES - SANTIAGO F. -256784321                  |\n")
        file.write("|GIRO: VENTAS AL POR MENOS DE MERCADERIA              |\n")
        file.write("|_____________________________________________________|\n")
        file.write(f" {formatted_date}          {formatted_time}\n")
        file.write(" Boleta Electronica:        123.456.789\n")
        file.write(" CAJA: 2 CAJERO: RICHARD MAZUELOS\n")
        file.write(" D E T A L L E\n")
        file.write(" ---------------\n")
        
        for code, quantity in current_cart.items():
            product_code = code
            product_name = self.products[code]["name"]
            price = self.products[code]["price"]
            total_price = quantity * price
            formatted_quantity = format_number(quantity)
            formatted_price = format_number(price)
            formatted_total_price = format_number(total_price)
            if quantity > 1:
                file.write(f" Codigo: {product_code}\n")
                file.write(f"{formatted_quantity:>3}X{formatted_price} {product_name:<33}$ {formatted_total_price:>10}\n")
            else:
                file.write(f" {product_code} {product_name:<28}$ {formatted_total_price:>10}\n")
        file.write(" -----------------------------------------------------\n")
        file.write(f"                             Neto:         $ {format_number(neto):>10}\n")
        file.write(f"                             IVA 19%:      $ {format_number(iva):>10}\n")
        file.write(f"                             TOTAL:        $ {format_number(total_amount):>10}\n")
        file.write(" ---------------------P A G O S-----------------------\n")
        if payment_method == "Efectivo":
            file.write(f" {payment_method}           $ {format_number(payment_quantity):>10}\n")
            file.write(f" Vuelto             $ { format_number(payment_quantity-total_amount):>10}\n")
            file.write(" =====================================================\n")
        else:
            file.write(f" {payment_method:<7}           $ {format_number(total_amount):>10}\n")
            file.write(" Vuelto            $          0\n")
            file.write(" =====================================================\n")

    print(f"Registro guardado en {filename}")

def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")
