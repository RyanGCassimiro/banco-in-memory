# Divisão de Tarefas — Banco de Dados In-Memory NoSQL

**Disciplina:** Estruturas de Dados e Algoritmos
**Prazo:** 09/06/2026 às 23:59
**Valor:** 80 pontos
**Repositório:** https://github.com/RyanGCassimiro/banco-in-memory

---

## Equipe

| Integrante | Responsabilidade principal |
|------------|--------------------------|
| Ryan | Estrutura de dados core (Red-Black Tree) |
| Wanessa | I/O, pipeline de execução e documentação |
| Gustavo | Algoritmos, operações avançadas e testes |

---

## Tarefas por Integrante

### Ryan

| Arquivo | Descrição | Status |
|---------|-----------|--------|
| `src/core/node.py` | Estrutura do nó (fields, constantes RED/BLACK, sentinela NIL) |100% Concluído |
| `src/core/red_black_tree.py` | Red-Black Tree completa: INSERT, SEARCH, DELETE, RANGE, inorder, rotações, fix_insert, fix_delete | 100% Concluído |
| `src/core/database.py` | Interface pública da Database, formatação de respostas JSON | 100%Concluído |
| `tests/test_red_black_tree.py` | 35 testes unitários cobrindo INSERT, SEARCH, DELETE, RANGE e propriedades RBT | 100% Concluído |
| `tests/test_merge_sort.py` | Testes unitários do MERGE_SORT e MERGE | ⏳ Pendente |
| `tests/test_range_query.py` | Testes unitários do RANGE | ⏳ Pendente |

---

### Wanessa

| Arquivo | Descrição | Status |
|---------|-----------|--------|
| `src/io/input_parse.py` | Parser e validação do JSON de entrada | 100% Concluído |
| `src/io/output_writer.py` | Serialização dos resultados em JSON de saída | 100% Concluído |
| `src/main.py` | Ponto de entrada: orquestra parse → execute → write |100% Concluído |
| `src/operations/executor.py` | Despachador de operações: roteia cada op para o módulo correto | 100% Concluído |
| `run.sh` | Script de execução via CLI | 100% Concluído |
| `Makefile` | Targets de automação (test, run, gerar dados) | ⏳ Pendente |
| `requirements.txt` | Dependências do projeto | 100% Concluído |
| `docs/COMPLEXIDADE.md` | Análise teórica + benchmarks de prova de carga | 100% Concluído |
| `docs/ARQUITETURA.md` | Documento de arquitetura do sistema | 100% Concluído |
| `docs/DIVISAO_TAREFAS.md` | Este documento | 100% Concluído |

---

### Gustavo

| Arquivo | Descrição | Status |
|---------|-----------|--------|
| `src/algorithms/merge_sort.py` | MergeSort manual (MERGE_SORT + MERGE) | 100% Concluído |
| `src/operations/backup_merge.py` | Consolidação de backups: lê JSONL, merge, resolve duplicatas, salva | 100% Concluído |
| `src/operations/range_query.py` | Implementação alternativa de RANGE (referência) | 100% Concluído |
| `scripts/gerar_basico.py` | Gerador de input_basico.json (caso típico) | 100% Concluído |
| `scripts/gerar_avancado.py` | Gerador de input_avancado.json (casos extremos) | 100% Concluído |
| `scripts/gerar_estresse.py` | Gerador de input_estresse.json (100k operações) | 100% Concluído |
 `tests/test_integration.py` | Testes de integração via arquivos JSON | 100% Concluído |

---

## Status Geral

### Concluído
- Engine funcionando end-to-end (`./run.sh data/input_basico.json saida.json`)
- Red-Black Tree com INSERT, SEARCH, DELETE e RANGE implementados e testados
- Pipeline de I/O completo (parse → execute → write)
- BACKUP_MERGE integrado ao executor
- Scripts geradores de dados (básico, avançado, estresse)
- Arquivos de gabarito gerados (`output_esperado_*.json`)
- Análise de complexidade com benchmarks empíricos


## Critérios de Aceite

| Critério | Responsável | Status |
|----------|-------------|--------|
| INSERT em O(log N) com RBT balanceada | Ryan | 100% |
| SEARCH em O(log N) | Ryan | 100%  |
| DELETE em O(log N) com fix_delete | Ryan | 100%  |
| RANGE em O(log N + K) com poda | Ryan | 100%  |
| BACKUP_MERGE com MergeSort manual em O(M log M) | Gustavo | 100%  |
| Parser valida schema de entrada | Wanessa | 100%  |
| Output em JSON determinístico | Wanessa |100%  |
| Testes unitários da RBT | Ryan |100%  |
| Testes unitários do MergeSort | Ryan | 100% |
| Testes unitários do RANGE | Ryan | 100% |
| Testes de integração | Gustavo | 100%  |
| Prova de carga (100k ops) | Wanessa | 100%  |
| Documentação de arquitetura | Wanessa | 100% |
| Sem bibliotecas externas de estrutura/ordenação | Todos | 100%  |