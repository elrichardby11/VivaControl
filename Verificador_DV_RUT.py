### Verificar DV de RUT

#Registra RUT
rut = int(input("Por favor, Ingrese su rut sin puntos ni digito verificador: "))
rut_listo = len(str(rut))

#Verificar si RUT tiene 8 digitos
if (rut_listo) == 8:

    #Inicializa las variables necesarias
    rut_str = str(rut)
    numeros_a_multiplicar = [3,2,7,6,5,4,3,2]
    resultados = []
    suma = 0

    #Multiplica cada uno de los digitos del rut
    for i, digito in enumerate(rut_str):
        resultado_individual = int(digito) * numeros_a_multiplicar[i]
        resultados.append(resultado_individual)
    
    #Suma cada uno de los resultados de la multiplicacion
    for digito in resultados:
        suma += digito
    
    #Obtener Digito Verificador
    dv = 11-(suma%11)

    #Excepciones para el usuario
    if dv == 11:
        dv = 0
    elif dv == 10:
        dv = "k"

    print("El numero verificador es: ", dv)
else:
    print("Rut invalido (8 digitos)... ")