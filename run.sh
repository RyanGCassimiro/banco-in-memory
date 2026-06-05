#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <input.json> <output.json>" >&2
    exit 1
fi

python -m src.main "$1" "$2"
