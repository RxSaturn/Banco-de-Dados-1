**Sistemas de Calendários Acadêmicos \- Criação do Banco**

**Banco de Dados I 					Data:** 27/06/2025  
**Nomes:** Henrique Augusto, Henrique Evangelista, Rayssa Mendes  
**Professor:** Marcos Roberto Ribeiro

## **Introdução**

	O sistema de banco de dados proposto permite uma gestão detalhada dos calendários acadêmicos da instituição, oferecendo recursos como categorização, visualização temporal, análises e identificação de conflitos. Além disso, a modelagem adotada facilita a manutenção e atualização das informações, garantindo a integridade e consistência dos dados. As consultas SQL implementadas mostram a flexibilidade e utilidade prática do modelo desenvolvido, possibilitando a extração rápida de informações relevantes para a tomada de decisões administrativas. Dessa forma, o sistema contribui para otimizar o planejamento acadêmico, melhorar a comunicação entre setores e assegurar o cumprimento dos prazos estabelecidos.

## **Metodologia**

	Para o desenvolvimento do sistema de banco de dados do calendário acadêmico, utilizamos a ferramenta **pgAdmin 4**, que é uma interface gráfica robusta para administração e desenvolvimento de bancos de dados PostgreSQL. O processo incluiu a criação do esquema do banco de dados, a definição das tabelas e suas relações, além da inserção dos dados iniciais necessários para o funcionamento do sistema.

As consultas SQL foram elaboradas e testadas diretamente no pgAdmin 4, permitindo validar a eficiência do modelo e a precisão dos resultados retornados. Essa abordagem facilitou a interação com o banco de dados, tornando o processo mais ágil e permitindo ajustes rápidos na estrutura conforme as necessidades do projeto.

## **Projeto Físico do Banco de Dados** 

O projeto físico representa a concretização do modelo lógico em uma estrutura de banco de dados real, pronta para uso. Nesta fase, foi feita a análise das tabelas, os relacionamentos e os tipos de dados adequados, considerando aspectos de desempenho e integridade dos dados. A implementação foi realizada no PostgreSQL por meio do pgAdmin 4, possibilitando a criação de um ambiente funcional para armazenar e manipular as informações acadêmicas de forma eficiente.

# **Criação do Banco**

DROP DATABASE IF EXISTS calendario\_academico;

CREATE DATABASE calendario\_academico;

CREATE TABLE Periodo (  
    Id\_periodo SERIAL PRIMARY KEY,  
    Descricao VARCHAR(30),  
    DataInicial DATE NOT NULL,  
    DataFinal DATE NOT NULL,  
    CONSTRAINT verificar\_datas\_periodo CHECK (DataFinal \>= DataInicial)  
);

CREATE TABLE TipoCalendario (  
    Id\_tipo SERIAL PRIMARY KEY,  
    Sigla CHAR(4) NOT NULL,  
    Nome VARCHAR(30) NOT NULL  
);

CREATE TABLE Calendario (  
    Id\_calendario SERIAL PRIMARY KEY,  
    Id\_tipo INTEGER NOT NULL REFERENCES TipoCalendario(Id\_tipo),       
    Nome VARCHAR(30) NOT NULL,  
    Ano INT NOT NULL CHECK (Ano \>= 2000),  
    DataInicio DATE NOT NULL,  
    DataFim DATE NOT NULL,  
    Ativo BOOLEAN DEFAULT TRUE,  
    CONSTRAINT verificar\_datas\_calendario CHECK (DataFim \>= DataInicio)  
);

CREATE TABLE CategoriaCalendario (  
    Id\_categoria SERIAL PRIMARY KEY,  
    Id\_calendario INTEGER NOT NULL REFERENCES Calendario(Id\_calendario),        
    Id\_periodo INTEGER NOT NULL REFERENCES Periodo(Id\_periodo),      
    Nome VARCHAR(30) NOT NULL,  
    CorAssociada VARCHAR(30),  
    TotalDias INT,  
    DiasSemanasValidos VARCHAR(30),  
    HabilitacaoContagem BOOLEAN  
);

CREATE TABLE Eventos (  
    Id\_evento SERIAL PRIMARY KEY,  
    Id\_categoria INTEGER NOT NULL REFERENCES CategoriaCalendario(Id\_categoria),     
    Titulo VARCHAR(100) NOT NULL,  
    Descricao VARCHAR(255),   
    DataInicio DATE NOT NULL,  
    DataFim DATE NOT NULL,  
    Dia\_todo BOOLEAN DEFAULT FALSE,  
    Local VARCHAR(100),  
    CONSTRAINT check\_datas\_evento CHECK (DataFim \>= DataInicio)  
);

# 

# **Inserção de dados no Banco**

* #  **Inserir períodos acadêmicos**

  INSERT INTO Periodo (Descricao, DataInicial, DataFinal) 

  VALUES 

  ('1º Semestre 2025', '2025-02-01', '2025-07-15'),

  ('2º Semestre 2025', '2025-08-01', '2025-12-20'),

  ('Férias Verão 2025', '2025-12-21', '2026-01-31'),

  ('Recesso Julho 2025', '2025-07-16', '2025-07-31');


* **Inserir tipos de calendário**

  INSERT INTO TipoCalendario (Sigla, Nome) 

  VALUES 

  ('GRAD', 'Graduação'),

  ('POS', 'Pós-Graduação'),

  ('INST', 'Institucional'),

  ('EVEN', 'Eventos Especiais');


*  **Inserir calendários**

  INSERT INTO Calendario (Id\_tipo, Nome, Ano, DataInicio, DataFim, Ativo) 

  VALUES 

  (1, 'Calendário Graduação', 2025, '2025-01-01', '2025-12-31', true),

  (2, 'Calendário Pós-Graduação', 2025, '2025-01-01', '2025-12-31', true),

  (3, 'Calendário Institucional', 2025, '2025-01-01', '2025-12-31', true),

  (4, 'Eventos Acadêmicos', 2025, '2025-01-01', '2025-12-31', true);


*  **Inserir categorias de calendário**

  INSERT INTO CategoriaCalendario (Id\_calendario, Id\_periodo, Nome, CorAssociada, TotalDias, DiasSemanasValidos, HabilitacaoContagem) 


  **VALUES** 

* **Graduação \- 1º Semestre**

  (1, 1, 'Aulas Regulares', '\#3788d8', 120, '12345', true),

  (1, 1, 'Provas', '\#d81b60', 14, '12345', true),

  (1, 1, 'Feriados', '\#8e24aa', NULL, '1234567', false),


*  **Graduação \- 2º Semestre**

  (1, 2, 'Aulas Regulares', '\#3788d8', 120, '12345', true),

  (1, 2, 'Provas', '\#d81b60', 14, '12345', true),

  (1, 2, 'Feriados', '\#8e24aa', NULL, '1234567', false),


*  **Pós-Graduação \- 1º Semestre**

  (2, 1, 'Aulas Pós', '\#4caf50', 90, '12345', true),

  (2, 1, 'Defesas e Seminários', '\#ff9800', NULL, '12345', false),


*  **Institucional \- Ano todo**

  (3, 1, 'Reuniões', '\#795548', NULL, '12345', false),

  (3, 2, 'Reuniões', '\#795548', NULL, '12345', false),


*  **Eventos \- Ano todo**

  (4, 1, 'Palestras', '\#607d8b', NULL, '12345', false),

  (4, 2, 'Congressos', '\#607d8b', NULL, '12345', false);


*  **Inserir eventos**

  INSERT INTO Eventos (Id\_categoria, Titulo, Descricao, DataInicio, DataFim, Dia\_todo, Local) 

  VALUES 

*  **Aulas Regulares \- 1º Semestre**

  (2, 'Início do Período Letivo', 'Início oficial das aulas do 1º semestre', '2025-02-03', '2025-02-03', true, 'Todos os campi'),

  (2, 'Encerramento do 1º Semestre', 'Último dia de aulas regulares', '2025-07-12', '2025-07-12', true, 'Todos os campi'),


*  **Provas \- 1º Semestre**

  (3, 'Semana de Provas P1', 'Primeira avaliação do semestre', '2025-04-07', '2025-04-11', false, 'Conforme grade de horários'),

  (3, 'Semana de Provas P2', 'Segunda avaliação do semestre', '2025-06-23', '2025-06-27', false, 'Conforme grade de horários'),

  (3, 'Exames Finais', 'Exames de recuperação final', '2025-07-07', '2025-07-11', false, 'Conforme grade de horários'),


*  **Feriados \- 1º Semestre**

  (4, 'Carnaval', 'Feriado nacional', '2025-03-04', '2025-03-04', true, NULL),

  (4, 'Tiradentes', 'Feriado nacional', '2025-04-21', '2025-04-21', true, NULL),

  (4, 'Dia do Trabalho', 'Feriado nacional', '2025-05-01', '2025-05-01', true, NULL),


*  **Aulas Regulares \- 2º Semestre**

  (5, 'Início do 2º Semestre', 'Início oficial das aulas do 2º semestre', '2025-08-04', '2025-08-04', true, 'Todos os campi'),

  (5, 'Encerramento do Ano Letivo', 'Último dia de aulas do ano letivo', '2025-12-13', '2025-12-13', true, 'Todos os campi'),


*  **Provas \- 2º Semestre**

  (6, 'Semana de Provas P1', 'Primeira avaliação do semestre', '2025-09-29', '2025-10-03', false, 'Conforme grade de horários'),

  (6, 'Semana de Provas P2', 'Segunda avaliação do semestre', '2025-11-24', '2025-11-28', false, 'Conforme grade de horários'),


* **Feriados \- 2º Semestre**

  (7, 'Independência do Brasil', 'Feriado nacional', '2025-09-07', '2025-09-07', true, NULL),

  (7, 'Nossa Senhora Aparecida', 'Feriado nacional', '2025-10-12', '2025-10-12', true, NULL),

  (7, 'Finados', 'Feriado nacional', '2025-11-02', '2025-11-02', true, NULL),

  (7, 'Proclamação da República', 'Feriado nacional', '2025-11-15', '2025-11-15', true, NULL),

  (7, 'Natal', 'Feriado nacional', '2025-12-25', '2025-12-25', true, NULL),


*  **Aulas Pós-Graduação \- 1º Semestre**

  (8, 'Início das Aulas de Pós-Graduação', 'Início das disciplinas de pós', '2025-02-10', '2025-02-10', false, 'Bloco P'),

  (8, 'Encerramento das Aulas de Pós', 'Último dia de aulas do semestre', '2025-07-05', '2025-07-05', false, 'Bloco P'),


* **Defesas e Seminários**

  (9, 'Seminário de Pesquisa', 'Apresentação de projetos de pesquisa', '2025-03-20', '2025-03-20', false, 'Auditório Central'),

  (9, 'Defesa de Dissertação: Maria Silva', 'Inteligência Artificial aplicada à Educação', '2025-05-15', '2025-05-15', false, 'Sala de Defesas 1'),

  (9, 'Defesa de Tese: João Santos', 'Algoritmos evolucionários em problemas de otimização', '2025-06-12', '2025-06-12', false, 'Sala de Defesas 2'),


*  **Reuniões Institucionais \- 1º Semestre**

  (10, 'Reunião do Conselho Universitário', 'Pauta: Orçamento anual', '2025-02-15', '2025-02-15', false, 'Sala do Conselho'),

  (10, 'Reunião de Coordenadores', 'Avaliação do início do semestre', '2025-03-10', '2025-03-10', false, 'Sala de Reuniões A'),

  (10, 'Colegiado de Graduação', 'Discussão de casos discentes', '2025-05-05', '2025-05-05', false, 'Sala de Reuniões B'),


*  **Palestras \- 1º Semestre**

  (11, 'Palestra de Boas-vindas', 'Orientações aos calouros', '2025-02-05', '2025-02-05', false, 'Auditório Principal'),

  (11, 'Palestra: Mercado de Trabalho em TI', 'Palestrante: Empresa BigTech', '2025-04-17', '2025-04-17', false, 'Auditório Principal'),

  (11, 'Palestra: Sustentabilidade Ambiental', 'Palestrante: Dr. Silva Costa', '2025-06-05', '2025-06-05', false, 'Auditório Secundário');


*  **Eventos com sobreposição para testar a detecção de conflitos**

  INSERT INTO Eventos (Id\_categoria, Titulo, Descricao, DataInicio, DataFim, Dia\_todo, Local)

  VALUES

  (11, 'Palestra Especial: Inovação Tecnológica', 'Palestrante convidado internacional', '2025-06-05', '2025-06-05', false, 'Auditório Secundário');

## **Principais Consultas**

*  **Lista todos os eventos ativos do período atual (usando a data atual)**  
  SELECT   
      e.Titulo,  
      e.Descricao,  
      e.DataInicio,  
      e.DataFim,  
      e.Local,  
      cc.Nome AS Categoria  
  FROM   
      Eventos e  
  JOIN   
      CategoriaCalendario cc ON e.Id\_categoria \= cc.Id\_categoria  
  JOIN   
      Calendario c ON cc.Id\_calendario \= c.Id\_calendario  
  JOIN   
      Periodo p ON cc.Id\_periodo \= p.Id\_periodo  
  WHERE   
      c.Ativo \= true  
      AND CURRENT\_DATE BETWEEN p.DataInicial AND p.DataFinal  
      AND e.DataInicio \>= CURRENT\_DATE  
  ORDER BY   
      e.DataInicio;

*  **Contabiliza total de dias letivos, excluindo feriados**  
  SELECT   
      p.Descricao AS Periodo,  
      c.Nome AS Calendario,  
      cc.Nome AS Categoria,  
      cc.TotalDias AS Dias\_Planejados,  
      COUNT(DISTINCT e.DataInicio) AS Dias\_Com\_Eventos,  
      SUM(CASE WHEN e.DataInicio BETWEEN CURRENT\_DATE \- 30 AND CURRENT\_DATE THEN 1 ELSE 0 END) AS Eventos\_Ultimos\_30\_Dias  
  FROM   
      Periodo p  
  JOIN   
      CategoriaCalendario cc ON p.Id\_periodo \= cc.Id\_periodo  
  JOIN   
      Calendario c ON cc.Id\_calendario \= c.Id\_calendario  
  LEFT JOIN   
      Eventos e ON cc.Id\_categoria \= e.Id\_categoria  
  WHERE   
      cc.HabilitacaoContagem \= true  
      AND cc.Nome NOT LIKE '%Feriados%'  
      AND cc.Nome NOT LIKE '%Recessos%'  
  GROUP BY   
      p.Descricao, c.Nome, cc.Nome, cc.TotalDias, p.DataInicial  
  ORDER BY   
      c.Nome, p.DataInicial;  
    
* **Eventos que ocorrem no mesmo local**  
  SELECT   
      e1.Id\_evento AS Evento1\_ID,   
      e1.Titulo AS Evento1\_Titulo,  
      e1.DataInicio AS Evento1\_Inicio,  
      e1.DataFim AS Evento1\_Fim,  
    
      e2.Id\_evento AS Evento2\_ID,  
      e2.Titulo AS Evento2\_Titulo,  
      e2.DataInicio AS Evento2\_Inicio,  
      e2.DataFim AS Evento2\_Fim,  
      e1.Local  
  FROM   
      Eventos e1  
  JOIN   
      Eventos e2 ON   
          e1.Id\_evento \< e2.Id\_evento  
          AND e1.Local \= e2.Local  
          AND e1.Local IS NOT NULL  
          AND e2.Local IS NOT NULL  
          AND e1.DataInicio \<= e2.DataFim  
          AND e1.DataFim \>= e2.DataInicio  
  ORDER BY   
      e1.DataInicio;

*  **Relatório de eventos por categoria e período**  
  SELECT   
      c.Nome AS Calendario,  
      p.Descricao AS Periodo,  
      cc.Nome AS Categoria,  
      COUNT(e.Id\_evento) AS Total\_Eventos,  
      MIN(e.DataInicio) AS Primeiro\_Evento,  
      MAX(e.DataFim) AS Ultimo\_Evento,  
      SUM(CASE WHEN e.Dia\_todo THEN 1 ELSE 0 END) AS Eventos\_Dia\_Todo  
  FROM   
      Calendario c  
  JOIN   
      CategoriaCalendario cc ON c.Id\_calendario \= cc.Id\_calendario  
  JOIN   
      Periodo p ON cc.Id\_periodo \= p.Id\_periodo  
  LEFT JOIN   
      Eventos e ON cc.Id\_categoria \= e.Id\_categoria  
  WHERE   
      c.Ativo \= true  
      AND c.Ano \= EXTRACT(YEAR FROM CURRENT\_DATE)  
  GROUP BY   
      c.Nome, p.Descricao, cc.Nome, p.DataInicial  
  ORDER BY   
      p.DataInicial, cc.Nome;

*  **Feriados que caem em dias letivos**   
  SELECT   
      f.Titulo AS Feriado,  
      f.DataInicio AS Data,  
      TO\_CHAR(f.DataInicio, 'Day') AS Dia\_Semana,  
      p.Descricao AS Periodo,  
      cc\_aulas.Nome AS Categoria\_Afetada  
  FROM   
      Eventos f  
  JOIN   
      CategoriaCalendario cc\_feriados ON f.Id\_categoria \= cc\_feriados.Id\_categoria  
  JOIN   
      Periodo p ON cc\_feriados.Id\_periodo \= p.Id\_periodo  
  JOIN   
      CategoriaCalendario cc\_aulas ON   
          cc\_aulas.Id\_periodo \= p.Id\_periodo   
          AND cc\_aulas.Nome LIKE '%Aulas%'  
  WHERE   
      cc\_feriados.Nome LIKE '%Feriados%'  
      AND EXTRACT(ISODOW FROM f.DataInicio) BETWEEN 1 AND 5 \-- Segunda a Sexta  
      AND EXTRACT(YEAR FROM f.DataInicio) \= EXTRACT(YEAR FROM CURRENT\_DATE)  
  ORDER BY   
      f.DataInicio;

*  **Encontrar lacunas no calendário (períodos de mais de 7 dias sem eventos)**  
  WITH EventosDatas AS (  
      SELECT   
          cc.Id\_calendario,  
          e.DataInicio AS Data,  
          ROW\_NUMBER() OVER (PARTITION BY cc.Id\_calendario ORDER BY e.DataInicio) AS Seq  
      FROM   
          Eventos e  
      JOIN   
          CategoriaCalendario cc ON e.Id\_categoria \= cc.Id\_categoria  
      WHERE   
          EXTRACT(YEAR FROM e.DataInicio) \= EXTRACT(YEAR FROM CURRENT\_DATE)  
      GROUP BY   
          cc.Id\_calendario, e.DataInicio  
  )  
  SELECT   
      c.Nome AS Calendario,  
      ed1.Data AS Data\_Anterior,  
      ed2.Data AS Proxima\_Data,  
      (ed2.Data \- ed1.Data) AS Dias\_Sem\_Eventos  
  FROM   
      EventosDatas ed1  
  JOIN   
      EventosDatas ed2 ON   
          ed1.Id\_calendario \= ed2.Id\_calendario  
          AND ed1.Seq \+ 1 \= ed2.Seq  
  JOIN   
      Calendario c ON ed1.Id\_calendario \= c.Id\_calendario  
  WHERE   
      (ed2.Data \- ed1.Data) \> 7  
  ORDER BY   
      c.Nome, ed1.Data;

*  **Visualização do calendário atual**  
  SELECT   
      c.Nome AS Calendario,  
      c.Ano,  
      COUNT(DISTINCT cc.Id\_categoria) AS Total\_Categorias,  
      COUNT(DISTINCT e.Id\_evento) AS Total\_Eventos,  
        
      COUNT(DISTINCT CASE   
      WHEN e.DataInicio \>= CURRENT\_DATE   
      THEN e.Id\_evento END) AS Eventos\_Futuros,  
        
      COUNT(DISTINCT CASE   
      WHEN e.DataInicio \< CURRENT\_DATE   
      THEN e.Id\_evento END) AS Eventos\_Passados,  
        
      MIN(e.DataInicio) AS Primeiro\_Evento,  
      MAX(e.DataFim) AS Ultimo\_Evento,  
      CASE   
          WHEN CURRENT\_DATE BETWEEN MIN(p.DataInicial) AND MAX(p.DataFinal)   
          THEN 'Em andamento'  
    
          WHEN CURRENT\_DATE \< MIN(p.DataInicial)   
          THEN 'Não iniciado'  
    
          ELSE 'Encerrado'  
      END AS Status  
  FROM   
      Calendario c  
  JOIN   
      CategoriaCalendario cc ON c.Id\_calendario \= cc.Id\_calendario  
  JOIN   
      Periodo p ON cc.Id\_periodo \= p.Id\_periodo  
  LEFT JOIN   
      Eventos e ON cc.Id\_categoria \= e.Id\_categoria  
  WHERE   
      c.Ativo \= true  
  GROUP BY   
      c.Nome, c.Ano  
  ORDER BY   
      c.Ano DESC;

* **Calendário mensal (eventos de um mês específico (Junho) )**  
  SELECT  
      e.Titulo,  
      e.Descricao,  
      cc.Nome AS Categoria,  
      e.DataInicio,  
      e.DataFim,  
      e.Local,  
      e.Dia\_todo,  
      c.Nome AS Calendario  
        
  FROM   
      Eventos e  
  JOIN   
      CategoriaCalendario cc ON e.Id\_categoria \= cc.Id\_categoria  
  JOIN   
      Calendario c ON cc.Id\_calendario \= c.Id\_calendario  
  WHERE   
      EXTRACT(MONTH FROM e.DataInicio) \= 6 \-- Junho  
      AND EXTRACT(YEAR FROM e.DataInicio) \= 2025  
  ORDER BY   
      e.DataInicio, e.Titulo;  
    
*  **Análise entre períodos (De um ano em específico (2025) )**  
  SELECT   
      p.Descricao AS Periodo,  
      COUNT(e.Id\_evento) AS Total\_Eventos,  
      COUNT(DISTINCT cc.Nome) AS Categorias\_Utilizadas,  
        
      COUNT(DISTINCT CASE   
      WHEN cc.Nome LIKE '%Aulas%'   
      THEN e.Id\_evento END) AS Eventos\_Aulas,  
        
      COUNT(DISTINCT CASE   
      WHEN cc.Nome LIKE '%Provas%'   
      THEN e.Id\_evento END) AS Eventos\_Provas,  
        
      COUNT(DISTINCT CASE   
      WHEN cc.Nome LIKE '%Feriados%'   
      THEN e.Id\_evento END) AS Feriados,  
        
      MAX(p.DataFinal) \- MIN(p.DataInicial) \+ 1 AS Duracao\_Periodo  
  FROM   
      Periodo p  
  JOIN   
      CategoriaCalendario cc ON p.Id\_periodo \= cc.Id\_periodo  
  LEFT JOIN   
      Eventos e ON cc.Id\_categoria \= e.Id\_categoria  
  WHERE   
      EXTRACT(YEAR FROM p.DataInicial) \= 2025  
  GROUP BY   
      p.Descricao  
  ORDER BY   
      MIN(p.DataInicial);  
    
* **Verifica a diferença entre os dias planejados e os eventos criados**  
  SELECT   
      cc.Nome AS Categoria,  
      p.Descricao AS Periodo,  
      cc.TotalDias AS Dias\_Planejados,  
      COUNT(DISTINCT e.DataInicio) AS Dias\_Com\_Eventos,  
      cc.TotalDias \- COUNT(DISTINCT e.DataInicio) AS Diferenca  
  FROM   
      CategoriaCalendario cc  
  JOIN   
      Periodo p ON cc.Id\_periodo \= p.Id\_periodo  
  LEFT JOIN   
      Eventos e ON cc.Id\_categoria \= e.Id\_categoria  
  WHERE   
      cc.HabilitacaoContagem \= true  
  GROUP BY   
      cc.Nome, p.Descricao, cc.TotalDias  
  HAVING   
      cc.TotalDias IS NOT NULL  
  ORDER BY   
      CASE WHEN cc.TotalDias IS NULL THEN 0   
      ELSE   
      ABS(cc.TotalDias \- COUNT(DISTINCT e.DataInicio))   
      END DESC;

## **Conclusão**

O desenvolvimento do sistema de Calendários Acadêmicos permitiu a aplicação prática dos conhecimentos adquiridos na disciplina de Banco de Dados I. A partir da definição do problema, estruturamos um modelo de dados que atende às necessidades de gestão temporal em ambiente acadêmico, implementando-o no PostgreSQL através do pgAdmin 4\.

A criação do banco de dados envolveu a definição cuidadosa de cinco tabelas principais (Periodo, TipoCalendario, Calendario, CategoriaCalendario e Eventos) com seus respectivos relacionamentos. A escolha do tipo DATE para os campos temporais representou uma decisão importante que simplificou o modelo, assim como o uso de SERIAL para os campos de identificação (id).

A inserção de dados demonstrou a eficiência da estrutura criada, permitindo o cadastramento organizado de informações para o ano letivo de 2025, com períodos semestrais bem definidos, categorias de eventos diferenciadas por cores e uma distribuição equilibrada de atividades ao longo do calendário acadêmico.

As consultas SQL desenvolvidas nesta etapa evidenciaram o potencial analítico do banco, possibilitando a extração de informações valiosas como eventos do período atual, contabilização de dias letivos, detecção de conflitos de agendamento e análise da distribuição de atividades por dia da semana. Estas consultas transformam dados brutos em informações estratégicas para a tomada de decisões administrativas.

Com este sistema, instituições de ensino ganham uma ferramenta para facilitar o planejamento e a comunicação de seus calendários acadêmicos, com recursos para criar múltiplos calendários por ano, personalizar categorias de eventos e visualizar informações de forma clara e intuitiva. O trabalho consolidou, portanto, tanto aspectos técnicos quanto práticos da implementação de bancos de dados relacionais voltados à gestão educacional.

