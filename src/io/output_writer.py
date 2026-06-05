from __future__ import annotations
import json
import sys
from typing import Any


def write_output(path: str, results: list[dict[str, Any]]) -> None:
    """Escreve o arquivo output.json de forma determinística."""
    output = {"results": results}
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
            f.write("\n")
    except OSError as e:
        print(f"Erro ao escrever '{path}': {e}", file=sys.stderr)
        sys.exit(1)
