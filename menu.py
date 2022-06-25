#Elaborado por: Needler Bonilla Serrano
#               Jose Pablo Agüero Mora
#Fecha de Creación: 25/09/2021 1:00pm 
#Fecha de última Modificación: 09/10/2021 03:00pm
#Versión: 3.9.6

############# Sección de notas importantes ###################
# Nota 1: Para el proceso de tokenización se utilizaron únicamente los datos
# brindados en las instrucciones de la tarea programada, por lo que para la
# clasificación de las palabras se hizo uso de esa información.

# Nota 2: A la hora de realizar el algoritmo de ordenamiento alfabético, se
# utilizó como base la fuente indicada en la primer referencia bibliográfica
# que implementa un ordenamiento por inserción, la cual fue modificada para
# satisfacer las necesidades de cada sublista en el presente proyecto.

# Nota 3: A la hora de ingresar datos, no se recomienda el uso de caracteres
# con tildes, así como se mencionó en clase, ya que puede significar un problema
# en el ordenamiento de los datos.
##############################################################

# Importe de librerías
from funciones import *
import re
from os import remove
from datetime import datetime

#Definición de Funciones

### Entrada de datos y ordenamiento alfabético ###
def entradaDatos1Aux(poracion):
    """
    Función: Valida la entrada de datos (poración)
    Entrada: Parámetro - (poracion) Texto ingresado por el usuario.
    Salida: Llamado de función graba Nuevo.
    """
    if poracion != "":
        grabaNuevo(poracion)
    else:
        print ("\nDebe ingresar una oración válida.")
        return entradaDatos1()

def entradaDatos1():
    """
    Función: Solicita al usuario la entrada de datos (Oración)
    Entrada:N/D
    Salida: Llamado de función de validación.
    """
    oracion = input("\nIngrese la oración: ")
    oracion = oracion.lower()
    entradaDatos1Aux(oracion)
    return 

def crearArticulos(lista):
    """
    Función: Lee cada elemento dentro de la lista y lo pasa por el filtro de orden alfabético.
    Entrada: Parámetro lista.
    Salida: Retorno de lista articulos ya ordenada.
    """
    articulos = identificarArticulos(lista)
    for indice in articulos:
        articulos = [elemeto for elemeto in alfabeticoSort(articulos)]
        break
    return articulos

def crearPreposiciones(lista):
    """
    Función: Lee cada elemento dentro de la lista y lo pasa por el filtro de orden alfabético.
    Entrada: Parámetro lista.
    Salida: Retorno de lista preposiciones ya ordenada.
    """
    preposiciones = identificarPreposiciones (lista)
    for indice in preposiciones:
        preposiciones = [elemeto for elemeto in alfabeticoSort(preposiciones)]
        break
    return preposiciones

def crearPronombres(lista):
    """
    Función: Lee cada elemento dentro de la lista y lo pasa por el filtro de orden alfabético.
    Entrada: Parámetro lista.
    Salida: Retorno de lista pronombres ya ordenada.
    """
    pronombres = identificarPronombres (lista)
    for indice in pronombres:
        pronombres = [elemeto for elemeto in alfabeticoSort(pronombres)]
        break
    return pronombres

def crearVerbos(lista):
    """
    Función: Lee cada elemento dentro de la lista y lo pasa por el filtro de orden alfabético.
    Entrada: Parámetro lista.
    Salida: Retorno de lista verbos ya ordenada.
    """
    verbos = identificarVerbo(lista)
    for indice in verbos:
        verbos = [elemeto for elemeto in alfabeticoSort(verbos)]
        break
    return verbos

def crearNumeros(lista):
    """
    Función: Lee cada elemento dentro de la lista y lo pasa por el filtro de orden alfabético.
    Entrada: Parámetro lista.
    Salida: Retorno de lista numeros ya ordenada.
    """
    numeros = identificarNumeros(lista)
    for indice in numeros:
        numeros = [elemeto for elemeto in alfabeticoSort(numeros)]
        break
    return numeros

def crearSClasificar(lista, articulos, preposiciones, pronombres, verbos, numeros):
    """
    Función: Lee cada elemento dentro de la lista y lo pasa por el filtro de orden alfabético sacando
                   elementos que no pertenecen a ningúna de las anteriores.
    Entrada: Parámetros lista, articulos, preposiciones, pronombres, verbos y  numeros.
    Salida: Retorno de lista sClasificar ya ordenada.
    """
    sClasificar = sinClasificar(lista, articulos, preposiciones, pronombres, verbos, numeros)
    for indice in sClasificar:
        sClasificar = [elemeto for elemeto in alfabeticoSort(sClasificar)]
        break
    return sClasificar

### Síntesis de lista para salidas ###
def creaListaPrincipal(articulos, preposiciones, pronombres, verbos, numeros, sClasificar):
    """
    Función: Agrega cada sublista de las categorías a la lista principal.
    Entrada: Parámetros - Cada una de las sublistas según categoría.
    Salida: Lista con cada una de las sublistas correspondientes.
    """
    listaGeneral = []
    listaGeneral.append(articulos)
    listaGeneral.append(preposiciones)
    listaGeneral.append(pronombres)
    listaGeneral.append(verbos)
    listaGeneral.append(numeros)
    listaGeneral.append(sClasificar)
    return listaGeneral

### Entrada principal de datos ###
def principal():
    """
    Función: Verifica si la oración ya existe en la base de datos y notifica su existencia.
    Entrada: N/D
    Salida: Mensaje de viso y Llamado a función entradaDatos1.
    """
    if verificaNuevo() == False:
        entradaDatos1()
        print ("\nTexto guardado satisfactoriamente")
    else:
        print ("Ya existe un archivo de texto creado. Se están leyendo estos datos...")

### Tokenización - Funciones auxiliares de las entradas ###
def tokenizar():
    """
    Función: Sub-divide cada elemento de la oración llamando funciónes para almacenarlas según su tipo.
    Entrada:N/D
    Salida: Lista con todos los elementos tokenizados. (pLista)
    """
    cadena = leeOtro() 
    preLista = convierteLista(cadena)
    lista = eliminaRepetidos(preLista)
    
    articulos = crearArticulos(lista)
    preposiciones = crearPreposiciones(lista)
    pronombres = crearPronombres(lista)
    verbos = crearVerbos(lista)
    numeros = crearNumeros(lista)
    sclas= crearSClasificar(lista, articulos, preposiciones, pronombres, verbos, numeros)
    pLista = creaListaPrincipal(articulos, preposiciones, pronombres, verbos, numeros, sclas)
    return pLista

def opcionHTML(lista):
    """
    Función: Incluye todos los procesos necesarios a realizar cuando se
    elige la opción Generar documento HTML.
    Entrada: Parámetro - (lista) Lista tokenizada y procesada.
    Salida: Realiza los procesos para crear y escribir automáticamente
    en el archivo HTML.
    """
    if lista == []:
        print ("\nNo se ha tokenizado el texto previamente.")
        menu (lista)
    else:
        if existeHTML() == True:
            print ("\nYa existe un archivo HTML creado.")
        else:
            otraLista = eliminaElementoEspacio(lista)
            nombreArchivo = generaNombre()
            crearHTML(nombreArchivo)
            cicloFilas(lista, nombreArchivo)
            txt = leeOtro()
            ingresaTexto(txt, nombreArchivo)
            cambiaFinal(otraLista, nombreArchivo)
            print ("\nEl archivo HTML se ha creado satisfactoriamente.")
    return ""

def opcionXML(lista):
    """
    Función: Incluye todos los procesos necesaerios a realizar cuando se
    elige la opción Generar documento XML.
    Entrada: Parámetro - (lista) Lista tokenizada y procesada.
    Salida: Realiza los procesos para crear y escribir automáticamente
    en el archivo XML.
    """
    if lista == []:
        print ("\nNo se ha tokenizado el texto previamente.")
    else:
        if verificaXML():
            print ("\nYa existe un archivo XML creado.")
        else:
            creaXML (lista)
    return ""

def opcionBinario(lista):
    """
    Función: Incluye todos los procesos necesaerios a realizar cuando se
    elige la opción Generar documento Binario.
    Entrada: Parámetro - (lista) Lista tokenizada y procesada.
    Salida: Realiza los procesos para crear y escribir automáticamente
    en el archivo Binario.
    """
    if lista == []:
        print ("\nNo se ha tokenizado el texto previamente.")
        menu (lista)
    else:
        if existeArchivo("BD") == True:
            print ("\nYa existe un archivo binario creado. Mostrando contenido...")
            eliminaEspaciosBinario()
        else:
            graba(lista)
            print ("\nEl archivo binario se ha creado satisfactoriamente.")
            eliminaEspaciosBinario()
    return ""

### Menú de selección ###
def menu (lista):
    """
    Función:Menú principal donde muestra la generación de documentos y tokenización de oraciones.
    Entrada: Parámetro lista.
    Salida: Llamado de las funciones pertinentes a cada opción.
    """
    estado = True
    while estado == True:
        print ("\n---------- Menú Principal ----------")
        print ("1. Tokenizar")
        print ("2. Generar documento HTML")
        print ("3. Generar documento XML")
        print ("4. Generar documento Binario")
        print ("5. Salir")
        print ("------------------------------------")
        opcion=input("Ingrese el digito de su opción deseada: ")
        if opcion == "1":
            lista = tokenizar()
            print ("\nEl texto se ha tokenizado satisfactoriamente")
        elif opcion == "2":
            opcionHTML(lista)
        elif opcion == "3":
            opcionXML(lista)
        elif opcion == "4":
            opcionBinario(lista)
        elif opcion == "5":
            print ("\nSaliendo del programa...")
            return 
        else:
            print ("\nDebe ingresar un entero de 1 a 6.")

#Programa principal
principal()
lista = []
menu(lista)


        
