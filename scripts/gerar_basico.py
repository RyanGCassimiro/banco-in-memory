from json import dump
from random import randint

print("Gerando o input_basico.json...")
operations = []

for i in range(50):
    operations.append({ "op": "INSERT", "key": i, "value": str(i)})

for i in range(10):
    operations.append({"op": "SEARCH", "key": i})

for i in range(10):
    a = randint(1, 50)
    b = randint(1, 50)
    operations.append({"op": "RANGE", "min": min(a,b), "max": max(a,b)})

for i in range(20):
    operations.append({ "op": "DELETE", "key": i})

#TO DO: criar os arquivos de backup para teste 
operations.append({"op": "BACKUP_MERGE", "files": ["data/backups_basico/backup_dia_1.json", "data/backups_basico/backup_dia_2.json"], "output": "data/backups_basico/backup_consolidado.json"})

with open(r'../data/input_basico.json', 'w', encoding="utf-8") as file:
    dump({"operations":operations}, file, ensure_ascii=False, indent=2)

print("Inputs criados com sucesso! Bom teste! :)")
