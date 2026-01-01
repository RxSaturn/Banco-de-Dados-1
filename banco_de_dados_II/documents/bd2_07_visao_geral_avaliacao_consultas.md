## Page 1

# Banco de dados II

## 7 – Visão geral da avaliação de consultas

Marcos Roberto Ribeiro

Departamento de Engenharia e Computação (DEC)
Curso de Engenharia de Computação
2024

&lt;img&gt;Logo with white squares and a circle on a green background&lt;/img&gt;
INSTITUTO FEDERAL
Minas Gerais
---
Bambuí

---


## Page 2

IFMG
&lt;page_number&gt;2&lt;/page_number&gt;

# Introdução

* Para avaliar uma consulta, os SGBD traduzem o código SQL para planos de execução/avaliação
* Os planos são representados na forma de árvores onde os nós são operadores da álgebra relacional
* Além dos operadores, os planos contém informações sobre qual algoritmo usar para avaliar cada operador
* O SGBD usa um processo de otimização de consulta para encontrar um bom plano de execução

---


## Page 3

&lt;page_number&gt;3&lt;/page_number&gt;

&lt;img&gt;IFMG&lt;/img&gt;

# Tabelas consideradas nos exemplos

## Tabela marinheiros

marinheiros (id_marinheiro: integer, nome_marinheiro: string,
avaliacao: integer, nascimento: date)

*   Registros de 50 bytes
*   500 páginas com 80 registros cada

## Tabela reservas

reservas(id_marinheiro: integer, id_barco: integer,
dia: date, nome_responsavel: string)

*   Registros de 40 bytes
*   1000 páginas com 100 registros cada

---


## Page 4

&lt;page_number&gt;4&lt;/page_number&gt;

IFMG

# Catálogo do sistema

*   Tabelas especiais que armazenam metadados sobre os bancos de dados
*   Também conhecido como dicionário de dados
*   Dados sobre tabelas: nome da tabela, nome do arquivo, estrutura do arquivo, nomes e tipos dos atributos, índices da tabela, restrições de integridade
*   Dados sobre índices: nome do índice, estrutura, atributos da chave de pesquisa
*   Os catálogos são armazenados em forma de tabela. Por quê?

---


## Page 5

IFMG
&lt;page_number&gt;5&lt;/page_number&gt;

# Estatísticas do catálogo do sistema

*   Estatísticas (atualizadas periodicamente):
    *   Cardinalidade: Número de registros/tuplas (*NTuplas*) de cada tabela
    *   Tamanho: Número de páginas (*NPaginas*) de cada tabela
    *   Cardinalidade do Índice: Número de chaves distintas (*NChaves*) de cada índice
    *   Tamanho do Índice: Número de páginas (*INPaginas*) de cada índice
    *   Altura do Índice: Número de níveis (*IAltura*) não folha de cada índice do tipo árvore
    *   Faixa de Índice: Valores mínimo (*IBaixo*) e máximo (*IAlto*) da chave de pesquisa de cada índice

---


## Page 6

IFMG
&lt;page_number&gt;6&lt;/page_number&gt;

# Introdução à avaliação de operadores

*   Cada operador pode possuir diversos algoritmos para avaliação
*   Nenhum algoritmo é universalmente superior
*   Alguns fatores que influenciam tais algoritmos
    *   Tamanho das tabelas
    *   Índices e ordenações existentes
    *   Quantidade de buffers disponíveis
    *   Política de substituição de buffers

---


## Page 7

IFMG
&lt;page_number&gt;7&lt;/page_number&gt;

# Técnicas comumente usadas no processamento de operadores

**Indexação:** Uso de índice para obter apenas às tuplas que atendem à uma determinada condição

**Iteração:** Varrer as tuplas de uma tabela ou as entradas de um índice

**Particionamento:** Decomposição de uma operação em outras operações mais simples sobre partições de dados

---


## Page 8

IFMG
&lt;page_number&gt;8&lt;/page_number&gt;

# Caminhos de acesso

*   Um caminho de acesso é uma forma de recuperar as tuplas de uma tabela
*   Esses caminho podem afetar significativamente o custo do operador
*   Exemplo: seleção usando índice
*   A **seletividade** de um caminho de acesso é o número de páginas recuperadas usando tal caminho
*   É melhor usar o caminho mais seletivo (que recupera o menor número de páginas)

---


## Page 9

IFMG
&lt;page_number&gt;9&lt;/page_number&gt;

# Algoritmos para operações relacionais – Seleção

- Pesquisa por um registro que atenda a certas condições
- Se houver índice:
    - Verifique se é viável usar o índice
- Senão, varra a tabela

---


## Page 10

IFMG
&lt;page_number&gt;10&lt;/page_number&gt;

# Algoritmos para operações relacionais – Projeção

*   A maior dificuldade está na eliminação de duplicatas (DISTINCT)
*   Algumas estratégias para esta situação:
    *   Ordenar primeiro os dados
    *   Avaliação somente de índice (se todos os campos estiverem na chave do índice)

---


## Page 11

&lt;page_number&gt;11&lt;/page_number&gt;

IFMG

# Algoritmos para operações relacionais - junção I

*   Operações caras e comuns (existem diversos algoritmos)
*   Exemplo: reservas ⋈ id_marinheiro=id_marinheiro marinheiros

## Junção de loops aninhados indexados

*   Supondo que haja um índice hash sobre marinheiros.id_marinheiro
*   Para cada tupla de reservas, use o índice para verificar a correspondência
*   Custo:
    *   Varredura de reservas: 100 × 1.000 = 100.000
    *   Obtenção da correspondência em marinheiros: 1,2 E/S (média de um índice hash) + 1 página de marinheiros
    *   Total: 1.000 + 100.000 × (1 + 1,2) = 221.000

---


## Page 12

IFMG
&lt;page_number&gt;12&lt;/page_number&gt;

# Algoritmos para operações relacionais - junção II

## Junção sort-merge

*   Supondo que não hajam índices
*   Ordenamos as tabelas sobre o atributo de junção e depois varremos para fazer a junção
*   Custo:
    *   Ordenação em duas passagens considerado apenas o custo de E/S e leitura/gravação em cada passagem:
        *   reservas: 2 × 2 × 1.000 = 4.000
        *   marinheiros: 2 × 2 × 500 = 2.000
    *   Consideramos mais uma varredura nas tabelas ordenadas
    *   Total: 4.000 + 2.000 + 1.000 + 500 = 7.500

---


## Page 13

IFMG
&lt;page_number&gt;13&lt;/page_number&gt;

# Introdução à otimização de consultas

*   Uma das tarefas mais importantes do SGBD
*   Uma consulta pode ser avaliada de várias formas e custo destas avaliações pode ser muito diferente
*   É muito difícil encontrar o plano ideal, mas podemos encontrar um bom plano

<mermaid>
graph TD
    A[Consulta] --> B[Analisador de Consultas]
    B -->|Consulta Analisada| C[Otimizador de Consultas]
    C -->|Gerador de Planos| D[Catálogo do Sistema]
    C -->|Estimador de Custo| D
    C -->|Plano Escolhido| E[Avaliador de Planos de Consulta]
</mermaid>

## Tarefas do Otimizador

*   Gerar de planos alternativos (não considera todos, o número é muito grande)
*   Avaliar o custo de cada plano alternativo
*   Escolher o plano com menor custo

---


## Page 14

IFMG &lt;page_number&gt;14&lt;/page_number&gt;

# Planos de avaliação de consultas

*   Um plano é uma árvore de operadores relacionais
*   Contém informações adicionais sobre método de acesso e algoritmos

## Consulta

```sql
SELECT m.nome_marinheiro
FROM reservas r, marinheiros m
WHERE r.id_marinheiro = m.id_marinheiro
AND r.id_barco = 100
AND m.avaliacao > 5;
```

## Plano

```mermaid
graph TD
    A[reservas] --> B(marinheiros)
    subgraph " "
        C[πnome_marinheiro]
        D[σid_barco=100 ∧ avaliacao > 5]
        E[×id_marinheiro=id_marinheiro]
    end
    B --> C
    C --> D
    D --> E

---


## Page 15

IFMG
&lt;page_number&gt;15&lt;/page_number&gt;

# Plano de execução completo

<mermaid>
graph TD
    A[reservas] --> B(marinheiros)
    C[&times; id_marinheiro = id_marinheiro] --> D[σ id_barco=100 & avaliacao > 5]
    E[π nome_marinheiro] --> F((durante a execução))
    G[σ id_barco=100 & avaliacao > 5] --> H((durante a execução))
    I[&times; id_marinheiro = id_marinheiro] --> J((laços aninhados simples))
    K[reservas] --> L((varredura de arquivo))
    M[marinheiros] --> N((varredura de arquivo))
</mermaid>

---


## Page 16

IFMG
&lt;page_number&gt;16&lt;/page_number&gt;

# Avaliação pipeline

*   O resultado de um operador pode ser encaminhado para outro operador sem a utilização de tabelas temporárias
*   Economia de gravar os dados e lê-los de volta
*   Quando se usa tabelas temporárias, dizemos que as tuplas são **materializadas**
*   A avaliação encadeada (*pipeline*) é escolhida sempre que possível
*   Quando um operador usa a avaliação encadeada, dizemos que tal operador é aplicado **durante a execução**

---


## Page 17

IFMG
&lt;page_number&gt;17&lt;/page_number&gt;

# A interface iteradora

*   Normalmente a implementação dos operadores possui uma interface iteradora uniforme
*   Esta interface esconde os detalhes de implementação e possui as seguintes funções
    *   open(): inicializa o operador
    *   get_next(): processa a(s) tupla(s) de entrada
    *   close(): finaliza o operador desalocando recursos usados
*   A interface iteradora suporta pipeline naturalmente
*   A decisão de materializar fica dentro do operador

---


## Page 18

IFMG
&lt;page_number&gt;18&lt;/page_number&gt;

# Planos alternativos - exemplo de motivação

```mermaid
graph TD
    A[π nome_marinheiro (durante a execução)] --> B[σ id_barco=100 ∧ avaliacao > 5 (durante a execução)]
    B --> C[⋈ id_marinheiro = id_marinheiro (laços aninhados simples)]
    C --> D[reservas (varredura de arquivo)]
    C --> E[marinheiros (varredura de arquivo)]
```

*   Varredura e junção com loops aninhados
*   Para cada página de reservas, leia todas as páginas de marinheiros fazendo a junção
*   Custo: 1.000 × 500 = 500.000 E/S

---


## Page 19

IFMG
&lt;page_number&gt;19&lt;/page_number&gt;

# Exemplo de motivação (empurrando seleções)

```
    π_{nome_marinheiro}
          |
        η_{id_marinheiro = id_marinheiro} (durante a execução)
          |
     σ_{id_barco = 100}       σ_{avaliacao > 5} (junção sort-merge)
          |         /
    vari()       vari()
    |       ____________
reservas       marinheiros (varredura; materializa)      (varredura; materializa)
         |
         (varredura de arquivo) (varredura de arquivo)
```

*   Varredura/seleção de reservas: 1.000
*   Gravação de T1 (supondo distribuição uniforme de reservas): 1.000 reservas / 100 barcos = 10
*   Varredura/seleção de marinheiros: 500
*   Gravação de T2 (supondo distribuição uniforme de avaliações entre 1 e 10): 50% de 500 = 250

*   Ordenação em duas passagens de T1 e T2: 2 × 2 × 10 = 40 + 2 × 2 × 250 = 1.000
*   Junção de T1 e T2: 10 × 250 = 2.500
*   Custo final: 1.000+10+500+250+1.000+2.500 = 5.260

---


## Page 20

IFMG
&lt;page_number&gt;20&lt;/page_number&gt;

# Tarefas de um otimizador típico

*   Usa equivalências da álgebra relacional para identificar obter expressões algébricas alternativas
*   Para cada expressão algébrica equivalente, considera as implementações disponíveis para os operadores para gerar planos
*   Avalia os custos dos planos e seleciona aquele com menor custo
*   Expressões algébricas são consideradas equivalentes se produzirem o mesmo resultado

**Exemplos:**
*   Seleções e produtos cartesianos podem ser combinados em junções
*   Junções podem ser reordenadas extensivamente
*   Seleções e junções podem ser empurradas para frente das junções

---


## Page 21

&lt;page_number&gt;21&lt;/page_number&gt;

IFMG

# Planos de profundidade à esquerda

## Árvore 1
&lt;img&gt;A tree diagram labeled "Árvore 1" with nodes A, B, C, D.&lt;/img&gt;
Tabela Externa

## Árvore 2
&lt;img&gt;A tree diagram labeled "Árvore 2" with nodes A, B, C, D.&lt;/img&gt;
Tabela Interna

## Árvore 3
&lt;img&gt;A tree diagram labeled "Árvore 3" with nodes A, B, C, D.&lt;/img&gt;

Árvores Lineares: Pelo menos um filho de junção é tabela
Árvore de Profundidade à Esquerda: O filho direito da junção sempre é uma tabela

---


## Page 22

IFMG
&lt;page_number&gt;22&lt;/page_number&gt;

# Planos de profundidade à esquerda

*   Os otimizadores usam *programação dinâmica* para pesquisar os planos de profundidade à esquerda
*   A medida que o número de junções aumenta, o número de planos alternativos pode crescer muito
*   É necessário podar o espaço de planos alternativos
*   Árvores de profundidade à esquerda permite generalizar os planos *integralmente encadeados* (pipeline em todas as junções)

---


## Page 23

IFMG
&lt;page_number&gt;23&lt;/page_number&gt;

# Avaliação de consultas no PostgreSQL

*   Podemos visualizar informações sobre avaliação de consultas no PostgreSQL utilizando a palavra chave **EXPLAIN** antes da consulta
*   Observe os próximos exemplos e identifique diferenças na avaliação das consultas

---


## Page 24

IFMG
&lt;page_number&gt;24&lt;/page_number&gt;

# Exemplo 1 - Valor total comprado de cada fornecedor

## Consulta

```sql
EXPLAIN
SELECT f.den_fornecedor,
       SUM(c.valor_total)
FROM fornecedor AS f,
     compra AS c
WHERE f.id_fornecedor =
      c.id_fornecedor
GROUP BY f.id_fornecedor,
         f.den_fornecedor;
```

## Plano

```mermaid
graph TD
    A[fornecedor] --> B[compra]
    C[id_fornecedor, den_fornecedor, SUM(valor_total)] --> B

---


## Page 25

IFMG
&lt;page_number&gt;25&lt;/page_number&gt;

# Exemplo 1 - Valor total comprado de cada fornecedor

## Avaliação

QUERY PLAN
---
HashAggregate (cost=2.68..2.73 rows=4 width=72)
    Group Key: f.id_fornecedor
        -> Hash Join (cost=1.09..2.52 rows=33 width=56)
            Hash Cond: (c.id_fornecedor = f.id_fornecedor)
                -> Seq Scan on compra c (cost=0.00..1.33 rows=33 width=24)
                -> Hash (cost=1.04..1.04 rows=4 width=40)
                    -> Seq Scan on fornecedor f (cost=0.00..1.04 rows=4 width=40)

---


## Page 26

&lt;page_number&gt;26&lt;/page_number&gt;

&lt;img&gt;IFMG&lt;/img&gt;

# Exemplo 2 - Valor total vendido para cada cidade

## Consulta
```
EXPLAIN
SELECT c.den_cidade,
       SUM(v.valor_total)
FROM cidade AS c,
     cliente AS cl,
     venda AS v
WHERE c.id_cidade = cl.id_cidade
AND cl.id_cliente = v.id_cliente
GROUP BY c.id_cidade,
         c.den_cidade;
```

## Plano
```
id_cidade, den_cidade γSUM(valor_total)
                       |
                       ⨯
                 venda   cidade cliente

---


## Page 27

IFMG
&lt;page_number&gt;27&lt;/page_number&gt;

# Exemplo 2 - Valor total vendido para cada cidade

## Avaliação

QUERY PLAN
---
HashAggregate (cost=31.57..36.52 rows=396 width=49)
Group Key: c.id_cidade
-> Hash Join (cost=17.18..29.59 rows=396 width=23)
    Hash Cond: (v.id_cliente = cl.id_cliente)
    -> Seq Scan on venda v (cost=0.00..6.96 rows=396 width=14)
    -> Hash (cost=15.71..15.71 rows=118 width=25)
        -> Nested Loop (cost=0.29..15.71 rows=118 width=25)
            -> Seq Scan on cliente cl (cost=0.00..2.18 rows=118 width=12)
            -> Memoize (cost=0.29..2.14 rows=1 width=17)
                Cache Key: cl.id_cidade
                Cache Mode: logical
                -> Index Scan using cidade_pk on cidade c (cost=0.28..2.13 rows=1 width=17)
                    Index Cond: (id_cidade = cl.id_cidade)

---


## Page 28

&lt;page_number&gt;28&lt;/page_number&gt;

&lt;img&gt;IFMG&lt;/img&gt;

# Referências

DATE, C. J. Introdução a sistemas de bancos de dados. Rio de Janeiro: Elsevier, 2004.

ELMASRI, R.; NAVATHE, S. B. Sistemas de banco de dados. 7. ed. São Paulo: Pearson Addison Wesley, 2018.

RAMAKRISHNAN, R.; GEHRKE, J. Sistemas de gerenciamento de banco de dados. 3. ed. São Paulo: McGrawHill, 2008.

SILBERSCHATZ, A.; KORTH, H. F.; SUDARSHAN, S. Sistema de bancos de dados. 3. ed. São Paulo: Campus, 2007.