from pathlib import Path #se utiliza par aobtener la ruta relativa del archivo
import re #se utiliza para el manejo de las expresiones regulares involucradas en la validacion  de las entradas
from scipy.spatial import distance_matrix #se utiliza para el calculo de la matriz de distancias en base a las  coordenadas del archivo
import numpy as np #se utiliza para el manejo de arreglos y matrices
import random #se utiliza para obtener las numeros aleatorios involucrados tanto en la ruleta como en generacion de numeros enteros par el llenado de listas
import sys #se utilizo para el manejo de excepciones en la validacion de las entradas
import os #se utilizo para preguntar si el archivo por el cual se consulta se encuentra en el sistema

random.seed(1) #se utiliza para controlart la secuencia de numeros aleatorios involucrados en el algoritmo y para, en cierta medida, controlar la desviación estandar de los valores con respecto al óptimo de la solucion

def next_node(path, visibility, actual_city_visited_by_ant,pheromone_matrix_copy): #funcion que permite elegir el siguiente nodo
    visibility[:,actual_city_visited_by_ant] = 0    #se hace 0 la fila  de la ciudad que estamos visitando en la matriz de visibilidad (1/distance_matrix)
    temp_p = pheromone_matrix_copy[actual_city_visited_by_ant,:] #se selecciona la fila de la ciudad actualmente visitada por la hormiga en la copia de la matriz de feromonas 
    temp_v = np.power(visibility[actual_city_visited_by_ant,:],heuristic_coefficient) #de acuerdo a la ecuación 1 se eleva al coeficiente heuristico la visibilidad (1/Dij) en el tramo que involucra a la ciudad visitada actualemente por la hormiga
    temp_p = temp_p[:,np.newaxis] #se agrega una dimension más  a temp_p para lograr una correcta multiplicacion
    temp_v = temp_v[:,np.newaxis] #se agrega una dimension mas  a temp_v   para lograr una correcta multiplicacion
    max_matrix = np.multiply(temp_p,temp_v) #multiplicacion entre temp_p y temp_v de acuerdo a la ecuación 2
    r = np.random.random_sample() #se declara un numero aleatorio entre 0  y 1 para elegir si se utiliza la ecuacion 1 o 2
    if r<=q0: #si la prob aleatoria es menor que la prob q0 que se ingreso por teclado
        maxim,j0 = maximo(max_matrix) #se busca el maximo y el indice en done se encontro
        visibility[:,j0] = 0 #se hace cero la fila dentro de la visibilidad de la ciudad visitada actualmente para no considerarla dentro de los posibles proximos maximos
        path[i,j+1]=j0 #se agrega al path principal el siguiente nodo visitado
    else: #si r > que q0 se procede de acuerdo a la ecuación 2
        suma = np.sum(max_matrix)   #se suman los elementos de max_matrix
        probs = max_matrix/suma #se divide cada elememnto de la matriz por  la suma de estos de acuerdo a la ecuacion 2
        cum_sum = np.cumsum(probs) #se calcula la suma acumulada de prbos para formar la ruleta
        spin_wheel = np.random.random_sample()  #se lanza la ruleta
        j0 = np.nonzero(cum_sum>spin_wheel)[0][0] #se elige un elemento de la matriz en base al tiro de la ruleta que corresponde a su vez al elemento de max_matrix seleccionado
        visibility[:,j0] = 0 #hacemos la visibilidad 0 en el vecindario del elemento para evitar volver a elegir el mismo elemento 
        path[i,j+1]=j0  #se agrega el elemento seleccionado al path principal
    return path #se retorna el path pero ahora con el elemento seleccionado

def finding_minimal_distance(path, distance_matrix):
    optimal_path = np.array(path) #copia del path principal
    cost_path = np.zeros((len(coordenates),1)) #se declara un arreglo para albergar el cosot de cada ruta seguida por cada hormiga
    for i in range(number_ants):   #hacer una vez por cada hormiga en el arreglo
        cumulative_distance = 0 #se declara una veariable cumulative_distance y se iguala a 0
        for j in range(len(coordenates)-1): #hacer una vez por cada ciudad en el conjunto de ciudades-1
            if j == 0 : #si es la primera ciudad
                initial = int(optimal_path[i,j]) #se rescata el indice de esta ciudad
            cumulative_distance += distance_matrix[int(optimal_path[i,j]),int(optimal_path[i,j+1])] #se suma la distancia entre cada ciudad y se agrega a cumulative_distance
        cumulative_distance += distance_matrix[int(optimal_path[i,j]),initial] #se agrega la distancia desde el ultimo elemento al primer elemento
        cost_path[i]=cumulative_distance #se agrega al costo de esa ruta el valor obtenido en cumulative_distance   
    index_minimal_cost = np.argmin(cost_path)  #seleccionamos el indice de donde se encontro la menor distancia obtenida del arreglo dse costos
    minimal_distance_local = cost_path[index_minimal_cost] #se almacena la menor distancia obtenida  
    return minimal_distance_local, index_minimal_cost #se retorna la menor distancia encontrada y el indice en donde se encontro esta

def maximo(max_matrix): #funcion que permite encontrar el maximo en un arreglo
    maxim=-1 #se declara maxim como el menor maximo posible
    J = -1 #se declara J con un valor menor al  del rango posible
    for i in range(len(max_matrix)): #se hara 1 vez opo cada elemento de max_matrix
        if max_matrix[i]>=maxim: #si el elemento de max_matrix es mayor que el maxim definido, entonces:
            maxim = max_matrix[i] #maxim es igual al elemento max_matrix[i] de
            J = i #se guarda el indice de donde se encontro el maximo
    return maxim,J #retornamos el maximo valor encontrado en max_matrix y el indice de donde se encontro


def initialize_ants(path, length): #funcion que permite inicializar las hormigas en el path
    ants = set() #se crea un set que no permite elementos repetidos llamado ants
    while len(ants) < length: #mientras la cantidad de elementos en ants sea menor que length hacer:
        ants.add(random.randint(0,length-1)) #añadir un numero randomico entre 0 y length-1 si este aún no esta en el set
    ants = list(ants) #cambiamos el tipo de dato de ants a lista
    return ants
def get_coordenates(name_file):
    relative = Path(name_file) #se obtiene la ruta relativa del archivo
    absPath = relative.absolute() #se obtinene la ruta absoluta del archivo
    with open(absPath,'r') as file:  #se abre el archivo
        coordenates = file.readlines() #coordenates tiene ahora una lista  en donde cada elemento corresponde a una linea del archivo
    coordenates = list(map( lambda f:f.strip(), coordenates)) #se eliminan los \n
    pattern = '[aA-zZ].*' #se crea un patron que puede ser una secuencia de caracteres
    coordenates = [re.sub(pattern,'',line) for line in coordenates] #se reemplaza la descripcion del archivo con espácios vacio
    coordenates = list(filter( lambda f:f!="", coordenates)) #se elimina los elementos de la lista que tienen espacios vacios
    coordenates = [ re.findall(r'\d+\.\d+', line) for line in coordenates ] #se filtra la lista y dejamos solo aquellos elementos que son coordenadas
    coordenates = [ [ int(float(element)) for element in line ] for line in coordenates ] #se cambia el tipo de dato str por int 
    return coordenates #se retorn una lista  2-tupla de int, con las coordenadas vistas en el archivo
def get_parameters():
    #Entrada del nombre del archivo y manejo de excepciones 
    name_file = sys.argv[1] #se obtiene la ruta absoluta del archivo
    if re.findall('([aA-zZ]*[0-9]*)*.\..*', name_file): #se pregunta si el archivo posee extensión
            sys.exit("El nombre del archivo no debe tener extensión Ej: Si el Archivo es 'berlin52.txt', usted debe ingresar 'berlin52'\n Intente Nuevamente")
    else: 
        name_file = name_file + ".txt" #se añade la extension txt al archivo
        if os.path.exists(name_file): #Preguntamos si el archivo existe
            pass
        else:
            message = '    El Archivo: '+ name_file +'  no se encuentra en ningún directorio. Asegurese de estar escribiendo el nombre correctamente'
            sys.exit(message)       
    #Ingreso  del factor de evaporación
    evaporation_rate = sys.argv[2] #se ingresa el factor de evaporacion
    if re.findall('[aA-zZ]', evaporation_rate): #se pregunta si la entrada es una secuencia de letras
        sys.exit("El Factor de Evaporación debe ser un Número, Intentelo Nuevamente")
    else:
        evaporation_rate = float(evaporation_rate) #cambiamos el tipo de dato de la entrada str a float
        if evaporation_rate<0 or evaporation_rate>1: #preguntamos si la entrada es menor que 0 o mayor que 1
            message ='El Factor de Evaporación debe estar entre 0 y 1'
            sys.exit(message)   
        else:
            pass
    #Ingreso  del número de iteraciones
    number_iterations = sys.argv[3] #ingreso de la cantidad de iteraciones
    if re.findall('[aA-zZ]', str(number_iterations)): #preguntamos si la entrada es una secuencia de caracteres
        sys.exit("El Número de iteraciones debe ser un Número, Intentelo Nuevamente")
    else: 
        if re.findall('[0-9]*\.[0-9]*',str(number_iterations)): #preguntamos si la entrada es un decimal
            message = 'El Número de  Iteraciones debe ser un Número Entero'
            sys.exit(message)
        elif int(number_iterations) <= 0:           #preguntamos si el entero ingresado es menor o igual que cero
            message = "\033[4;35m"+'El Número de  Iteraciones debe ser mayor que 0'
            sys.exit(message)
        else:
            number_iterations = int(number_iterations) #cambiamos el tipo de dato de la entrada que era str a int
    #Ingreso de la cantidad de hormigas
    number_ants = sys.argv[4] #ingreso de la cantidad de hormigas
    if re.findall('[aA-zZ]', str(number_ants)): #se pregunta si la entrada es una secuencia de caracteres no numericos
        sys.exit("El Número de Hormigas debe ser un Número, Intentelo Nuevamente")
    else: 
        if re.findall('[0-9]*\.[0-9]*',str(number_ants)): #se pregunta si la entrada es un decimal
            message = "\033[4;35m"+'El Número de  Hormigas debe ser un Número Entero'
            sys.exit(message)
        elif int(number_ants) <= 0:          #se pregunta si la entrada es menor que 0  
            message = "\033[4;35m"+'El Número de  Hormigas debe ser mayor que 0'
            sys.exit(message)
        else:
            number_ants = int(number_ants) #cambiamos el tipo de dato que era str a int
    #Ingreso  de el coeficiente heurístico
    heuristic_coefficient = sys.argv[5] #se ingresa heuristic_coefficient
    if re.findall('[aA-zZ]', str(heuristic_coefficient)): #pregunta si la entrada no es un numero
        sys.exit("El Coeficiente Heurístico debe ser un Número, Intentelo Nuevamente")
    else: 
        if re.findall('[0-9]*\.[0-9]*',str(heuristic_coefficient)): #pregunta si el numero ingresado es decimal
            heuristic_coefficient = float(heuristic_coefficient)
            if heuristic_coefficient<=0: #se pregunta si la entrada  es negativa
                sys.exit("El Coeficiente Heurístico debe ser Positivo")
            else:
                pass
        elif isinstance(int(heuristic_coefficient), int): #se pregunta si el numero es un entero
            sys.exit("El Coeficiente Heurístico debe ser un Número Decimal, Intentelo Nuevamente")
            if int(heuristic_coefficient)<=0: #se pregunta si el numero entero ingresado es positivo
                sys.exit("El Coeficiente Heurístico debe ser Positivo")
    #Ingreso  de la probabilidad de selección del sigueinte nodo
    q0 = sys.argv[6] #se pide la entrada de q0
    if re.findall('[aA-zZ]', str(q0)): #preguntamos si q0 es un numero
        sys.exit("La Probabilidad de selección de Siguiente Nodo debe ser un Número, Intentelo Nuevamente")
    else: 
        if re.findall('[0-9]*\.[0-9]*',str(q0)): #preguntamos si la prob ingresada es un numero decimal
            q0 = float(q0) #declaramos que q0 es un decimal
            if q0<=0: #se pregunta si la prob ingresada es menor que 0
                sys.exit("La Probabilidad de Selección del Siguiente Nodo debe ser Positivo")
            else:
                if q0>1: #se pregunta si la prob ingresada es mayor que 1
                    sys.exit("La Probabilidad de Selección del Siguiente Nodo debe estar entre 0 y 1")            
                else:
                    pass
        elif isinstance(int(q0), int): #se pregunta si la prbo ingresada es un entero
            sys.exit("La Probabilidad de Selección del Siguiente Nodo debe ser un Número Decimal, Intentelo Nuevamente")
            if int(q0)<=0: #se pregunta si la prob es menor que 0
                sys.exit("La Probabilidad de Selección del Siguiente Nodo debe ser Positivo")

    return name_file, evaporation_rate, number_iterations, number_ants, heuristic_coefficient, q0 #se retornan los parametros ingresados por el usuario



name_file, evaporation_rate, number_iterations, number_ants, heuristic_coefficient, q0 = get_parameters() #se obtienen las entradas
coordenates = get_coordenates(name_file) #se llama a la funcion get_coordenates y se le pasa como parametro el nombre del archivo

distance_matrix = distance_matrix(coordenates, coordenates).astype(int) #se calcula la distancia entre los nodos y se setea a valores enteros
distance_matrix_copy = np.where(distance_matrix==0, -1, distance_matrix) #se reemplazan los ceros por -1 para poder calcular el inverso

reciprocal_distance_matrix = np.reciprocal(distance_matrix_copy.astype(np.float32)) #se calclua el inverso de los enteros en la matriz de distancias
reciprocal_distance_matrix = np.where(reciprocal_distance_matrix==-1, 0, reciprocal_distance_matrix) #volvemos a cambiar la diagonal con valores 0

pheromone_matrix =  np.full((number_ants,len(coordenates)),evaporation_rate) #se inicializa la matriz de feromonas haciendo que cada elemento sea evaporation_rate

path = np.ones((number_ants,len(coordenates))).astype(int) #se inicializa la matriz de rutas
  
minimal_distance_global = 100000
print("Por Favor, Espere Un Momento")
for iteration in range(number_iterations): #se establece un ciclo repetitivo para hacer las iteraciones
    path[:,0] = initialize_ants(path, number_ants)  #inicializa las hormigas en cada segmento del grafo
    pheromone_matrix_copy = np.array(pheromone_matrix) #copia de la matriz de feromonas
    for i in range(number_ants):  #ciclo repetitivo para cada hormiga
        visibility = np.array(reciprocal_distance_matrix) #se crea una copia de la matriz del inverso de la distancia
        for j in range(len(coordenates)-1):  #ciclo repetitivo de para seleccionar el siguiente nodo a ser alcanzado
            actual_city_visited_by_ant = int(path[i,j]) #seleccionamos la ciudad que visitaremos 
            path= next_node(path, visibility, actual_city_visited_by_ant, pheromone_matrix_copy) #se selecciona el siguiente nodo        
        minimal_distance_local, index_minimal_cost = finding_minimal_distance(path, distance_matrix)  #Se obtiene la menor distancia encontrada y el indice en donde se encuentra esta distancia
        if minimal_distance_local< minimal_distance_global: #Si la menor distancia encontrada en esta iteracion es menor que la menor distancia global, entonces:
            best_path = path[index_minimal_cost,:] #La mejor ruta es  reemplzada por la mejor ruta encontrada en esta iteracion
            minimal_distance = minimal_distance_local #la mejor distancia ahora es la mejor distancia encontrada en esta iteracion
        pheromone_matrix_copy[actual_city_visited_by_ant,:]=(1-evaporation_rate)*pheromone_matrix_copy[actual_city_visited_by_ant, :]+evaporation_rate*pheromone_matrix[actual_city_visited_by_ant,:] #Se Calcula la Actualización Local de la Feromona
    dt = 1/minimal_distance 
    pheromone_matrix_copy[index_minimal_cost,:] = (1-evaporation_rate)*pheromone_matrix_copy[index_minimal_cost,:]+evaporation_rate*dt #Se Calcula la Actualización Global de la Feromona
    
print("La Mejor Ruta Encontrada es:  "+ str(best_path)) #Se Imprime La Mejor Ruta Encontrada
print("El Costo de la Ruta es : " + str(int(minimal_distance[0])))     #Se Imprime el Costo de la Mejor Ruta     

    
    
    
    
    
    
    
    
    


            
            
        