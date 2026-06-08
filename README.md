# Banco de Dados In-Memory NoSQL

Projeto 3 — Engine de Banco de Dados In-Memory com Árvore Red-Black e MergeSort.

## Membros

- Wanessa Costa
- Ryan G. Cassimiro
- Gustavo Lima (Guga-of-Sosaria)

## Como executar

**Pré-requisito:** Python 3.10+

```bash
./run.sh data/input_basico.json output.json
./run.sh data/input_avancado.json output.json
./run.sh data/input_estresse.json output.json
```

Ou diretamente via Python:

```bash
python -m src.main <input.json> <output.json>
```

## Gerar os dados de teste

```bash
cd scripts
python3 gerar_basico.py
python3 gerar_avancado.py
python3 gerar_estresse.py
```

Os arquivos são gerados em `data/`.

## Estruturas implementadas

- **Árvore Red-Black** (`src/core/red_black_tree.py`): estrutura primária. INSERT, SEARCH e DELETE em O(log N) no pior caso, com balanceamento automático via rotações e recoloração.
- **MergeSort** (`src/algorithms/merge_sort.py`): ordenação estável em O(N log N) usada na consolidação de backups diários.
- **RANGE com caminhamento em-ordem podado** (`src/core/red_black_tree.py`): responde a intervalos `[min, max]` em O(log N + K), sem visitar subárvores fora do intervalo.

## Operações suportadas

| Operação | Descrição | Complexidade |
|---|---|---|
| `INSERT` | Insere ou atualiza chave-valor | O(log N) |
| `SEARCH` | Busca por chave | O(log N) |
| `DELETE` | Remove chave | O(log N) |
| `RANGE` | Retorna todos os pares em [min, max] | O(log N + K) |
| `BACKUP_MERGE` | Consolida arquivos de backup com MergeSort | O(M log M) |

## Documentação técnica

Ver [`docs/COMPLEXIDADE.md`](docs/COMPLEXIDADE.md) para análise de complexidade teórica e prova de carga empírica com 100.000 operações.