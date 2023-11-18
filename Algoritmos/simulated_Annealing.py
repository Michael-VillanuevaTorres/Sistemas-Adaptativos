import random
import time
import sys
import math

def objective_function(consensus, data):
    distance=0
    for line in data:
        different_letter=0
        for i in range(len(line)):
            if consensus[i]!=line[i]:
                different_letter+=1
            
        distance+=different_letter**2
    return distance

def greedy(data):

    dict = [] 
    ans = ''    
    for i in range(len(data[0])): ## i desde 0 a len de cada linea en data, en este caso 15
        dict.append({'A': 0, 'C': 0, 'T': 0, 'G': 0}) ## Dentro de la lista dict genera un mapa con { , , }
        for line in data: ## Dentro de cada linea de data
            dict[i][line[i]] += 1  ## dentro de cada dict (15 dict en este caso)[line[i] igual va desde cada letra dentro de una linea aumentado esa letra en la dict] 
        max_val = max(dict[i].values())
        candidates = []
        for protein in dict[i]:
            if dict[i][protein] == max_val:
                candidates.append(protein)
        selected = random.randint(0, len(candidates) - 1)
        ans += candidates[selected]

    result=ans

    return (result)

def simulated(data,initial_temperature,cooling_rate,maxTime):
    consensus = greedy(data)
    current_distance = objective_function(consensus, data)
    greedy_distance=current_distance
    best_consensus = consensus
    best_distance = current_distance
    
    temperature = initial_temperature

    start = time.time()

    while time.time() - start <= maxTime: 
        # Genera una solución vecina perturbando la solución actual
        neighbor = list(consensus)
        index_to_change = random.randint(0, len(neighbor) - 1)
        neighbor[index_to_change] = random.choice('ACGT')
        neighbor = ''.join(neighbor)

        neighbor_distance = objective_function(neighbor, data)
        
        # Calcula la diferencia en la función objetivo entre la solución actual y la vecina
        delta = neighbor_distance - current_distance
        
        # Decide si aceptar la solución vecina
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            consensus = neighbor
            current_distance = neighbor_distance
        
        # Actualiza la mejor solución si es necesario
        if current_distance < best_distance:
            best_consensus = consensus
            best_distance = current_distance
        
        # Reduce la temperatura 
        temperature *= cooling_rate
 
    return greedy_distance,best_consensus, best_distance

    
if __name__ == "__main__":

    initial_temperature = 10000.0
    cooling_rate = 0.95
    # Verifica si se proporciona al menos un argumento
    if len(sys.argv) < 5:
        print("Por favor, proporciona este tipo de entrada --> ´python3 simulated_Annealing.py -i instanciaProblema -t tiempoMaximoSegundos´ .")
        exit()
    elif len(sys.argv) == 5:
        # El segundo argumento (sys.argv[1]) es el nombre del archivo con la entrada
        # El tercer argumento (sys.argv[2]) es el nivel de determinismo
        iIndex = sys.argv.index('-i')
        inst = sys.argv[iIndex + 1]
        tIndex = sys.argv.index('-t')
        maxTime = sys.argv[tIndex + 1]
        maxTime = float(maxTime)
    else:
        iIndex = sys.argv.index('-i')
        inst = sys.argv[iIndex + 1]
        tIndex = sys.argv.index('-t')
        maxTime = sys.argv[tIndex + 1]
        maxTime = float(maxTime)
        itIndex = sys.argv.index('-it')
        initial_temperature = float(sys.argv[itIndex + 1])
        crIndex = sys.argv.index('-cr')
        cooling_rate = float(sys.argv[crIndex + 1])

        

                    
        with open ('../instancias1/inst_200_15_4_'+str(inst)+".txt","r") as input:
            data = []
            for line in input:
                line =line.replace("\n","")
                data.append(line)

            greedy_distance,best_consensus, best_distance=simulated(data,initial_temperature,cooling_rate,maxTime)

            print(str(inst)+" greedy_distance: "+str(greedy_distance)+" mh_distance: "+str(best_distance)+"")  
            