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

def crossover(parent1, parent2):
    # Punto de cruce
    crossover_point = random.randint(1, len(parent1) - 1)
    
    # Genera hijos combinando las partes de los padres
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    
    return child1, child2

def mutate(individual):
    # Mutación: Cambia un carácter aleatorio en el individuo
    mutation_point = random.randint(0, len(individual) - 1)
    mutated_individual = list(individual)
    mutated_individual[mutation_point] = random.choice('ACGT')
    return ''.join(mutated_individual)

def generate_neighbor(consensus, data, genetic_probability):
    if random.random() < genetic_probability:
        # Aplicar operador genético para generar vecino
        # Selección de dos padres aleatorios
        parent1 = consensus
        parent2 = greedy(data)
        
        # Aplicar crossover
        child1, child2 = crossover(parent1, parent2)
        
        # Aplicar mutación a los hijos
        child1 = mutate(child1)
        child2 = mutate(child2)
        
        # Elegir uno de los hijos aleatoriamente como vecino
        neighbor = child1 if random.random() < 0.5 else child2
    else:
        # Generar vecino perturbando la solución actual
        neighbor = list(consensus)
        index_to_change = random.randint(0, len(neighbor) - 1)
        neighbor[index_to_change] = random.choice('ACGT')
        neighbor = ''.join(neighbor)

    return neighbor

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

def simulated(data,initial_temperature, cooling_rate, max_time,genetic_probability):
    start = time.time()
    best_last_time = max_time
    consensus = greedy(data)
    current_distance = objective_function(consensus, data)
    best_consensus = consensus
    best_distance = current_distance
    
    temperature = initial_temperature

    while time.time() - start <= max_time: 
        # Genera una solución vecina perturbando la solución actual
        neighbor = generate_neighbor(consensus,data,genetic_probability)

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
        initial_temperature_index = sys.argv.index('-it')
        initial_temperature = sys.argv[initial_temperature_index + 1]
        initial_temperature = float(initial_temperature)
    except:
        initial_temperature = 13000

    try:
        cooling_rate_index = sys.argv.index('-c')
        cooling_rate = sys.argv[cooling_rate_index + 1]
        cooling_rate = float(cooling_rate)
    except:
        cooling_rate = 0.6
    try:
        genetic_probality_index = sys.argv.index('-g')
        genetic_probality = sys.argv[genetic_probality_index + 1]
        genetic_probality = float(genetic_probality)
    except:
        genetic_probality = 0.2

    data = []
    with open (f'./n100_m200_l15_a4/{inst}.txt',"r") as input:
        for line in input:
            line =line.replace("\n","")
            data.append(line)
    best_consensus, best_distance, best_time = simulated(data, initial_temperature, cooling_rate, max_time,genetic_probality)
    print(f'{best_distance}')