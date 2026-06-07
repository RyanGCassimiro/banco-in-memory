"""
tests/test_merge_sort.py

Testa o MergeSort implementado em src/algorithms/merge_sort.py.
Cobre: ordenação básica, lista vazia, lista com um elemento,
lista já ordenada, duplicatas, estabilidade, e listas grandes.
"""

import pytest
from src.algorithms.merge_sort import merge_sort


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def registros(*chaves) -> list[dict]:
    """Cria lista de registros { key, value } a partir de chaves."""
    return [{"key": k, "value": f"val_{k}"} for k in chaves]


def chaves(lista: list[dict]) -> list[int]:
    """Extrai só as chaves de uma lista de registros."""
    return [item["key"] for item in lista]


# ------------------------------------------------------------------
# 1. Casos básicos de ordenação
# ------------------------------------------------------------------

def test_ordena_lista_simples():
    entrada = registros(30, 10, 20)
    resultado = merge_sort(entrada)
    assert chaves(resultado) == [10, 20, 30]


def test_ordena_lista_invertida():
    entrada = registros(50, 40, 30, 20, 10)
    resultado = merge_sort(entrada)
    assert chaves(resultado) == [10, 20, 30, 40, 50]


def test_ordena_lista_fora_de_ordem_aleatoria():
    entrada = registros(7, 2, 9, 1, 5, 3, 8, 4, 6)
    resultado = merge_sort(entrada)
    assert chaves(resultado) == [1, 2, 3, 4, 5, 6, 7, 8, 9]


# ------------------------------------------------------------------
# 2. Casos extremos de tamanho
# ------------------------------------------------------------------

def test_lista_vazia_retorna_lista_vazia():
    assert merge_sort([]) == []


def test_lista_com_um_elemento_retorna_ela_mesma():
    entrada = registros(42)
    resultado = merge_sort(entrada)
    assert chaves(resultado) == [42]


def test_lista_com_dois_elementos_ordenados():
    entrada = registros(5, 3)
    resultado = merge_sort(entrada)
    assert chaves(resultado) == [3, 5]


# ------------------------------------------------------------------
# 3. Lista já ordenada — não deve alterar a ordem
# ------------------------------------------------------------------

def test_lista_ja_ordenada_permanece_igual():
    entrada = registros(10, 20, 30, 40, 50)
    resultado = merge_sort(entrada)
    assert chaves(resultado) == [10, 20, 30, 40, 50]


# ------------------------------------------------------------------
# 4. Duplicatas — comportamento determinístico
# ------------------------------------------------------------------

def test_duplicatas_sao_mantidas_na_saida():
    """Backup pode ter chaves repetidas; todas devem aparecer após sort."""
    entrada = [
        {"key": 20, "value": "antigo"},
        {"key": 10, "value": "val_10"},
        {"key": 20, "value": "novo"},
    ]
    resultado = merge_sort(entrada)
    assert chaves(resultado) == [10, 20, 20]


def test_todas_as_chaves_identicas():
    entrada = [{"key": 5, "value": f"v{i}"} for i in range(5)]
    resultado = merge_sort(entrada)
    assert all(item["key"] == 5 for item in resultado)
    assert len(resultado) == 5


# ------------------------------------------------------------------
# 5. Estabilidade — registros com mesma chave mantêm ordem relativa
# ------------------------------------------------------------------

def test_merge_sort_é_estavel():
    """
    Dois registros com key=30: o que veio primeiro na entrada
    deve aparecer primeiro na saída (estabilidade).
    """
    entrada = [
        {"key": 30, "value": "primeiro"},
        {"key": 10, "value": "val_10"},
        {"key": 30, "value": "segundo"},
    ]
    resultado = merge_sort(entrada)
    itens_key30 = [r for r in resultado if r["key"] == 30]
    assert itens_key30[0]["value"] == "primeiro"
    assert itens_key30[1]["value"] == "segundo"


# ------------------------------------------------------------------
# 6. Não modifica a lista original
# ------------------------------------------------------------------

def test_nao_modifica_lista_original():
    entrada = registros(30, 10, 20)
    copia = [dict(r) for r in entrada]
    merge_sort(entrada)
    assert chaves(entrada) == chaves(copia)


# ------------------------------------------------------------------
# 7. Valores JSON complexos — value pode ser dict
# ------------------------------------------------------------------

def test_ordena_registros_com_value_dict():
    entrada = [
        {"key": 30, "value": {"nome": "Carol", "score": 70}},
        {"key": 10, "value": {"nome": "Alice", "score": 95}},
        {"key": 20, "value": {"nome": "Bob",   "score": 80}},
    ]
    resultado = merge_sort(entrada)
    assert chaves(resultado) == [10, 20, 30]
    assert resultado[0]["value"]["nome"] == "Alice"


# ------------------------------------------------------------------
# 8. Lista grande — prova de consistência
# ------------------------------------------------------------------

def test_ordena_lista_grande():
    import random
    random.seed(42)
    n = 10_000
    chaves_aleatorias = random.sample(range(n * 10), n)
    entrada = [{"key": k, "value": f"v_{k}"} for k in chaves_aleatorias]
    resultado = merge_sort(entrada)

    resultado_chaves = chaves(resultado)
    assert resultado_chaves == sorted(resultado_chaves)
    assert len(resultado) == n


def test_ordena_lista_grande_com_duplicatas():
    import random
    random.seed(7)
    n = 5_000
    # Chaves repetidas propositalmente (range menor que n)
    chaves_entrada = [random.randint(0, 1000) for _ in range(n)]
    entrada = [{"key": k, "value": f"v_{i}"} for i, k in enumerate(chaves_entrada)]
    resultado = merge_sort(entrada)

    resultado_chaves = chaves(resultado)
    assert resultado_chaves == sorted(resultado_chaves)
    assert len(resultado) == n


# ------------------------------------------------------------------
# 9. Chaves negativas e zero
# ------------------------------------------------------------------

def test_ordena_com_chaves_negativas():
    entrada = registros(0, -10, 5, -20, 15)
    resultado = merge_sort(entrada)
    assert chaves(resultado) == [-20, -10, 0, 5, 15]


def test_lista_com_apenas_zero():
    entrada = registros(0)
    resultado = merge_sort(entrada)
    assert chaves(resultado) == [0]