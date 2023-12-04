import random
import time
import sys

def objective_function(consensus, data):
    distance=0
    for line in data:
        different_letter=0
        for i in range(len(line)):
            if consensus[i]!=line[i]:
                different_letter+=1
            
        distance+=different_letter**2
    return distance

def aleatory_population(population_size,sequence_length):
    population=[]
    for i in range(population_size):
        solution = ''.join(random.choice('ACGT') for j in range(sequence_length))
        population.append(solution)
    return population

def mutate(consensus, mutation_rate):
    mutated_position = random.randint(0, len(consensus) - 1)
    if random.random() < mutation_rate:
        consensus = consensus[:mutated_position] + random.choice('ACGT') + consensus[mutated_position + 1:]
    return consensus

def crossover(parent1, parent2):
    # Elije un punto de corte aleatorio
    point = random.randint(0, len(parent1))

    # Crea dos descendientes combinando las partes de los padres
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2

def genetic(data, max_time, population_size, mutation_rate, elite_percentage):

    adn_len = len(data[0])

    best_time = 0

    # Inicializacion de la población aleatoria
    population = aleatory_population(population_size, adn_len)

    # Evaluacion de la poblacion
    fitness_values = [objective_function(consensus, data) for consensus in population]

    # Encuentra la mejor solución en la primera generacion
    current_best_index = fitness_values.index(min(fitness_values))
    current_best_solution = population[current_best_index]

    best_solution = current_best_solution
    best_fitness = fitness_values[current_best_index]

    start_time = time.time()
    while time.time() - start_time <= max_time:
        # Encuentra los mejores individuos (élites)
        elite_count = int(elite_percentage * population_size)
        elite_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i])[:elite_count]
        elite = [population[i] for i in elite_indices]

        # Obtener el resto de la población
        non_elite = list(filter(lambda i: i not in elite_indices, range(population_size)))
        rest_of_population = [population[i] for i in non_elite]

        # Realiza torneos para seleccionar individuos para reemplazo(padres) y saca genera los decendientes
        descendants = []
    
        # Cruzamos a la elite
        while len(elite) > 1:
            # Seleccionamos padres aleatorios de la elite
            parent1_index = random.randint(0, len(elite) - 1)
            parent2_index = random.randint(0, len(elite) - 1)
            while parent2_index == parent1_index:
                parent2_index = random.randint(0, len(elite) - 1)

            # Cruza
            child1,child2 = crossover(elite[parent1_index], elite[parent2_index])
            descendants.extend([child1, child2])

            elite.pop(parent1_index)
            if parent1_index < parent2_index:
                elite.pop(parent2_index - 1)
            else:
                elite.pop(parent2_index)

        if len(elite) > 0:
            rest_of_population += elite

        # Mutamos poblacion no elite para reciclar en siguiente generacion
        for i in range(len(rest_of_population)):
            mutate(rest_of_population[i], mutation_rate)

        # Generamos nueva generacion
        new_population = descendants + rest_of_population

        # Evaluacion de la nueva poblacion
        fitness_values = [objective_function(consensus, data) for consensus in new_population]

        # Encuentra la mejor solución en actual
        current_best_index = fitness_values.index(min(fitness_values))
        current_best_solution = new_population[current_best_index]

        # Actualiza la mejor solucion global
        if fitness_values[current_best_index] < objective_function(best_solution, data):
            best_time += (time.time() - start_time)
            best_solution = current_best_solution
            best_fitness = fitness_values[current_best_index]

        # Actualiza la nueva generacion
        population = new_population
    
    return best_solution, best_fitness, best_time


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
        population_size_index = sys.argv.index('-p')
        population_size = sys.argv[population_size_index + 1]
        population_size = int(population_size)
    except:
        population_size = int(30)

    try:
        mutation_rate_index = sys.argv.index('-m')
        mutation_rate = sys.argv[mutation_rate_index + 1]
        mutation_rate = float(mutation_rate)
    except:
        mutation_rate = 0.5

    try:
        elite_percentage_index = sys.argv.index('-e')
        elite_percentage = sys.argv[elite_percentage_index + 1]
        elite_percentage = float(elite_percentage)
    except:
        elite_percentage = 0.2
    
    with open('resultados_200_15.txt', 'w') as output:
        tiempo_promedio = 0
        fitness_promedio = 0
        for inst in range(100):
            data = []
            with open (f'../instancias1/inst_200_15_4_{inst}.txt',"r") as input:
                for line in input:
                    line =line.replace("\n","")
                    data.append(line)

            # Datos iniciales Tal vez pedirlos como parametros
            best_solution, best_fitness, best_time = genetic(data, max_time, population_size, mutation_rate, elite_percentage)
            tiempo_promedio += best_time
            fitness_promedio += best_fitness
            output.write(f'{inst} 200 15 {best_fitness}\n')
        
        tiempo_promedio /= 100
        fitness_promedio /= 100
        output.write(f'promedio 200 15 {fitness_promedio} {tiempo_promedio} s\n')