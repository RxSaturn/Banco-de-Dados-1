# Sistemas de Calendários Acadêmicos - Aplicação Conectada ao Banco de Dados

**Banco de Dados I**  
**Data:** 01/08/2025  
**Nomes:** Henrique Augusto, Henrique Evangelista, Rayssa Mendes  
**Professor:** Marcos Roberto Ribeiro

## Introdução

Este projeto tem como objetivo o desenvolvimento de um sistema de banco de dados relacional para a gestão de calendários acadêmicos em instituições de ensino. A proposta surgiu da necessidade de centralizar e organizar informações sobre eventos acadêmicos, períodos letivos, categorias de eventos e cursos, proporcionando uma estrutura acessível e eficiente para consulta e manutenção desses dados.

O banco de dados foi implementado utilizando o sistema gerenciador PostgreSQL e conta com recursos como visões (views), regras (rules), funções (functions) e gatilhos (triggers), aplicados conforme as necessidades do sistema para garantir integridade, automação e padronização de operações.

Além da estrutura do banco, este trabalho inclui uma aplicação conectada ao banco de dados, desenvolvida com o objetivo de facilitar a interação com os dados por meio de uma interface simples e funcional. A aplicação permite, por exemplo, a visualização de eventos por período, cadastro de novas informações e atualizações em tempo real.

Este documento apresenta as decisões de modelagem, a estrutura lógica do banco, exemplos de consultas e funcionalidades implementadas, bem como instruções de uso do sistema desenvolvido.

## Metodologia

A terceira etapa do desenvolvimento do banco de dados acadêmico teve como foco a implementação de recursos avançados no sistema gerenciador de banco de dados PostgreSQL, com o objetivo de tornar a estrutura mais funcional, automatizada e eficiente no suporte à gestão de calendários acadêmicos.

Nesta fase, foram criadas diversas visões (views) para facilitar consultas recorrentes e centralizar informações de interesse institucional, como a listagem de eventos ativos, categorização de eventos por tipo e visualizações filtradas por período ou curso.

Também foram desenvolvidas funções (functions) em PL/pgSQL, permitindo encapsular lógicas específicas, como cálculos de intervalos de tempo, validações de datas ou manipulações automatizadas de dados.

Para garantir a integridade e a reatividade do banco, foram definidos gatilhos (triggers) que executam ações automaticamente diante de determinados eventos, como inserções ou atualizações em tabelas sensíveis, mantendo a consistência das informações armazenadas.

Além disso, foram implementadas regras (rules) com o intuito de personalizar o comportamento de comandos SQL em determinadas visões, controlando permissões de escrita e redirecionando operações para as tabelas corretas.

Toda a implementação foi realizada diretamente no PostgreSQL, utilizando comandos SQL e PL/pgSQL. Desenvolvi a aplicação de integração em Python, empregando o microframework web Flask para a camada de apresentação e SQLAlchemy como ORM para mapear, integrar e relacionar os dados do banco de dados, facilitando a comunicação entre a interface e a camada persistente. A integração entre a aplicação e o banco foi testada com endpoints REST básicos e scripts de inicialização de dados; detalhes de implantação e autenticação serão abordados em etapas posteriores do projeto.

## Criação das Visões

As visões (views) são consultas salvas que permitem apresentar os dados de forma organizada e simplificada. Elas são especialmente úteis quando é necessário reutilizar comandos SQL complexos ou quando se deseja restringir o acesso direto às tabelas originais, oferecendo uma camada de abstração mais segura e prática para os usuários. A seguir são apresentadas todas as visões que implementamos no nosso banco de dados:

### Eventos Ativos no Período Atual

```sql
CREATE VIEW vw_eventos_ativos_hoje AS
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
    CategoriaCalendario cc ON e.Id_categoria = cc.Id_categoria
JOIN 
    Calendario c ON cc.Id_calendario = c.Id_calendario
JOIN 
    Periodo p ON cc.Id_periodo = p.Id_periodo
WHERE 
    c.Ativo = true
    AND CURRENT_DATE BETWEEN p.DataInicial AND p.DataFinal
    AND e.DataInicio >= CURRENT_DATE
ORDER BY 
    e.DataInicio;
```

Exemplo de uso:

```sql
SELECT * FROM vw_eventos_ativos_hoje; 
```

### Total de Dias Letivos (excluindo feriados)

```sql
CREATE VIEW vw_dias_letivos AS
SELECT 
    p.Descricao AS Periodo,
    c.Nome AS Calendario,
    cc.Nome AS Categoria,
    cc.TotalDias AS Dias_Planejados,
    COUNT(DISTINCT e.DataInicio) AS Dias_Com_Eventos,
    SUM(CASE WHEN e.DataInicio BETWEEN CURRENT_DATE - 30 AND CURRENT_DATE THEN 1 ELSE 0 END) AS Eventos_Ultimos_30_Dias
FROM 
    Periodo p
JOIN 
    CategoriaCalendario cc ON p.Id_periodo = cc.Id_periodo
JOIN 
    Calendario c ON cc.Id_calendario = c.Id_calendario
LEFT JOIN 
    Eventos e ON cc.Id_categoria = e.Id_categoria
WHERE 
    cc.HabilitacaoContagem = true
    AND cc.Nome NOT LIKE '%Feriados%'
    AND cc.Nome NOT LIKE '%Recessos%'
GROUP BY 
    p.Descricao, c.Nome, cc.Nome, cc.TotalDias, p.DataInicial
ORDER BY 
    c.Nome, p.DataInicial;
```

Exemplo de uso:

```sql
SELECT * FROM vw_dias_letivos; 
```

### Resumo do Calendário

```sql
CREATE VIEW vw_resumo_calendario AS
SELECT 
    c.Id_calendario,
    c.Nome AS NomeCalendario,
    c.Ano,
    c.DataInicio,
    c.DataFim,
    c.Ativo,
    tc.Nome AS TipoCalendario,
    COUNT(DISTINCT cc.Id_categoria) AS TotalCategorias,
    COUNT(e.Id_evento) AS TotalEventos
FROM 
    Calendario c
JOIN 
    TipoCalendario tc ON c.Id_tipo = tc.Id_tipo
LEFT JOIN 
    CategoriaCalendario cc ON c.Id_calendario = cc.Id_calendario
LEFT JOIN 
    Eventos e ON cc.Id_categoria = e.Id_categoria
GROUP BY 
    c.Id_calendario, c.Nome, c.Ano, c.DataInicio, c.DataFim, c.Ativo, tc.Nome
ORDER BY 
    c.Ano DESC, c.Nome;
```

Exemplo de uso:

```sql
SELECT * FROM vw_resumo_calendario; 
```

### Feriados Em Dias Letivos

```sql
CREATE VIEW vw_feriados_dias_letivos AS
SELECT 
    f.Titulo AS Feriado,
    f.DataInicio AS Data,
    TO_CHAR(f.DataInicio, 'Day') AS Dia_Semana,
    p.Descricao AS Periodo,
    cc_aulas.Nome AS Categoria_Afetada
FROM 
    Eventos f
JOIN 
    CategoriaCalendario cc_feriados ON f.Id_categoria = cc_feriados.Id_categoria
JOIN 
    Periodo p ON cc_feriados.Id_periodo = p.Id_periodo
JOIN 
    CategoriaCalendario cc_aulas ON 
    cc_aulas.Id_periodo = p.Id_periodo 
    AND cc_aulas.Nome LIKE '%Aulas%'
WHERE 
    cc_feriados.Nome LIKE '%Feriados%'
    AND EXTRACT(ISODOW FROM f.DataInicio) BETWEEN 1 AND 5 -- Segunda a Sexta
    AND EXTRACT(YEAR FROM f.DataInicio) = EXTRACT(YEAR FROM CURRENT_DATE)
ORDER BY 
    f.DataInicio;
```

Exemplo de uso:

```sql
SELECT * FROM vw_feriados_dias_letivos; 
```

### Eventos Futuros Ativos

```sql
CREATE VIEW vw_eventos_futuros_ativos AS
SELECT 
    e.Id_evento,
    e.Titulo,
    e.DataInicio,
    e.DataFim,
    c.Nome AS calendario,
    cc.Nome AS categoria
FROM Eventos e
JOIN CategoriaCalendario cc ON e.Id_categoria = cc.Id_categoria
JOIN Calendario c ON cc.Id_calendario = c.Id_calendario
WHERE 
    c.Ativo = TRUE 
    AND e.DataInicio > CURRENT_DATE;
```

Exemplo de uso:

```sql
SELECT * FROM vw_eventos_futuros_ativos;
```

### Feriados do ano

```sql
CREATE VIEW vw_feriados_do_ano AS
SELECT 
    e.Id_evento,
    e.Titulo AS feriado,
    e.DataInicio,
    e.DataFim,
    c.Nome AS calendario
FROM Eventos e
JOIN CategoriaCalendario cc ON e.Id_categoria = cc.Id_categoria
JOIN Calendario c ON cc.Id_calendario = c.Id_calendario
WHERE 
    c.Ativo = TRUE
    AND LOWER(cc.Nome) LIKE '%feriado%'
    AND EXTRACT(YEAR FROM e.DataInicio) = EXTRACT(YEAR FROM CURRENT_DATE);
```

Exemplo de uso:

```sql
SELECT * FROM vw_feriados_do_ano;
```

### Dias letivos por periodo

```sql
CREATE OR REPLACE VIEW vw_dias_letivos_por_periodo AS
SELECT 
    p.Descricao AS periodo,
    COUNT(DISTINCT e.DataInicio) AS total_dias_letivos
FROM 
    Periodo p
JOIN 
    CategoriaCalendario cc ON p.Id_periodo = cc.Id_periodo
JOIN 
    Eventos e ON cc.Id_categoria = e.Id_categoria
WHERE 
    cc.HabilitacaoContagem = true
    AND cc.Nome NOT LIKE '%Feriados%'
    AND cc.Nome NOT LIKE '%Recessos%'
GROUP BY 
    p.Descricao
ORDER BY 
    p.Descricao;
```

Exemplo de uso:

```sql
SELECT * FROM vw_dias_letivos_por_periodo;
```

## Criação das Regras

As regras (rules) são mecanismos que modificam ou redirecionam a execução de comandos SQL, como INSERT, UPDATE ou DELETE. No contexto deste projeto, elas foram utilizadas principalmente para permitir a inserção de dados diretamente em visões específicas, garantindo que essas operações fossem devidamente refletidas nas tabelas envolvidas, mantendo a integridade dos dados. A seguir são apresentadas todas as regras que implementamos no nosso banco de dados:

### Impedir Inserção De Eventos Em Calendários Inativos

```sql
CREATE RULE impedir_delete_periodo_utilizado AS
ON DELETE TO Periodo
WHERE EXISTS (
    SELECT 1
    FROM CategoriaCalendario
    WHERE Id_periodo = OLD.Id_periodo
)
DO INSTEAD NOTHING;
```

### Desativar Calendário encerrado

```sql
CREATE RULE desativar_calendario_encerrado AS
ON UPDATE TO Calendario
WHERE NEW.Ativo = TRUE AND NEW.DataFim < CURRENT_DATE
DO INSTEAD
UPDATE Calendario
SET Ativo = FALSE
WHERE Id_calendario = NEW.Id_calendario;
```

### Impedir exclusão de períodos que estão sendo usados

```sql
CREATE RULE impedir_delete_periodo_utilizado AS
ON DELETE TO Periodo
WHERE EXISTS (
    SELECT 1
    FROM CategoriaCalendario
    WHERE Id_periodo = OLD.Id_periodo
)
DO INSTEAD NOTHING;
```

### Impedir Ativação De Calendários Com Datas Inválidas

```sql
CREATE RULE bloquear_ativacao_calendario_invalido AS
ON UPDATE TO Calendario
WHERE NEW.Ativo = TRUE AND NEW.DataFim < NEW.DataInicio
DO INSTEAD NOTHING;
```

## Criação das Funções

As funções (functions) são blocos de código armazenados no banco, escritos em PL/pgSQL (ou outras linguagens suportadas), que executam tarefas específicas quando chamadas. Elas permitem encapsular lógicas de negócio, cálculos, verificações e manipulações de dados, tornando o sistema mais modular, reutilizável e organizado. A seguir são apresentadas todas as funções que implementamos nosso banco de dados:

### Calcular a Duração Total De Um Período em Dias

```sql
CREATE OR REPLACE FUNCTION calcular_duracao_periodo(id_per INTEGER)
RETURNS INTEGER AS $$
DECLARE
    dias INTEGER;
BEGIN
    SELECT (DataFinal - DataInicial) INTO dias
    FROM Periodo
    WHERE Id_periodo = id_per;

    RETURN dias;
END;
$$ LANGUAGE plpgsql;
```

Exemplo de uso:

```sql
SELECT calcular_duracao_periodo(1);
```

### Contar Total de Eventos Em Uma Categoria Específica

```sql
CREATE OR REPLACE FUNCTION contar_eventos_por_categoria(id_cat INTEGER)
RETURNS INTEGER AS $$
DECLARE
    total INTEGER;
BEGIN
    SELECT COUNT(*) INTO total
    FROM Eventos
    WHERE Id_categoria = id_cat;

    RETURN total;
END;
$$ LANGUAGE plpgsql;
```

Exemplo de uso:

```sql
SELECT contar_eventos_por_categoria(2);
```

### Verificar Se Um Calendário Está Atualmente Ativo

```sql
CREATE OR REPLACE FUNCTION esta_calendario_ativo(id_cal INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    resultado BOOLEAN;
BEGIN
    SELECT (CURRENT_DATE BETWEEN DataInicio AND DataFim) AND Ativo
    INTO resultado
    FROM Calendario
    WHERE Id_calendario = id_cal;

    RETURN resultado;
END;
$$ LANGUAGE plpgsql;
```

Exemplo de uso:

```sql
SELECT esta_calendario_ativo(1);
```

## Criação dos Gatilhos

Os gatilhos (triggers), por sua vez, são mecanismos que disparam automaticamente uma ação (geralmente a execução de uma função) em resposta a eventos como inserções, atualizações ou exclusões de dados em uma tabela. No contexto deste projeto, os gatilhos foram utilizados para manter a consistência dos dados, garantir atualizações automáticas em registros relacionados e aplicar regras de validação no momento da modificação das tabelas. A seguir são apresentados todos os gatilhos que implementamos no nosso banco de dados:

### Marcar Evento Como Dia Inteiro

```sql
CREATE OR REPLACE FUNCTION marcar_evento_como_dia_todo()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.DataInicio = NEW.DataFim THEN
        NEW.Dia_todo := TRUE;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_dia_todo_automatico
BEFORE INSERT OR UPDATE ON Eventos
FOR EACH ROW
EXECUTE FUNCTION marcar_evento_como_dia_todo();
```

Exemplo de uso:

```sql
SELECT * FROM Eventos WHERE Titulo = 'Início do Período Letivo';
```

### Impedir Cadastro De Eventos Com Título Vazio

```sql
CREATE OR REPLACE FUNCTION validar_titulo_evento()
RETURNS TRIGGER AS $$
BEGIN
    IF TRIM(NEW.Titulo) = '' THEN
        RAISE EXCEPTION 'O título do evento não pode estar vazio.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_titulo_obrigatorio
BEFORE INSERT OR UPDATE ON Eventos
FOR EACH ROW
EXECUTE FUNCTION validar_titulo_evento();
```

### Impedir inserção de eventos com títulos duplicados na mesma categoria

```sql
CREATE OR REPLACE FUNCTION impedir_evento_duplicado()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM Eventos 
        WHERE Titulo = NEW.Titulo AND Id_categoria = NEW.Id_categoria
    ) THEN
        RAISE EXCEPTION 'Já existe um evento com esse título na mesma categoria.';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_evento_titulo_unico
BEFORE INSERT ON Eventos
FOR EACH ROW
EXECUTE FUNCTION impedir_evento_duplicado();
```

### Impedir conflito local eventos

```sql
CREATE OR REPLACE FUNCTION impedir_conflito_local_eventos()
RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM Eventos e
    WHERE 
      e.Local IS NOT NULL
      AND e.Local = NEW.Local
      AND e.Id_evento <> NEW.Id_evento
      AND e.DataInicio <= NEW.DataFim
      AND e.DataFim >= NEW.DataInicio
  ) THEN
    RAISE EXCEPTION 'Conflito detectado: já existe um evento agendado nesse local e período.';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_impedir_conflito_local
BEFORE INSERT OR UPDATE ON Eventos
FOR EACH ROW
EXECUTE FUNCTION impedir_conflito_local_eventos();
```
