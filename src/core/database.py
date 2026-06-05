from __future__ import annotations
from typing import Any

from .red_black_tree import RedBlackTree

class Database:
    """
    Engine de banco de dados in-memory NoSQL.

    Encapsula a Red-Black Tree e expõe operações no formato de dicionário
    pronto para serialização em JSON pelo output_writer.

    Cada método retorna um dict com pelo menos a chave "op", seguindo
    o contrato definido em output.json.
    """

    def __init__(self) -> None:
        self._tree: RedBlackTree = RedBlackTree()

    # ------------------------------------------------------------------
    # INSERT — O(log N)
    # ------------------------------------------------------------------

    def insert(self, key: int, value: Any) -> dict[str, Any]:
        """
        Insere ou atualiza um par chave-valor.

        Retorna:
            { "op": "INSERT", "key": <key>, "status": "OK" }
            { "op": "INSERT", "key": <key>, "status": "UPDATED" }
        """
        status = self._tree.insert(key, value)
        return {"op": "INSERT", "key": key, "status": status}

    # ------------------------------------------------------------------
    # SEARCH — O(log N)
    # ------------------------------------------------------------------

    def search(self, key: int) -> dict[str, Any]:
        """
        Busca uma chave.

        Retorna:
            { "op": "SEARCH", "key": <key>, "found": True,  "value": <value> }
            { "op": "SEARCH", "key": <key>, "found": False }
        """
        found, value = self._tree.search(key)
        result: dict[str, Any] = {"op": "SEARCH", "key": key, "found": found}
        if found:
            result["value"] = value
        return result

    # ------------------------------------------------------------------
    # DELETE — O(log N)
    # ------------------------------------------------------------------

    def delete(self, key: int) -> dict[str, Any]:
        """
        Remove uma chave.

        Retorna:
            { "op": "DELETE", "key": <key>, "status": "OK" }
            { "op": "DELETE", "key": <key>, "status": "NOT_FOUND" }
        """
        status = self._tree.delete(key)
        return {"op": "DELETE", "key": key, "status": status}

    # ------------------------------------------------------------------
    # RANGE — O(log N + K)
    # ------------------------------------------------------------------

    def range_query(self, min_key: int, max_key: int) -> dict[str, Any]:
        """
        Retorna todos os pares com chave em [min_key, max_key], ordenados.

        Casos especiais tratados:
            - min > max  → result vazio (sem erro)
            - nenhum item no intervalo → result vazio

        Retorna:
            {
                "op": "RANGE",
                "min": <min_key>,
                "max": <max_key>,
                "result": [ { "key": k, "value": v }, ... ]
            }
        """
        items = self._tree.range_query(min_key, max_key)
        return {
            "op": "RANGE",
            "min": min_key,
            "max": max_key,
            "result": items,
        }

    # ------------------------------------------------------------------
    # DUMP ordenado — usado pelo BACKUP_MERGE (Gustavo)
    # ------------------------------------------------------------------

    def dump_inorder(self) -> list[dict[str, Any]]:
        """
        Exporta todos os registros em memória ordenados por chave.

        Retorna lista de dicts { "key": k, "value": v }.
        Usado por backup_merge.py para consolidar memória + arquivos.

        Complexidade: O(N)
        """
        return [{"key": k, "value": v} for k, v in self._tree.inorder()]

    # ------------------------------------------------------------------
    # Utilitários
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        """Número de registros atualmente em memória."""
        return len(self._tree)

    def __repr__(self) -> str:
        return f"Database(records={len(self)})"