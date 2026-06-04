#To do: Importar a classe do nó assim que este estiver pronto

def RANGE(no, min, max, resultado):
    if no == None:
        return
    
    if no.key > min:
        RANGE(no.left, min, max, resultado)
    
    if min <= no.key <= max:
        resultado.append({"key": no.key, "value": no.value})

    if no.key < max:
        RANGE(no.right, min, max, resultado)