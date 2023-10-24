### VivaControl

# Manual de Usuario de VivaControl - Punto de Venta (PoS)

## Introducción
Bienvenido al Manual de Usuario de VivaControl - Punto de Venta (PoS). Esta aplicación ha sido diseñada para ayudarte en el proceso de venta de productos, permitiéndote escanear productos, gestionar tu carrito de compras y realizar transacciones de manera eficiente.

## Contenido
1. **Requisitos del Sistema**
2. **Inicio Rápido**
3. **Escaneo de Productos**
4. **Gestión del Carrito de Compras**
5. **Selección del Método de Pago**
6. **Registro de Transacciones**
7. **Errores Comunes y Soluciones**
8. **Contacto y Soporte Técnico**

## 1. Requisitos del Sistema
Antes de utilizar la aplicación PoS, asegúrate de que tu sistema cumple con los siguientes requisitos:
- Sistema operativo compatible con Python y Tkinter.
- Instalación de Python en tu sistema.
- Archivos de productos definidos en el archivo `products.py`.

## 2. Inicio Rápido
Para comenzar a utilizar la aplicación PoS, sigue estos pasos:

1. Ejecuta el archivo `main.py` en Python.
2. Se abrirá la ventana principal de la aplicación.
3. La fecha y hora actual se mostrarán en la parte superior de la ventana.
4. Escanea un producto utilizando el campo "Escanea el código del producto."
5. Haz clic en "Agregar al carrito" o pulsa la tecla "Enter".
6. Gestiona los productos en el carrito, selecciona el método de pago y completa la transacción.

## 3. Escaneo de Productos
- En el campo "Escanea el código del producto," ingresa el código de barras del producto o utiliza un lector de códigos de barras.
- Haz clic en "Agregar al carrito" o presiona la tecla "Enter" para agregar el producto al carrito.

## 4. Gestión del Carrito de Compras
- En la sección "Carrito:", verás los productos agregados junto con su cantidad y precio.
- Puedes editar la cantidad de un producto seleccionando el producto y haciendo clic en "Editar".
- Puedes eliminar un producto seleccionando el producto y haciendo clic en "Eliminar".

## 5. Selección del Método de Pago
- En la sección "Selecciona el método de pago," elige entre "Efectivo," "Débito" o "Crédito."
- Si seleccionas "Efectivo," ingresa el monto en efectivo en el campo "Monto en Efectivo."
- Si seleccionas "Débito" o "Crédito," el sistema asumirá que el pago es igual al total de compra.

## 6. Registro de Transacciones
- Una vez que hayas seleccionado el método de pago, haz clic en "Pagar."
- Se mostrará un resumen de la compra, incluido el total y el cambio si se paga en efectivo.
- Confirma la transacción para guardarla en un archivo de registro con detalles como la fecha, hora, productos, cantidades y método de pago.

## 7. Errores Comunes y Soluciones
- **Producto no encontrado:** Asegúrate de que el código de barras del producto sea correcto y esté definido en el archivo `products.py`.
- **Monto en efectivo incorrecto:** Verifica que el monto en efectivo sea suficiente para cubrir el total de la compra.
- **Transacción no confirmada:** Si no deseas realizar la transacción, simplemente haz clic en "Cancelar."

## 8. Contacto y Soporte Técnico
Si necesitas asistencia o tienes alguna pregunta sobre la aplicación PoS, no dudes en ponerte en contacto con nuestro equipo de soporte técnico en [correo electrónico de soporte] o en el número de teléfono [número de teléfono de soporte].

¡Gracias por utilizar VivaControl - Punto de Venta (PoS)!
