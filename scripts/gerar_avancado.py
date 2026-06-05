from json import dump
from random import randint

print("Gerando input_avancado.json...")
operations = []

#Operações normais de insert
for i in range(10):
    operations.append({"op": "INSERT", "key": i, "value": str(i)})

#Caso 1: operações com chaves duplicadas
for i in range(10):
    operations.append({"op": "INSERT", "key": 16, "value":"16"})

#Caso 2: deletes inexistentes
for i in range(10):
    operations.append({"op": "DELETE", "key": (i + 17)})

#Caso 3: range vazio
for i in range(10):
    operations.append({"op": "RANGE", "min":None, "max":None})

#Caso 4: range invertido
for i in range(10):
    a = randint(1, 10)
    b = randint(1, 10)
    operations.append({"op": "RANGE", "min": max(a,b), "max": min(a,b)})

#Caso 5: backups com duplicata
#TO DO: Criar aquivos de backup para teste
operations.append({"op": "BACKUP_MERGE", "files": ["data/backup_dia_1.json", "data/backup_dia_2.json"], "output": "data/backup_consolidado.json"})

with open(r'../data/input_avancado.json', 'w', encoding="utf-8") as file:
    dump({"operations": operations}, file, ensure_ascii=False, indent=2)

print("Inputs criados com sucesso! Bom teste! :)")
