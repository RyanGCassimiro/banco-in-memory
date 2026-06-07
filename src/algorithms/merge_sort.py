def merge_sort(lista):
    if len(lista) <= 1:
        return lista

    # Determina onde fica o meio da lista
    meio = len(lista) // 2

    # Divide a lista em duas e usa o merge sort recursivamente para organizar cada metade
    esquerda = merge_sort(lista[0:meio])
    direita = merge_sort(lista[meio:])

    # Reúne e retorna as duas metades organizadas
    return _merge(esquerda, direita)


def _merge(esquerda, direita):
    # Armazenará o resultado final da organização
    resultado = []

    # Índices denotando esquerda e direita, respectivamente
    i = j = 0

    # Organiza as duas listas
    # <= em vez de < garante estabilidade: chaves iguais mantêm ordem de chegada
    while i < len(esquerda) and j < len(direita):
        if esquerda[i]["key"] <= direita[j]["key"]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    # Reúne as listas em uma só
    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])

    # Retorna a lista organizada
    return resultado