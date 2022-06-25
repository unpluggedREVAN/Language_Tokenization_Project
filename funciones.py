#Elaborado por: Needler Bonilla Serrano
#               Jose Pablo Agüero Mora
#Fecha de Creación: 25/09/2021 1:00pm 
#Fecha de última Modificación: 09/10/2021 03:00pm
#Versión: 3.9.6

# Importación de librerías
import sys
sys.setrecursionlimit(5000)
import pickle
from xml.dom import minidom
import re
from datetime import datetime
import os

#Definición de Funciones

####################### Sub Listas #######################
#Articulos
def identificarArticulos (lista):
    """
    Función:Identifica si el parámetro se encuentra entre la lista de Articulos y lo almacena.
    Entrada: Parámetro lista (Oración tokenizada).
    Salida: Nueva lista con elementos encontrados.
    """
    palabras=["el","la","los","las","un","una","unos","unas","lo","al","del"]
    listaArticulos=[]
    for elemento in lista:
        if elemento in palabras:
            listaArticulos.append(elemento)
    return list(set(listaArticulos))

#Preposiciones
def identificarPreposiciones (lista):
    """
    Función:Identifica si el parámetro se encuentra entre la lista de Preposiciones y lo almacena.
    Entrada: Parámetro lista (Oración tokenizada).
    Salida: Nueva lista con elementos encontrados.
    """
    palabras=["a","ante","bajo","cabe","con","contra","de","desde","durante","en",\
                   "entre","hacia","hasta","mediante","para","por","según","sin","so","sobre",\
                   "tras","versus","vía"]
    listaPreposiciones=[]
    for elemento in lista:
        if elemento in palabras:
            listaPreposiciones.append(elemento)
    return list(set(listaPreposiciones))

#Pronombres
def identificarPronombres (lista):
    """
    Función:Identifica si el parámetro se encuentra entre la lista de Pronombres y lo almacena.
    Entrada: Parámetro lista (Oración tokenizada).
    Salida: Nueva lista con elementos encontrados.
    """
    palabras=["yo","me","mí","conmigo","nosotros","nosotras","nos","tú","te","ti","contigo",\
              "vosotros","vosotras","vos","él","ella","se","consigo","le","les","Mío","mía","míos",\
              "mías","nuestro","nuestra","nuestros","nuestras","tuyo","tuya","tuyos","vuestro","vuestra",\
              "vuestros","vuestras","suyo","suya","suyos","suyas"]
    listaPronombres=[]
    for elemento in lista:
        if elemento in palabras:
            listaPronombres.append(elemento)
    return list(set(listaPronombres))

#Verbos
def identificarVerbo(lista):
    """
    Función:Identifica si parámetro se encuentra en la lista de terminaciones de Verbos y lo almacena.
    Entrada: Parámetro lista (Oración tokenizada).
    Salida: Nueva lista con elementos encontrados.
    """
    listaVerbos = []
    for palabra in lista:
        # Participio:
        if re.search("^i{1}e{1}n{1}d{1}o{1}$", palabra[-5:]):
            listaVerbos.append(palabra)
        elif re.search("^a{1}n{1}d{1}o{1}$", palabra[-4:]):
            listaVerbos.append(palabra)
        # Infinitivos:
        elif re.search("^(a|e|i){1}r{1}$", palabra[-2:]):
            listaVerbos.append(palabra)
        # Gerundios:
        elif re.search("^(a|i){1}d{1}o{1}$", palabra[-3:]):
            listaVerbos.append(palabra)
        elif re.search("^(t|s){1}o{1}$", palabra[-2:]):
            listaVerbos.append(palabra)
        elif re.search("^c{1}h{1}o{1}$", palabra[-3:]):
            listaVerbos.append(palabra)
    return listaVerbos

#Números
def identificarNumeros(lista):
    """
    Función:Identifica si parámetro dentro de lista es de caracter numérico y lo almacerna.
    Entrada: Parámetro lista (Oración tokenizada).
    Salida: Nueva lista con elementos encontrados.
    """
    listaNumeros = []
    for elemento in lista:
        if re.search("\d+", elemento):
            listaNumeros.append(elemento)
    return listaNumeros

#Sin clasificar
def sinClasificar(lista, articulos, preposiciones, pronombres, verbos, numeros):
    """
    Función: Verifica si los elemento ingresados no pertenecen a ningúna sub lista.
    Entrada: Parámetro lista, articulos, preposiciones, pronombres, verbos, numeros.
    Salida: Lista con los elementos sin clasificar.
    """
    listaSinClasificar = []
    for elemento in lista:
        if elemento not in articulos:
            if elemento not in preposiciones:
                if elemento not in pronombres:
                    if elemento not in verbos:
                        if elemento not in numeros:
                            listaSinClasificar.append(elemento)
    return listaSinClasificar
####################### Sub Listas #######################

### Orden Alfabético ###
def alfabeticoSort(lista):
    """
    Función: Acomoda y ordena en memoria todos los elemento ingresados en parámetro lista.
    Entrada: Parámetro lista (oración Tokenizada).
    Salida: Lista con cada elemento ordenado numérica y alfabeticamente.
    """
    largo = len(lista)
    if largo == 0:
        return  
    menor = 0             
    min = lista[menor]    
    minimoprev = None     
    encontro = True        
    while encontro:
        for indice in range(largo):
            if lista[indice] < min and (minimoprev == None or lista[indice] > minimoprev):
                menor = indice
                min = lista[menor]
                encontro = True
        if encontro:
            yield min
            for indice in range(menor + 1, largo):
                if lista[indice] == min:
                    yield min
            encontro = False
            for indice in range(largo):
                if lista[indice] > min:
                    menor = indice
                    encontro = True
                    break
            minimoprev = min
            min = lista[menor]

############ Preparación del texto Pre-Tokenización ###########
def eliminaElementoEspacio(listaPuntuacion):
    """
    Función: Busca y elimina los espacios dentro de la lista ya tokenizada y los almacena.
    Entrada: Parámetro listaPuntuación (Lista Tokenizada).
    Salida: Lista Final sin espacios en su interior.
    """
    listaFinal = []
    for elemento in listaPuntuacion:
        if elemento != "":
            listaFinal.append(elemento)
    return listaFinal

def eliminaRepetidos(xLista):
    """
    Función: Elimina los elementos repetidos en una lista.
    Entrada: Parámetro - (xLista) Sublista de cada grupo.
    Salida: Lista sin elementos repetidos.
    """
    sinRepetidos = []
    for elemento in xLista:
        if elemento not in sinRepetidos:
            sinRepetidos.append(elemento)
    return sinRepetidos

def eliminaEspaciosBinario():
    """
    Función: Toma los valores del archivo binario y elimina espacios sobrantes.
    Entrada: N/D
    Salida: Llama a la función que imprime la información correspondiente.
    """
    matriz = lee("BD")

    articulos = eliminaElementoEspacio(matriz[0])
    preposiciones = eliminaElementoEspacio(matriz[1])
    pronombres = eliminaElementoEspacio(matriz[2])
    verbos = eliminaElementoEspacio(matriz[3])
    numeros = eliminaElementoEspacio(matriz[4])
    sinClasificar = eliminaElementoEspacio(matriz[5])
    lFinal = [articulos, preposiciones, pronombres, verbos, numeros, sinClasificar]

    return imprimeBinario(lFinal)

def eliminaPuntuacion(listaEspacios):
    """
    Función: Busca y elimina los signos de puntuación dentro de la lista ya tokenizada y los almacena.
    Entrada: Parámetro listaPuntuación (Lista Tokenizada).
    Salida: Lista Final sin signos de puntuación en su interior.
    """
    listaPuntuacion = []
    for elemento in listaEspacios:
        concaElemento = ""
        elemento = list(elemento)
        for posicion in elemento:
            if posicion.isalnum():
                concaElemento += posicion
        listaPuntuacion.append(concaElemento)
    return eliminaElementoEspacio(listaPuntuacion)
        
def convierteLista(poracion):
    """
    Función: Elimina las comillas dentro del parámetro oración.
    Entrada: Parámetro poración
    Salida: Retorno de lista sin comilla a eliminaPuntuacion
    """
    lista = poracion.split(" ")
    return eliminaPuntuacion(lista)
############ Preparación del texto Pre-Tokenización ###########

################################ Archivos txt #####################################
def grabaNuevo(lista):
    """
    Función: Abre el archivo txt e ingresa elementos deseados.
    Entrada: Parámetro lista
    Salida: N/D
    """
    with open ("archivo.txt","w") as salida:
        salida.write(str(lista))
        return ""

def leeOtro():
    """
    Función: Retorna el contenido dentro del txt al programa.
    Entrada: N/D
    Salida: Contenido dentro del txt.
    """
    with open ("archivo.txt","r") as salida:
        for linea in salida:
            return linea

def verificaNuevo():
    """
    Función: Verifica que exista un documento txt dentro de la base de datos.
    Entrada: N/D
    Salida: Flags de True o False según cada caso.
    """
    try:
        with open ("archivo.txt","r") as salida:
            return True
    except:
        return False
################################ Archivos txt ##################################

############################# Archivos binarios ##################################
def existeArchivo(nomArchLeer):
    """
    Función: Verifica que exista un archivo con el nombre indicado.
    Entradas: Parámetro - Nombre del archivo (nomArchLeer).
    Salidas: 1 si existe el archivo en la carpeta, -1 si no existe el archivo.
    """
    try:
        f=open(nomArchLeer,"rb")
        pickle.load(f)
        f.close()
        return True
    except:
        return False

def lee(nomArchLeer):
    """
    Función: Lee los datos del archivo indicado.
    Entradas: Parámetro - Nombre del archivo (nomArchLeer).
    Salidas: Retorna los datos (codigos) del archivo indicado.
    """
    try:
        f=open(nomArchLeer,"rb")
        codigos = pickle.load(f)
        f.close()
        return codigos
    except:
        print("Error al leer el archivo: ", nomArchLeer)
    return

def graba(lista):
    """
    Función: Crea el archivo inicial con la lista de códigos.
    Entradas: Parámetro - Nombre de la lista (lista).
    Salidas: Crea el archivo o envía un mensaje de error en caso de que no sea posible.
    """
    nomArchGrabar = "BD"
    try:
        f=open(nomArchGrabar,"wb")
        pickle.dump(lista,f)
        f.close()
    except:
        print("Error al grabar el archivo: ", nomArchGrabar)
    return

##------ Creación de binario ------##
def generaBinario(lista):
    """
    Función: Determina si existe un archivo txt y si no existe lo créa.
    Entrada:Parámetro lista.
    Salida: Mensaje de notificaión y retorno de función graba.
    """
    if existeArchivo("BD"):
        print ("Ya existe un archivo binario guardado.")
    else:
        graba(lista)
        print ("El archivo se ha creado satisfactoriamente.")

def quitaTildes(cadena):
    """
    Función: Lee cada elemento de una lista tíldada y los cambia por unos sin tílde.
    Entrada: Parámetro cadena (Oración Tokenizada).
    Salida: Retorno de lista ingresada como parámetro.
    """
    a,b = 'áéíóúüñÁÉÍÓÚÜÑ','aeiouunAEIOUUN'
    trans = str.maketrans(a,b)
    convertida = cadena.translate(trans)
    return convertida

def imprimeBinario(lFinal):
    """
    Función: Imprime la información encontrada en el archivo binario.
    Entrada: Parámetro - (lFinal) Lista con la información ordenada.
    Salida: Impresión ordenada de los datos.
    """
    matriz = lFinal
    print("\nArtículos:")
    for elemento in matriz[0]:
        print ("-", elemento)
    print("\nPreposiciones:")
    for elemento in matriz[1]:
        print ("-", elemento)
    print("\nPronombres:")
    for elemento in matriz[2]:
        print ("-", elemento)
    print("\nVerbos:")
    for elemento in matriz[3]:
        print ("-", elemento)
    print("\nNúmeros:")
    for elemento in matriz[4]:
        print ("-", elemento)
    print("\nSin Clasificar:")
    for elemento in matriz[5]:
        print ("-", elemento)
    return ""
############################# Archivos binarios ###########################

########################### Creación de XML #####################
def verificaXML():
    """
    Función: Verifica que exista un documento txt dentro de la base de datos.
    Entrada: N/D
    Salida: Flags de True o False según cada caso.
    """
    try:
        with open ("Documento(XML).xml","r") as salida:
            return True
    except:
        return False

def listaString (lista):
    """
    Función:Almacena las Sub-Listas tokenizadas y las combierte en string para ser utilizadas en XML.
    Entrada: Parámetro Lista.
    Salida: Lista Principal con todas las sub listas en su interior.
    """
    articulos = eliminaElementoEspacio(lista[0])
    preposiciones = eliminaElementoEspacio(lista[1])
    pronombres = eliminaElementoEspacio(lista[2])
    verbos = eliminaElementoEspacio(lista[3])
    numeros = eliminaElementoEspacio(lista[4])
    sinClasificar = eliminaElementoEspacio(lista[5])

    articulos = str(articulos)
    preposiciones = str(preposiciones)
    pronombres = str(pronombres)
    verbos = str(verbos)
    numeros = str(numeros)
    sinClasificar = str(sinClasificar)

    listaPrincipal=[quitaTildes(articulos),quitaTildes(preposiciones),quitaTildes(pronombres),quitaTildes(verbos),quitaTildes(numeros),quitaTildes(sinClasificar)]
    print ("\nEl archivo XML se ha creado satisfactoriamente.")
    return listaPrincipal

#----------Funcionamiento de XML----------
def creaXML (lista):
    """
    Función: Crea un xml y determina las pocisiones de las sublistas dentro del mismo
    Entrada: Parámetro lista (Lista principal con sub listas)
    Salida: Documento XML Con todos los elementos de listaPrincipal.
    """
    Seis=["Articulos","Preposiciones","Pronombres","Verbos","Numeros","SinClasificar"]
    
    DOMimpl = minidom.getDOMImplementation()
    xmldoc= DOMimpl.createDocument(None,"Documento",None)
    listaPrincipal = listaString (lista)
    doc_root = xmldoc.documentElement
    cont=0
    for ordenador in listaPrincipal:
        nodo1 = xmldoc.createElement ("Parte")
        nodo1.setAttribute("Seccion",Seis[cont])
        
        elemento = xmldoc.createElement ("Contenido")
        elemento.appendChild(xmldoc.createTextNode(ordenador))
        nodo1.appendChild(elemento)

        doc_root.appendChild(nodo1)
        
        cont+=1
    fichero = open("Documento(XML).xml","w")
    fichero.write(xmldoc.toxml ())
    fichero.close()
########################### Creación de XML #####################

########################### Creación de HMTL #####################
template = """
<center>
    <p><font size="5"><b>Contenido del archivo original: </b>{txt}</font></p>
    <h1>----------</h1>
    <table border width="40%">
        <tr>
            <th colspan=6 style= "font-size:150%">Análisis del documento</th>
        </tr>
        <tr>
            <td style="font-size:150%">Artículos</td> <td style="font-size:150%">Preposiciones</td> <td style="font-size:150%">Pronombres</td> <td style="font-size:150%">Verbos</td> <td style="font-size:150%">Números</td> <td style="font-size:150%">Sin Clasificar</td>
        </tr>
"""

def crearHTML(nombreArchivo):
    """
    Función: Créa un HTML y determina las pocisiones de las sublistas dentro del mismo.
    Entrada: N/D
    Salida: Documento HTML Con todos los elementos de SubLista.
    """
    f = open(nombreArchivo, 'w')
    html_template = template
    f.write(html_template) 
    f.close()


def ingresaTexto(txt, nombreArchivo):
    """
    Función: Abre y sustituye elementos dentro el HTML.
    Entrada: Parámetro txt.
    Salida:N/D
    """
    with open(nombreArchivo, "r") as file:
        content = file.read()

    content = content.replace("{txt}", txt)

    with open(nombreArchivo, "w") as file:
        file.write(content)

def leer2(nombreArchivo):   
    """
    Función: Lée el contenido del HTML
    Entrada:N/D
    Salida: Retorno de variable content
    """
    with open(nombreArchivo, "r") as file:
        content = file.read()
        return content

def existeHTML():
    """
    Función: Verifica que exista un archivo con el nombre indicado.
    Entradas: Parámetro - Nombre del archivo (nomArchLeer).
    Salidas: 1 si existe el archivo en la carpeta, -1 si no existe el archivo.
    """
    contenido = os.listdir()
    for elemento in contenido:
        if re.match("^.*\.(html)$", elemento):
            return True
    return False

def listaMayor(lista):
    """
    Función: Calcula la sublista con mayor cantidad de elementos.
    Entrada: Parámetro - (lista) Matriiz con todos los datos.
    Salida: Mayor cifra de elementos y cantidad de elementos de
    todas las sublistas.
    """
    cantidad = []
    for sub in lista:
        cantidad.append(len(sub))
        
    mayor = 0
    for elem in cantidad:
        if elem > mayor:
            mayor = elem
    return mayor, cantidad


def rellenaListas(lista, cantidad):
    """
    Función: Rellena las sublistas con espacios vacíos para poder
    generar la tabla en HTML.
    Entrada: Parámetro - (lista) Matriiz con todos los datos.
    Salida: Lista con elementos vacíos añadidos.
    """
    numeros = listaMayor(lista)[1]
    contador = 0
    while contador < len(lista):
        cont = 0
        while cont < (cantidad - numeros[contador]):
            lista[contador].append("")
            cont += 1
        contador += 1
    return lista

def agregaFilas(lista, indice):
    """
    Función: Agrega las filas de la tabla con sus respectivos valores.
    Entrada: Parámetro - (lista) Matriiz con todos los datos y
    (indice) que es el indicador de la columna.
    Salida: Edición del contenido HMTL.
    """
    content = """
        <tr>"""
    content += """
            <td>"""+lista[0][indice]+"</td>"+" <td>"+lista[1][indice]+"</td>"+" <td>"+lista[2][indice]+"</td>"+" <td>"+lista[3][indice]+"</td>"+" <td>"+lista[4][indice]+"</td>"+" <td>"+lista[5][indice]+"</td>"
    content += """
        </tr>"""
    return content

def agregaEtiquetas():
    """
    Función: Agrega las líneas finales del HTML.
    Entrada: N/D
    Salida: Variable con las etiquetas.
    """
    content = """
    </table>
    <h1>----------</h1>
    <p><font size="5"><b>Reporte: </b>El texto original tiene {total} tokens de los cuales hay: {articulos} artículos, {preposiciones} preposiciones, {pronombres} pronombres, {verbos} verbos, {numeros} números y {sclas} sin clasificar.</font></p>
</center>"""

    return content

def grabaFinal(content, nombreArchivo):
    """
    Función: Abre el documento HTML y agrega todos los elemento dentro del documento.
    Entrada: Parámetro - (content) Contenido acumulado hasta el momento.
    Salida: N/D
    """
    with open(nombreArchivo, "w") as file:
        file.write(content)   

def cambiaFinal(otraLista, nombreArchivo):
    """
    Función: Sustituye las cantidades del reporte en el archivo HMTL.
    Entrada: Parámetro - (otraLista) Lista original para hacer el conteo.
    Salida: Sustitución de los parámetros en el HTML.
    """
    with open(nombreArchivo, "r") as file:
        content = file.read()

    articulos = len(eliminaElementoEspacio(otraLista[0]))
    preposiciones = len(eliminaElementoEspacio(otraLista[1]))
    pronombres = len(eliminaElementoEspacio(otraLista[2]))
    verbos = len(eliminaElementoEspacio(otraLista[3]))
    numeros = len(eliminaElementoEspacio(otraLista[4]))
    sclas = len(eliminaElementoEspacio(otraLista[5]))
    total = articulos + preposiciones + pronombres + verbos + numeros + sclas
  
    content = content.replace("{total}", str(total))
    content = content.replace("{articulos}", str(articulos))
    content = content.replace("{preposiciones}", str(preposiciones))
    content = content.replace("{pronombres}", str(pronombres))
    content = content.replace("{verbos}", str(verbos))
    content = content.replace("{numeros}", str(numeros))
    content = content.replace("{sclas}", str(sclas))

    with open(nombreArchivo, "w") as file:
        file.write(content)
    
def cicloFilas(lista, nombreArchivo):
    """
    Función: Se encarga de llenar cada celda de la planilla con elementos deseados de la lista.
    Entrada: Parámetro lista.
    Salida: N/D
    """
    cantidad = listaMayor(lista)[0]
    matriz = rellenaListas(lista, cantidad)
    content = leer2(nombreArchivo)
    contador = 0
    while contador < cantidad:
        content += agregaFilas(matriz, contador)
        contador += 1
    ### Sección para añadir últimas dos etiquetas ###
    content += agregaEtiquetas()
    grabaFinal(content, nombreArchivo)

def generaNombre():
    """
    Función: Genera el nombre del archivo HTML.
    Entrada: N/D
    Salida: Nombre con la fecha y la hora específica.
    """
    completo = ""
    now = datetime.now()
    
    dia = str(now.day)
    mes = str(now.month)
    anno = str(now.year)
    hora = str(now.hour)
    minuto = str(now.minute)
    seg = str(now.second)

    completo += "Analisis-"+dia+"-"+mes+"-"+anno+"-"+hora+"-"+minuto+"-"+seg+".html"
    return completo
########################### Creación de HMTL #####################
