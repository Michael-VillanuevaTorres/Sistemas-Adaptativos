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

    best_last_time = maxTime

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
            best_last_time = time.time() - start
        
        # Reduce la temperatura 
        temperature *= cooling_rate
 
    return greedy_distance,best_consensus, best_distance, best_last_time

    
if __name__ == "__main__":

    initial_temperature = 10000.0
    cooling_rate = 0.95
    maxTime=60

        
    with open ("greedydatos1000.txt","w") as output:
        output.write("inst    m     l     greedy      mh")
        
        mh_time = 0
        for inst in range(100):
                    
            with open ('../instancias1/inst_200_15_4_'+str(inst)+".txt","r") as input:
                data = []
                for line in input:
                    line =line.replace("\n","")
                    data.append(line)

            greedy_distance,best_consensus, best_distance,best_last_time=simulated(data,initial_temperature,cooling_rate,maxTime)

            print(str(inst)+"  "+str(greedy_distance)+"   "+str(best_distance)+"")  
            output.write(str(inst)+" 200 400   "+str(greedy_distance)+"   "+str(best_distance)+"\n")
            mh_time+=best_last_time
        mh_time /= 100
        print('Mh Promedio = ' + str(mh_time) + 's')