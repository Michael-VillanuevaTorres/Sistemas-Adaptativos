import random

with open ('../n100_m200_l15_a4/inst_200_15_4_0.txt',"r") as input:
    data = []
    for line in input:
        line =line.replace("\n","")
        data.append(line)

dict = []
ans = ''

for i in range(len(data[0])):
    dict.append({'A': 0, 'C': 0, 'T': 0, 'G': 0})
    for line in data:
        dict[i][line[i]] += 1
    max_val = max(dict[i].values())
    candidates = []
    for protein in dict[i]:
        if dict[i][protein] == max_val:
            candidates.append(protein)
    selected = random.randint(0, len(candidates) - 1)
    ans += candidates[selected]

print(ans)