import json
from ..algorithms.merge_sort import merge_sort as MERGE_SORT
from ..core.database import Database

def BACKUP_MERGE(files, output, memory_records):
    registros = []
    
    for arquivo in files:
        registros += ler_registros_do_backup(arquivo)
    
    registros += memory_records
    ordenados = MERGE_SORT(registros)
    consolidados = resolver_duplicatas(ordenados)
    salvar_json(output, consolidados)

    return({ "status": "OK", "records": len(consolidados), "output": output})


#Função auxiliar para o BACKUP_MERGE
def ler_registros_do_backup(arquivo):
    registros_backup = []
    with open(arquivo, 'r') as f:
        for linha in f:
            registros_backup.append(json.loads(linha))

    return registros_backup

#Função para salvar no JSON
def salvar_json(output, lista):
    with open(output, 'w') as file:
        for i in lista:
            json.dump(i, file)
            file.write('\n')

#Função auxiliar para resolver duplicatas
def resolver_duplicatas(lista):
    lista_resolvida = list({ each["key"] : each for each in lista}.values())
    return lista_resolvida
