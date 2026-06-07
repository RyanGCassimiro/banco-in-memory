# Arquitetura — Banco de Dados In-Memory NoSQL

## Visão Geral

O sistema é uma engine de banco de dados in-memory que armazena pares chave-valor em uma Árvore Red-Black e suporta buscas por intervalo e consolidação de backups via MergeSort.

```
src/
├── main.py                  # Ponto de entrada CLI
├── core/
│   ├── node.py              # Nó da árvore (key, value, color, parent, left, right)
│   ├── red_black_tree.py    # Árvore Red-Black (INSERT, SEARCH, DELETE, RANGE)
│   └── database.py          # Fachada da engine — expõe operações no formato JSON
├── algorithms/
│   └── merge_sort.py        # MergeSort manual para consolidação de backups
├── operations/
│   ├── executor.py          # Despacha cada operação do input para o módulo correto
│   └── backup_merge.py      # Lê arquivos de backup, mescla com memória via MergeSort
└── io/
    ├── input_parse.py       # Lê e valida o input.json
    └── output_writer.py     # Serializa os resultados em output.json
```

## Fluxo de Execução

```
input.json
    └─► input_parse.py      (valida e desserializa)
            └─► executor.py  (itera operações)
                    ├─► database.py → red_black_tree.py   (INSERT/SEARCH/DELETE/RANGE)
                    └─► backup_merge.py → merge_sort.py   (BACKUP_MERGE)
                    
Após o processamento de todas as operações:
    └─► output_writer.py    (serializa saída)
            └─► output.json
```

## Estrutura de Dados Principal — Árvore Red-Black

A Árvore Red-Black é uma BST com as propriedades:
1. Todo nó é RED ou BLACK.
2. A raiz é BLACK.
3. Toda folha (NIL sentinela) é BLACK.
4. Filhos de nó RED são BLACK.
5. Todo caminho raiz→folha tem o mesmo número de nós BLACK (black-height).

Essas propriedades garantem altura máxima `2 · log₂(N+1)`, o que limita INSERT, SEARCH e DELETE a O(log N) no pior caso.

### Nó Sentinela (NIL)

Em vez de usar `None`, a árvore usa um único objeto `NIL` compartilhado como folha. Isso simplifica as rotações e o `fix_delete`, eliminando verificações de nulo espalhadas pelo código.

## Algoritmo de Consolidação — MergeSort

O `BACKUP_MERGE` lê N arquivos de backup (formato NDJSON) e os mescla com os registros em memória. A lista unificada é ordenada por chave com MergeSort (O(M log M)) e duplicatas são resolvidas mantendo o registro mais recente (última ocorrência por chave).
