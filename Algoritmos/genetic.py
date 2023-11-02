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
    for _ in range(population_size):
        solution = ''.join(random.choice('ACGT') for _ in range(sequence_length))
        population_size.append(solution)
    return population_size

def tournament(population,fitness_values,tournament_size):
    selected_parents = []
    while len(selected_parents) < 2:
        tournament = random.sample(range(len(population)), tournament_size)        
        best_individual = min(tournament, key=lambda i: fitness_values[i])
        selected_parents.append(population[best_individual])
    return selected_parents

def genetic(population_initial,data, population_size,tournament_size,  sequence_length, max_generations):

    population = population_initial
    best_solution = None

    for generation in range(max_generations):
        # Evaluación de la población
        fitness_values = [objective_function(consensus, data) for consensus in population]

        # Encuentra la mejor solución en la generación actual
        current_best_index = fitness_values.index(min(fitness_values))
        current_best_solution = population[current_best_index]

        # Actualiza la mejor solución global
        if best_solution is None or fitness_values[current_best_index] < objective_function(best_solution, data):
            best_solution = current_best_solution
        
        # Seleccion
        parents=tournament(population,fitness_values,tournament_size)
        # Recombinacion
        # Mutacion
        # Remplazo
        # Repeticion



if __name__ == "__main__":
    
    # Verifica si se proporciona al menos un argumento
    if len(sys.argv) < 5:
        print("Por favor, proporciona este tipo de entrada --> ´python3 genetic.py -i instanciaProblema -t tiempoMaximoSegundos´ .")
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
        

    with open ('../n100_m200_l15_a4/inst_'+inst+'.txt',"r") as input:
        data = []
        for line in input:
            line =line.replace("\n","")
            data.append(line)

    # Datos iniciales Tal vez pedirlos como parametros
    data_tam=len(data)
    adn_len=len(data[1])
    population_size=data_tam/3
    print(str(data_tam)+ " " +str(adn_len))
    initial_population=aleatory_population(population_size,adn_len)
    max_generations = 100
    


