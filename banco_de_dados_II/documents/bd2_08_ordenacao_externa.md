## Page 1

# Banco de dados II

## 7 – Ordenação externa

Marcos Roberto Ribeiro

Departamento de Engenharia e Computação (DEC)
Curso de Engenharia de Computação
2024

&lt;img&gt;Logo with white squares forming a grid pattern&lt;/img&gt;
INSTITUTO FEDERAL
Minas Gerais
---
Campus
Bambuí

---


## Page 2

&lt;page_number&gt;2&lt;/page_number&gt;

IFMG

# Quando ordenar dados?

*   O usuário pode precisar do resultado em alguma ordem (ex.: data de nascimento)
*   Carregamento em massa para criação de índices
*   Eliminação de duplicadas
*   Alguns algoritmos de junção

## Ordenação Externa

Ordenação de dados que não cabem na memória principal

---


## Page 3

&lt;page_number&gt;3&lt;/page_number&gt;

IFMG

# Merge-sort de duas vias simples

<mergesort_diagram>
    <description>
        A flowchart illustrating the two-way simple merge sort algorithm.
        
        **Arquivo de Entrada (Input File):**
        - 8 series ordered by 1 page each.

        **Passagem 0:** 8 séries ordenadas de 1 página
        - Each series is split into pairs of single-page segments.
        - Pairs are merged into double-page segments.
        - 4 double-page segments result.

        **Passagem 1:** 4 séries ordenadas de 2 páginas
        - Each double-page segment is split into pairs of double-page segments.
        - Pairs are merged into quadruple-page segments.
        - 2 quadruple-page segments result.

        **Passagem 2:** 2 séries ordenadas de 4 páginas
        - Each quadruple-page segment is split into pairs of quadruple-page segments.
        - Pairs are merged into octuple-page segments.
        - 1 octuple-page segment result.

        **Passagem 3:** 1 série ordenada de 8 páginas
        - The final octuple-page segment is merged to produce a single 8-page series.
    </description>
</mergesort_diagram>

---


## Page 4

&lt;page_number&gt;3&lt;/page_number&gt;

IFMG

# Merge-sort de duas vias simples

Arquivo de Entrada

Passagem 0: 8 séries ordenadas de 1 página

Passagem 1: 4 séries ordenadas de 2 páginas

Passagem 2: 2 séries ordenadas de 4 páginas

Passagem 3: 1 série ordenada de 8 páginas

```mermaid
graph TD
    subgraph Arquivo de Entrada
        A[3,4]
        B[6,2]
        C[9,4]
        D[8,7]
        E[5,6]
        F[3,1]
        G[2,8]
        H[4]
    end

    subgraph Passagem 0: 8 séries ordenadas de 1 página
        I[3,4]
        J[2,6]
        K[4,9]
        L[7,8]
        M[5,6]
        N[1,3]
        O[2,8]
        P[4]
    end

    subgraph Passagem 1: 4 séries ordenadas de 2 páginas
        Q[2,3]
        R[4,6]
        S[4,7]
        T[8,9]
        U[1,3]
        V[5,6]
        W[2,4]
        X[8]
    end

    subgraph Passagem 2: 2 séries ordenadas de 4 páginas
        Y[2,3]
        Z[4,4]
        AA[6,7]
        AB[8,9]
        AC[1,2]
        AD[3,4]
        AE[5,6]
        AF[8]
    end

    subgraph Passagem 3: 1 série ordenada de 8 páginas
        AG[1,2]
        AH[2,3]
        AI[3,4]
        AJ[4,4]
        AK[5,6]
        AL[6,7]
        AM[8,8]
        AN[9]
    end

    A --> I
    B --> J
    C --> K
    D --> L
    E --> M
    F --> N
    G --> O
    H --> P

    I --> Q
    J --> R
    K --> S
    L --> T
    M --> U
    N --> V
    O --> W
    P --> X

    Q --> Y
    R --> Z
    S --> AA
    T --> AB
    U --> AC
    V --> AD
    W --> AE
    X --> AF

    Y --> AG
    Z --> AH
    AA --> AI
    AB --> AJ
    AC --> AK
    AD --> AL
    AE --> AM
    AF --> AN

---


## Page 5

&lt;page_number&gt;3&lt;/page_number&gt;

IFMG

# Merge-sort de duas vias simples

<mergesort_diagram>
    <description>
        A flowchart illustrating the two-way simple merge sort algorithm.
        
        **Arquivo de Entrada (Input File):**
        - 8 series ordenadas de 1 página
        - 6,2
        - 9,4
        - 8,7
        - 5,6
        - 3,1
        - 2,8
        - 4
        
        **Passagem 0: 8 séries ordenadas de 1 página**
        - 3,4
        - 2,6
        - 4,9
        - 7,8
        - 5,6
        - 1,3
        - 2,8
        - 4
        
        **Passagem 1: 4 séries ordenadas de 2 páginas**
        - 2,3
        - 4,6
        - 4,7
        - 8,9
        - 1,3
        - 5,6
        - 2,4
        - 8
        
        **Passagem 2: 2 séries ordenadas de 4 páginas**
        - 2,3
        - 4,4
        - 6,7
        - 8,9
        - 1,2
        - 3,4
        - 5,6
        - 8
        
        **Passagem 3: 1 série ordenada de 8 páginas**
        - 1,2
        - 2,3
        - 3,4
        - 4,4
        - 5,6
        - 6,7
        - 8,8
        - 9
    </description>
</mergesort_diagram>

---


## Page 6

&lt;page_number&gt;3&lt;/page_number&gt;

IFMG

# Merge-sort de duas vias simples

<mergesort_diagram>
    <description>
        A flowchart illustrating the two-way simple merge sort algorithm.
        
        **Arquivo de Entrada (Input File):**
        - 8 series ordenadas de 1 página
        - 6,2
        - 9,4
        - 8,7
        - 5,6
        - 3,1
        - 2,8
        - 4
        
        **Passagem 0: 8 séries ordenadas de 1 página**
        - 3,4
        - 2,6
        - 4,9
        - 7,8
        - 5,6
        - 1,3
        - 2,8
        - 4
        
        **Passagem 1: 4 séries ordenadas de 2 páginas**
        - 2,3
        - 4,6
        - 4,7
        - 8,9
        - 1,3
        - 5,6
        - 2,4
        - 8
        
        **Passagem 2: 2 séries ordenadas de 4 páginas**
        - 2,3
        - 4,4
        - 6,7
        - 8,9
        - 1,2
        - 3,4
        - 5,6
        - 8
        
        **Passagem 3: 1 série ordenada de 8 páginas**
        - 1,2
        - 2,3
        - 3,4
        - 4,4
        - 5,6
        - 6,7
        - 8,8
        - 9
    </description>
</mergesort_diagram>

---


## Page 7

&lt;page_number&gt;3&lt;/page_number&gt;

IFMG

# Merge-sort de duas vias simples

<mergesort_diagram>
    <description>
        A flowchart illustrating the two-way simple merge sort algorithm.
        
        **Arquivo de Entrada (Input File):**
        - 3,4
        - 6,2
        - 9,4
        - 8,7
        - 5,6
        - 3,1
        - 2,8
        - 4
        
        **Passagem 0: 8 séries ordenadas de 1 página (Passage 0: 8 sorted series of 1 page)**
        - 3,4
        - 2,6
        - 4,9
        - 7,8
        - 5,6
        - 1,3
        - 2,8
        - 4
        
        **Passagem 1: 4 séries ordenadas de 2 páginas (Passage 1: 4 sorted series of 2 pages)**
        - 2,3
        - 4,6
        - 4,7
        - 8,9
        - 1,3
        - 5,6
        - 2,4
        - 8
        
        **Passagem 2: 2 séries ordenadas de 4 páginas (Passage 2: 2 sorted series of 4 pages)**
        - 2,3
        - 4,4
        - 6,7
        - 8,9
        - 1,2
        - 3,4
        - 5,6
        - 8
        
        **Passagem 3: 1 série ordenada de 8 páginas (Passage 3: 1 sorted series of 8 pages)**
        - 1,2
        - 2,3
        - 3,4
        - 4,4
        - 5,6
        - 6,7
        - 8,8
        - 9
    </description>
</mergesort_diagram>

---


## Page 8

&lt;page_number&gt;4&lt;/page_number&gt;

IFMG

# Merge-sort de duas vias simples

*   Nessa versão, o algoritmo usa apenas 3 páginas (sub-arquivos chamados de séries)
*   Se o arquivo de entrada possui $2^N$ páginas:
    *   A passagem 0 produz $2^N$ séries ordenadas de 1 página
    *   A passagem 1 produz $2^{N-1}$ séries ordenadas de 2 páginas
    *   A passagem 2 produz $2^{N-2}$ séries ordenadas de 4 páginas
    *   ...
    *   A passagem $N$ produz uma série ordenadas de $2^N$ páginas
*   Em cada passagem, as páginas são lidas, ordenadas e gravadas (2 E/S por página por passagem)
*   Se o arquivo possui $N$ páginas, são feitas $\lceil \log_2 N \rceil + 1$ passagens
*   O custo total será de $2N(\lceil \log_2 N \rceil + 1)$ E/S

---


## Page 9

IFMG
&lt;page_number&gt;5&lt;/page_number&gt;

# Merge-sort externo

*   O algoritmo anterior não aproveita todo o espaço em memória disponível
*   Considerando um arquivo de N páginas e B páginas disponíveis em memória, o *merge-sort externo* funciona da seguinte maneira

<mermaid>
graph TD
    subgraph Disco
        A[Disco]
        B[Disco]
    end

    subgraph Memória
        C[Memória]
    end

    D[ENTRADA 1] --> C
    E[ENTRADA 2] --> C
    F[...]
    G[ENTRADA B-1] --> C

    H[SAÍDA] --> C

    I[Passagem 0: Leia B páginas por vez, ordene-as internamente e grave ⌊N/B⌋ séries de B páginas]

    J[Demais Passagens: Use B - 1 páginas de de entrada e uma de saída. Ordene as entradas por intercalação e grave na saída]

    A --> D
    A --> E
    A --> F
    A --> G

    C --> H

    H --> B

    style A fill:#fff,stroke:#333,stroke-width:2px
    style B fill:#fff,stroke:#333,stroke-width:2px
    style C fill:#fff,stroke:#333,stroke-width:2px
    style D fill:#fff,stroke:#333,stroke-width:2px
    style E fill:#fff,stroke:#333,stroke-width:2px
    style F fill:#fff,stroke:#333,stroke-width:2px
    style G fill:#fff,stroke:#333,stroke-width:2px
    style H fill:#fff,stroke:#333,stroke-width:2px
    style I fill:#fff,stroke:#333,stroke-width:2px
    style J fill:#fff,stroke:#333,stroke-width:2px
</mermaid>

---


## Page 10

&lt;page_number&gt;6&lt;/page_number&gt;

IFMG

# Merge-sort externo

*   Com a intercalação em $B-1$ vias o número de passagens cai para $\lceil \log_{B-1} N \rceil + 1$ (contra $\lceil \log_2 N \rceil + 1$ do algoritmo anterior)
*   Normalmente $B$ é grande e o desempenho aumenta consideravelmente

## Exemplo: arquivo de 108 páginas com 5 em memória

Passagem 0: $\lceil 108/5 \rceil = 22$ séries ordenadas de 5 páginas

Passagem 1: $\lceil 108/5 \rceil = 6$ séries ordenadas de 20 páginas

Passagem 2: $\lceil 6/4 \rceil = 2$ séries ordenadas de 80 páginas

Passagem 3: Arquivo ordenado

---


## Page 11

IFMG
&lt;page_number&gt;7&lt;/page_number&gt;

Redução do número de passagem com o aumento de B

<table>
  <thead>
    <tr>
      <th>N</th>
      <th>B=3</th>
      <th>B=5</th>
      <th>B=9</th>
      <th>B=17</th>
      <th>B=129</th>
      <th>B=257</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>100</td>
      <td>7</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <td>1.000</td>
      <td>10</td>
      <td>5</td>
      <td>4</td>
      <td>3</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <td>10.000</td>
      <td>13</td>
      <td>7</td>
      <td>5</td>
      <td>4</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <td>100.000</td>
      <td>17</td>
      <td>9</td>
      <td>6</td>
      <td>5</td>
      <td>3</td>
      <td>3</td>
    </tr>
    <tr>
      <td>1.000.000</td>
      <td>20</td>
      <td>10</td>
      <td>7</td>
      <td>5</td>
      <td>3</td>
      <td>3</td>
    </tr>
    <tr>
      <td>10.000.000</td>
      <td>23</td>
      <td>12</td>
      <td>8</td>
      <td>6</td>
      <td>4</td>
      <td>3</td>
    </tr>
    <tr>
      <td>100.000.000</td>
      <td>26</td>
      <td>14</td>
      <td>9</td>
      <td>7</td>
      <td>4</td>
      <td>4</td>
    </tr>
    <tr>
      <td>1.000.000.000</td>
      <td>30</td>
      <td>15</td>
      <td>10</td>
      <td>8</td>
      <td>5</td>
      <td>4</td>
    </tr>
  </tbody>
</table>

---


## Page 12

IFMG
&lt;page_number&gt;8&lt;/page_number&gt;

# Custo de E/S x número de E/S

*   É importante reduzir o número de E/S
*   Porém, existe o problema da *E/S bloqueada* (operações de E/S independentes são mais caras do que E/S em bloco)
*   Podemos reduzir a E/S bloqueada com operações sobre grupos de *b* (*b* < *B*) páginas de uma vez
*   O número de passagens aumenta, mas há um equilíbrio entre o número de passagens e o custo da E/S bloqueada

---


## Page 13

IFMG
&lt;page_number&gt;9&lt;/page_number&gt;

Número de passagens considerando b = 32

<table>
<thead>
<tr>
<th>N</th>
<th>B=1.000</th>
<th>B=5.000</th>
<th>B=10.000</th>
<th>B=50.000</th>
</tr>
</thead>
<tbody>
<tr>
<td>100</td>
<td>1</td>
<td>1</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>1.000</td>
<td>1</td>
<td>1</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>10.000</td>
<td>2</td>
<td>2</td>
<td>1</td>
<td>1</td>
</tr>
<tr>
<td>100.000</td>
<td>3</td>
<td>2</td>
<td>2</td>
<td>2</td>
</tr>
<tr>
<td>1.000.000</td>
<td>3</td>
<td>2</td>
<td>2</td>
<td>2</td>
</tr>
<tr>
<td>10.000.000</td>
<td>4</td>
<td>3</td>
<td>3</td>
<td>2</td>
</tr>
<tr>
<td>100.000.000</td>
<td>5</td>
<td>3</td>
<td>3</td>
<td>2</td>
</tr>
<tr>
<td>1.000.000.000</td>
<td>5</td>
<td>4</td>
<td>3</td>
<td>3</td>
</tr>
</tbody>
</table>

---


## Page 14

IFMG
&lt;page_number&gt;10&lt;/page_number&gt;

# Bufferização dupla

*   No caso da ordenação, o custo de CPU também é importante
*   Seria interessante manter a CPU ocupada enquanto realizados operações de E/S

```mermaid
graph TD
    subgraph Memória
        A[Entrada 1]
        B[Entrada 1']
        C[Entrada 2]
        D[Entrada 2']
        E[Entrada k]
        F[Entrada k']
        G[Saída]
        H[Saída']
    end

    subgraph Disco
        I[...]
        J[...]
    end

    A --> B
    C --> D
    E --> F

    B --> G
    D --> H

    I --> A
    J --> C
    K --> E

    G --> H
    H --> G

---


## Page 15

IFMG
&lt;page_number&gt;11&lt;/page_number&gt;

Usando árvores B+ para ordenação - índice agrupado

&lt;img&gt;A diagram showing a B+ tree structure. The top level (root) has three branches pointing to three lower levels. Each lower level contains multiple nodes connected by arrows, indicating a linked list structure within each level.&lt;/img&gt;

- Muito eficiente, os dados já estão ordenadas pelas folhas da árvore

---


## Page 16

IFMG
&lt;page_number&gt;12&lt;/page_number&gt;

Usando árvores B+ para ordenação - índice não agrupado

&lt;img&gt;A diagram showing a B+ tree structure. The top level (root) has four branches pointing to four nodes at the next level. Each of these nodes has multiple branches pointing to leaf nodes. The leaf nodes are represented by small rectangles.&lt;/img&gt;

*   Pode ser menos eficiente do que varrer as páginas de dados dos arquivos. Por quê?

---


## Page 17

&lt;page_number&gt;13&lt;/page_number&gt;

IFMG

# Referências

DATE, C. J. Introdução a sistemas de bancos de dados. Rio de Janeiro: Elsevier, 2004.

ELMASRI, R.; NAVATHE, S. B. Sistemas de banco de dados. 7. ed. São Paulo: Pearson Addison Wesley, 2018.

RAMAKRISHNAN, R.; GEHRKE, J. Sistemas de gerenciamento de banco de dados. 3. ed. São Paulo: McGrawHill, 2008.

SILBERSCHATZ, A.; KORTH, H. F.; SUDARSHAN, S. Sistema de bancos de dados. 3. ed. São Paulo: Campus, 2007.