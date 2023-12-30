from datetime import datetime
from menu.apps.pos.insert_data import insert_data

def save_to_file(self, cart_info):

    insert_data(self, cart_info)
    now, fecha, hora = get_date()

    with open_file(now) as file:
        write_header(file, fecha, hora)
        write_detail(self, file, cart_info)
        write_payments(file, cart_info)

def get_date():
    now = datetime.now()
    fecha = now.strftime("Fecha: %d-%m-%Y")
    hora = now.strftime("Hora: %H:%M:%S")
    return now, fecha, hora

def open_file(now):
    filename = now.strftime("%Y-%m-%d_%H-%M-%S.txt")
    print(f"Registro guardado en {filename}")
    return open(filename, "w")

def write_header(file, fecha, hora):
    file.write(" _____________________________________________________ \n")
    file.write("|                                                     |\n")
    file.write("|RUT: 11.111.111-1                                    |\n")
    file.write("|RAZON SOCIAL: FANTASIA S.A                           |\n")
    file.write("|BLABLA NRO 999 - PISO 1234B                          |\n")
    file.write("|LAS CONDES - SANTIAGO F. -256784321                  |\n")
    file.write("|GIRO: VENTAS AL POR MENOR DE MERCADERIA              |\n")
    file.write("|_____________________________________________________|\n")
    file.write(f" {fecha}          {hora}\n")
    file.write(" Boleta Electronica:        123.456.789\n")
    file.write(" CAJA: 1 CAJERO: RICHARD MAZUELOS\n")
    file.write("  D E T A L L E  \n")
    file.write(" --------------- \n")

def write_detail(self, file, cart_info):

    current_cart = cart_info.get("current_cart", {})
    last_digit = cart_info.get("last_digit", None)
    total_amount = cart_info.get("total_amount", 0)
    total_amount_law = cart_info.get("total_amount_law", None)
    payment_method = cart_info.get("payment_method", "")
    symbol = cart_info.get("symbol", None)

    if last_digit in [0, None]:
        neto = round(total_amount / 1.19)
        iva = round(total_amount - neto)
    else:
        total_amount_2 = total_amount
        total_amount = total_amount_law
        neto = round(total_amount / 1.19)
        iva = round(total_amount - neto)

    for code, quantity in current_cart.items():
        product_code = code
        product_name = self.products[code]["name"]
        price = self.products[code]["price"]
        total_price = quantity * price
        formatted_quantity = format_number(quantity)
        formatted_price = format_number(price)
        formatted_total_price = format_number(total_price)
        if quantity > 1:
            cantidad = (40 - (len(formatted_quantity) + len(formatted_price) + len(product_name)))
            file.write(f" Codigo: {product_code}\n")
            file.write(f" {formatted_quantity}X{formatted_price} {product_name}{' ' * cantidad}{'$'}{formatted_total_price:>11}\n")
        else:
            cantidad = 45 - len(product_name)
            file.write(f" {product_code:>13} {product_name:<{cantidad}}{'$'}{formatted_total_price:>11}\n")
    if ((payment_method == "Efectivo") and (last_digit in [0, None])) or (payment_method != "Efectivo"):
        file.write(" ----------------------------------------------------- \n")
        file.write(f"                                SUBTOTAL      $ {format_number(total_amount):>7}\n")
        file.write(f"                        TOTAL AFECTO       $ {format_number(neto):>10}\n")
        file.write(f"                        TOTAL EXCENTO      $          0\n")
        file.write(f"                        TOTAL IVA 19%      $ {format_number(iva):>10}\n")
        file.write(f"                                TOTAL         $ {format_number(total_amount):>7}\n")
    else:
        if payment_method == "Efectivo" and last_digit != 0:
            file.write(" ----------------------------------------------------- \n")
            file.write(f"                                SUBTOTAL      $ {format_number(total_amount_2):>7}\n")
            file.write(f"                        REDONDEO 20.956    $ {symbol:>8} {format_number(last_digit)}\n")
            file.write(f"                        TOTAL AFECTO       $ {format_number(neto):>10}\n")
            file.write(f"                        TOTAL EXCENTO      $          0\n")
            file.write(f"                        TOTAL IVA 19%      $ {format_number(iva):>10}\n")
            file.write(f"                                TOTAL         $ {format_number(total_amount_law):>7}\n")

def write_payments(file, cart_info):

    payment_method = cart_info.get("payment_method", "")
    payment_quantity = cart_info.get("payment_quantity", 0)
    total_amount = cart_info.get("total_amount", 0)
    total_amount_law = cart_info.get("total_amount_law", None)
    last_digit = cart_info.get("last_digit", None)
    
    if not last_digit in [0, None]:
        total_amount = total_amount_law

    file.write(" ---------------------P A G O S----------------------- \n")

    if payment_method == "Efectivo":
        file.write(f" {payment_method}           $ {format_number(payment_quantity):>10}\n")
        file.write(f" Vuelto             $ { format_number(payment_quantity-total_amount):>10}\n")
        file.write(" ===================================================== ")
    else:
        file.write(f" {payment_method:<7}            $ {format_number(total_amount):>10}\n")
        file.write(" Vuelto             $          0\n")
        file.write(" ===================================================== ")

def format_number(number):
    return "{:,.0f}".format(number).replace(",", ".")