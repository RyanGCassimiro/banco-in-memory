def MERGE_SORT(lista):
    if len(lista) <= 1:
        return lista
    
    #Determina onde fica o meio da lista
    meio = len(lista) // 2
    
    #Divide a lista em duas, e usa o merge sort recursivamente para organizar
    #cada metade
    esquerda = MERGE_SORT(lista[0:meio])
    direita = MERGE_SORT(lista[meio:])

    #Reúne e retorna as duas metades organizadas no final
    return MERGE(esquerda, direita)

def MERGE(esquerda, direita):
    #Armazenará o resultado final da organização
    resultado = []
    #Índices denotando esquerda e direita, respectivamente
    i = j = 0

    #Organiza as duas lista
    while i < len(esquerda) and j < len(direita):
        if esquerda[i]["key"] < direita[j]["key"]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    #Reúne as listas em uma só
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])

    #retorna a lista organizada
    return resultado

