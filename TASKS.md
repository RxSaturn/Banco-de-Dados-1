# TASKS — Refatoração do repositório

Documento de trabalho. Cada item equivale a um commit ou menos.
Categoria definida na Fase 0: **Educacional / Estudo**.

---

## Fase 1 — Sondagem de capacidade `[concluída]`

Ferramentas disponíveis nesta sessão:

| Ferramenta | Estado | Consequência |
|---|---|---|
| `git` | disponível | Movimentos com `git mv`, histórico preservado. |
| `python3` 3.11.15 | disponível | Scripts executáveis. |
| `matplotlib` 3.11.1 + `numpy` 2.4.6 | instalados nesta sessão | Os dois scripts rodam de verdade. |
| `ruff` 0.15.8 | disponível | Lint real do código Python. |
| `node` 22.22.2 | disponível | Não usado. O repositório não tem JavaScript. |
| `latexmk` | **ausente** | Irrelevante. O repositório não tem LaTeX. |

Inventário: 24 arquivos `.md`, 13 `.pdf`, 9 `.png`, 2 `.py`. Pacote de 8,61 MiB.
Árvore de trabalho limpa. Nenhum arquivo não rastreado ou ignorado presente.

---

## Fase 3 — Subtrair

- [ ] Confirmar: **não há resíduo para remover**. Sem `node_modules/`, sem `build/`,
      sem `.DS_Store`, sem artefatos LaTeX, sem arquivos duplicados. O `.gitignore`
      atual já cobre cache Python, ambientes virtuais, IDE e ruído de sistema.
- [ ] Corrigir a regra `*.png` do `.gitignore`. Hoje ela ignora todo PNG e abre
      exceção apenas para `apresentacao_assets/`. Se as imagens mudarem de pasta,
      o Git passa a ignorá-las. Trocar por uma regra que acompanhe o novo caminho.

> Esta fase quase não remove nada. O repositório já está limpo. O relatório final
> registra isso como resultado, não como falha.

---

## Fase 4 — Estrutura

Agrupar por disciplina. Cada movimento usa `git mv`, então o histórico segue o arquivo.

### 4.1 Criar `banco_de_dados_I/` e mover o material da raiz

- [ ] `bd1_0*.pdf` (6 arquivos) → `banco_de_dados_I/slides/`
- [ ] `Exercicios/*.pdf` (6 arquivos) → `banco_de_dados_I/exercicios/`
- [ ] `Exercício1.md` → `banco_de_dados_I/exercicios/exercicio-01-views-sql.md`
- [ ] `Exercício2.md` → `banco_de_dados_I/exercicios/exercicio-02-triggers-sql.md`
- [ ] `Projeto/` → `banco_de_dados_I/projeto-sgca/`, com renomeação:
      - `Requisitos Calendário Acadêmico.md` → `00-requisitos.md`
      - `Sistema Calendários Acadêmicos - Parte 1 Corrigida.md` → `01-modelagem.md`
      - `Sistemas de Calendários Acadêmicos - Criação do Banco.md` → `02-criacao-do-banco.md`
      - `Sistemas de Calendários Acadêmicos - Aplicação Conectada ao Banco de Dados.md` → `03-aplicacao.md`
      - `SGCA.pdf` permanece com o nome atual

### 4.2 Organizar `banco_de_dados_II/`

- [ ] Criar `resumos/` e mover os quatro resumos temáticos, com prefixo numérico
      que reflete a ordem já declarada nos títulos:
      - `Intro_conclusão.md` → `resumos/00-introducao-e-conclusao.md`
      - `Introdução a Índices e Organização de Arquivos.md` → `resumos/01-introducao-a-indices.md`
      - `Armazenamento de Dados e Hierarquia de Memória.md` → `resumos/02-armazenamento-e-memoria.md`
      - `Índices em Árvore (B-Tree e B+Tree).md` → `resumos/03-indices-em-arvore.md`
      - `Índices Hash.md` → `resumos/04-indices-hash.md`
- [ ] Criar `guias/`:
      - `Guia_de_Estudos_Avancados_BD2.md` → `guias/guia-de-estudos-avancados.md`
      - `Guia_de_Exercicios_BD2.md` → `guias/guia-de-exercicios.md`
      - corrigir o link interno entre os dois guias
- [ ] `documents/` → `transcricoes/`, mantendo `bd2_06` a `bd2_11` e `exercicios/`

### 4.3 Reunir o trabalho de Sharding

Hoje o trabalho está dividido entre `apresentacao_assets/` na raiz e dois arquivos
dentro de `banco_de_dados_II/`. Reunir tudo em
`banco_de_dados_II/apresentacao-sharding/`:

- [ ] `Sharding_e_Particionamento_em_Bancos_de_Dados_Distribuidos.md` → `artigo.md`
- [ ] `apresentacao_assets/APRESENTACAO_SLIDES.md` → `slides.md`
- [ ] `apresentacao_assets/*.png` (9 arquivos) → `img/`
- [ ] `apresentacao_assets/generate_diagrams.py` → `scripts/generate_diagrams.py`
- [ ] `banco_de_dados_II/scripts/consistent_hashing_visualization.py` → `scripts/`

### 4.4 Decisão pendente

- [ ] `bd1_06_nomaliza.pdf` tem erro de digitação. O arquivo equivalente em
      `Exercicios/` escreve `normaliza`. **Perguntar antes de renomear.**

---

## Fase 5 — Código e revisão

- [ ] Ajustar `save_figure()` em `generate_diagrams.py`. A função grava ao lado do
      próprio arquivo. Depois do movimento, o destino correto é `../img/`.
- [ ] Rodar `generate_diagrams.py` e comparar as 9 imagens com as versões commitadas.
- [ ] Rodar `consistent_hashing_visualization.py` e registrar a saída real.
- [ ] Rodar `ruff check` nos dois scripts. Corrigir o que for mecânico.
- [ ] **Defeito real:** `slides.md` cita as imagens como texto entre crases, não como
      imagem markdown. O GitHub não renderiza nada. Trocar por `![alt](caminho)`.
- [ ] Atualizar todo caminho `apresentacao_assets/` citado dentro dos documentos.

---

## Fase 6 — Arquivos de higiene

A matriz da categoria Educacional pede apenas `LICENSE` e `README`. Nada de
`CODE_OF_CONDUCT`, `SECURITY` ou modelos de issue. Um repositório de anotações não
recebe contribuição externa, e esses arquivos viram cerimônia vazia.

- [ ] **Decisão pendente: qual licença.** Ver a seção "Decisões abertas" abaixo.
- [ ] `.gitignore` revisado (item da Fase 3)
- [ ] `CONTRIBUTING.md` — **opcional**, curto, só se você quiser

---

## Fase 7 — Automação

A matriz pede apenas lint para esta categoria. Sem CI de build, sem release.

- [ ] `.github/workflows/lint.yml` — `ruff check` nos scripts Python e verificação
      de links markdown quebrados
- [ ] Bloco `permissions: contents: read` em todo workflow
- [ ] `actions/checkout@v5` e `actions/setup-python@v6`
- [ ] `.github/dependabot.yml` para `github-actions` e `pip`
- [ ] Validar que o YAML faz parse com `python3 -c "import yaml..."`

> Não é possível executar o workflow aqui. Acompanhe a primeira execução no GitHub.

---

## Fase 8 — README

Só depois que todas as fases acima fecharem.

- [ ] Título, descrição de uma linha, linha de badges com URLs reais
- [ ] Sumário
- [ ] O que é e por que existe
- [ ] Mapa das duas disciplinas, com links para cada pasta
- [ ] Diagrama Mermaid da estrutura
- [ ] Como rodar os scripts Python
- [ ] Nota de escopo honesta: material de curso, não biblioteca
- [ ] Licença e crédito de autoria

---

## Fase 9 — Entrega

Esta sessão **tem** acesso de escrita ao repositório, ao contrário do padrão da skill.

- [ ] Commit por unidade na branch `claude/new-session-yulomk`
- [ ] `git push -u origin claude/new-session-yulomk`
- [ ] Relatório final: removido, adicionado, executado com saída real, não executado
      e por quê, decisões abertas, lista de imagens sugeridas

---

## Decisões abertas (suas)

1. **Licença.** Há um problema real aqui. Os 13 PDFs incluem slides e listas do
   professor. Esse material não é seu para licenciar. Uma licença única aplicada ao
   repositório inteiro faria uma afirmação falsa. Opções na pergunta que farei na
   Fase 6.
2. **`bd1_06_nomaliza.pdf`** — corrigir o erro de digitação no nome?
3. **`documents/` → `transcricoes/`** — troca o único nome de pasta em inglês por
   português. Confirma?
4. **Este arquivo `TASKS.md`** — mantenho no repositório como registro do trabalho,
   ou removo no último commit?
