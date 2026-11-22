# 📦 Entregável 6: Repositório do Projeto (Organização e Guia de Reprodutibilidade)

**Projeto:** Observatório Interseccional da Violência contra a Mulher nas Capitais do Brasil (2025)  
**Alinhamento Agenda 2030:** **ODS 5** (Igualdade de Gênero) e **ODS 18** (Igualdade Étnico-Racial)  
**Repositórios Git Publicados pela Equipe:**
- **Repositório do Projeto / Pipeline de Dados (`process-data`):** [`https://github.com/DevVini8/process-data`](https://github.com/DevVini8/process-data)
- **Repositório Dedicado da Infraestrutura Terraform (`terraform`):** [`https://github.com/DevVini8/terraform`](https://github.com/DevVini8/terraform)

---

## 1. Visão Geral da Organização do Repositório

O repositório do projeto foi estruturado seguindo os padrões de **Engenharia de Dados Moderna (DataOps & DevSecOps)**, separando claramente as responsabilidades em módulos independentes para garantir legibilidade, governança LGPD e reprodutibilidade ponta a ponta:

1. **Código Utilizado no Tratamento dos Dados (`/etl`):** Pipeline modular completo em Python (`extract.py`, `transform.py`, `load.py`, `config.py`, `pipeline.py` e `schema.sql`) que transforma as bases brutas (`fonte original.xlsx` e `complemento fogo cruzado.xlsx`) na base final tratada e no Data Warehouse em Esquema Estrela.
2. **Arquivos Relacionados à Infraestrutura (`/terraform`):** Infraestrutura como Código (IaC) utilizando HashiCorp Terraform (`versions.tf`, `main.tf`, `variables.tf`, `outputs.tf`, `terraform.tfvars.example` e `sql/`) para provisionamento automatizado do PostgreSQL 16 na Aiven Cloud.
3. **Documentação Técnica Completa (`README.md`, `/docs` e `.docx`):** Relatórios técnicos detalhados de cada entregável, dicionário de dados, diagramas de arquitetura e Entidade-Relacionamento (Mermaid), justificativas técnicas e roteiro de apresentação.
4. **Demais Arquivos para Reprodução, Acesso ao Banco e Compreensão da Solução (`/data/processed`, `/dashboard`, `/tests`, `acessar_banco.py`, `requirements.txt`, `.env.example`, `.github/workflows`):** Bases tratadas em CSV, banco relacional portátil SQLite3 (`.db`), Dump SQL completo (`.sql`), utilitário CLI de consulta ao banco, aplicação interativa de BI em Streamlit e suíte de testes unitários automatizados.

---

## 2. Mapa de Identificação dos Artefatos Obrigatórios no Repositório

| Requisito do Entregável 6 | Diretório / Arquivos no Repositório | Descrição e Papel na Solução |
| :--- | :--- | :--- |
| **1. Código utilizado no tratamento dos dados** | [`/etl/config.py`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/etl/config.py)<br>[`/etl/extract.py`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/etl/extract.py)<br>[`/etl/transform.py`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/etl/transform.py)<br>[`/etl/load.py`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/etl/load.py)<br>[`/etl/pipeline.py`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/etl/pipeline.py)<br>[`/etl/schema.sql`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/etl/schema.sql) | Implementa a extração das planilhas brutas, padronização Unicode, aplicação dos 6 Critérios de Inclusão e 3 Critérios de Exclusão da equipe, anonimização LGPD (SHA-256 + truncamento espacial de coordenadas), construção do Esquema Estrela e carga em lotes (`chunksize=5000`). |
| **2. Arquivos relacionados à infraestrutura** | [`/terraform/versions.tf`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/terraform/versions.tf)<br>[`/terraform/main.tf`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/terraform/main.tf)<br>[`/terraform/variables.tf`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/terraform/variables.tf)<br>[`/terraform/outputs.tf`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/terraform/outputs.tf)<br>[`/terraform/terraform.tfvars.example`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/terraform/terraform.tfvars.example)<br>[`/terraform/sql/schema.sql`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/terraform/sql/schema.sql)<br>[`/terraform/sql/seed_star_schema.sql`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/terraform/sql/seed_star_schema.sql) | Provisiona como código (Terraform + provider `aiven/aiven`) a instância PostgreSQL 16 (`free-tier-1gb`), o banco `dw_violencia_interseccional`, usuários segregados (`etl_ods_writer` e `analista_ods_reader`), regras de firewall/SSL e o bootstrap do Esquema Estrela. |
| **3. Documentação** | [`README.md`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/README.md)<br>[`/docs/ENTREGAVEL_1_BASE_TRATADA.md`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/docs/ENTREGAVEL_1_BASE_TRATADA.md)<br>[`/docs/ENTREGAVEL_2_PROCESSO_DE_TRATAMENTO.md`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/docs/ENTREGAVEL_2_PROCESSO_DE_TRATAMENTO.md)<br>[`/docs/ENTREGAVEL_3_BANCO_DE_DADOS.md`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/docs/ENTREGAVEL_3_BANCO_DE_DADOS.md)<br>[`/docs/ENTREGAVEL_4_INFRAESTRUTURA_TERRAFORM.md`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/docs/ENTREGAVEL_4_INFRAESTRUTURA_TERRAFORM.md)<br>[`/docs/ENTREGAVEL_6_REPOSITORIO_DO_PROJETO.md`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/docs/ENTREGAVEL_6_REPOSITORIO_DO_PROJETO.md)<br>[`/docs/PITCH_APRESENTACAO.md`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/docs/PITCH_APRESENTACAO.md)<br>Arquivos `.docx` dos Entregáveis 1, 2, 3, 4 e 6 | Documenta a origem dos dados, diagnóstico das versões brutas, decisões técnicas, justificativa do modelo Star Schema, dicionário de tipos e relacionamentos, infraestrutura IaC e guia passo a passo de execução. |
| **4. Demais arquivos para reprodução e compreensão da solução** | [`/data/processed/dw_violencia_interseccional.db`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/data/processed/dw_violencia_interseccional.db)<br>[`/data/processed/dump_dw_violencia_interseccional.sql`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/data/processed/dump_dw_violencia_interseccional.sql)<br>[`/data/processed/*.csv`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/data/processed)<br>[`acessar_banco.py`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/acessar_banco.py)<br>[`/dashboard/app.py`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/dashboard/app.py) & [`business_rules.py`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/dashboard/business_rules.py)<br>[`/tests/test_business_rules_and_lgpd.py`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/tests/test_business_rules_and_lgpd.py)<br>[`requirements.txt`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/requirements.txt), [`.env.example`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/.env.example), [`.gitignore`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/.gitignore)<br>[`/.github/workflows/ci_etl_deploy.yml`](file:///C:/Users/Vinicius%20Freitas/Desktop/BIGDATA/.github/workflows/ci_etl_deploy.yml) | Permite reproduzir o pipeline em 1 comando, consultar o banco SQL imediatamente sem depender de credenciais externas, navegar pelo Dashboard Analítico com 6 KPIs e Console SQL ao vivo, e validar todas as regras com testes unitários e CI/CD. |

---

## 3. Árvore Completa de Diretórios do Projeto

```text
BIGDATA/
├── README.md                                               # Documentação principal da arquitetura, 5 V's, LGPD, Star Schema e Deploy
├── requirements.txt                                        # Dependências Python para reprodução do ETL, Banco, Testes e Dashboard
├── .env.example                                            # Template seguro de variáveis de ambiente (sem segredos reais)
├── .gitignore                                              # Proteção contra versionamento de .env, *.tfstate e *.tfvars
├── acessar_banco.py                                        # Utilitário CLI para consulta imediata e console SQL interativo no banco
│
├── etl/                                                    # [ENTREGÁVEL 2 & 3] Código do Processo de Tratamento dos Dados (ETL)
│   ├── __init__.py                                         # Inicializador do pacote Python ETL
│   ├── config.py                                           # Configurações, critérios da equipe e dicionário oficial das 27 Capitais
│   ├── extract.py                                          # Extração resiliente das planilhas brutas (.xlsx) e cache otimizado
│   ├── transform.py                                        # Limpeza, filtros de inclusão/exclusão, LGPD (SHA-256) e Star Schema
│   ├── load.py                                             # Carga no PostgreSQL Aiven (chunksize=5000), SQLite (.db) e Dump (.sql)
│   ├── pipeline.py                                         # Orquestrador CLI ponta a ponta (python -m etl.pipeline)
│   └── schema.sql                                          # DDL SQL do Esquema Estrela (4 Dimensões, 2 Tabelas Fato e 2 Views)
│
├── terraform/                                              # [ENTREGÁVEL 4] Infraestrutura como Código (IaC - Aiven PostgreSQL 16)
│   ├── versions.tf                                         # Versão do Terraform (>= 1.3.0) e providers (aiven/aiven ~> 4.0)
│   ├── main.tf                                             # Recursos do PostgreSQL 16, database, usuários e bootstrap SQL
│   ├── variables.tf                                        # Variáveis parametrizadas e segredos protegidos (sensitive = true)
│   ├── outputs.tf                                          # Outputs de host, porta e URIs SSL para integração com ETL e BI
│   ├── terraform.tfvars.example                            # Exemplo seguro de configuração de variáveis
│   ├── .gitignore                                          # Proteção específica de arquivos de estado Terraform
│   ├── README.md                                           # Documentação dedicada da infraestrutura Terraform
│   └── sql/                                                # Estrutura física e carga inicial do banco alocadas junto à IaC
│       ├── schema.sql                                      # DDL do Esquema Estrela para bootstrap na instância provisionada
│       └── seed_star_schema.sql                            # Dump SQL completo com os 688 registros tratados
│
├── data/
│   └── processed/                                          # [ENTREGÁVEL 1 & 3] Bases Tratadas e Banco de Dados Armazenado
│       ├── sinesp_tratado.csv                              # Base tratada SINESP (Capitais 2025 - 1.233 vítimas femininas)
│       ├── fogo_cruzado_tratado.csv                        # Base tratada e anonimizada Fogo Cruzado (77 mulheres 18-45a)
│       ├── dim_tempo.csv                                   # Tabela Dimensão Tempo (73 registros)
│       ├── dim_localidade.csv                              # Tabela Dimensão Localidade (89 registros)
│       ├── dim_perfil_vitima.csv                           # Tabela Dimensão Perfil da Vítima (11 registros)
│       ├── dim_contexto_crime.csv                          # Tabela Dimensão Contexto do Crime (39 registros)
│       ├── fato_violencia_sinesp.csv                       # Tabela Fato 1 - SINESP Capitais 2025 (399 registros)
│       ├── fato_vitimas_fogo_cruzado.csv                   # Tabela Fato 2 - Fogo Cruzado Capitais 2025 (77 registros)
│       ├── dw_violencia_interseccional.db                  # Banco Relacional SQLite3 completo pronto para acesso imediato (144 KB)
│       └── dump_dw_violencia_interseccional.sql            # Dump SQL completo (DDL + INSERTs dos 688 registros)
│
├── dashboard/                                              # Camada Analítica e Explorador Visual do Banco (Streamlit + Plotly)
│   ├── app.py                                              # Aplicação web com 6 KPIs, filtros cruzados, drill-down e Console SQL (Aba 6)
│   ├── business_rules.py                                   # Regras de negócio interseccionais ODS 5 & ODS 18 e Média vs. Mediana
│   └── requirements.txt                                    # Dependências para publicação no Streamlit Community Cloud
│
├── docs/                                                   # Documentação Técnica Markdown por Entregável
│   ├── ENTREGAVEL_1_BASE_TRATADA.md                        # Relatório Técnico do Entregável 1 (Base de Dados Tratada)
│   ├── ENTREGAVEL_2_PROCESSO_DE_TRATAMENTO.md              # Relatório Técnico do Entregável 2 (Processo de Tratamento ETL)
│   ├── ENTREGAVEL_3_BANCO_DE_DADOS.md                      # Relatório Técnico do Entregável 3 (Base Armazenada em Banco de Dados)
│   ├── ENTREGAVEL_4_INFRAESTRUTURA_TERRAFORM.md            # Relatório Técnico do Entregável 4 (Infraestrutura Terraform)
│   ├── ENTREGAVEL_6_REPOSITORIO_DO_PROJETO.md              # Relatório Técnico do Entregável 6 (Organização do Repositório)
│   └── PITCH_APRESENTACAO.md                               # Roteiro executivo de apresentação e defesa técnica (10 minutos)
│
├── tests/                                                  # Garantia de Qualidade e Reprodutibilidade Automatizada
│   └── test_business_rules_and_lgpd.py                     # Testes unitários dos critérios da equipe, LGPD e Star Schema
│
├── .github/
│   └── workflows/
│       └── ci_etl_deploy.yml                               # Pipeline CI/CD (GitHub Actions) validando Terraform e Testes Python
│
├── Entregavel_1_Base_de_Dados_Tratada.docx                 # Documento Word formal do Entregável 1
├── Entregavel_2_Processo_de_Tratamento_dos_Dados.docx      # Documento Word formal do Entregável 2
├── Entregavel_3_Base_Armazenada_em_Banco_de_Dados.docx     # Documento Word formal do Entregável 3
├── Entregavel_4_Infraestrutura_Terraform.docx              # Documento Word formal do Entregável 4
└── Entregavel_6_Repositorio_do_Projeto.docx                # Documento Word formal do Entregável 6
```

---

## 4. Guia Rápido de Reprodução da Solução a partir do Repositório

Qualquer avaliador ou integrante da equipe pode reproduzir integralmente a solução em menos de 2 minutos executando os 4 passos abaixo:

```bash
# 1. Instalar as dependências do projeto
pip install -r requirements.txt

# 2. Executar o pipeline ETL completo (Gera bases tratadas, Star Schema CSVs, Banco .db e Dump .sql)
python -m etl.pipeline --skip-db

# 3. Consultar o Banco de Dados Relacional diretamente pelo terminal (ou abrir console SQL interativo)
python acessar_banco.py
python acessar_banco.py --interativo

# 4. Executar os testes unitários automatizados e iniciar o Dashboard Interativo
python -m unittest discover -s tests -p "test_*.py" -v
streamlit run dashboard/app.py
```
