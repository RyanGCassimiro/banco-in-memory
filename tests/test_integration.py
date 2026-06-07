from pathlib import Path
from src.io.input_parse import load_input
from src.io.output_writer import write_output
from src.core.database import Database
from src.operations.executor import execute_all
import json

DATA = Path(__file__).parent.parent / "data"


def _rodar(input_file, output_file):
    operations = load_input(str(DATA / input_file))
    db = Database()
    results = execute_all(operations, db)
    write_output(str(DATA / output_file), results)
    with open(DATA / output_file, encoding="utf-8") as f:
        return json.load(f)


def _carregar_esperado(filename):
    with open(DATA / filename, encoding="utf-8") as f:
        return json.load(f)


#Teste 1: input básico
def teste_basico():
    output_gerado = _rodar("input_basico.json", "output_basico.json")
    output_esperado = _carregar_esperado("output_esperado_basico.json")
    assert output_gerado == output_esperado


#Teste 2: input avançado
def teste_avancado():
    output_gerado = _rodar("input_avancado.json", "output_avancado.json")
    output_esperado = _carregar_esperado("output_esperado_avancado.json")
    assert output_gerado == output_esperado


#Teste 3: input de estresse
def teste_estresse():
    output_gerado = _rodar("input_estresse.json", "output_estresse.json")
    output_esperado = _carregar_esperado("output_esperado_estresse.json")
    assert output_gerado == output_esperado
