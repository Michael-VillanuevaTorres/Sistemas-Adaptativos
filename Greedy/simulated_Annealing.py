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


# Verifica si se proporciona al menos un argumento
if len(sys.argv) < 3:
    print("Por favor, proporciona este tipo de entrada --> ´python3 simulated_Annealing.py -i instanciaProblema -t tiempoMaximoSegundos´ .")
    exit()
else:
    # El segundo argumento (sys.argv[1]) es el nombre del archivo con la entrada
    # El tercer argumento (sys.argv[2]) es el nivel de determinismo
    inst = sys.argv[1]    

    if len(sys.argv) > 2:
        Tiempo = float(sys.argv[2])

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

def simulated(data,initial_temperature,cooling_rate,max_iterations):
    consensus = greedy(data)
    current_distance = objective_function(consensus, data)
    
    best_consensus = consensus
    best_distance = current_distance
    
    temperature = initial_temperature

    for iteration in range(max_iterations):
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
 
    return best_consensus, best_distance

    
if __name__ == "__main__":
    initial_temperature = 1000.0
    cooling_rate = 0.95
    max_iterations = 10000

    with open ('../n100_m200_l15_a4/inst_200_15_4_'+str(inst)+".txt","r") as input:
        data = []
        for line in input:
            line =line.replace("\n","")
            data.append(line)

    best_consensus, best_distance=simulated(data,initial_temperature,cooling_rate,max_iterations)
    
    print("Mejor consenso:", best_consensus)
    print("Distancia mínima:", best_distance)