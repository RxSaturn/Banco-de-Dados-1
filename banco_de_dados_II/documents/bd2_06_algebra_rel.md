## Page 1

Banco de dados II

6 – Álgebra Relacional

Marcos Roberto Ribeiro

Departamento de Engenharia e Computação (DEC)
Curso de Engenharia de Computação
2024

&lt;img&gt;INSTITUTO FEDERAL Minas Gerais Campus Bambuí logo&lt;/img&gt;

---


## Page 2

IFMG
Introdução
&lt;page_number&gt;2&lt;/page_number&gt;

* A Álgebra Relacional é uma linguagem muito importante utilizada no modelo relacional
* Ela é composta por um conjunto de operadores que, quando combinados, permitem realizar diversos tipos de operações sobre uma relação ou um conjunto de relação
* A álgebra relacional está relacionada com a linguagem SQL, sendo que os SGBD atuais traduzem as consultas SQL para expressões da álgebra relacional para realizar o processamento das consultas
* Toda operação da Álgebra Relacional possui uma mais relações como entrada e uma relação como saída

---


## Page 3

IFMG
&lt;page_number&gt;3&lt;/page_number&gt;

# Principais operações da álgebra relacional

*   Seleção (σ)
*   Projeção (π)
*   Renomeação (ρ)
*   Junção (⋈)
*   Funções de agregação (γ)
*   União (∪)
*   Interseção (∩)
*   Diferença (-)
*   Produto Cartesiano (×)

---


## Page 4

IFMG
Seleção
&lt;page_number&gt;4&lt;/page_number&gt;

* A operação de seleção (σ) permite selecionar tuplas de uma relação que atendam certas condições

    σ<condição>(<relação>)

* A condição pode conter comparações de atributos e valores usando os operadores =, ≠, <, ≤, > e ≥

* Além disso, as comparações podem ser combinadas com os conectivos ∧, ∨ e ¬

---


## Page 5

IFMG
&lt;page_number&gt;5&lt;/page_number&gt;

# Exemplo de seleção

## Relação cliente

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
    </tr>
    <tr>
      <td>t₂</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
    </tr>
    <tr>
      <td>t₃</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
    </tr>
    <tr>
      <td>t₄</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
    </tr>
  </tbody>
</table>

- Consulta: "Informe os clientes com saldo maior ou igual a 100"

SQL
```sql
SELECT * FROM cliente
WHERE saldo >= 100;
```

Expressão algébrica
$\sigma_{saldo\geq100}(Cliente)$

---


## Page 6

IFMG
&lt;page_number&gt;5&lt;/page_number&gt;

# Exemplo de seleção

## Relação cliente

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
    </tr>
    <tr>
      <td>t₂</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
    </tr>
    <tr>
      <td>t₃</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
    </tr>
    <tr>
      <td>t₄</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
    </tr>
  </tbody>
</table>

- Consulta: “Informe os clientes com saldo maior ou igual a 100”

## SQL

```sql
SELECT * FROM cliente
WHERE saldo >= 100;
```

## Expressão algébrica

$\sigma_{\text{saldo}\geq 100}(\text{cliente})$

---


## Page 7

IFMG
Projeção
&lt;page_number&gt;6&lt;/page_number&gt;

* A operação de projeção projeta as colunas selecionadas de uma relação (é uma espécie de seleção vertical)
  π<atributos>(<relação>)
* Os atributos são separados por vírgula

---


## Page 8

&lt;page_number&gt;7&lt;/page_number&gt;

IFMG

# Exemplo de Projeção

## Relação cliente

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
    </tr>
    <tr>
      <td>t₂</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
    </tr>
    <tr>
      <td>t₃</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
    </tr>
    <tr>
      <td>t₄</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
    </tr>
  </tbody>
</table>

- Consulta: "Informe o nome e endereço dos clientes"

SQL
```sql
SELECT nome_cliente, endereco
FROM cliente;
```

Expressão algébrica
$\pi_{nome\_cliente,endereco}(Cliente)$

---


## Page 9

&lt;page_number&gt;7&lt;/page_number&gt;

IFMG

# Exemplo de Projeção

## Relação cliente

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
    </tr>
    <tr>
      <td>t₂</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
    </tr>
    <tr>
      <td>t₃</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
    </tr>
    <tr>
      <td>t₄</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
    </tr>
  </tbody>
</table>

*   Consulta: “Informe o nome e endereço dos clientes”

## SQL

```sql
SELECT nome_cliente, endereco
FROM cliente;
```

## Expressão algébrica

π<sub>nome_cliente,endereco</sub>(cliente)

---


## Page 10

IFMG
&lt;page_number&gt;8&lt;/page_number&gt;

# Exemplo de seleção e projeção

## Relação cliente

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
    </tr>
    <tr>
      <td>t₂</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
    </tr>
    <tr>
      <td>t₃</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
    </tr>
    <tr>
      <td>t₄</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
    </tr>
  </tbody>
</table>

- Consulta: "Informe o nome e endereço dos clientes com saldo maior ou igual 100"

## SQL

```sql
SELECT nome_cliente, endereco
FROM cliente
WHERE saldo >= 100;
```

## Expressão algébrica

$\pi_{nome\_cliente,endereco}(\sigma_{saldo\geq100}(cliente))$

---


## Page 11

IFMG
&lt;page_number&gt;8&lt;/page_number&gt;

# Exemplo de seleção e projeção

## Relação cliente

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
    </tr>
    <tr>
      <td>t₂</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
    </tr>
    <tr>
      <td>t₃</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
    </tr>
    <tr>
      <td>t₄</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
    </tr>
  </tbody>
</table>

*   Consulta: "Informe o nome e endereço dos clientes com saldo maior ou igual 100"

## SQL

```sql
SELECT nome_cliente, endereco
FROM cliente
WHERE saldo >= 100;
```

## Expressão algébrica

$\pi_{nome\_cliente,endereco}(\sigma_{saldo\geq100}(cliente))$

---


## Page 12

IFMG
&lt;page_number&gt;9&lt;/page_number&gt;

# Produto Cartesiano

* A operação de produto cartesiano combina as tuplas de duas relações
  `<relação1> × <relação2>`
* O produto cartesiano retorna todas as combinações de tuplas possíveis
* Se a *relação1* possui *n* tuplas e a *relação2* possui *m* tuplas, a relação resultante terá *n × m* tuplas
* As tuplas resultantes terão os atributos das duas relações de entrada

---


## Page 13

IFMG
&lt;page_number&gt;10&lt;/page_number&gt;

# Exemplo de produto cartesiano

## Relação cliente

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
      <th>id_vend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
      <td>10</td>
    </tr>
    <tr>
      <td>t₂</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
      <td>10</td>
    </tr>
    <tr>
      <td>t₃</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
      <td>20</td>
    </tr>
    <tr>
      <td>t₄</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
      <td>20</td>
    </tr>
  </tbody>
</table>

## Relação vendedor

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_vend</th>
      <th>nome_vend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t'₁</td>
      <td>10</td>
      <td>João</td>
    </tr>
    <tr>
      <td>t'₂</td>
      <td>20</td>
      <td>Maria</td>
    </tr>
  </tbody>
</table>

Consulta: "Informe os cliente combinados com os vendedores"

---


## Page 14

IFMG
&lt;page_number&gt;11&lt;/page_number&gt;

# Exemplo de produto cartesiano (resultado)

## SQL

```sql
SELECT *
FROM cliente, vendedor;
```

## Expressão algébrica

cliente × vendedor

## Resultado

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
      <th>id_vend</th>
      <th>id_vend'</th>
      <th>nome_vend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$t_1 \times t'_1$</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
      <td>10</td>
      <td>10</td>
      <td>João</td>
    </tr>
    <tr>
      <td>$t_2 \times t'_1$</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
      <td>10</td>
      <td>10</td>
      <td>João</td>
    </tr>
    <tr>
      <td>$t_3 \times t'_1$</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
      <td>20</td>
      <td>10</td>
      <td>João</td>
    </tr>
    <tr>
      <td>$t_4 \times t'_1$</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
      <td>20</td>
      <td>10</td>
      <td>João</td>
    </tr>
    <tr>
      <td>$t_1 \times t'_2$</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
      <td>10</td>
      <td>20</td>
      <td>Maria</td>
    </tr>
    <tr>
      <td>$t_2 \times t'_2$</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
      <td>10</td>
      <td>20</td>
      <td>Maria</td>
    </tr>
    <tr>
      <td>$t_3 \times t'_2$</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
      <td>20</td>
      <td>20</td>
      <td>Maria</td>
    </tr>
    <tr>
      <td>$t_4 \times t'_2$</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
      <td>20</td>
      <td>20</td>
      <td>Maria</td>
    </tr>
  </tbody>
</table>

---


## Page 15

IFMG
&lt;page_number&gt;12&lt;/page_number&gt;

# Renomeação

* A operação de renomeação permite renomear relações e atributos

```
ρ_{<relação>}(<relação>)
ρ(<A'_1>,...,<A'_n>)(<relação>)
ρ(<A_1>/<A'_1>)(<relação>)
ρ_{<relação>}(<A'_1>,...,<A'_n>)(<relação>)
```

* A renomeação é especialmente útil quando uma tabela precisa de ser usada mais de uma vez em uma expressão

---


## Page 16

IFMG
&lt;page_number&gt;13&lt;/page_number&gt;

# Exemplo de Renomeação

<table>
  <tr>
    <td>
      <b>SQL</b><br>
      SELECT * FROM cliente AS c;
    </td>
    <td>
      <b>Expressão algébrica</b><br>
      $\rho_{c}(\text{cliente})$
    </td>
  </tr>
  <tr>
    <td>
      <b>SQL</b><br>
      SELECT id_cliente AS id, nome_cliente AS n,<br>
      endereco AS e, saldo<br>
      FROM cliente;
    </td>
    <td>
      <b>Expressão algébrica</b><br>
      $\rho_{(id,n,e,saldo)}(\text{cliente})$
    </td>
  </tr>
  <tr>
    <td>
      <b>SQL</b><br>
      SELECT nome_cliente AS nome<br>
      FROM cliente AS c;
    </td>
    <td>
      <b>Expressão algébrica</b><br>
      $\rho_{c(\text{nome_cliente}/\text{nome})}(\text{cliente})$
    </td>
  </tr>
</table>

---


## Page 17

IFMG &lt;page_number&gt;14&lt;/page_number&gt;

# Operações com conjuntos

*   As operações com conjuntos permitem realizar a união, interseção ou diferença entre duas relações
    *   `<relação1> ∪ <relação2>`
    *   `<relação1> ∩ <relação2>`
    *   `<relação1> – <relação2>`
*   As duas relações envolvidas na operação precisam ter o mesmo número de atributos e os domínios dos atributos correspondentes precisam ser idênticos

---


## Page 18

IFMG
&lt;page_number&gt;15&lt;/page_number&gt;

# Exemplo de operações com conjuntos

## SQL
```sql
SELECT nome_cliente FROM cliente
UNION
SELECT nome_vend FROM vendedor;
```
## Expressão algébrica
$\pi_{nome\_cliente}(cliente) \cup \pi_{nome\_vend}(vendedor)$

## SQL
```sql
SELECT nome_cliente FROM cliente
INTERSECT
SELECT nome_vend FROM vendedor;
```
## Expressão algébrica
$\pi_{nome\_cliente}(cliente) \cap \pi_{nome\_vend}(vendedor)$

## SQL
```sql
SELECT nome_cliente FROM cliente
EXCEPT
SELECT nome_vend FROM vendedor;
```
## Expressão algébrica
$\pi_{nome\_cliente}(cliente) - \pi_{nome\_vend}(vendedor)$

---


## Page 19

IFMG
&lt;page_number&gt;16&lt;/page_number&gt;

# Junção

* A operação de junção permite combinar tuplas de duas relações considerando comparações entre os atributos destas relações

`<relação1> x <condição> <relação2>`

* A `<condição>` da junção é semelhante a condição da seleção, mas devem haver comparações entre os atributos da `<relação1>` e da `<relação2>`
* Se a condição for omitida, é feita a junção natural
* Quando as relações participantes possuem atributos homônimos, pode ser feita a *junção natural* sobre estes atributos sem precisar de nenhuma condição
* Também existem traduções para as junções externas da linguagem SQL:

`A ⌈x⌉ B`: LEFT JOIN
`A ⌊x⌋ B`: RIGHT JOIN
`A ⌈x⌉ B`: LEFT RIGHT JOIN

---


## Page 20

IFMG
&lt;page_number&gt;17&lt;/page_number&gt;

# Exemplo de junção: “Informe os cliente e seus vendedores”

## Relação cliente

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
      <th>id_vend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
      <td>10</td>
    </tr>
    <tr>
      <td>t₂</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
      <td>10</td>
    </tr>
    <tr>
      <td>t₃</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
      <td>20</td>
    </tr>
    <tr>
      <td>t₄</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
      <td>20</td>
    </tr>
  </tbody>
</table>

## Relação vendedor

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_vend</th>
      <th>nome_vend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t'₁</td>
      <td>10</td>
      <td>João</td>
    </tr>
    <tr>
      <td>t'₂</td>
      <td>20</td>
      <td>Maria</td>
    </tr>
  </tbody>
</table>

## SQL

```sql
SELECT nome_cliente, nome_vendedor
FROM cliente, vendedor
WHERE cliente.id_vendedor =
    vendedor.id_vendedor
AND saldo > 100;
```

## Expressão algébrica

cliente ⨯(cliente.id_vend=vendedor.id_vend) vendedor

---


## Page 21

IFMG
&lt;page_number&gt;18&lt;/page_number&gt;

Exemplo de junção: “Informe os cliente e seus vendedores”

Relação cliente

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
      <th>id_vend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
      <td>10</td>
    </tr>
    <tr>
      <td>t₂</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
      <td>10</td>
    </tr>
    <tr>
      <td>t₃</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
      <td>20</td>
    </tr>
    <tr>
      <td>t₄</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
      <td>20</td>
    </tr>
  </tbody>
</table>

Relação vendedor

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_vend</th>
      <th>nome_vend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t'₁</td>
      <td>10</td>
      <td>João</td>
    </tr>
    <tr>
      <td>t'₂</td>
      <td>20</td>
      <td>Maria</td>
    </tr>
  </tbody>
</table>

---


## Page 22

IFMG
&lt;page_number&gt;18&lt;/page_number&gt;

Exemplo de junção: “Informe os cliente e seus vendedores”

Relação cliente

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
      <th>id_vend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
      <td>10</td>
    </tr>
    <tr>
      <td>t₂</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
      <td>10</td>
    </tr>
    <tr>
      <td>t₃</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
      <td>20</td>
    </tr>
    <tr>
      <td>t₄</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
      <td>20</td>
    </tr>
  </tbody>
</table>

Relação vendedor

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_vend</th>
      <th>nome_vend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁'</td>
      <td>10</td>
      <td>João</td>
    </tr>
    <tr>
      <td>t₂'</td>
      <td>20</td>
      <td>Maria</td>
    </tr>
  </tbody>
</table>

Resultado

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
      <th>id_vend</th>
      <th>id_vend'</th>
      <th>nome_vend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁''</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
      <td>10</td>
      <td>10</td>
      <td>João</td>
    </tr>
    <tr>
      <td>t₂''</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
      <td>10</td>
      <td>10</td>
      <td>João</td>
    </tr>
  </tbody>
</table>

---


## Page 23

IFMG
&lt;page_number&gt;18&lt;/page_number&gt;

Exemplo de junção: “Informe os cliente e seus vendedores”

Relação cliente

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
      <th>id_vend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
      <td>10</td>
    </tr>
    <tr>
      <td>t₂</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
      <td>10</td>
    </tr>
    <tr>
      <td>t₃</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
      <td>20</td>
    </tr>
    <tr>
      <td>t₄</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
      <td>20</td>
    </tr>
  </tbody>
</table>

Relação vendedor

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_vend</th>
      <th>nome_vend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁'</td>
      <td>10</td>
      <td>João</td>
    </tr>
    <tr>
      <td>t₂'</td>
      <td>20</td>
      <td>Maria</td>
    </tr>
  </tbody>
</table>

Resultado

<table>
  <thead>
    <tr>
      <th></th>
      <th>id_cliente</th>
      <th>nome_cliente</th>
      <th>endereco</th>
      <th>saldo</th>
      <th>id_vend</th>
      <th>id_vend'</th>
      <th>nome_vend</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>t₁''</td>
      <td>1</td>
      <td>José</td>
      <td>Rua X</td>
      <td>90,00</td>
      <td>10</td>
      <td>10</td>
      <td>João</td>
    </tr>
    <tr>
      <td>t₂''</td>
      <td>2</td>
      <td>Cristina</td>
      <td>Avenida 1</td>
      <td>110,00</td>
      <td>10</td>
      <td>10</td>
      <td>João</td>
    </tr>
    <tr>
      <td>t₃''</td>
      <td>3</td>
      <td>Tadeu</td>
      <td>Avenida 3</td>
      <td>234,00</td>
      <td>20</td>
      <td>20</td>
      <td>Maria</td>
    </tr>
    <tr>
      <td>t₄''</td>
      <td>4</td>
      <td>Rodrigo</td>
      <td>Rua X</td>
      <td>37,00</td>
      <td>20</td>
      <td>20</td>
      <td>Maria</td>
    </tr>
  </tbody>
</table>

---


## Page 24

IFMG
&lt;page_number&gt;19&lt;/page_number&gt;

# Funções de agregação

* A operação de função de agregação agrupar tuplas e sumarizar dados de atributos
  `<A₁>,...,<Aₙ> γ <F₁(A'₁)>,...,<F₂(A'm)> (<relação>)`
* Os atributos `<A₁>,...,<Aₙ>` são usados para agrupar os dados e as funções `<F₁(A'₁)>,...,<F₂(A'm)>` realizar a sumarização sobre os atributos `A'₁,...,A'm`
* Podem ser usadas as mesmas funções da linguagem SQL (AVG, SUM, MAX, MIN, COUNT, etc.)

---


## Page 25

IFMG
&lt;page_number&gt;20&lt;/page_number&gt;

# Exemplo de função de agregação

## Relação venda

<table>
  <thead>
    <tr>
      <th>id_cliente</th>
      <th>mes</th>
      <th>valor</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>2015-02</td>
      <td>470,00</td>
    </tr>
    <tr>
      <td>1</td>
      <td>2015-03</td>
      <td>390,00</td>
    </tr>
    <tr>
      <td>3</td>
      <td>2015-03</td>
      <td>230,00</td>
    </tr>
    <tr>
      <td>2</td>
      <td>2015-04</td>
      <td>210,00</td>
    </tr>
    <tr>
      <td>3</td>
      <td>2015-04</td>
      <td>140,00</td>
    </tr>
    <tr>
      <td>2</td>
      <td>2015-05</td>
      <td>110,00</td>
    </tr>
    <tr>
      <td>2</td>
      <td>2015-05</td>
      <td>480,00</td>
    </tr>
  </tbody>
</table>

SQL
```sql
SELECT mes, SUM(valor) FROM venda GROUP BY mes;
```

Expressão algébrica
mes ∑ SUM(valor) (venda)

Resultado

<table>
  <thead>
    <tr>
      <th>mes</th>
      <th>SUM(valor)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2015-02</td>
      <td>470,00</td>
    </tr>
    <tr>
      <td>2015-03</td>
      <td>620,00</td>
    </tr>
    <tr>
      <td>2015-04</td>
      <td>350,00</td>
    </tr>
    <tr>
      <td>2015-05</td>
      <td>590,00</td>
    </tr>
  </tbody>
</table>

Consulta: “Informe total de vendas de cada mês”

---


## Page 26

&lt;page_number&gt;20&lt;/page_number&gt;

IFMG

# Exemplo de função de agregação

## Relação venda

<table>
  <thead>
    <tr>
      <th>id_cliente</th>
      <th>mes</th>
      <th>valor</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>2015-02</td>
      <td>470,00</td>
    </tr>
    <tr>
      <td>1</td>
      <td>2015-03</td>
      <td>390,00</td>
    </tr>
    <tr>
      <td>3</td>
      <td>2015-03</td>
      <td>230,00</td>
    </tr>
    <tr>
      <td>2</td>
      <td>2015-04</td>
      <td>210,00</td>
    </tr>
    <tr>
      <td>3</td>
      <td>2015-04</td>
      <td>140,00</td>
    </tr>
    <tr>
      <td>2</td>
      <td>2015-05</td>
      <td>110,00</td>
    </tr>
    <tr>
      <td>2</td>
      <td>2015-05</td>
      <td>480,00</td>
    </tr>
  </tbody>
</table>

*   Consulta: “Informe total de vendas de cada mês”

## SQL

```sql
SELECT mes, SUM(valor) FROM venda GROUP BY mes;
```

## Expressão algébrica

mes / SUM(valor) (venda)

## Resultado

<table>
  <thead>
    <tr>
      <th>mes</th>
      <th>SUM(valor)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>2015-02</td>
      <td>470,00</td>
    </tr>
    <tr>
      <td>2015-03</td>
      <td>620,00</td>
    </tr>
    <tr>
      <td>2015-04</td>
      <td>350,00</td>
    </tr>
    <tr>
      <td>2015-05</td>
      <td>590,00</td>
    </tr>
  </tbody>
</table>

---


## Page 27

IFMG
&lt;page_number&gt;21&lt;/page_number&gt;

# Eliminação de duplicatas

* A álgebra relacional faz a eliminação de duplicadas em todos os operadores
* Para lidar com duplicatas é preciso utilizar os seguintes operadores de multi-conjunto:
    * Seleção (σ*)
    * Projeção (π*)
    * Junção (×*)
    * União (∪*)
    * Interseção (∩*)
    * Diferença (-*)

---


## Page 28

IFMG &lt;page_number&gt;22&lt;/page_number&gt;

# Planos de execução de consultas

* Uma das importantes aplicações da álgebra relacional está relacionada ao processamento de consultas
* Os SGBD traduzem as consultas para expressões algébricas e, posteriormente, para planos de execução representados por árvores
* Exemplo:

## Consulta
```sql
SELECT nome_cliente, nome_vendedor
FROM cliente, vendedor
WHERE cliente.id_vendedor = vendedor.id_vendedor
AND saldo > 100;
```

## Expressão algébrica
π<sub>nome_cliente, nome_vendedor (σ<sub>saldo &gt; 100</sub>(Cliente ⋈<sub>id_vendedor = id_vendedor</sub> vendedor))</sub>

## Plano de execução

<mermaid>
graph TD
    A[Cliente ⋈<sub>id_vendedor = id_vendedor</sub> vendedor] --> B(σ<sub>saldo &gt; 100</sub>)
    B --> C[π<sub>nome_cliente, nome_vendedor</sub>]
</mermaid>

---


## Page 29

IFMG &lt;page_number&gt;22&lt;/page_number&gt;

# Planos de execução de consultas

*   Uma das importantes aplicações da álgebra relacional está relacionada ao processamento de consultas
*   Os SGBD traduzem as consultas para expressões algébricas e, posteriormente, para planos de execução representados por árvores
*   Exemplo:

## Consulta

```sql
SELECT nome_cliente, nome_vendedor
FROM cliente, vendedor
WHERE cliente.id_vendedor = vendedor.id_vendedor
AND saldo > 100;
```

## Expressão algébrica

`π_{nome_cliente, nome_vendedor} (σ_{saldo > 100} (cliente θ_{id_vendedor=id_vendedor} vendedor))`

## Plano de execução

<mermaid>
graph TD
    A[Cliente] -- θ_{id_vendedor=id_vendedor} --> B[Vendedor]
    C[π_{nome_cliente, nome_vendedor}] --> A
    C --> B
</mermaid>

---


## Page 30

IFMG
Referências
&lt;page_number&gt;23&lt;/page_number&gt;

ELMASRI, R.; NAVATHE, S. B. *Sistemas de banco de dados*. 7. ed. São Paulo: Pearson Addison Wesley, 2018.

RAMAKRISHNAN, R.; GEHRKE, J. *Sistemas de gerenciamento de banco de dados*. 3. ed. São Paulo: McGrawHill, 2008.
