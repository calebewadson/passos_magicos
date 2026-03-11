# Passos Mágicos — Predição de risco de defasagem escolar com foco em MLOps

## Visão geral

Este repositório entrega uma solução de Machine Learning end-to-end para estimar o risco de defasagem escolar de estudantes do case **Passos Mágicos**. O projeto foi estruturado para execução local, versionamento em GitHub, demonstração técnica em vídeo e avaliação prática de engenharia de ML.

A solução cobre:

- ingestão e harmonização das abas `PEDE2022`, `PEDE2023` e `PEDE2024`
- definição explícita de target com estratégia temporal
- feature engineering reprodutível
- treinamento, avaliação e seleção de modelo
- serialização do pipeline completo
- API de inferência em FastAPI
- logs estruturados e persistência de predições
- monitoramento simples de drift com relatório HTML e dashboard Streamlit
- testes automatizados com cobertura acima de 80%
- Dockerfile, docker-compose e documentação operacional

## Problema de negócio

O objetivo é antecipar quais alunos têm maior probabilidade de apresentar **defasagem escolar no ano seguinte**, permitindo que a organização priorize acompanhamento pedagógico, psicológico e operacional antes que o problema se consolide.

Em contexto educacional, perder um caso de risco tende a ser mais custoso do que produzir alguns falsos positivos. Por isso, a seleção do modelo prioriza **recall da classe de risco**, sem ignorar F1 e capacidade discriminativa global.

## Base de dados

Arquivo de entrada principal:

- `BASE DE DADOS PEDE 2024 - DATATHON.xlsx`

Abas utilizadas:

- `PEDE2022`
- `PEDE2023`
- `PEDE2024`

As colunas reais foram lidas diretamente da planilha. Entre as variáveis usadas no projeto estão, por exemplo:

- `RA`
- `Fase`
- `Turma`
- `Idade 22` / `Idade`
- `Gênero`
- `Ano ingresso`
- `Instituição de ensino`
- `Pedra 20`, `Pedra 21`, `Pedra 22`, `Pedra 23`, `Pedra 2023`, `Pedra 2024`
- `INDE 22`, `INDE 23`, `INDE 2023`, `INDE 2024`
- `IAA`, `IEG`, `IPS`, `IPP`, `IDA`, `IPV`, `IAN`
- `Matem`, `Portug`, `Inglês`, `Mat`, `Por`, `Ing`
- `Atingiu PV`
- `Fase ideal` / `Fase Ideal`
- `Defas` / `Defasagem`
- `Ativo/ Inativo`

## Escolha do target

### Target adotado

Foi adotado o target:

- `target_risco_defasagem_proximo_ano`

Definição:

- valor `1` quando a coluna de **defasagem do ano seguinte** é negativa
- valor `0` caso contrário

Implementação no código:

- 2022 usa `Defas` de 2023 como rótulo futuro após pareamento por `RA`
- 2023 usa `Defasagem` de 2024 como rótulo futuro após pareamento por `RA`

Em termos de fonte original do rótulo:

- `Defas` em 2022
- `Defasagem` em 2023 e 2024

### Por que essa escolha representa risco de defasagem

A variável `Defas`/`Defasagem` é a representação mais direta, observável e supervisionada do fenômeno de defasagem escolar presente na planilha. Porém, usar a defasagem do mesmo ano como alvo em produção induziria vazamento, porque várias features do mesmo ciclo podem refletir a própria condição que se deseja prever.

Por isso, a solução foi formulada como:

- **predizer o risco de defasagem no próximo ano**, com base apenas nas informações disponíveis no ano corrente

Essa abordagem é mais robusta para inferência operacional, porque preserva causalidade temporal e evita proxies diretos do rótulo contemporâneo.

### Formulação do problema

A formulação adotada foi:

- **classificação binária**

Classes:

- `1` = aluno em risco de defasagem no ano seguinte
- `0` = aluno sem risco de defasagem no ano seguinte

### Estratégia temporal

Foram construídas duas janelas supervisionadas:

- `2022 -> 2023`
- `2023 -> 2024`

Uso no pipeline:

- treino/seleção inicial: `2022 -> 2023`
- validação holdout temporal: `2023 -> 2024`
- treino final do artefato serializado: todas as linhas rotuladas disponíveis

## Harmonização de schema

As abas possuem diferenças de nomenclatura entre anos. O módulo `src/data_loader.py` normaliza explicitamente essas divergências, por exemplo:

- `Nome` → `nome_anonimizado`
- `Ano nasc` / `Data de Nasc`
- `Idade 22` / `Idade`
- `Pedra 22`, `Pedra 2023`, `Pedra 2024` → histórico/atual
- `INDE 22`, `INDE 2023`, `INDE 2024` → histórico/atual
- `Matem`, `Portug`, `Inglês` e `Mat`, `Por`, `Ing`
- `Fase ideal` e `Fase Ideal`
- `Defas` e `Defasagem`

Também há tratamento explícito para:

- conversão numérica segura
- parsing de datas
- remoção de duplicados por `RA`
- padronização de anos de referência

## Estratégia de dados e prevenção de leakage

A pipeline remove o risco mais óbvio de vazamento ao prever o rótulo do **ano seguinte**. Não é usada nenhuma coluna do futuro na inferência.

Ainda assim, algumas variáveis do ano corrente podem ser fortemente correlacionadas com risco pedagógico, como `INDE`, `IDA`, `IEG`, `IPV`, `IAN`, `Pedra` e `Atingiu PV`. Elas foram mantidas porque representam estado observável do aluno no momento da decisão e são plausíveis em produção.

A checagem mínima de qualidade inclui:

- nulos
- cardinalidade
- tipos
- duplicidade por aluno

Um relatório objetivo é gerado em:

- `artifacts/reports/data_quality_report.csv`

## Feature engineering

O módulo `src/feature_engineering.py` cria variáveis derivadas sem depender de informação futura. Entre elas:

- `tempo_programa`
- `idade_x_tempo_programa`
- `flag_possui_ingles`
- `flag_tem_rec_psicologia`
- `flag_indicado`
- `flag_atingiu_pv`
- `media_notas_idioma`
- `media_academica`
- `desvio_academico`
- `indice_engajamento_aprendizado`
- `historico_inde_delta`
- `historico_inde_delta_recente`
- `pedra_atual_ord`
- `pedra_2022_ord`
- `evolucao_pedra`
- `missing_count`
- `flag_fase_textualmente_compativel`

O pré-processamento usa `ColumnTransformer` e `Pipeline` do scikit-learn com:

- imputação mediana para numéricas
- padronização com `StandardScaler`
- imputação por moda para categóricas
- `OneHotEncoder(handle_unknown="ignore")`

## Modelagem

### Modelos candidatos

Foram treinados três modelos:

- Logistic Regression
- Random Forest
- Gradient Boosting

### Split de validação

Foi adotado **split temporal**, porque o problema possui estrutura longitudinal por ano e o risco de leakage seria alto em um split aleatório.

### Critério de seleção

A ordenação do melhor modelo prioriza:

1. `recall_risco`
2. `f1_risco`
3. `pr_auc`

A escolha reflete o custo de negócio de não identificar um aluno em risco.

### Melhor modelo selecionado

Modelo vencedor no holdout temporal:

- `random_forest`

### Métricas do holdout temporal (`2023 -> 2024`)

- Recall da classe de risco: **0.8214**
- Precision da classe de risco: **0.5349**
- F1-score da classe de risco: **0.6479**
- ROC-AUC: **0.7675**
- PR-AUC: **0.6889**

Interpretação objetiva:

- o modelo privilegia sensibilidade e recupera a maior parte dos casos de risco
- há custo de precisão, aceitável neste contexto como baseline operacional
- a capacidade discriminativa geral é razoável para um pipeline tabular clássico e reproduzível

Os arquivos de métricas ficam em:

- `artifacts/metrics/logistic_regression_metrics.json`
- `artifacts/metrics/random_forest_metrics.json`
- `artifacts/metrics/gradient_boosting_metrics.json`

## Interpretabilidade

São gerados artefatos simples de interpretabilidade em:

- `artifacts/reports/random_forest_feature_importance.csv`
- `artifacts/reports/random_forest_feature_importance.png`

As features mais influentes no modelo final incluem, entre outras:

- `IAN`
- `IPV`
- `INDE atual`
- `IPP`
- `indice_engajamento_aprendizado`
- `num_avaliacoes`
- `media_academica`
- `Cf`
- `portugues`

Essas variáveis são consistentes com o racional pedagógico do problema: desempenho, engajamento, evolução e histórico acadêmico ajudam a explicar risco futuro.

## Estrutura do projeto

```text
passos_magicos_mlops/
├── app/
│   ├── config.py
│   ├── logging_config.py
│   ├── main.py
│   ├── model/
│   │   ├── metadata.json
│   │   └── model.joblib
│   ├── schemas.py
│   └── services.py
├── artifacts/
│   ├── drift/
│   ├── logs/
│   ├── metrics/
│   └── reports/
├── data/
│   └── raw/
│       └── passos_magicos.xlsx
├── notebooks/
│   └── eda.ipynb
├── src/
│   ├── data_loader.py
│   ├── evaluate.py
│   ├── feature_engineering.py
│   ├── logging_utils.py
│   ├── monitor.py
│   ├── predict.py
│   ├── preprocessing.py
│   ├── settings.py
│   ├── train.py
│   └── utils.py
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_data_loader.py
│   ├── test_feature_engineering.py
│   ├── test_more.py
│   ├── test_predict.py
│   ├── test_preprocessing.py
│   └── test_train.py
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── pytest.ini
├── README.md
└── requirements.txt