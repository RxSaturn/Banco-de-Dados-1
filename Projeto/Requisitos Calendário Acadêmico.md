**Do****cumentação de Requisitos – Sistema de Calendários** **Acadêmicos** 

**1****. Visão do Produto** 

O sistema de Confecção de Calendários Acadêmicos tem como objetivo permitir que instituições de ensino planejem e visualizem seus calendários acadêmicos de forma clara e organizada. A ferramenta possibilita a criação de múltiplos calendários por ano, a definição de categorias de datas \(letivas e não letivas\), bem como a associação de cores e períodos dentro das categorias. A interface deve apresentar o calendário anual com uma visualização intuitiva das datas e uma legenda explicativa, facilitando o planejamento institucional e a comunicação com alunos e docentes. 

**2****. Personas** 

**Fe****lisberto, o Coordenador de Gestão Acadêmica \(CGA\)** 

**Contexto**: Coordena o calendário acadêmico de uma instituição de ensino. 

**Objetivo**: Criar calendários acadêmicos anuais de forma rápida, marcando feriados, recessos e datas letivas. 

**Dores**: Perde tempo montando calendários manualmente, com dificuldade para conferir informações. 

**3****. Histórias de Usuário** 

**Hi****stória 1 - Tipos de calendários** 

**Como** CGA **quero** cadastrar \(criar, alterar e apagar\) tipos de calendários que poderão ser criados, **para** facilitar a inclusão de datas obrigatórias que devem aparecer em cada tipo de calendário. 

**Critérios de Aceitação:** - Deve ser possível cadastrar uma sigla e um nome para cada tipo - Exemplos: - CCS - Calendário de Cursos Superiores -

CCT - Calendário de Cursos Técnicos 

**Hi****stória 2 - Categorias de datas** 

**Como** CGA, 

**quero** cadastrar, para cada tipo de calendário, categorias de datas com cores associadas, total de dias, habilitação de contagem e dias da semana válidos **para** manter um de categorias nos calendários. 

**Critérios de Aceitação:** - O sistema deve permitir definir nome da categoria, cor associada, total de dias e habilitação de contagem - Para cada categoria deve ser permitido selecionar os dias da semana válidos - Não pode ser utilizada uma mesma cor para mais de uma categoria 

**Hi****stória 3 - Calendários** 

**Como** CGA **quero**, para cada tipo de calendário, gerenciar \(criar, copiar, alterar e apagar\) calendários com ano, nome, data de início e data de fim. 

**para** organizar os planejamentos anuais da instituição. 

**Critérios de Aceitação:** - O sistema deve permitir gerenciar de calendários com tipo, ano e nome - Deve ser possível manter mais de um calendário por tipo e ano 

**Hi****stória 4 - Controle de datas** 

**Como** CGA, 

**quero** cadastrar as datas de cada categoria de um calendário **para** representar todos os períodos e datas necessárias. 

**Critérios de Aceitação:** - O sistema deve permitir a inclusão de um ou mais períodos de data para cada categoria - O período deve conter descrição, data inicial e data final - A data final do período deve ser maior ou igual a data inicial - As datas inicial e final do período devem estar contidas dentro no início e fim do calendário - Para uma única data como um feriado, o período a data inicial fica igual a data final - O sistema deve calcular a soma dos dias válidos dos períodos de cada categoria - Os dias válidos de um período são os dias da semana da categoria dentro do intervalo do período - O sistema deve garantir que o total de dias da categoria seja igual à soma dos dias válidos de seus períodos - Por exemplo, a categoria *Sábado letivos* possui um total de 5 dias e somente o dia de semana *sábado*, se for acrescentado um período de um mês inteiro contendo 4 sábados, a categoria ainda precisa de mais períodos de datas até atingir os 5 sábados 

**Hi****stória 5 - Visualização de calendário** **Como** CGA, 

**quero** visualizar o calendário anual com cores e uma legenda, 

**para** entender rapidamente os períodos letivos e não letivos. 

**Critérios de Aceitação:** - O calendário deve mostrar os meses do ano com cores indicativas das categorias - A legenda deve listar as categorias com seus nomes e cores - Se a categoria tiver contagem habilitada, a legenda deve mostrar a soma dos dias válidos dos períodos da categoria - O

calendário deve ter um anexo mostrando todos os períodos e datas de cada categoria com sua descrição - Se a data inicial e final do período forem iguais, o anexo deve mostrar apenas uma delas



