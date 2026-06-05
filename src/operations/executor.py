from __future__ import annotations
from typing import Any

from ..core.database import Database
from ..operations.backup_merge import BACKUP_MERGE


def execute_all(operations: list[dict[str, Any]], db: Database) -> list[dict[str, Any]]:
    """Executa todas as operações do input em sequência e retorna a lista de resultados."""
    return [_dispatch(op, db) for op in operations]


def _dispatch(op: dict[str, Any], db: Database) -> dict[str, Any]:
    name = op["op"]

    if name == "INSERT":
        return db.insert(op["key"], op["value"])

    if name == "SEARCH":
        return db.search(op["key"])

    if name == "DELETE":
        return db.delete(op["key"])

    if name == "RANGE":
        min_k = op["min"]
        max_k = op["max"]
        if min_k is None or max_k is None:
            return {"op": "RANGE", "min": min_k, "max": max_k, "result": []}
        return db.range_query(min_k, max_k)

    if name == "BACKUP_MERGE":
        memory_records = db.dump_inorder()
        result = BACKUP_MERGE(op["files"], op["output"], memory_records)
        result["op"] = "BACKUP_MERGE"
        return result

    return {"op": name, "status": "UNKNOWN_OP"}
