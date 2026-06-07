# Análise de Complexidade — Banco de Dados In-Memory NoSQL

Documento técnico referente ao **Projeto 3 — Engine de Banco de Dados In-Memory (NoSQL)**, desenvolvido para a disciplina de Estruturas de Dados / Algoritmos.

O objetivo deste documento é justificar as complexidades teóricas das estruturas e algoritmos implementados, além de registrar os resultados reais de validação e prova de carga executados no projeto.

---

## 1. Complexidades Teóricas

| Operação | Estrutura/Algoritmo | Complexidade | Observação |
|---|---|---|---|
| `INSERT` | Red-Black Tree | O(log N) | Inclui rotações e recoloração no `fix_insert` |
| `SEARCH` | Red-Black Tree | O(log N) | Busca pela chave na árvore balanceada |
| `DELETE` | Red-Black Tree | O(log N) | Inclui `fix_delete`, rotações e recoloração |
| `RANGE` | In-order podado | O(log N + K) | K = número de itens retornados |
| `BACKUP_MERGE` | MergeSort | O(M log M) | M = total de registros consolidados |

---

## 2. Justificativa das Complexidades

### 2.1 `INSERT`, `SEARCH` e `DELETE` — O(log N)

A **Red-Black Tree** é uma árvore binária de busca balanceada. Ela mantém o balanceamento por meio de regras de cor, rotações e recoloração dos nós.

Uma propriedade importante da Red-Black Tree é que sua altura máxima é limitada por:

```txt
2 · log2(N + 1)
```

Assim, mesmo no pior caso, a árvore não cresce de forma linear como poderia acontecer em uma árvore binária de busca simples desbalanceada.

As operações `INSERT`, `SEARCH` e `DELETE` percorrem, no máximo, a altura da árvore. Como essa altura é logarítmica em relação ao número de elementos armazenados, essas operações possuem complexidade:

```txt
O(log N)
```

No caso do `INSERT`, após a inserção inicial, pode ser necessário executar `fix_insert`, com rotações e recoloração. No caso do `DELETE`, pode ser necessário executar `fix_delete`, também com rotações e recoloração. Essas correções percorrem, no pior caso, a altura da árvore, mantendo a complexidade O(log N).

---

### 2.2 `RANGE [min, max]` — O(log N + K)

A operação `RANGE` responde consultas do tipo:

```txt
RANGE [min] [max]
```

Para isso, o sistema utiliza **caminhamento em ordem com poda**.

O caminhamento em ordem garante que os resultados sejam retornados em ordem crescente de chave. A poda evita percorrer subárvores que estão completamente fora do intervalo solicitado.

A complexidade é:

```txt
O(log N + K)
```

Onde:

- `N` é a quantidade total de elementos armazenados na árvore;
- `K` é a quantidade de registros retornados dentro do intervalo.

O termo `K` é inevitável, pois todos os registros encontrados precisam ser visitados e escritos na saída. Portanto, quando os intervalos consultados retornam muitos elementos, o tempo e o tamanho do arquivo de saída crescem proporcionalmente ao número de itens retornados.

---

### 2.3 `BACKUP_MERGE` — O(M log M)

A consolidação dos dados de backup utiliza **MergeSort** implementado manualmente em:

```txt
src/algorithms/merge_sort.py
```

O MergeSort divide a lista de registros recursivamente ao meio e depois mescla as partes ordenadas.

Para `M` registros totais, considerando os dados de backup e os dados exportados da memória:

- a profundidade da recursão é `log2(M)`;
- cada nível da recursão processa `M` elementos durante as mesclagens.

Assim, a complexidade final do algoritmo é:

```txt
O(M log M)
```

---

## 3. Ambiente de Execução

As complexidades teóricas apresentadas neste documento **não dependem do hardware** utilizado, pois representam o comportamento assintótico dos algoritmos.

Entretanto, os tempos empíricos medidos na prova de carga podem variar conforme processador, memória RAM, sistema operacional, versão do Python e carga atual da máquina.

| Item | Informação |
|---|---|
| Equipamento | MacBook Pro |
| Processador | Apple Silicon M4 |
| Arquitetura | arm64 |
| Memória RAM | 32 GB |
| Sistema operacional | macOS / Darwin |
| Python | 3.13.1 |

O hardware foi registrado apenas como contexto para interpretação dos tempos medidos. Ele não altera as complexidades O(log N), O(log N + K) e O(M log M).

---

## 4. Validação Automatizada com Pytest

Comando executado:

```bash
python3 -m pytest -q
```

Resultado obtido:

```txt
......................................................................                                        [100%]
70 passed in 18.70s
```

Esse resultado confirma que os testes automatizados do projeto foram executados com sucesso, incluindo testes unitários e/ou de integração.

---

## 5. Prova de Carga via CLI

O teste de estresse foi executado usando o script padrão do projeto:

```bash
time ./run.sh data/input_estresse.json data/saida_estresse.json
```

Resultado obtido:

```txt
./run.sh data/input_estresse.json data/saida_estresse.json  13.76s user 0.30s system 99% cpu 14.082 total
```

| Métrica | Resultado |
|---|---:|
| Total de operações | 105.000 |
| `INSERTs` | 100.000 |
| `RANGEs` | 5.000 |
| Tempo de usuário | 13.76s |
| Tempo de sistema | 0.30s |
| Uso de CPU | 99% |
| Tempo total real | 14.082s |

O teste completo foi executado via CLI, incluindo:

1. leitura do arquivo `input_estresse.json`;
2. processamento das operações;
3. execução das inserções na Red-Black Tree;
4. execução das consultas `RANGE`;
5. geração do arquivo `saida_estresse.json`.

A execução foi concluída sem travamento e sem estouro de memória.

---

## 6. Tamanho dos Arquivos de Estresse

Comando executado:

```bash
ls -lh data/input_estresse.json data/saida_estresse.json
```

Resultado obtido:

```txt
-rw-r--r--@ 1 wanessacosta  staff   7.8M Jun  7 21:59 data/input_estresse.json
-rw-r--r--@ 1 wanessacosta  staff   562M Jun  7 22:17 data/saida_estresse.json
```

| Arquivo | Tamanho |
|---|---:|
| `data/input_estresse.json` | 7.8 MB |
| `data/saida_estresse.json` | 562 MB |

A saída do teste de estresse ficou significativamente maior que a entrada porque cada operação `RANGE` pode retornar múltiplos registros.

Esse comportamento confirma, na prática, o impacto do fator `K` na complexidade:

```txt
O(log N + K)
```

Mesmo que a busca inicial na árvore seja logarítmica, todos os `K` elementos encontrados precisam ser percorridos e escritos no arquivo de saída.

---

## 7. Observação sobre Versionamento

O arquivo:

```txt
data/saida_estresse.json
```

foi gerado localmente durante a prova de carga, mas não deve ser versionado no Git devido ao seu tamanho elevado.

Ele serve como evidência local de execução, mas não precisa ser incluído no repositório final como arquivo de saída gerado.

Recomenda-se manter no `.gitignore`:

```gitignore
data/saida_*.json
```

Observação: arquivos de gabarito exigidos para correção, como `output_esperado_basico.json`, `output_esperado_avancado.json` ou `output_esperado_estresse.json`, não devem ser ignorados caso façam parte da entrega definida pela equipe/professor.

---

## 8. Relação entre Teoria e Resultado Prático

Os resultados obtidos são coerentes com as complexidades esperadas.

| Operação | Complexidade teórica | Observação prática |
|---|---|---|
| `INSERT` | O(log N) | Suportou 100.000 inserções no cenário de estresse |
| `SEARCH` | O(log N) | Busca eficiente pela chave na árvore balanceada |
| `DELETE` | O(log N) | Mantém a árvore balanceada após remoções |
| `RANGE` | O(log N + K) | O tamanho da saída demonstra o impacto direto do número de itens retornados |
| `BACKUP_MERGE` | O(M log M) | MergeSort implementado manualmente para consolidação de registros |

A prova de carga executada contém 100.000 operações `INSERT` e 5.000 operações `RANGE`. O sistema processou todas as 105.000 operações em 14.082 segundos via CLI, incluindo leitura do arquivo de entrada, execução das operações e geração da saída.

O arquivo `saida_estresse.json` atingiu 562 MB porque as consultas `RANGE` retornaram muitos registros. Esse resultado reforça que o crescimento do tempo de execução não depende apenas da quantidade de operações, mas também da quantidade de registros retornados por cada consulta de intervalo.

Assim, o comportamento observado está alinhado com a análise teórica: a Red-Black Tree garante operações principais em O(log N), enquanto o `RANGE` apresenta custo O(log N + K), sendo `K` o número de registros retornados.

---

## 9. Conclusão

A implementação atende às exigências do **Projeto 3 — Engine de Banco de Dados In-Memory NoSQL**.

As operações principais de armazenamento, busca e remoção utilizam **Red-Black Tree implementada manualmente**, garantindo complexidade O(log N). A operação `RANGE` utiliza caminhamento em ordem com poda, atingindo O(log N + K). A consolidação de backups utiliza **MergeSort manual**, com complexidade O(M log M).

Além disso, o sistema foi validado com **70 testes automatizados** e executou com sucesso o cenário de estresse exigido, contendo:

- 100.000 inserções;
- 5.000 consultas `RANGE`;
- 105.000 operações no total;
- tempo total real de 14.082 segundos via CLI.

A implementação não utiliza bibliotecas externas para árvore balanceada, ordenação ou mecanismos centrais de busca, respeitando a exigência de implementação manual das estruturas de dados e algoritmos principais.