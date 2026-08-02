# 📊 **15 Views a Partir das Consultas SQL para o Sistema Acadêmico**

Neste documento, apresento 15 views criadas a partir das consultas das listas de exercícios anteriores. Cada view encapsula uma consulta SQL específica, tornando seu uso mais simples e padronizado no sistema.

## 1️⃣ **Views de Consultas Básicas**

### **View 1: Matrículas e Notas**
```sql name=vw_matriculas_notas.sql
CREATE VIEW vw_matriculas_notas AS
SELECT 
    a.nome_aluno,
    d.nome_disciplina,
    m.nota
FROM aluno a
INNER JOIN matriculado m ON a.id_aluno = m.id_aluno
INNER JOIN disciplina d ON m.id_disciplina = d.id_disciplina
ORDER BY a.nome_aluno, d.nome_disciplina;

-- Uso: SELECT * FROM vw_matriculas_notas;
```
*Descrição: Fornece uma visão integrada de todos os alunos, suas disciplinas e respectivas notas.*

### **View 2: Carga de Professores**
```sql name=vw_carga_professores.sql
CREATE VIEW vw_carga_professores AS
SELECT 
    CONCAT(p.nome_professor, ' ', p.sobrenome) AS nome_completo,
    COUNT(d.id_disciplina) AS quantidade_disciplinas
FROM professor p
LEFT JOIN disciplina d ON p.id_professor = d.id_professor
GROUP BY p.id_professor, p.nome_professor, p.sobrenome
ORDER BY quantidade_disciplinas DESC;

-- Uso: SELECT * FROM vw_carga_professores;
```
*Descrição: Mostra quantas disciplinas cada professor ministra, incluindo professores sem disciplinas atribuídas.*

### **View 3: Estatísticas de Disciplinas**
```sql name=vw_estatisticas_disciplinas.sql
CREATE VIEW vw_estatisticas_disciplinas AS
SELECT 
    d.nome_disciplina,
    ROUND(AVG(m.nota)::NUMERIC, 2) AS nota_media,
    MAX(m.nota) AS maior_nota,
    MIN(m.nota) AS menor_nota
FROM disciplina d
INNER JOIN matriculado m ON d.id_disciplina = m.id_disciplina
WHERE m.nota IS NOT NULL
GROUP BY d.nome_disciplina
ORDER BY nota_media DESC;

-- Uso: SELECT * FROM vw_estatisticas_disciplinas;
```
*Descrição: Apresenta estatísticas sobre as notas de cada disciplina, incluindo média, maior e menor nota.*

## 2️⃣ **Views de Consultas Intermediárias**

### **View 4: Alunos Aprovados**
```sql name=vw_alunos_aprovados.sql
CREATE VIEW vw_alunos_aprovados AS
SELECT 
    a.nome_aluno,
    d.nome_disciplina,
    m.nota
FROM aluno a
JOIN matriculado m ON a.id_aluno = m.id_aluno
JOIN disciplina d ON m.id_disciplina = d.id_disciplina
WHERE m.nota >= 70
ORDER BY d.nome_disciplina, m.nota DESC;

-- Uso: SELECT * FROM vw_alunos_aprovados;
```
*Descrição: Lista todos os alunos que foram aprovados (nota >= 70) nas diversas disciplinas.*

### **View 5: Médias por Aluno**
```sql name=vw_medias_aluno.sql
CREATE VIEW vw_medias_aluno AS
SELECT 
    a.nome_aluno,
    ROUND(AVG(m.nota)::NUMERIC, 2) AS media_geral
FROM aluno a
LEFT JOIN matriculado m ON a.id_aluno = m.id_aluno
WHERE m.nota IS NOT NULL
GROUP BY a.id_aluno, a.nome_aluno
ORDER BY media_geral DESC;

-- Uso: SELECT * FROM vw_medias_aluno;
```
*Descrição: Calcula a média geral de cada aluno com base nas notas registradas no sistema.*

### **View 6: Alunos de Computação**
```sql name=vw_alunos_computacao.sql
CREATE VIEW vw_alunos_computacao AS
SELECT DISTINCT a.nome_aluno
FROM aluno a
JOIN matriculado m ON a.id_aluno = m.id_aluno
JOIN disciplina d ON m.id_disciplina = d.id_disciplina
JOIN professor p ON d.id_professor = p.id_professor
WHERE p.area = 'Computação'
ORDER BY a.nome_aluno;

-- Uso: SELECT * FROM vw_alunos_computacao;
```
*Descrição: Identifica todos os alunos matriculados em pelo menos uma disciplina da área de Computação.*

### **View 7: Pares de Alunos**
```sql name=vw_pares_alunos.sql
CREATE VIEW vw_pares_alunos AS
SELECT 
    a1.nome_aluno AS aluno_1,
    a2.nome_aluno AS aluno_2
FROM aluno a1
CROSS JOIN aluno a2
WHERE a1.id_aluno < a2.id_aluno
ORDER BY a1.nome_aluno, a2.nome_aluno;

-- Uso: SELECT * FROM vw_pares_alunos;
```
*Descrição: Gera todos os possíveis pares de alunos sem repetições, útil para formação de duplas ou análises de relacionamento.*

## 3️⃣ **Views de Consultas com Filtros**

### **View 8: Alunos de Bom Desempenho**
```sql name=vw_bom_desempenho.sql
CREATE VIEW vw_bom_desempenho AS
SELECT 
    nome_aluno,
    data_nascimento,
    media
FROM aluno
WHERE media > 80
ORDER BY media DESC;

-- Uso: SELECT * FROM vw_bom_desempenho;
```
*Descrição: Lista alunos com média superior a 80, considerados de bom desempenho acadêmico.*

### **View 9: Professores por Área**
```sql name=vw_professores_por_area.sql
CREATE VIEW vw_professores_por_area AS
SELECT 
    id_professor,
    CONCAT(nome_professor, ' ', sobrenome) AS nome_completo,
    area
FROM professor
WHERE area IN ('Matemática', 'Computação')
ORDER BY area, sobrenome;

-- Uso: SELECT * FROM vw_professores_por_area WHERE area = 'Computação';
```
*Descrição: Fornece a lista de professores por área de conhecimento, com ênfase em Matemática e Computação.*

### **View 10: Disciplinas com Termo**
```sql name=vw_disciplinas_termo.sql
CREATE VIEW vw_disciplinas_termo AS
SELECT 
    id_disciplina,
    nome_disciplina,
    carga_horaria
FROM disciplina
WHERE nome_disciplina LIKE '%de%'
ORDER BY nome_disciplina;

-- Uso: SELECT * FROM vw_disciplinas_termo;
```
*Descrição: Identifica disciplinas que possuem a preposição "de" em seu nome, útil para análises linguísticas do currículo.*

## 4️⃣ **Views de Consultas Avançadas**

### **View 11: Detalhes de Algoritmos**
```sql name=vw_detalhes_algoritmos.sql
CREATE VIEW vw_detalhes_algoritmos AS
SELECT 
    a.nome_aluno,
    m.nota,
    CONCAT(p.nome_professor, ' ', p.sobrenome) AS professor
FROM aluno a
JOIN matriculado m ON a.id_aluno = m.id_aluno
JOIN disciplina d ON m.id_disciplina = d.id_disciplina
JOIN professor p ON d.id_professor = p.id_professor
WHERE d.nome_disciplina = 'Algoritmos'
ORDER BY m.nota DESC;

-- Uso: SELECT * FROM vw_detalhes_algoritmos;
```
*Descrição: Apresenta detalhes específicos sobre o desempenho dos alunos na disciplina de Algoritmos.*

### **View 12: Alunos com Notas Similares**
```sql name=vw_notas_similares.sql
CREATE VIEW vw_notas_similares AS
SELECT 
    d.nome_disciplina,
    a1.nome_aluno AS aluno1,
    a2.nome_aluno AS aluno2,
    m1.nota AS nota1,
    m2.nota AS nota2,
    ABS(m1.nota - m2.nota) AS diferenca
FROM matriculado m1
JOIN matriculado m2 ON m1.id_disciplina = m2.id_disciplina
JOIN aluno a1 ON m1.id_aluno = a1.id_aluno
JOIN aluno a2 ON m2.id_aluno = a2.id_aluno
JOIN disciplina d ON m1.id_disciplina = d.id_disciplina
WHERE m1.id_aluno < m2.id_aluno
AND ABS(m1.nota - m2.nota) < 5
ORDER BY d.nome_disciplina, diferenca;

-- Uso: SELECT * FROM vw_notas_similares WHERE nome_disciplina = 'Cálculo';
```
*Descrição: Identifica pares de alunos com notas similares (diferença < 5 pontos) em uma mesma disciplina.*

### **View 13: Desvios da Média**
```sql name=vw_desvios_media.sql
CREATE VIEW vw_desvios_media AS
WITH medias_disciplinas AS (
    SELECT 
        id_disciplina, 
        AVG(nota) AS media_disciplina
    FROM matriculado
    WHERE nota IS NOT NULL
    GROUP BY id_disciplina
)
SELECT 
    a.nome_aluno,
    d.nome_disciplina,
    m.nota,
    ROUND(md.media_disciplina::NUMERIC, 2) AS media_turma,
    ROUND((m.nota - md.media_disciplina)::NUMERIC, 2) AS desvio_media
FROM matriculado m
JOIN aluno a ON m.id_aluno = a.id_aluno
JOIN disciplina d ON m.id_disciplina = d.id_disciplina
JOIN medias_disciplinas md ON m.id_disciplina = md.id_disciplina
WHERE m.nota IS NOT NULL
ORDER BY desvio_media DESC;

-- Uso: SELECT * FROM vw_desvios_media WHERE desvio_media > 10;
```
*Descrição: Calcula o desvio de cada nota em relação à média da turma, identificando desempenhos significativamente acima ou abaixo da média.*

## 5️⃣ **Views de Consultas Especiais**

### **View 14: Boletim Completo**
```sql name=vw_boletim_completo.sql
CREATE VIEW vw_boletim_completo AS
SELECT 
    a.id_aluno,
    a.nome_aluno,
    d.nome_disciplina,
    d.carga_horaria,
    CONCAT(p.nome_professor, ' ', p.sobrenome) AS professor,
    m.nota,
    CASE 
        WHEN m.nota IS NULL THEN 'Em andamento'
        WHEN m.nota >= 70 THEN 'Aprovado'
        ELSE 'Reprovado'
    END AS situacao
FROM aluno a
JOIN matriculado m ON a.id_aluno = m.id_aluno
JOIN disciplina d ON m.id_disciplina = d.id_disciplina
LEFT JOIN professor p ON d.id_professor = p.id_professor
ORDER BY a.nome_aluno, d.nome_disciplina;

-- Uso: SELECT * FROM vw_boletim_completo WHERE id_aluno = 123;
```
*Descrição: Fornece um boletim acadêmico completo para cada aluno, incluindo situação de aprovação em cada disciplina.*

### **View 15: Alunos Acima da Média**
```sql name=vw_alunos_acima_media.sql
CREATE VIEW vw_alunos_acima_media AS
SELECT 
    a.nome_aluno,
    ROUND(AVG(m.nota)::NUMERIC, 2) AS media_aluno,
    (SELECT ROUND(AVG(nota)::NUMERIC, 2) FROM matriculado WHERE nota IS NOT NULL) AS media_geral
FROM aluno a
JOIN matriculado m ON a.id_aluno = m.id_aluno
WHERE m.nota IS NOT NULL
GROUP BY a.id_aluno, a.nome_aluno
HAVING AVG(m.nota) > (
    SELECT AVG(nota)
    FROM matriculado
    WHERE nota IS NOT NULL
)
ORDER BY media_aluno DESC;

-- Uso: SELECT * FROM vw_alunos_acima_media;
```
*Descrição: Identifica alunos com média de notas superior à média geral da instituição, destacando os estudantes de melhor desempenho relativo.*

## 📋 **Considerações sobre o Uso de Views**

As views criadas oferecem diversas vantagens para o sistema acadêmico:

1. **Simplificação de acesso**: Consultas complexas são encapsuladas em interfaces simples
2. **Padronização**: Garantem consistência nas análises realizadas por diferentes usuários
3. **Segurança**: Podem ser usadas para restringir acesso a dados sensíveis
4. **Manutenção**: Mudanças na estrutura do banco podem ser absorvidas pela view
5. **Performance**: Views materializadas (no PostgreSQL) podem armazenar resultados para consultas frequentes

Para modificar qualquer uma dessas views, utilize:
```sql
CREATE OR REPLACE VIEW nome_da_view AS 
-- nova definição da consulta
```

Para remover uma view:
```sql
DROP VIEW nome_da_view;
```

Para verificar todas as views do sistema:
```sql
SELECT table_name 
FROM information_schema.views 
WHERE table_schema = 'public';
```

**💡 Dica para a prova**: Compreenda que views são relações virtuais que não armazenam dados, apenas definem como eles são apresentados. Na álgebra relacional, são expressões relacionais nomeadas para reuso.
