# Soluções SQL para Automatização do Sistema Acadêmico

Vou criar as instruções SQL necessárias para implementar as regras de automação solicitadas. Para isso, usarei triggers e functions no PostgreSQL, que permitem executar procedimentos automaticamente quando determinados eventos ocorrem no banco de dados.

## (a) Atualização automática da média das disciplinas

Para que a média das disciplinas seja atualizada automaticamente sempre que houver alterações nas notas dos alunos, precisamos criar uma function e um trigger que atualize o campo `media` na tabela `disciplina`. Vamos implementar isso:

```sql name=atualizacao_automatica_media_disciplina.sql
-- Criação da function que calculará a média das notas por disciplina
CREATE OR REPLACE FUNCTION calcular_media_disciplina()
RETURNS TRIGGER AS $$
BEGIN
    -- Atualiza a média da disciplina afetada pela operação
    UPDATE disciplina
    SET media = (
        SELECT COALESCE(AVG(nota), 0)
        FROM matriculado
        WHERE id_disciplina = COALESCE(NEW.id_disciplina, OLD.id_disciplina)
        AND nota > -1  -- Desconsidera as matrículas sem notas (-1)
    )
    WHERE id_disciplina = COALESCE(NEW.id_disciplina, OLD.id_disciplina);
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Criação do trigger que será disparado em qualquer alteração na tabela matriculado
CREATE TRIGGER atualiza_media_disciplina
AFTER INSERT OR UPDATE OR DELETE ON matriculado
FOR EACH ROW
EXECUTE FUNCTION calcular_media_disciplina();
```

Explicação:
1. A function `calcular_media_disciplina()` calcula a média das notas de uma disciplina, desconsiderando notas iguais a -1.
2. O trigger `atualiza_media_disciplina` é acionado após qualquer inserção, atualização ou exclusão na tabela `matriculado`.
3. Usamos `COALESCE(NEW.id_disciplina, OLD.id_disciplina)` para garantir que a function funcione tanto para inserções (onde NEW existe) quanto para exclusões (onde OLD existe).

## (b) Matrícula automática em disciplinas sem pré-requisitos

Para matricular automaticamente os novos alunos em disciplinas sem pré-requisitos, vamos criar uma function e um trigger que serão acionados quando um novo aluno for inserido no sistema:

```sql name=matricula_automatica_alunos.sql
-- Criação da function que matricula novos alunos em disciplinas sem pré-requisitos
CREATE OR REPLACE FUNCTION matricular_aluno_automaticamente()
RETURNS TRIGGER AS $$
BEGIN
    -- Insere matrículas para o novo aluno em todas as disciplinas sem pré-requisitos
    INSERT INTO matriculado (id_disciplina, id_aluno, nota)
    SELECT id_disciplina, NEW.id_aluno, -1  -- Nota -1 indica apenas matriculado sem nota
    FROM disciplina
    WHERE id_prerequisito IS NULL  -- Disciplinas sem pré-requisitos
    OR id_prerequisito = 0;  -- Considerando que 0 também pode indicar ausência de pré-requisito
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Criação do trigger que será disparado quando um novo aluno for inserido
CREATE TRIGGER matricula_automatica
AFTER INSERT ON aluno
FOR EACH ROW
EXECUTE FUNCTION matricular_aluno_automaticamente();
```

Explicação:
1. A function `matricular_aluno_automaticamente()` insere registros na tabela `matriculado` para cada disciplina sem pré-requisitos.
2. O trigger `matricula_automatica` é acionado após a inserção de um novo aluno na tabela `aluno`.
3. Consideramos que disciplinas sem pré-requisitos são aquelas onde `id_prerequisito` é NULL ou 0 (dependendo da implementação específica do sistema).
4. A nota é definida como -1, indicando que o aluno está apenas matriculado, sem nota atribuída.

## Observações importantes

1. **Tratamento de pré-requisitos**: A solução assume que disciplinas sem pré-requisitos são identificadas por `id_prerequisito IS NULL` ou `id_prerequisito = 0`. Se o sistema utilizar outra convenção, o código deve ser ajustado.

2. **Performance**: Em sistemas com muitos alunos e disciplinas, essas operações podem impactar o desempenho. Para bancos de dados maiores, pode ser necessário otimizar as consultas ou considerar outras abordagens.

3. **Tratamento de erros**: Para um sistema em produção, seria importante adicionar tratamento de erros e logging para monitorar possíveis falhas nas operações automáticas.

4. **Transações**: As operações estão encapsuladas em transações implícitas por serem triggers, o que garante atomicidade mesmo em caso de falhas parciais.
