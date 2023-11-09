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


def aleatory_population(population_size,sequence_length):
    population=[]
    for _ in range(population_size):
        solution = ''.join(random.choice('ACGT') for _ in range(sequence_length))
        population.append(solution)
    return population

def tournament(population,fitness_values,tournament_size):
    selected_parents = []
    while len(selected_parents) < 2:
        tournament = random.sample(range(len(population)), tournament_size)        
        best_individual = min(tournament, key=lambda i: fitness_values[i])
        selected_parents.append(population[best_individual])
    return selected_parents

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

def genetic(data, population_size,tournament_size,mutation_rate, elite_percentage):

    adn_len = len(data[0])

    # Inicialización de la población aleatoria
    population = aleatory_population(population_size, adn_len)
    best_solution = None

    start_time = time.time()
    best_time = None
    
    while time.time() - start_time <= maxTime: 

        # Evaluación de la población
        fitness_values = [objective_function(consensus, data) for consensus in population]

        # Encuentra la mejor solución en la generación actual
        current_best_index = fitness_values.index(min(fitness_values))
        current_best_solution = population[current_best_index]

        # Encuentra los mejores individuos (élites)
        elite_count = int(elite_percentage * population_size)
        elite_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i])[:elite_count]
        elites = [population[i] for i in elite_indices]

        # Actualiza la mejor solución global
        if best_solution is None or fitness_values[current_best_index] < objective_function(best_solution, data):
            best_solution = current_best_solution
            best_time=time.time()-start_time
            print (best_solution)
        # Realiza torneos para seleccionar individuos para reemplazo(padres) y saca genera los decendientes
        
        candidates_for_replacement = []
        descendants = []
        while len(candidates_for_replacement) < population_size - elite_count:
            parents = tournament(population, fitness_values, tournament_size)
            parent1,parent2=parents
            descendants.append(parents)
            # Recombinación 
            child1,child2 = crossover(parent1, parent2)
            # Mutación 
            mutacion1=mutate(child1,mutation_rate)
            mutaion2=mutate(child2,mutation_rate)
            descendants.extend([mutacion1, mutaion2])
    
        # Reemplazo (implementar)

        new_population = elites + descendants
        population = new_population

        return best_solution,best_time



if __name__ == "__main__":
    
    # Verifica si se proporciona al menos un argumento
    if len(sys.argv) < 7:
        print("Por favor, proporciona este tipo de entrada --> ´python3 genetic.py -i instanciaProblema -t tiempoMaximoSegundos -p populationSize´ .")
        exit()
    elif len(sys.argv) == 8:
        # El segundo argumento (sys.argv[1]) es el nombre del archivo con la entrada
        # El tercer argumento (sys.argv[2]) es el nivel de determinismo
        iIndex = sys.argv.index('-i')
        inst = sys.argv[iIndex + 1]
        tIndex = sys.argv.index('-t')
        maxTime = sys.argv[tIndex + 1]
        maxTime = float(maxTime)
        pIndex = sys.argv.index('-p')
        population_size = sys.argv[pIndex + 1]
        population_size = int(population_size)

    else:
        iIndex = sys.argv.index('-i')
        inst = sys.argv[iIndex + 1]
        tIndex = sys.argv.index('-t')
        maxTime = sys.argv[tIndex + 1]
        maxTime = float(maxTime)
        pIndex = sys.argv.index('-p')
        population_size = sys.argv[pIndex + 1]
        population_size = int(population_size)


    with open ('../n100_m200_l15_a4/'+inst+'.txt',"r") as input:
        data = []
        for line in input:
            line =line.replace("\n","")
            data.append(line)

    # Datos iniciales Tal vez pedirlos como parametros
    data_tam=len(data)
    adn_len=len(data[1])
    tournament_size=100
    mutation_rate=0.4
    elite_percentage=0.3
    result=genetic(data, population_size,tournament_size,mutation_rate, elite_percentage)
    print(result)
    


