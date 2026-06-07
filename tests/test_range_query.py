"""
tests/test_range_query.py

Testa a operação RANGE da engine in-memory.
Cobre: range completo, range vazio, item único, fora dos limites,
ordenação crescente, min > max, e valores JSON complexos.
"""

import pytest
from src.core.database import Database


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture
def db_populado():
    """
    Banco com 7 chaves fixas para todos os testes de range.

        10 → "Alice"
        20 → "Bob"
        30 → "Carol"
        40 → "Dave"
        50 → "Eve"
        60 → "Frank"
        70 → "Grace"
    """
    db = Database()
    for key, name in [(10, "Alice"), (20, "Bob"), (30, "Carol"),
                      (40, "Dave"), (50, "Eve"), (60, "Frank"), (70, "Grace")]:
        db.insert(key, name)
    return db


@pytest.fixture
def db_vazio():
    return Database()


# ------------------------------------------------------------------
# 1. Range completo — retorna todos os itens
# ------------------------------------------------------------------

def test_range_retorna_todos_quando_intervalo_cobre_tudo(db_populado):
    resultado = db_populado.range_query(10, 70)
    chaves = [item["key"] for item in resultado["result"]]
    assert chaves == [10, 20, 30, 40, 50, 60, 70]


# ------------------------------------------------------------------
# 2. Range parcial — subconjunto do meio
# ------------------------------------------------------------------

def test_range_parcial_retorna_subconjunto_correto(db_populado):
    resultado = db_populado.range_query(25, 55)
    chaves = [item["key"] for item in resultado["result"]]
    assert chaves == [30, 40, 50]


# ------------------------------------------------------------------
# 3. Range com item único
# ------------------------------------------------------------------

def test_range_retorna_exatamente_um_item(db_populado):
    resultado = db_populado.range_query(40, 40)
    assert len(resultado["result"]) == 1
    assert resultado["result"][0]["key"] == 40
    assert resultado["result"][0]["value"] == "Dave"


# ------------------------------------------------------------------
# 4. Range vazio — intervalo válido mas sem chaves dentro
# ------------------------------------------------------------------

def test_range_vazio_entre_chaves_existentes(db_populado):
    # Não há chaves entre 21 e 29
    resultado = db_populado.range_query(21, 29)
    assert resultado["result"] == []


def test_range_vazio_acima_de_todas_as_chaves(db_populado):
    resultado = db_populado.range_query(80, 100)
    assert resultado["result"] == []


def test_range_vazio_abaixo_de_todas_as_chaves(db_populado):
    resultado = db_populado.range_query(1, 9)
    assert resultado["result"] == []


# ------------------------------------------------------------------
# 5. Range em banco vazio
# ------------------------------------------------------------------

def test_range_em_banco_vazio_retorna_lista_vazia(db_vazio):
    resultado = db_vazio.range_query(0, 100)
    assert resultado["result"] == []


# ------------------------------------------------------------------
# 6. min > max — deve retornar vazio sem lançar exceção
# ------------------------------------------------------------------

def test_range_min_maior_que_max_retorna_vazio(db_populado):
    resultado = db_populado.range_query(60, 20)
    assert resultado["result"] == []


# ------------------------------------------------------------------
# 7. Ordenação crescente — resultado sempre ordenado por chave
# ------------------------------------------------------------------

def test_range_resultado_sempre_ordenado_crescente(db_populado):
    resultado = db_populado.range_query(10, 70)
    chaves = [item["key"] for item in resultado["result"]]
    assert chaves == sorted(chaves)


def test_range_ordenado_apos_insercoes_fora_de_ordem():
    """Insere chaves fora de ordem e verifica ordenação no RANGE."""
    db = Database()
    for key in [50, 10, 90, 30, 70]:
        db.insert(key, f"val_{key}")
    resultado = db.range_query(10, 90)
    chaves = [item["key"] for item in resultado["result"]]
    assert chaves == [10, 30, 50, 70, 90]


# ------------------------------------------------------------------
# 8. Formato do resultado — contrato do output.json
# ------------------------------------------------------------------

def test_range_formato_da_resposta(db_populado):
    resultado = db_populado.range_query(20, 40)
    assert resultado["op"] == "RANGE"
    assert resultado["min"] == 20
    assert resultado["max"] == 40
    assert isinstance(resultado["result"], list)
    for item in resultado["result"]:
        assert "key" in item
        assert "value" in item


# ------------------------------------------------------------------
# 9. Valores JSON complexos — value pode ser dict
# ------------------------------------------------------------------

def test_range_com_valores_json_complexos():
    db = Database()
    db.insert(10, {"nome": "Alice", "score": 95})
    db.insert(20, {"nome": "Bob",   "score": 80})
    db.insert(30, {"nome": "Carol", "score": 70})

    resultado = db.range_query(10, 25)
    assert len(resultado["result"]) == 2
    assert resultado["result"][0]["value"]["nome"] == "Alice"
    assert resultado["result"][1]["value"]["nome"] == "Bob"


# ------------------------------------------------------------------
# 10. Range nas bordas exatas das chaves
# ------------------------------------------------------------------

def test_range_inclui_bordas_min_e_max(db_populado):
    resultado = db_populado.range_query(10, 70)
    chaves = [item["key"] for item in resultado["result"]]
    assert 10 in chaves
    assert 70 in chaves


def test_range_exclui_elementos_fora_das_bordas(db_populado):
    resultado = db_populado.range_query(20, 60)
    chaves = [item["key"] for item in resultado["result"]]
    assert 10 not in chaves
    assert 70 not in chaves


# ------------------------------------------------------------------
# 11. Range após DELETE — chave removida não aparece no resultado
# ------------------------------------------------------------------

def test_range_nao_retorna_chave_deletada(db_populado):
    db_populado.delete(30)
    resultado = db_populado.range_query(20, 40)
    chaves = [item["key"] for item in resultado["result"]]
    assert 30 not in chaves
    assert chaves == [20, 40]


# ------------------------------------------------------------------
# 12. Range com chave única na árvore
# ------------------------------------------------------------------

def test_range_com_apenas_uma_chave_na_arvore():
    db = Database()
    db.insert(42, "único")

    # Intervalo que inclui a chave
    resultado = db.range_query(40, 50)
    assert len(resultado["result"]) == 1
    assert resultado["result"][0]["key"] == 42

    # Intervalo que não inclui a chave
    resultado = db.range_query(0, 41)
    assert resultado["result"] == []