#!/usr/bin/python3

import random
import time
import sys
import math

def objective_function(consensus, data):
    distance = 0
    for line in data:
        different_letter = 0
        for i in range(len(line)):
            if consensus[i]!=line[i]:
                different_letter += 1
            
        distance += different_letter ** 2
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

def simulated(data, initial_temperature, cooling_rate, max_time):
    start = time.time()
    best_last_time = max_time
    consensus = greedy(data)
    current_distance = objective_function(consensus, data)
    best_consensus = consensus
    best_distance = current_distance
    
    temperature = initial_temperature

    while time.time() - start <= max_time: 
        # Genera una solución vecina perturbando la solución actual
        neighbor = list(consensus)
        index_to_change = random.randint(0, len(neighbor) - 1)
        neighbor[index_to_change] = random.choice('ACGT')
        neighbor = ''.join(neighbor)

        neighbor_distance = objective_function(neighbor, data)
        
        # Calcula la diferencia en la función objetivo entre la solución actual y la vecina
        delta = neighbor_distance - current_distance
        
        # Decide si aceptar la solución vecina
        if temperature!=0 :
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                consensus = neighbor
                current_distance = neighbor_distance
        else:
            if delta < 0 :
                consensus = neighbor
                current_distance = neighbor_distance
        # Actualiza la mejor solución si es necesario
        if current_distance < best_distance:
            best_consensus = consensus
            best_distance = current_distance
            best_last_time = time.time() - start
        # Reduce la temperatura 
        temperature *= cooling_rate
 
    return best_consensus, best_distance, best_last_time


if __name__ == "__main__":

    try:
        maxtime_index = sys.argv.index('-t')
        max_time = sys.argv[maxtime_index + 1]
        max_time = float(max_time)
    except:
        max_time = float(60)


    try:
        initial_temperature_index = sys.argv.index('-it')
        initial_temperature = sys.argv[initial_temperature_index + 1]
        initial_temperature = float(initial_temperature)
    except:
        initial_temperature = 9000.0

    try:
        cooling_rate_index = sys.argv.index('-c')
        cooling_rate = sys.argv[cooling_rate_index + 1]
        cooling_rate = float(cooling_rate)
    except:
        cooling_rate = 0.9

    n=100
    with open('resultados_500.txt', 'w') as output:
        tiempo_promedio = 0
        fitness_promedio = 0
        output.write("inst    m     l     mh")
        mh_time = 0
        distance_prom=0
        for aux in range(2):
            for inst in range(100):
                data = []
                with open (f'../n100_m200_l15_a4/inst_500_'+str(n)+'_4_'+str(inst)+'.txt',"r") as input:
                    for line in input:
                        line =line.replace("\n","")
                        data.append(line)

                best_consensus, best_distance, best_last_time = simulated(data, initial_temperature, cooling_rate, max_time)
                print(f'{best_distance}')
                output.write(str(inst)+" 500   "+str(n)+"   "+str(best_distance)+"\n")
                mh_time+=best_last_time
                distance_prom=distance_prom+best_distance
            n=n+200
            
            mh_time /= 100
            distance_prom/=100
            print('Tiempo Mh Promedio = ' + str(mh_time) + 's')
            print('Distancia Mh Promedio = ' + str(distance_prom) + 's')
