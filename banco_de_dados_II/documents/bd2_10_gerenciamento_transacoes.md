## Page 1

# Banco de dados II

## 10 – Gerenciamento de Transações

Marcos Roberto Ribeiro

Departamento de Engenharia e Computação (DEC)
Curso de Engenharia de Computação
2023

&lt;img&gt;Green square with white grid pattern&lt;/img&gt;
INSTITUTO FEDERAL
Minas Gerais
---
Campus Bambuí

---


## Page 2

IFMG
&lt;page_number&gt;2&lt;/page_number&gt;

# Introdução

*   Considere um banco de dados de reserva de passagens aéreas com diversos clientes reservando assentos simultaneamente
*   O Sistema de Gerenciamento de Banco de Dados (SGBD) deve evitar conflitos
*   Por exemplo, se dois clientes tentarem reservar o mesmo assento
*   Além disso, o SGBD deve proteger os dados de falhas
*   As alterações em memória que ainda não foram persistidas, devem ser restauradas
*   Determinadas aplicações podem alterar o banco de dados por meio de transações
*   Uma transação é uma execução de comandos de leitura e escrita realizada como se fosse uma única operação
*   O SGBD deve executar transações concorrentes de forma que cada transação não se preocupe com as demais

---


## Page 3

IFMG &lt;page_number&gt;3&lt;/page_number&gt;

# As propriedades ACID

Para um efetivo controle de transações, o SGBD deve garantir quatro propriedades importantes:

1.  As transações devem ser **atômicas**, ou todas as ações são executadas ou nenhuma é. Por exemplo, débito em uma conta corrente e crédito em outra para transferências
2.  As transações devem preservar a **consistência** do banco de dados. Por exemplo, o total de uma venda deve ser a soma dos valores de seus itens
3.  Cada transação deve ser **isolada** das demais, o SGBD pode intercalar operações de várias transações para melhorar o desempenho, mas uma transação não pode comprometer a execução de outra
4.  Depois que o SGBD informou que uma transação foi concluída, seus efeitos devem persistir, mesmo que ocorram falhas. Essa propriedades é chamada de **durabilidade**

---


## Page 4

&lt;page_number&gt;4&lt;/page_number&gt;

IFMG

# Consistência e Isolamento

* A consistência da transação deve ser garantida pelo usuário ou programa que manipula o banco de dados

## Exemplo

* A venda de um produto deve reduzir sua quantidade em estoque
* Quando um produto é adicionado na tabela de vendas, o banco de dados está em um estado inconsistente
* Quando a quantidade vendida é subtraída do estoque do produto, o banco de dados volta a ser consistente

* A propriedade de isolamento deve garantir que, mesmo com a intercalação de ações de várias transações, o resultado seria o mesmo que executar as transações uma após a outra

---


## Page 5

IFMG
&lt;page_number&gt;5&lt;/page_number&gt;

# Atomicidade e durabilidade

*   As transações podem ser incompletas pelos seguintes motivos:
    *   Uma transação pode ser cancelada pelo SGBD devido a uma anomalia
    *   Podem ocorrer falhas que comprometam a execução do SGBD
    *   Nesses casos, o SGBD reinicia a transação automaticamente
*   Uma transação interrompida pode deixar o banco de dados inconsistente, portanto o SGBD deve remover os efeitos de transações interrompidas (garantia da atomicidade)
*   Os SGBDs utilizam sistemas de log para garantir a durabilidade
*   Se houverem falhas antes da gravação em disco, o log é usado para restaurar o banco de dados

---


## Page 6

IFMG
&lt;page_number&gt;6&lt;/page_number&gt;

# Transações e plano de execução

*   O SGBD enxerga uma transação como uma lista de ações de escrita ou leitura sobre objetos
*   Além disso, uma transação deve finalizar com uma efetivação ou cancelamento
    *   $R_T(O)$: Leitura do objeto O pela transação T
    *   $W_T(O)$: Gravação no objeto O pela transação T
    *   $ROLL_T$: Cancelamento (rollback) da transação T
    *   $COMM_T$: Efetivação (commit) da transação T

---


## Page 7

IFMG
&lt;page_number&gt;7&lt;/page_number&gt;

# Plano de execução

*   Um **plano de execução** é uma lista de ações de um conjunto de transações.
*   Um plano é **completo** se todas as suas transações possuírem cancelamento ou efetivação
*   Quando as ações das transações não intercalam, o plano é chamado de **serial**

<table>
  <thead>
    <tr>
      <th colspan="2">Exemplo de plano</th>
    </tr>
    <tr>
      <th>T1</th>
      <th>T2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>R(A)</td>
      <td></td>
    </tr>
    <tr>
      <td>W(A)</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>R(B)</td>
    </tr>
    <tr>
      <td></td>
      <td>W(B)</td>
    </tr>
    <tr>
      <td></td>
      <td>R(C)</td>
    </tr>
    <tr>
      <td></td>
      <td>W(C)</td>
    </tr>
  </tbody>
</table>

---


## Page 8

IFMG
&lt;page_number&gt;8&lt;/page_number&gt;

# Execução concorrente de transações

*   Garantir a intercalação de transações é difícil, mas necessário por motivos de desempenho
*   Enquanto uma transação aguarda um reposta de disco, a CPU pode processar outra transação
*   Isso aumenta o throughput (número médio de transação completas)
*   A execução intercalada de uma transação curta com uma longa, permite que a curta termine rapidamente

---


## Page 9

IFMG
&lt;page_number&gt;9&lt;/page_number&gt;

# Serialidade

*   Um plano de execução serializável sobre um conjunto de transações efetivadas é um plano de execução equivalente a um plano de execução serial completo

<table>
  <thead>
    <tr>
      <th>Plano 1</th>
      <th>Plano 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        T1<br>
        R(A)<br>
        W(A)<br><br>
        R(B)<br>
        w(B)<br><br>
        COMM
      </td>
      <td>
        T2<br>
        R(A)<br>
        W(A)<br><br>
        R(A)<br>
        R(B)<br>
        R(B)<br>
        W(B)<br><br>
        w(A)<br>
        R(B)<br>
        W(B)<br><br>
        COMM
      </td>
    </tr>
  </tbody>
</table>

*   O Plano 1 é equivalente a executar T1 e depois T2
*   Já o Plano 2, equivale a executar T2 e depois T1

---


## Page 10

IFMG
&lt;page_number&gt;10&lt;/page_number&gt;

# Anomalias em razão da execução intercalada

*   A execução de transações concorrentes pode deixar um banco de dados inconsistente se houver uma operação de gravação sobre um mesmo objeto executada por mais de uma transação
*   Quando isso ocorre, dizemos que existe conflito entre as ações das transações
*   Existem três situações de conflito:
    *   WR: Gravação seguida de leitura
    *   RW: Leitura seguida de gravação
    *   WW: Gravação seguida de gravação

---


## Page 11

IFMG &lt;page_number&gt;11&lt;/page_number&gt;

# Lendo dados não efetivados (WR)

* Quando uma transação lê um objeto que foi modificado por outra transação não efetivada, ocorre a leitura suja

* Como exemplo, vamos considerar as transações T1 e T2 e duas contas A e B com R$1.000,00 de saldo

* No exemplo, T1 transfere R$100,00 de A para B e T2 acrescenta 10% em A e B

* A transação T2 lê um valor de A gravado por T1, mas T1 ainda não foi efetivada

* Esse plano não é serializável pois o resultado é diferente de qualquer execução serial de T1 e T2

<table>
  <thead>
    <tr>
      <th colspan="3">Exemplo de leitura suja</th>
    </tr>
    <tr>
      <th>T1</th>
      <th>T2</th>
      <th>A</th>
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>R(A)</td>
      <td>1000</td>
      <td>1000</td>
      <td>1000</td>
    </tr>
    <tr>
      <td>W(A)</td>
      <td>900</td>
      <td>1000</td>
      <td>1000</td>
    </tr>
    <tr>
      <td>R(A)</td>
      <td>900</td>
      <td>1000</td>
      <td>1000</td>
    </tr>
    <tr>
      <td>W(A)</td>
      <td>990</td>
      <td>1000</td>
      <td>1000</td>
    </tr>
    <tr>
      <td>R(B)</td>
      <td>990</td>
      <td>1000</td>
      <td>1000</td>
    </tr>
    <tr>
      <td>W(A)</td>
      <td>990</td>
      <td>1100</td>
      <td>1000</td>
    </tr>
    <tr>
      <td>COMM</td>
      <td>990</td>
      <td>1100</td>
      <td>1200</td>
    </tr>
    <tr>
      <td>R(B)</td>
      <td>990</td>
      <td>1100</td>
      <td>1200</td>
    </tr>
    <tr>
      <td>W(B)</td>
      <td>990</td>
      <td>1200</td>
      <td>1200</td>
    </tr>
    <tr>
      <td>COMM</td>
      <td>990</td>
      <td>1200</td>
      <td>1200</td>
    </tr>
  </tbody>
</table>

---


## Page 12

IFMG
&lt;page_number&gt;12&lt;/page_number&gt;

# Leitura não repetível (RW)

* Outra anomalia é quando uma transação T2 altera um objeto A que foi lido por uma transação T1 que está em andamento
* Se T1 ler A novamente, terá um resultado diferente mesmo sem ter alterado A

Exemplo de leitura não repetível

* Essa situação é chamada de leitura não repetível
* Como exemplo, podemos considerar duas transações que tentem sacar R$80,00 de uma conta A com R$100,00 de saldo
* A transação T1 leu o saldo de R$100,00, mas esse saldo foi modificado por T2

<table>
  <thead>
    <tr>
      <th></th>
      <th>T1</th>
      <th>T2</th>
      <th>A</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>R(A)</td>
      <td>R(A)</td>
      <td>100</td>
    </tr>
    <tr>
      <td></td>
      <td>R(A)</td>
      <td>W(A)</td>
      <td>100</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>COMM</td>
      <td>20</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>W(A)</td>
      <td>20</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>COMM</td>
      <td>20</td>
    </tr>
  </tbody>
</table>

---


## Page 13

IFMG &lt;page_number&gt;13&lt;/page_number&gt;

# Sobrescrevendo dados não efetivados (WW)

*   Outro caso de anomalia ocorre quando uma transação T2 sobrescreve um objeto A que foi modificado por uma transação T1 ainda em execução
*   Esse tipo de problema acontece em gravações cegas, ou seja, transações que gravam dados sem fazer leituras

## Exemplo com gravação cega

*   Como exemplo, podemos considerar duas transações T1 e T2 que tentam definir a taxa de juros de aplicações bancárias para 2% e 3%, respectivamente
*   Como regra de negócio, todas as aplicações devem possuir a mesma taxa de juros

<table>
<thead>
<tr>
<th></th>
<th>T1</th>
<th>T2</th>
<th>A</th>
<th>B</th>
</tr>
</thead>
<tbody>
<tr>
<td></td>
<td></td>
<td>W(A)</td>
<td>0.02</td>
<td>?</td>
</tr>
<tr>
<td></td>
<td></td>
<td>W(A)</td>
<td>0.03</td>
<td>?</td>
</tr>
<tr>
<td></td>
<td></td>
<td>W(B)</td>
<td>0.03</td>
<td>0.03</td>
</tr>
<tr>
<td></td>
<td></td>
<td>COMM</td>
<td>0.03</td>
<td>0.03</td>
</tr>
<tr>
<td></td>
<td></td>
<td>W(B)</td>
<td>0.03</td>
<td>0.02</td>
</tr>
<tr>
<td></td>
<td></td>
<td>COMM</td>
<td>0.03</td>
<td>0.02</td>
</tr>
</tbody>
</table>

---


## Page 14

IFMG
&lt;page_number&gt;14&lt;/page_number&gt;

# Leituras fantasmas

- Imagine que uma transação T1 obtenha o saldo médio de todas as contas de uma agência bancária (para isso é preciso ler todas as contas existentes na agência)
- Em seguida, uma outra transação T2 cria novas contas na mesma agência
- Se T1 calcular o saldo médio novamente, chegará a um valor diferente, esse problema é conhecido como leitura fantasma

---


## Page 15

IFMG &lt;page_number&gt;15&lt;/page_number&gt;

# Planos de execução com transações canceladas

*   Até o momento, não consideramos planos com transações canceladas
*   Um plano contendo transações canceladas é serializável se for equivalente a algum plano serial completo contendo apenas suas transações efetivadas
*   Em um plano de execução recuperável, as transações só leem objeto cujas alterações já foram efetivadas
*   Se o plano é recuperável, o cancelamento de uma transação pode ser feito sem que ocorra o cancelamento em cascata

---


## Page 16

IFMG
&lt;page_number&gt;16&lt;/page_number&gt;

# Exemplo com transação cancelada

*   Como exemplo, vamos considerar uma transação T1 que saque R$100,00 de uma conta A e uma transação T2 que transfira R$50,00 de A para B
*   A transação T1 inicia, seguida por T2, mas T1 é cancelada deixando o banco de dados inconsistente
*   Esse plano é chamado de irrecuperável

<table>
  <thead>
    <tr>
      <th colspan="2">Exemplo com transação cancelada</th>
      <th>T1</th>
      <th>T2</th>
      <th>A</th>
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="8"></td>
      <td>R(A)</td>
      <td></td>
      <td></td>
      <td>200</td>
      <td>100</td>
    </tr>
    <tr>
      <td>W(A)</td>
      <td></td>
      <td></td>
      <td>100</td>
      <td>100</td>
    </tr>
    <tr>
      <td>R(A)</td>
      <td></td>
      <td></td>
      <td>100</td>
      <td>100</td>
    </tr>
    <tr>
      <td>W(A)</td>
      <td></td>
      <td></td>
      <td>50</td>
      <td>100</td>
    </tr>
    <tr>
      <td>R(B)</td>
      <td></td>
      <td></td>
      <td>50</td>
      <td>100</td>
    </tr>
    <tr>
      <td>W(B)</td>
      <td></td>
      <td></td>
      <td>50</td>
      <td>150</td>
    </tr>
    <tr>
      <td>COMM</td>
      <td></td>
      <td></td>
      <td>50</td>
      <td>150</td>
    </tr>
    <tr>
      <td>ROLL</td>
      <td></td>
      <td></td>
      <td>200</td>
      <td>150</td>
    </tr>
  </tbody>
</table>

---


## Page 17

IFMG &lt;page_number&gt;17&lt;/page_number&gt;

# Controle de concorrência baseado em bloqueio

* Para evitar os problemas visto até o momento, os SGBDs utilizam protocolos de bloqueio
* Um dos protocolos mais usados pelos SGBD é o Strict 2PL (Two-Phase Locking). Ele possui duas regras:
    * 1 Para ter acesso a um objeto, uma transação precisa solicitar um bloqueio sobre o mesmo. O bloqueio pode ser compartilhado para leitura ou exclusivo para leitura e escrita
    * 2 Todos os bloqueios de uma transação são liberados após o seu término
* Uma transação que solicita um bloqueio é suspensa até que o SGBD seja capaz de garantir o bloqueio solicitado
* O SGBD monitora os bloqueios que concedeu e garante que, se uma transação mantiver um bloqueio exclusivo sobre um objeto, nenhuma outra conseguirá um bloqueio compartilhado ou exclusivo sobre o mesmo objeto

---


## Page 18

IFMG Exemplo com Strict 2PL &lt;page_number&gt;18&lt;/page_number&gt;

<table>
  <thead>
    <tr>
      <th colspan="3">Plano com conflito WR</th>
      <th colspan="3">Plano com Strict 2PL</th>
    </tr>
    <tr>
      <th>T1</th>
      <th>T2</th>
      <th>A</th>
      <th>B</th>
      <th>T1</th>
      <th>T2</th>
      <th>A</th>
      <th>B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>R(A)</td>
      <td></td>
      <td>1000</td>
      <td>1000</td>
      <td>SX(A)</td>
      <td></td>
      <td>1000</td>
      <td>1000</td>
    </tr>
    <tr>
      <td>W(A)</td>
      <td></td>
      <td>900</td>
      <td>1000</td>
      <td>SX(B)</td>
      <td></td>
      <td>1000</td>
      <td>1000</td>
    </tr>
    <tr>
      <td></td>
      <td>R(A)</td>
      <td>900</td>
      <td>1000</td>
      <td>X(A)</td>
      <td></td>
      <td>1000</td>
      <td>1000</td>
    </tr>
    <tr>
      <td></td>
      <td>W(A)</td>
      <td>990</td>
      <td>1000</td>
      <td>X(B)</td>
      <td></td>
      <td>1000</td>
      <td>1000</td>
    </tr>
    <tr>
      <td></td>
      <td>R(B)</td>
      <td>990</td>
      <td>1000</td>
      <td>R(A)</td>
      <td></td>
      <td>1000</td>
      <td>1000</td>
    </tr>
    <tr>
      <td></td>
      <td>W(A)</td>
      <td>990</td>
      <td>1100</td>
      <td>W(A)</td>
      <td></td>
      <td>900</td>
      <td>1000</td>
    </tr>
    <tr>
      <td></td>
      <td>COMM</td>
      <td>990</td>
      <td>1100</td>
      <td>SX(A)</td>
      <td></td>
      <td>900</td>
      <td>1000</td>
    </tr>
    <tr>
      <td>R(B)</td>
      <td></td>
      <td>990</td>
      <td>1100</td>
      <td>SX(B)</td>
      <td></td>
      <td>900</td>
      <td>1000</td>
    </tr>
    <tr>
      <td>W(B)</td>
      <td></td>
      <td>990</td>
      <td>1200</td>
      <td>R(B)</td>
      <td></td>
      <td>900</td>
      <td>1000</td>
    </tr>
    <tr>
      <td>COMM</td>
      <td></td>
      <td>990</td>
      <td>1200</td>
      <td>W(B)</td>
      <td></td>
      <td>900</td>
      <td>1100</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>COMM</td>
      <td></td>
      <td>900</td>
      <td>1100</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>X(A)</td>
      <td></td>
      <td>900</td>
      <td>1100</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>X(B)</td>
      <td></td>
      <td>900</td>
      <td>1100</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>R(A)</td>
      <td></td>
      <td>900</td>
      <td>1100</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>W(A)</td>
      <td></td>
      <td>990</td>
      <td>1100</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>R(B)</td>
      <td></td>
      <td>990</td>
      <td>1100</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>W(B)</td>
      <td></td>
      <td>990</td>
      <td>1210</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>COMM</td>
      <td></td>
      <td>990</td>
      <td>1210</td>
    </tr>
  </tbody>
</table>

*   SX(A): Solicitação de bloqueio exclusivo para A
*   X(A): Confirmação de bloqueio exclusivo para A
*   As transações não precisam fazer os pedidos de bloqueio explicitamente, o SGBD pode identificá-los

---


## Page 19

&lt;page_number&gt;19&lt;/page_number&gt;

IFMG

# Ações intercaladas

## Strict 2PL com intercalação

<table>
  <thead>
    <tr>
      <th>T1</th>
      <th>T2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SS(A)<br>S(A)</td>
      <td>SS(A)<br>S(A)<br>R(A)<br>SX(B)<br>X(B)<br>R(B)<br>W(B)<br>COMM</td>
    </tr>
    <tr>
      <td></td>
      <td>SX(C)<br>X(C)<br>R(C)<br>W(C)<br>COMM</td>
    </tr>
  </tbody>
</table>

*   No exemplo anterior, o protocolo **Strict 2PL** obrigou a execução serial das transações T1 e T2
*   Porém, existirão muitas situações onde será possível a intercalação de ações de transações

---


## Page 20

IFMG
&lt;page_number&gt;20&lt;/page_number&gt;

# Impasses (deadlocks)

## Exemplo de Impasse

<table>
  <tr>
    <td>T1</td>
    <td>T2</td>
  </tr>
  <tr>
    <td>SX(A)</td>
    <td></td>
  </tr>
  <tr>
    <td>S(A)</td>
    <td></td>
  </tr>
  <tr>
    <td></td>
    <td>SX(B)</td>
  </tr>
  <tr>
    <td></td>
    <td>X(B)</td>
  </tr>
  <tr>
    <td>SX(B)</td>
    <td></td>
  </tr>
  <tr>
    <td></td>
    <td>SX(A)</td>
  </tr>
  <tr>
    <td>...</td>
    <td>...</td>
  </tr>
</table>

*   T1 espera o término de um bloqueio de T2 e vice-versa
*   Essa situação é chamada de **impasse (deadlock)**
*   Tais transações não farão progresso e manterão bloqueios que podem ser solicitados por outras transações
*   O SGBD deve resolver essas situações

---


## Page 21

IFMG
&lt;page_number&gt;21&lt;/page_number&gt;

# Transações em SQL

*   Na linguagem SQL, o usuário pode ajustar modo de acesso e nível de isolamento das transações através da instrução **SET TRANSACTION**

    SET TRANSACTION ISOLATION LEVEL
    <nível de isolamento>
    <modo de acesso>;

*   O modo de acesso pode ser:
    *   **READ WRITE**: As transações podem fazer alterações
    *   **READ ONLY**: As transações podem fazer apenas leituras

---


## Page 22

IFMG
&lt;page_number&gt;22&lt;/page_number&gt;

# Nível de isolamento

* O nível de isolamento controla até que ponto uma transação pode ser afetada pelas demais

## Níveis de isolamento

<table>
  <thead>
    <tr>
      <th>Nível</th>
      <th>Leitura suja</th>
      <th>Leitura não repetível</th>
      <th>Leitura fantasma</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>READ UNCOMMITTED</td>
      <td>Possível</td>
      <td>Possível</td>
      <td>Possível</td>
    </tr>
    <tr>
      <td>READ COMMITTED</td>
      <td>Impossível</td>
      <td>Possível</td>
      <td>Possível</td>
    </tr>
    <tr>
      <td>REPEATABLE READ</td>
      <td>Impossível</td>
      <td>Impossível</td>
      <td>Possível</td>
    </tr>
    <tr>
      <td>SERIALIZABLE</td>
      <td>Impossível</td>
      <td>Impossível</td>
      <td>Impossível</td>
    </tr>
  </tbody>
</table>

* O nível de isolamento **READ COMMITTED** é o padrão utilizado pelo PostgreSQL e também não permite sobrescrever dados não efetivados

---


## Page 23

IFMG
&lt;page_number&gt;23&lt;/page_number&gt;

# Nível de isolamento

*   O grau mais alto de isolamento é o **SERIALIZABLE** impedindo, inclusive, que uma transação altere conjunto de dados lidos por outras transações (leitura fantasma)
*   O nível **REPEATABLE READ** garante que uma transação T só leia dados efetivados e nenhum dado lido ou gravado por T pode ser acessado até que T seja efetivada
*   O nível **READ COMMITTED** garante que uma transação T só leia dados efetivados e nenhum dado gravado por T pode ser acessado até que T seja efetivada

---


## Page 24

IFMG
&lt;page_number&gt;24&lt;/page_number&gt;

# Controle de transações no PostgreSQL

- Para demonstrar o funcionamento do controle de transações no PostgreSQL, utilizaremos o seguinte banco de dados:

```sql
CREATE TABLE conta(
    id SERIAL PRIMARY KEY NOT NULL,
    saldo FLOAT NOT NULL
);

INSERT INTO conta(saldo)
VALUES (1000), (500);

---


## Page 25

IFMG
&lt;page_number&gt;25&lt;/page_number&gt;

# Início e fim de transações

*   O início de uma transação é realizado com a instrução **BEGIN**
*   A finalização é feita com os comandos:
    *   **COMMIT**: Solicita a gravação de todas as ações depois do último **BEGIN**
    *   **ROLLBACK**: Solicita o cancelamento de todas as ações desde o último **BEGIN**

## Exemplo com COMMIT

```sql
BEGIN;
INSERT INTO conta(saldo)
VALUES (400);
COMMIT;
SELECT * FROM conta;
```

## Exemplo com ROLLBACK

```sql
BEGIN;
INSERT INTO conta(saldo)
VALUES (700);
SELECT * FROM conta;
ROLLBACK;
SELECT * FROM conta;

---


## Page 26

IFMG
&lt;page_number&gt;26&lt;/page_number&gt;

# Pontos de salvamento

*   É possível controlar os comandos na transação de uma forma mais granular utilizando os pontos de salvamento (savepoints)
*   Os pontos de salvamento permitem cancelar partes da transação seletivamente, e efetivar as demais partes
*   Após definir o ponto de salvamento, através da instrução SAVEPOINT, é possível cancelar a transação até o ponto de salvamento
*   Isso é feito com a instrução ROLLBACK TO
*   Todas as alterações no banco de dados efetuadas entre a definição do ponto de salvamento e o cancelamento são desprezadas, mas as alterações efetuadas antes do ponto de salvamento são mantidas

---


## Page 27

IFMG
&lt;page_number&gt;27&lt;/page_number&gt;

-- Exemplo com SAVEPOINT

BEGIN;

INSERT INTO conta(saldo)
VALUES (2000);
SELECT * FROM conta;

SAVEPOINT a;

INSERT INTO conta(saldo)
VALUES (3000);
SELECT * FROM conta;

ROLLBACK TO a;

SELECT * FROM conta;

ROLLBACK;

SELECT * FROM conta;

---


## Page 28

IFMG
&lt;page_number&gt;28&lt;/page_number&gt;

# Simulando conflito no PostgreSQL

* Agora, vamos simular os conflitos estudados executando transações concorrentes no PostgreSQL
* Para cada tipo de conflito a ser simulado, mudaremos o nível de isolamento das transação para permitir o conflito
* o PostgreSQL utiliza o Multiversion Concurrency Control (MVCC) para controlar a concorrência de transações
* Esse controle, inerentemente, não permite leituras sujas nem sobrescrever dados não efetivados
* Portanto, não conseguiremos simular esses conflitos

---


## Page 29

IFMG
&lt;page_number&gt;29&lt;/page_number&gt;

# Simulando leitura não repetível

*   Para simular o conflito de leitura não repetível, é preciso mudar o nível de isolamento das transações para **READ COMMITTED**
*   Como esse é o nível de isolamento padrão do PostgreSQL, não é preciso executar o **SET TRANSACTION**

<table>
  <thead>
    <tr>
      <th>T1</th>
      <th>T2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>BEGIN;<br>CREATE TEMPORARY TABLE saldo AS SELECT saldo FROM conta WHERE id = 1;</td>
      <td>BEGIN;<br>CREATE TEMPORARY TABLE saldo AS SELECT saldo FROM conta WHERE id = 1;</td>
    </tr>
    <tr>
      <td>UPDATE conta SET saldo=s.saldo - 100 FROM saldo AS s WHERE id = 1;<br>COMMIT;</td>
      <td>UPDATE conta SET saldo=s.saldo - 100 FROM saldo AS s WHERE id = 1;<br>COMMIT;</td>
    </tr>
  </tbody>
</table>

---


## Page 30

IFMG
&lt;page_number&gt;30&lt;/page_number&gt;

# Evitando a leitura não repetível

*   O que aconteceu após a execução das duas transações?
*   Qual o nível de isolamento adequado para executar essas transações?
*   Execute novamente as transações no nível de isolamento correto.

---


## Page 31

IFMG
&lt;page_number&gt;31&lt;/page_number&gt;

# Simulando leitura fantasma

* Para simular o conflito de leitura não repetível, é preciso mudar o nível de isolamento das transações para REPEATABLE READ

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

<table>
  <tr>
    <td><b>T1</b></td>
    <td><b>T2</b></td>
  </tr>
  <tr>
    <td>BEGIN;<br>SELECT AVG(saldo) AS media FROM conta<br>WHERE id &gt;= 1;</td>
    <td>BEGIN;<br>INSERT INTO conta(saldo) VALUES<br>(5000);<br>COMMIT;</td>
  </tr>
  <tr>
    <td>SELECT AVG(saldo) AS media FROM conta<br>WHERE id &gt;= 1;<br>COMMIT;</td>
    <td></td>
  </tr>
</table>

---


## Page 32

IFMG
&lt;page_number&gt;32&lt;/page_number&gt;

# Evitando a leitura fantasma

*   O que aconteceu após a execução das duas transações?
*   Qual o nível de isolamento adequado para executar essas transações?
*   Execute novamente as transações no nível de isolamento correto.

---


## Page 33

IFMG
Exercícios
&lt;page_number&gt;33&lt;/page_number&gt;

Faça as seguintes simulações no PostgreSQL:

1 Plano de execução do slide 16

2 Plano de execução com um impasse

---


## Page 34

<header>IFMG</header>

&lt;page_number&gt;34&lt;/page_number&gt;

# Simulando deadlock

<table>
  <tr>
    <th>T1</th>
    <th>T2</th>
  </tr>
  <tr>
    <td>
      BEGIN;<br>
      UPDATE conta SET saldo = saldo + 100<br>
      WHERE id = 1;<br>
      UPDATE conta SET saldo = saldo - 100<br>
      WHERE id = 2;<br>
      COMMIT;
    </td>
    <td>
      BEGIN;<br>
      UPDATE conta SET saldo = saldo + 100<br>
      WHERE id = 2;<br>
      UPDATE conta SET saldo = saldo - 100<br>
      WHERE id = 1;<br>
      COMMIT;
    </td>
  </tr>
</table>

---


## Page 35

IFMG
&lt;page_number&gt;35&lt;/page_number&gt;

# Referências

DATE, C. J. Introdução a sistemas de bancos de dados. Rio de Janeiro: Elsevier, 2004.

ELMASRI, R.; NAVATHE, S. B. Sistemas de banco de dados. 7. ed. São Paulo: Pearson Addison Wesley, 2018.

RAMAKRISHNAN, R.; GEHRKE, J. Sistemas de gerenciamento de banco de dados. 3. ed. São Paulo: McGrawHill, 2008.

SILBERSCHATZ, A.; KORTH, H. F.; SUDARSHAN, S. Sistema de bancos de dados. 3. ed. São Paulo: Campus, 2007.