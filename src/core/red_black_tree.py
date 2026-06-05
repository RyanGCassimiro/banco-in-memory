from __future__ import annotations
from typing import Any, Generator

from .node import Node, make_nil, RED, BLACK


class RedBlackTree:
    """
    Árvore Red-Black com INSERT, SEARCH, DELETE e caminhamento em-ordem.

    Complexidade:
        INSERT, SEARCH, DELETE: O(log N)
        Caminhamento em-ordem:  O(N)
        RANGE podado:           O(log N + K)
    """

    def __init__(self) -> None:
        self.NIL: Node = make_nil()
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.NIL.parent = self.NIL
        self.root: Node = self.NIL
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def _rotate_left(self, x: Node) -> None:
        """
        Rotação à esquerda em torno de x.

        Antes:          Depois:
            x               y
           / \\             / \\
          A   y           x   C
             / \\         / \\
            B   C       A   B
        """
        y = x.right
        x.right = y.left

        if y.left is not self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is self.NIL:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _rotate_right(self, y: Node) -> None:
        """
        Rotação à direita em torno de y.

        Antes:          Depois:
            y               x
           / \\             / \\
          x   C           A   y
         / \\                 / \\
        A   B               B   C
        """
        x = y.left
        y.left = x.right

        if x.right is not self.NIL:
            x.right.parent = y

        x.parent = y.parent

        if y.parent is self.NIL:
            self.root = x
        elif y is y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    def insert(self, key: int, value: Any) -> str:
        """
        Insere ou atualiza a chave.

        Retorna:
            "OK"      -- chave nova inserida com sucesso
            "UPDATED" -- chave já existia; valor foi atualizado
        """
        # Busca o nó existente para tratar chave repetida
        existing = self._search_node(key)
        if existing is not self.NIL:
            existing.value = value
            return "UPDATED"

        # Cria o novo nó como RED
        new_node = Node(
            key=key,
            value=value,
            color=RED,
            left=self.NIL,
            right=self.NIL,
            parent=self.NIL,
        )

        # Inserção BST padrão
        parent: Node = self.NIL
        current: Node = self.root

        while current is not self.NIL:
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is self.NIL:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._size += 1
        self._fix_insert(new_node)
        return "OK"

    def _fix_insert(self, z: Node) -> None:
        """
        Restaura as propriedades Red-Black após inserção.

        Enquanto o pai de z for RED (violação da propriedade 4),
        analisa o tio de z e aplica recoloração ou rotações.
        """
        while z.parent.is_red():
            if z.parent is z.parent.parent.left:
                # Pai é filho ESQUERDO do avô
                uncle = z.parent.parent.right

                if uncle.is_red():
                    # Caso 1: tio vermelho → recoloração sobe o problema
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        # Caso 2: z é filho direito → rotação esquerda prepara caso 3
                        z = z.parent
                        self._rotate_left(z)
                    # Caso 3: z é filho esquerdo → rotação direita no avô
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._rotate_right(z.parent.parent)
            else:
                # Pai é filho DIREITO do avô — espelho dos casos acima
                uncle = z.parent.parent.left

                if uncle.is_red():
                    # Caso 1 espelho
                    z.parent.color = BLACK
                    uncle.color = BLACK
                    z.parent.parent.color = RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        # Caso 2 espelho
                        z = z.parent
                        self._rotate_right(z)
                    # Caso 3 espelho
                    z.parent.color = BLACK
                    z.parent.parent.color = RED
                    self._rotate_left(z.parent.parent)

        self.root.color = BLACK           # Propriedade 2: raiz sempre BLACK

    # ------------------------------------------------------------------
    # SEARCH — O(log N)
    # ------------------------------------------------------------------

    def search(self, key: int) -> tuple[bool, Any]:
        """
        Busca uma chave.

        Retorna:
            (True,  value) -- chave encontrada
            (False, None)  -- chave não existe
        """
        node = self._search_node(key)
        if node is self.NIL:
            return False, None
        return True, node.value

    def _search_node(self, key: int) -> Node:
        """Retorna o nó com a chave, ou NIL se não encontrado."""
        current = self.root
        while current is not self.NIL:
            if key == current.key:
                return current
            current = current.left if key < current.key else current.right
        return self.NIL

    # ------------------------------------------------------------------
    # DELETE — O(log N)
    # ------------------------------------------------------------------

    def delete(self, key: int) -> str:
        """
        Remove a chave da árvore.

        Retorna:
            "OK"        -- chave removida
            "NOT_FOUND" -- chave não existia
        """
        node = self._search_node(key)
        if node is self.NIL:
            return "NOT_FOUND"

        self._delete_node(node)
        self._size -= 1
        return "OK"

    def _delete_node(self, z: Node) -> None:
        """
        Remove o nó z aplicando a lógica BST + fix_delete quando necessário.

        Variáveis seguem a nomenclatura do CLRS (Cormen et al.):
            y  -- nó que será fisicamente removido ou movido
            x  -- nó que ocupa o lugar de y após a remoção
            y_original_color -- cor de y antes de qualquer alteração
        """
        y = z
        y_original_color = y.color

        if z.left is self.NIL:
            # z tem no máximo filho direito
            x = z.right
            self._transplant(z, z.right)

        elif z.right is self.NIL:
            # z tem apenas filho esquerdo
            x = z.left
            self._transplant(z, z.left)

        else:
            # z tem dois filhos → substitui pelo sucessor in-order (mínimo da subárvore direita)
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent is z:
                # y é filho direto de z
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color          # y herda a cor de z

        if y_original_color == BLACK:
            # Remoção de nó BLACK pode violar a propriedade 5
            self._fix_delete(x)

    def _transplant(self, u: Node, v: Node) -> None:
        """
        Substitui a subárvore enraizada em u pela subárvore enraizada em v.
        Não atualiza v.left, v.right — isso fica a cargo do chamador.
        """
        if u.parent is self.NIL:
            self.root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _fix_delete(self, x: Node) -> None:
        """
        Restaura as propriedades Red-Black após remoção de nó BLACK.

        x carrega um "crédito" BLACK extra que precisa ser redistribuído.
        Quatro casos (mais seus espelhos) resolvem o problema por
        recoloração e rotações.
        """
        while x is not self.root and x.is_black():
            if x is x.parent.left:
                w = x.parent.right          # irmão de x

                if w.is_red():
                    # Caso 1: irmão vermelho → rotação converte para caso 2/3/4
                    w.color = BLACK
                    x.parent.color = RED
                    self._rotate_left(x.parent)
                    w = x.parent.right

                if w.left.is_black() and w.right.is_black():
                    # Caso 2: irmão e seus filhos são BLACK → recoloração sobe o problema
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.is_black():
                        # Caso 3: filho direito do irmão é BLACK → rotação prepara caso 4
                        w.left.color = BLACK
                        w.color = RED
                        self._rotate_right(w)
                        w = x.parent.right

                    # Caso 4: filho direito do irmão é RED → rotação resolve definitivamente
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self._rotate_left(x.parent)
                    x = self.root           # encerra o loop
            else:
                # Espelho: x é filho DIREITO
                w = x.parent.left

                if w.is_red():
                    # Caso 1 espelho
                    w.color = BLACK
                    x.parent.color = RED
                    self._rotate_right(x.parent)
                    w = x.parent.left

                if w.right.is_black() and w.left.is_black():
                    # Caso 2 espelho
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.is_black():
                        # Caso 3 espelho
                        w.right.color = BLACK
                        w.color = RED
                        self._rotate_left(w)
                        w = x.parent.left

                    # Caso 4 espelho
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self._rotate_right(x.parent)
                    x = self.root

        x.color = BLACK                     # garante que x (ou raiz) seja BLACK

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------

    def _minimum(self, node: Node) -> Node:
        """Retorna o nó com menor chave na subárvore enraizada em node."""
        while node.left is not self.NIL:
            node = node.left
        return node

    # ------------------------------------------------------------------
    # Caminhamento em-ordem — base para RANGE e dump de backup
    # ------------------------------------------------------------------

    def inorder(self) -> Generator[tuple[int, Any], None, None]:
        """
        Gera todos os pares (key, value) em ordem crescente de chave.
        Usado pelo BACKUP_MERGE para exportar a memória ordenada.

        Complexidade: O(N)
        """
        yield from self._inorder_recursive(self.root)

    def _inorder_recursive(
        self, node: Node
    ) -> Generator[tuple[int, Any], None, None]:
        if node is self.NIL:
            return
        yield from self._inorder_recursive(node.left)
        yield (node.key, node.value)
        yield from self._inorder_recursive(node.right)

    def range_query(
        self, min_key: int, max_key: int
    ) -> list[dict[str, Any]]:
        """
        Retorna todos os pares cuja chave está em [min_key, max_key],
        em ordem crescente.

        Usa caminhamento em-ordem PODADO: subárvores fora do intervalo
        não são visitadas.

        Complexidade: O(log N + K), onde K = número de itens retornados.
        """
        result: list[dict[str, Any]] = []
        if min_key > max_key:
            return result
        self._range_recursive(self.root, min_key, max_key, result)
        return result

    def _range_recursive(
        self,
        node: Node,
        min_key: int,
        max_key: int,
        result: list[dict[str, Any]],
    ) -> None:
        if node is self.NIL:
            return
        # Poda esquerda: só visita se puder haver chaves >= min_key
        if node.key > min_key:
            self._range_recursive(node.left, min_key, max_key, result)
        # Visita o nó atual se estiver no intervalo
        if min_key <= node.key <= max_key:
            result.append({"key": node.key, "value": node.value})
        # Poda direita: só visita se puder haver chaves <= max_key
        if node.key < max_key:
            self._range_recursive(node.right, min_key, max_key, result)