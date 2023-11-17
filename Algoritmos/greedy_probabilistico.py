import random
import time
import sys

# Verifica si se proporciona al menos un argumento
if len(sys.argv) < 2:
    print("Por favor, proporciona el numero de la entrada y recuerde que puede colocar el nivel de determinismo como 2do argumento.")
    exit()
else:
    # El segundo argumento (sys.argv[1]) numero de la instancia
    # El tercer argumento (sys.argv[2]) es el nivel de determinismo
    inst = sys.argv[1]    

    if len(sys.argv) > 2:
        n_determinist = float(sys.argv[2])
    else:
        n_determinist = 0.9 # Valor predeterminado



with open ('../n100_m200_l15_a4/'+str(inst)+".txt","r") as input:
    data = []
    for line in input:
        line =line.replace("\n","")
        data.append(line)

dict = [] 
ans = ''

start_time = time.time()

for i in range(len(data[0])): ## i desde 0 a len de cada linea en data, en este caso 15
    dict.append({'A': 0, 'C': 0, 'T': 0, 'G': 0}) ## Dentro de la lista dict genera un mapa con { , , }
    for line in data: ## Dentro de cada linea de data
        dict[i][line[i]] += 1  ## dentro de cada dict (15 dict en este caso)[line[i] igual va desde cada letra dentro de una linea aumentado esa letra en la dict] 
    numero_aleatorio = random.random()
    max_val = max(dict[i].values())


    candidates_max = []
    candidates_aleatorios = []
    for protein in dict[i]:
        if dict[i][protein] == max_val:
            candidates_max.append(protein)
        else:
            candidates_aleatorios.append(protein)
            

    if numero_aleatorio > n_determinist and len(candidates_aleatorios)!=0:
        selected = random.randint(0, len(candidates_aleatorios) - 1)
        ans += candidates_aleatorios[selected]
    else:
        selected = random.randint(0, len(candidates_max) - 1)
        ans += candidates_max[selected]

end_time = time.time()

total_time=end_time-start_time

distance=0

for line in data:
    different_letter=0
    for i in range(len(line)):
        if ans[i]!=line[i]:
            different_letter+=1
        
    distance+=different_letter**2

print("Concenso: "+ans+", Tiempo: "+ str(total_time)+" seg"+", Distancia: "+str(distance))
