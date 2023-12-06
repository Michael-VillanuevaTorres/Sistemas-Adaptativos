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

def p_greedy(data, n_determinist):
    dict = [] 
    ans = ''
    for i in range(len(data[0])):
        dict.append({'A': 0, 'C': 0, 'T': 0, 'G': 0})
        for line in data:
            dict[i][line[i]] += 1
        max_val = max(dict[i].values())

        candidates_max = []
        candidates_aleatorios = []
        for protein in dict[i]:
            if dict[i][protein] == max_val:
                candidates_max.append(protein)
            else:
                candidates_aleatorios.append(protein)
                
        numero_aleatorio = random.random()
        if numero_aleatorio > n_determinist and len(candidates_aleatorios) != 0:
            selected = random.randint(0, len(candidates_aleatorios) - 1)
            ans += candidates_aleatorios[selected]
        else:
            selected = random.randint(0, len(candidates_max) - 1)
            ans += candidates_max[selected]

    result=ans

    return result

def simulated(data, n_determinist, initial_temperature, cooling_rate, max_time):
    start = time.time()
    best_last_time = max_time
    consensus = p_greedy(data, n_determinist)
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
        inst_index = sys.argv.index('-i')
        inst = sys.argv[inst_index + 1]
    except:
        print('Debes ingresar una instancia')
        exit()

    try:
        maxtime_index = sys.argv.index('-t')
        max_time = sys.argv[maxtime_index + 1]
        max_time = float(max_time)
    except:
        max_time = float(60)

    try:
        n_determinist_index = sys.argv.index('-d')
        n_determinist = sys.argv[n_determinist_index + 1]
        n_determinist = float(n_determinist)
    except:
        n_determinist = 0.9

    try:
        initial_temperature_index = sys.argv.index('-it')
        initial_temperature = sys.argv[initial_temperature_index + 1]
        initial_temperature = float(initial_temperature)
    except:
        initial_temperature = 10000.0

    try:
        cooling_rate_index = sys.argv.index('-c')
        cooling_rate = sys.argv[cooling_rate_index + 1]
        cooling_rate = float(cooling_rate)
    except:
        cooling_rate = 0.95

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

                best_consensus, best_distance, best_last_time = simulated(data, n_determinist, initial_temperature, cooling_rate, max_time)
            n=n+200
            print(f'{best_distance}')
            output.write(str(inst)+" 500   "+str(n)+"   "+str(best_distance)+"\n")
            mh_time+=best_last_time
            distance_prom=distance_prom+best_distance
        mh_time /= 100
        distance_prom/=100
        print('Tiempo Mh Promedio = ' + str(mh_time) + 's')
        print('Distancia Mh Promedio = ' + str(distance_prom) + 's')
