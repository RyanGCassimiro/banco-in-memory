from __future__ import annotations
import sys

from .io.input_parse import load_input
from .io.output_writer import write_output
from .core.database import Database
from .operations.executor import execute_all


def main() -> None:
    if len(sys.argv) != 3:
        print("Uso: python -m src.main <input.json> <output.json>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    operations = load_input(input_path)
    db = Database()
    results = execute_all(operations, db)
    write_output(output_path, results)


if __name__ == "__main__":
    main()
