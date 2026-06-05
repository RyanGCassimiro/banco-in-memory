from ..core.node import Node, make_nil, BLACK, RED

def RANGE(no: Node, min, max, resultado):
    if no.isBlack() and no.value == None and no.key == None:
        return
    
    if no.key > min:
        RANGE(no.left, min, max, resultado)
    
    if min <= no.key <= max:
        resultado.append({"key": no.key, "value": no.value})

    if no.key < max:
        RANGE(no.right, min, max, resultado)