from __future__ import annotations
import json
import sys
from typing import Any

VALID_OPS = {"INSERT", "SEARCH", "DELETE", "RANGE", "BACKUP_MERGE"}


def load_input(path: str) -> list[dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{path}' não encontrado.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file '{path}': {e}", file=sys.stderr)
        sys.exit(1)
    
    if not isinstance(data, dict) or "operations" not in data:
        print(f"Erro: input deve ser um objeto JSON com chave 'operations'.", file=sys.stderr)
        sys.exit(1)
    
    ops = data["operations"]
    if not isinstance(ops, list):
        print(f"Erro: 'operations' deve ser uma lista.", file=sys.stderr)
        sys.exit(1)
    
    try:
        _validate_operations(ops)
    except ValueError as e:
        print(f"Erro de validação: {e}", file=sys.stderr)
        sys.exit(1)
    
    return ops 

def _validate_operations(ops: list[dict]) -> None:
    for i, op in enumerate(ops):
        if not isinstance(op, dict):
            raise ValueError(f"Operação no índice {i} não é um objeto JSON.")

        name = op.get("op")
        if name not in VALID_OPS:
            raise ValueError(f"Operação desconhecida: '{name}' (índice {i}).")

        if name in ("INSERT", "SEARCH", "DELETE") and "key" not in op:
            raise ValueError(f"Operação {name} (índice {i}) sem campo 'key'.")

        if name == "INSERT" and "value" not in op:
            raise ValueError(f"INSERT (índice {i}) sem campo 'value'.")

        if name == "RANGE" and ("min" not in op or "max" not in op):
            raise ValueError(f"RANGE (índice {i}) sem 'min' ou 'max'.")

        if name == "BACKUP_MERGE" and ("files" not in op or "output" not in op):
            raise ValueError(f"BACKUP_MERGE (índice {i}) sem 'files' ou 'output'.")