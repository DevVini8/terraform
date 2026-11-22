# 📄 Entregável 1: Relatório Técnico da Base de Dados Tratada

**Projeto:** Observatório Interseccional da Violência contra a Mulher nas Capitais do Brasil (2025)
**Alinhamento Agenda 2030:** **ODS 5** (Igualdade de Gênero) e **ODS 18** (Igualdade Étnico-Racial)

---

## 1. Origem dos Dados

O projeto integra duas bases de dados públicas e auditáveis que combinam a visão oficial macro-governamental da segurança pública brasileira com o detalhamento interseccional de microdados levantados pela sociedade civil organizada:

| Fonte de Dados | Arquivo Bruto | Instituição Responsável | Cobertura Original | Granularidade |
| :--- | :--- | :--- | :--- | :--- |
| **1. SINESP / MJSP (Fonte Original)** | `fonte original.xlsx` | Ministério da Justiça e Segurança Pública (SINESP / Governo Federal) | 27 UFs e 5.570 Municípios do Brasil (Ano 2025) | Mensal por Município, Natureza do Evento e Sexo da Vítima |
| **2. Instituto Fogo Cruzado (Complemento)** | `complemento fogo cruzado.xlsx` | Instituto Fogo Cruzado (Sociedade Civil / Dados Abertos) | Regiões Metropolitanas de RJ, PE, BA e PA (2016–2026) | Microdado por Vítima Individual Baleada e Ocorrência |

---

## 2. Versão Original Utilizada (Diagnóstico das Bases Brutas)

### 2.1. Base Original 1: `fonte original.xlsx` (SINESP / MJSP)
- **Dimensões e Tamanho:** `832.293` registros (linhas de dados excluindo o cabeçalho) × `14` colunas, na aba `2025` (`23,9 MB` compactado em `.xlsx`; `309,8 MB` em XML bruto).
- **Colunas Originais (`14`):** `uf`, `municipio`, `evento`, `data_referencia`, `agente`, `arma`, `faixa_etaria`, `feminino`, `masculino`, `nao_informado`, `total_vitima`, `total`, `total_peso`, `abrangencia`.
- **Inconsistências e Ruídos Identificados na Versão Original:**
  1. **Excesso de Linhas Cartesianas Zeradas:** `728.846` linhas (**87,57%** de toda a planilha) apresentavam `feminino = 0`, `masculino = 0`, `total_vitima = 0` e `total = 0`.
  2. **Eventos Fora do Escopo de Violência de Gênero:** Presença de 29 categorias distintas, incluindo registros administrativos e patrimoniais (`Emissão de Alvarás de licença`, `Realização de vistorias`, `Combate a incêndios`, `Furto de veículo`, etc.).
  3. **Ausência de Município no Evento *Estupro*:** Todos os `324` registros mensais de `Estupro` (`27 UFs × 12 meses`, somando `18.218` vítimas femininas) estavam consolidados apenas em nível estadual, com a coluna `municipio` vazia.
  4. **Datas em Formato Serial:** Coluna `data_referencia` armazenada como número serial do Excel (ex: `45658.0` para `01/01/2025`).

### 2.2. Base Original 2: `complemento fogo cruzado.xlsx` (Instituto Fogo Cruzado)
- **Dimensões e Tamanho:** `45.025` registros (linhas de vítimas excluindo o cabeçalho) × `31` colunas, na aba `vitimas (2)` (`9,8 MB` compactado em `.xlsx`; `50,0 MB` em XML bruto).
- **Colunas Originais (`31`):** `estado`, `cidade`, `bairro`, `ocorrencia_id`, `ocorrencia_numero`, `data`, `endereco`, `latitude`, `longitude`, `acao_policial`, `presenca_agente`, `motivo_principal`, `motivos_complementares`, `recortes`, `chacina`, `vitima_id`, `situacao`, `circunstancias`, `data_morte`, `tipo_pessoa`, `idade`, `faixa_etaria`, `genero`, `raca`, `local`, `status_servico`, `qualificacoes`, `corporacao`, `cargo_agente`, `status_agente`, `unidade`.
- **Inconsistências e Riscos LGPD Identificados na Versão Original:**
  1. **Registros Fora do Recorte Temporal e Geográfico:** Série histórica de 2016 a 2026 (`39.559` registros fora de 2025) e municípios periféricos/interior fora das capitais.
  2. **Incompletude Demográfica:** Presença de `1.240` registros sem gênero informado (`Não identificado`), `40.560` registros masculinos e `96` registros de mulheres nas capitais em 2025 sem idade informada (`vazio/NaN`).
  3. **Quase-Identificadores Sensíveis à LGPD:** Presença do logradouro físico exato (`endereco`), coordenadas GPS com erro de escala decimal (`-129255147` em vez de `-12.9255147`) e dados funcionais individualizados de agentes públicos (`corporacao`, `cargo_agente`, `status_agente`, `unidade`).

---

## 3. Principais Decisões Tomadas Durante o Processo (Critérios da Equipe e Governança)

| Tipo de Decisão | Critério Definido pela Equipe | Base Aplicada | Regra Técnica Executada no Pipeline (`/etl/transform.py`) |
| :--- | :--- | :--- | :--- |
| **✅ Inclusão 1** | **Dados entre janeiro e dezembro de 2025** | Ambas | Filtro temporal estrito: `ano == 2025` e `1 <= mes <= 12`. |
| **✅ Inclusão 2** | **Somente Capitais do Brasil** | Ambas | Validação pelo dicionário oficial das **27 Capitais (`UF -> Capital`)** no SINESP e pelas **4 Capitais** monitoradas no Fogo Cruzado (`Salvador`, `Recife`, `Rio de Janeiro` e `Belém`). |
| **✅ Inclusão 3** | **Eventos ocorridos por Estupro, Feminicídio e Tentativa de feminicídio** | SINESP | Filtro categórico estrito: `evento IN ('Estupro', 'Feminicídio', 'Tentativa de feminicídio')`. |
| **✅ Inclusão 4** | **Vítimas do sexo feminino na fonte original** | SINESP | Retenção exclusiva de `feminino > 0`, zerando `masculino = 0` e `nao_informado = 0` e definindo `total_vitima = feminino`. |
| **✅ Inclusão 5** | **Mulheres entre 18 e 45 anos no Fogo Cruzado** | Fogo Cruzado | Filtro numérico estrito: `18 <= idade <= 45`. |
| **✅ Inclusão 6** | **Somente gênero de Mulheres cis e Mulheres trans e travesti** | Fogo Cruzado | Filtro categórico estrito: `genero IN ('Mulher cis', 'Mulher trans e travesti')`. |
| **🚫 Exclusão 1** | **Dados sem gêneros informados no Fogo Cruzado** | Fogo Cruzado | Descarte integral de registros com `genero` nulo, vazio ou `'Não identificado'` (além dos registros masculinos). |
| **🚫 Exclusão 2** | **Dados sem município identificado** | Ambas | Descarte de registros com `municipio`/`cidade` vazio ou `'NÃO INFORMADO'`. |
| **🚫 Exclusão 3** | **Dados sem idade informada no Fogo Cruzado** | Fogo Cruzado | Descarte dos `96` registros de mulheres nas capitais em 2025 que não possuíam o campo `idade` preenchido. |
| **🛡️ Governança LGPD** | **Minimização, Pseudonimização e *k*-Anonimato Espacial** | Fogo Cruzado | Remoção de `endereco`, `cargo_agente`, `corporacao` e `unidade`; hash **SHA-256** (`vitima_hash`, `ocorrencia_hash`) e truncamento de coordenadas em 2 casas decimais (`lat_aprox`, `lon_aprox`). |

---

## 4. Versão Resultante Após o Tratamento

As versões tratadas encontram-se disponíveis em [data/processed/sinesp_tratado.csv](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/data/processed/sinesp_tratado.csv) e [data/processed/fogo_cruzado_tratado.csv](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/data/processed/fogo_cruzado_tratado.csv), além de estruturadas no Esquema Estrela ([etl/schema.sql](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/etl/schema.sql)).

### 4.1. Comparativo Antes vs. Depois do Tratamento

| Indicador | Base 1: SINESP (`fonte original.xlsx` → `sinesp_tratado.csv`) | Base 2: Fogo Cruzado (`complemento fogo cruzado.xlsx` → `fogo_cruzado_tratado.csv`) |
| :--- | :--- | :--- |
| **Registros na Versão Original** | `832.293` linhas | `45.025` linhas |
| **Registros na Versão Tratada** | **`496` registros ativos nas 27 Capitais** (`820` incluindo mapeamento de *Estupro* UF) | **`77` registros** de mulheres (18–45 anos, Cis e Trans/Travesti) nas Capitais em 2025 |
| **Volume de Vítimas no Recorte** | **`1.233` vítimas femininas nas 27 Capitais** (`292` Feminicídios + `941` Tentativas) | **`77` mulheres baleadas** (`47` Mortas [61,04%] e `30` Feridas [38,96%]) |
| **Recorte Interseccional / Demográfico** | `100%` Vítimas do Sexo Feminino nas Capitais Brasileiras em 2025 | `75` Mulheres cis e `2` Mulheres trans/travestis \| `75,51%` Negras (dentre as c/ cor id.) \| Idade Média: `29,6 anos` (Mediana: `29,0 anos`) |
| **Tamanho do Arquivo** | Reduzido de `23,9 MB` para **`65 KB`** | Reduzido de `9,8 MB` para **`12 KB`** |

---

## 5. Justificativas para as Transformações Realizadas

1. **Sincronismo Temporal (Janeiro a Dezembro de 2025):** Garante que ambas as fontes retratem exatamente o mesmo recorte cronológico anual (os 12 meses de 2025), eliminando distorções sazonais ou históricas.
2. **Foco nas Capitais do Brasil e Exclusão de Município Não Identificado:** As capitais estaduais concentram a rede especializada de atendimento à mulher e permitem o cruzamento territorial direto entre o SINESP (27 capitais) e o Instituto Fogo Cruzado (`Salvador`, `Recife`, `Rio de Janeiro` e `Belém`). A exclusão de dados sem município identificado evita que ocorrências estaduais sem localização municipal distorçam os indicadores das capitais.
3. **Recorte de Violência Baseada em Gênero (Estupro, Feminicídio, Tentativa de Feminicídio e Sexo Feminino no SINESP):** Alinha estritamente a base governamental à **Meta 5.2 da ODS 5**, eliminando o ruído de mais de 728 mil linhas zeradas e de crimes patrimoniais/administrativos.
4. **Coorte de Mulheres Cis e Mulheres Trans/Travestis de 18 a 45 Anos (Fogo Cruzado):** Incorpora a perspectiva interseccional inclusiva de identidade de gênero (**ODS 5**) e raça/cor (**ODS 18**) na faixa etária adulta jovem e reprodutiva (`18–45 anos`), permitindo mensurar com exatidão a letalidade armada (`61,04%`) e a vitimização de mulheres negras (`75,51%` das identificadas).
5. **Exclusão de Registros sem Gênero ou sem Idade Informada:** Essencial para garantir veracidade estatística e permitir o funcionamento sem viés do alternador dinâmico entre **Média (`29,6 anos`)** e **Mediana (`29,0 anos`)** no Dashboard (Fase 4).
6. **Conformidade Legal com a LGPD (Lei nº 13.709/2018):** A remoção de `endereco` físico e dados funcionais de agentes, somada ao hash SHA-256 nos IDs e ao truncamento das coordenadas para 2 casas decimais, cumpre os artigos 6º (minimização), 12 e 13 (anonimização para estudos e pesquisa) da LGPD.
7. **Otimização para o Limite de 1 GB da Aiven (Fase 3):** A eliminação das linhas cartesianas zeradas e de registros fora dos critérios da equipe reduz o consumo de armazenamento no PostgreSQL da Aiven em mais de **99%**, mantendo o Data Warehouse completo em menos de **5 MB** com performance instantânea de consulta.
