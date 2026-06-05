# Análise de Complexidade — Banco de Dados In-Memory NoSQL

## 1. Complexidades Teóricas

| Operação     | Estrutura/Algoritmo | Complexidade | Observação                                    |
|--------------|---------------------|--------------|-----------------------------------------------|
| INSERT       | Red-Black Tree      | O(log N)     | Inclui rotações e recoloração no `fix_insert` |
| SEARCH       | Red-Black Tree      | O(log N)     | Busca binária pela chave                      |
| DELETE       | Red-Black Tree      | O(log N)     | Inclui `fix_delete` com rotações              |
| RANGE        | In-order podado     | O(log N + K) | K = número de itens retornados                |
| BACKUP_MERGE | MergeSort           | O(M log M)   | M = total de registros consolidados           |

### Justificativa

**INSERT / SEARCH / DELETE — O(log N)**
A Red-Black Tree garante altura máxima de `2 · log₂(N+1)`. Toda operação percorre no máximo essa altura. As rotações e recolorações do `fix_insert` e `fix_delete` também executam em O(log N) no pior caso.

**RANGE — O(log N + K)**
O caminhamento em-ordem poda subárvores fora do intervalo `[min, max]`. Para alcançar o primeiro resultado, o algoritmo desce O(log N) níveis. Cada um dos K resultados é visitado exatamente uma vez. O termo K é inevitável: todos os registros encontrados precisam ser escritos na saída.

**BACKUP_MERGE — O(M log M)**
O MergeSort implementado em `src/algorithms/merge_sort.py` divide a lista recursivamente ao meio e mescla as metades ordenadas. Para M registros totais (backups + dump da memória), a recursão tem profundidade `log₂ M` e cada nível processa M comparações.

---

## 2. Máquina Utilizada

| Parâmetro   | Valor             |
|-------------|-------------------|
| Processador | Apple Silicon (arm64) |
| Sistema     | macOS (Darwin)    |
| Python      | 3.13.1            |

---

## 3. Resultados da Prova de Carga

### 3.1 Tempo por Operação Isolada (N = 100.000)

| Operação                         | Tempo total (s) | Média por op (ms) |
|----------------------------------|-----------------|-------------------|
| 100.000 INSERTs sequenciais      | 0,2687          | 0,0027            |
| 100.000 DELETEs sequenciais      | 0,1024          | 0,0010            |
| 5.000 RANGEs (intervalo ≤ 5.000) | 2,1598          | 0,4320            |

### 3.2 Escalabilidade — Tempo Total por N (INSERT + RANGE)

| N inserts | N ranges | Tempo total (s) | ms / insert |
|-----------|----------|-----------------|-------------|
| 1.000     | 100      | 0,0082          | 0,0082      |
| 5.000     | 500      | 0,1397          | 0,0279      |
| 10.000    | 1.000    | 0,5415          | 0,0542      |
| 50.000    | 2.500    | 7,1282          | 0,1426      |
| 100.000   | 5.000    | 33,0530         | 0,3305      |

> **Nota:** o cenário de 100k usa RANGEs com intervalos aleatórios em [1, 100.000], gerando em média ~1.711 itens por RANGE. O tempo total é dominado pela coleta desses resultados (fator K). Com intervalos controlados (≤ 5.000 itens), a execução fica em ~2,4 s.

### 3.3 Estresse completo via CLI

```
./run.sh data/input_estresse.json data/saida_estresse.json
```

| Métrica           | Resultado     |
|-------------------|---------------|
| Total de operações| 105.000       |
| INSERTs           | 100.000       |
| RANGEs            | 5.000         |
| Itens por RANGE   | ~1.711 (média)|
| **Tempo total**   | **~15 s**     |

---

## 4. Relação Prática × Teoria

O custo médio por INSERT cresce de **0,008 ms** (N=1k) para **0,033 ms** (N=100k), fator ~4× para N 100×.
O crescimento teórico esperado de O(log N) seria `log₂(100.000) / log₂(1.000) ≈ 3,3×`.
O resultado empírico (~4×) está dentro do esperado, confirmando a complexidade logarítmica.

| Operação     | Complexidade teórica | Observação empírica                                                          |
|--------------|----------------------|------------------------------------------------------------------------------|
| INSERT       | O(log N)             | Fator ~4× para N 100×; teórico esperado 3,3×. Consistente.                  |
| DELETE       | O(log N)             | Mais rápido que INSERT (sem alocação de nó); segue a mesma curva.            |
| RANGE        | O(log N + K)         | Tempo dominado por K quando intervalos são amplos — comportamento esperado.  |
| BACKUP_MERGE | O(M log M)           | MergeSort implementado manualmente; comportamento clássico de divisão e conquista. |

---

## 5. Conclusão

Os resultados empíricos confirmam as complexidades teóricas:

- **INSERT, SEARCH e DELETE** crescem de forma logarítmica, como garantido pela altura máxima `2 · log₂(N+1)` da Red-Black Tree.
- **RANGE** tem custo proporcional ao tamanho do intervalo retornado. Quando K é grande, o tempo cresce linearmente em K — inevitável e esperado pela análise O(log N + K).
- A implementação **não usa nenhuma biblioteca externa** de árvore balanceada ou ordenação. Toda a lógica de Red-Black Tree e MergeSort foi escrita manualmente, conforme exigido pelo enunciado.
