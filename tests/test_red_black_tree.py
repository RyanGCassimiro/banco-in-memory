import pytest
from src.core.red_black_tree import RedBlackTree
from src.core.node import BLACK, RED


# Helpers para verificar as propriedades Red-Black

def _black_height(tree: RedBlackTree, node) -> int:
    """Retorna a black-height a partir de node, ou -1 se inconsistente."""
    if node is tree.NIL:
        return 1  # NIL conta como preto

    bh_left = _black_height(tree, node.left)
    bh_right = _black_height(tree, node.right)

    if bh_left == -1 or bh_right == -1 or bh_left != bh_right:
        return -1

    return bh_left + (1 if node.color == BLACK else 0)


def _has_red_red(tree: RedBlackTree, node) -> bool:
    """Retorna True se existe nó vermelho com filho vermelho."""
    if node is tree.NIL:
        return False
    if node.is_red() and (node.left.is_red() or node.right.is_red()):
        return True
    return _has_red_red(tree, node.left) or _has_red_red(tree, node.right)


def assert_rbt_properties(tree: RedBlackTree) -> None:
    """Verifica as 5 propriedades obrigatórias da Red-Black Tree."""
    # Propriedade 2: raiz é preta
    if tree.root is not tree.NIL:
        assert tree.root.color == BLACK, "Raiz deve ser BLACK"

    # Propriedade 4: nenhum nó vermelho tem filho vermelho
    assert not _has_red_red(tree, tree.root), "Violação RED-RED encontrada"

    # Propriedade 5: black-height uniforme em todos os caminhos
    bh = _black_height(tree, tree.root)
    assert bh != -1, "Black-height inconsistente entre caminhos"


# INSERT

class TestInsert:
    def test_raiz_preta_apos_insercao(self):
        tree = RedBlackTree()
        tree.insert(10, "a")
        assert tree.root.color == BLACK

    def test_retorna_ok_para_chave_nova(self):
        tree = RedBlackTree()
        assert tree.insert(10, "a") == "OK"

    def test_retorna_updated_para_chave_duplicada(self):
        tree = RedBlackTree()
        tree.insert(10, "a")
        assert tree.insert(10, "b") == "UPDATED"

    def test_duplicata_atualiza_valor(self):
        tree = RedBlackTree()
        tree.insert(10, "original")
        tree.insert(10, "atualizado")
        found, val = tree.search(10)
        assert found and val == "atualizado"

    def test_tamanho_cresce_com_insercoes(self):
        tree = RedBlackTree()
        for i in range(10):
            tree.insert(i, str(i))
        assert len(tree) == 10

    def test_duplicata_nao_altera_tamanho(self):
        tree = RedBlackTree()
        tree.insert(5, "a")
        tree.insert(5, "b")
        assert len(tree) == 1

    def test_propriedades_apos_insercoes_sequenciais(self):
        tree = RedBlackTree()
        for i in range(50):
            tree.insert(i, i)
        assert_rbt_properties(tree)

    def test_propriedades_apos_insercoes_inversas(self):
        tree = RedBlackTree()
        for i in range(49, -1, -1):
            tree.insert(i, i)
        assert_rbt_properties(tree)

    def test_propriedades_apos_insercoes_aleatorias(self):
        tree = RedBlackTree()
        for k in [3, 7, 1, 9, 5, 2, 8, 4, 6, 0]:
            tree.insert(k, str(k))
        assert_rbt_properties(tree)

    def test_propriedades_apos_mil_insercoes(self):
        tree = RedBlackTree()
        for i in range(1000):
            tree.insert(i, i)
        assert_rbt_properties(tree)


# SEARCH

class TestSearch:
    def test_busca_chave_existente(self):
        tree = RedBlackTree()
        tree.insert(42, "hello")
        found, val = tree.search(42)
        assert found is True
        assert val == "hello"

    def test_busca_chave_inexistente_retorna_false(self):
        tree = RedBlackTree()
        tree.insert(10, "a")
        found, val = tree.search(99)
        assert found is False
        assert val is None

    def test_busca_em_arvore_vazia(self):
        tree = RedBlackTree()
        found, val = tree.search(1)
        assert found is False
        assert val is None

    def test_busca_todos_apos_multiplas_insercoes(self):
        tree = RedBlackTree()
        data = {i: f"val_{i}" for i in range(20)}
        for k, v in data.items():
            tree.insert(k, v)
        for k, v in data.items():
            found, val = tree.search(k)
            assert found is True
            assert val == v

    def test_busca_valor_json(self):
        tree = RedBlackTree()
        tree.insert(1, {"nome": "Alice", "score": 91})
        found, val = tree.search(1)
        assert found is True
        assert val == {"nome": "Alice", "score": 91}


# DELETE


class TestDelete:
    def test_delete_existente_retorna_ok(self):
        tree = RedBlackTree()
        tree.insert(10, "a")
        assert tree.delete(10) == "OK"

    def test_delete_inexistente_retorna_not_found(self):
        tree = RedBlackTree()
        tree.insert(10, "a")
        assert tree.delete(99) == "NOT_FOUND"

    def test_delete_reduz_tamanho(self):
        tree = RedBlackTree()
        tree.insert(10, "a")
        tree.insert(20, "b")
        tree.delete(10)
        assert len(tree) == 1

    def test_search_apos_delete_retorna_false(self):
        tree = RedBlackTree()
        tree.insert(10, "a")
        tree.delete(10)
        found, _ = tree.search(10)
        assert found is False

    def test_propriedades_apos_deletes(self):
        tree = RedBlackTree()
        for i in range(20):
            tree.insert(i, i)
        for i in range(0, 20, 2):
            tree.delete(i)
        assert_rbt_properties(tree)

    def test_delete_todos_nos(self):
        tree = RedBlackTree()
        for i in range(10):
            tree.insert(i, i)
        for i in range(10):
            tree.delete(i)
        assert len(tree) == 0
        assert tree.root is tree.NIL

    def test_propriedades_apos_operacoes_mistas(self):
        tree = RedBlackTree()
        for i in range(100):
            tree.insert(i, i)
        for i in range(0, 100, 3):
            tree.delete(i)
        assert_rbt_properties(tree)

    def test_delete_inexistente_nao_altera_tamanho(self):
        tree = RedBlackTree()
        tree.insert(5, "a")
        tree.delete(999)
        assert len(tree) == 1

    def test_delete_no_com_dois_filhos(self):
        tree = RedBlackTree()
        for k in [10, 5, 15, 3, 7, 12, 20]:
            tree.insert(k, str(k))
        tree.delete(10)
        assert_rbt_properties(tree)
        found, _ = tree.search(10)
        assert found is False

    def test_delete_raiz(self):
        tree = RedBlackTree()
        tree.insert(10, "a")
        tree.delete(10)
        assert tree.root is tree.NIL


# RANGE

class TestRangeQuery:
    def test_range_basico(self):
        tree = RedBlackTree()
        for i in [10, 20, 30, 40, 50]:
            tree.insert(i, str(i))
        result = tree.range_query(15, 45)
        assert [r["key"] for r in result] == [20, 30, 40]

    def test_range_vazio_min_maior_que_max(self):
        tree = RedBlackTree()
        tree.insert(10, "a")
        assert tree.range_query(50, 10) == []

    def test_range_sem_resultados(self):
        tree = RedBlackTree()
        for i in [10, 20, 30]:
            tree.insert(i, str(i))
        assert tree.range_query(40, 60) == []

    def test_range_inclui_limites(self):
        tree = RedBlackTree()
        for i in [10, 20, 30]:
            tree.insert(i, str(i))
        result = tree.range_query(10, 30)
        assert [r["key"] for r in result] == [10, 20, 30]

    def test_range_um_unico_item(self):
        tree = RedBlackTree()
        tree.insert(15, "unico")
        result = tree.range_query(10, 20)
        assert len(result) == 1
        assert result[0]["key"] == 15

    def test_range_retorna_ordenado_crescente(self):
        tree = RedBlackTree()
        for k in [5, 1, 3, 7, 9, 2, 8]:
            tree.insert(k, str(k))
        result = tree.range_query(1, 9)
        keys = [r["key"] for r in result]
        assert keys == sorted(keys)

    def test_range_arvore_vazia(self):
        tree = RedBlackTree()
        assert tree.range_query(0, 100) == []

    def test_range_min_igual_max(self):
        tree = RedBlackTree()
        tree.insert(5, "cinco")
        result = tree.range_query(5, 5)
        assert len(result) == 1
        assert result[0]["key"] == 5

    def test_range_min_igual_max_sem_resultado(self):
        tree = RedBlackTree()
        tree.insert(5, "cinco")
        assert tree.range_query(6, 6) == []

    def test_range_conteudo_correto(self):
        tree = RedBlackTree()
        tree.insert(10, "dez")
        tree.insert(20, "vinte")
        tree.insert(30, "trinta")
        result = tree.range_query(10, 20)
        assert result == [{"key": 10, "value": "dez"}, {"key": 20, "value": "vinte"}]
