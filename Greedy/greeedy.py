import random

with open ('../n100_m200_l15_a4/inst_200_15_4_0.txt',"r") as input:
    data = []
    for line in input:
        line =line.replace("\n","")
        data.append(line)

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

print(ans) 
