# ☁️ Entregável 4: Infraestrutura como Código (Terraform) — Armazenamento do Banco de Dados

**Projeto:** Observatório Interseccional da Violência contra a Mulher nas Capitais do Brasil (2025)  
**Alinhamento Agenda 2030:** **ODS 5** (Igualdade de Gênero) e **ODS 18** (Igualdade Étnico-Racial)  
**Provedor de Nuvem & Banco de Dados:** **Aiven Cloud — Managed PostgreSQL 16 (`free-tier-1gb`)**  
**Ferramenta de IaC:** **HashiCorp Terraform (`>= 1.3.0`)** com Provider Oficial **`aiven/aiven` (`~> 4.0`)**

---

## 1. Visão Geral da Infraestrutura de Armazenamento

Toda a infraestrutura responsável por hospedar e armazenar o **Data Warehouse Dimensional (`dw_violencia_interseccional`)** foi codificada de forma declarativa, versionável e reprodutível utilizando **Terraform**.

A arquitetura provisionada na **Aiven Cloud** contempla:
1. **Instância Gerenciada PostgreSQL 16 (`aiven_pg.pg_bigdata_ods`):**
   - Configurada no plano `free-tier-1gb` (1 GB de armazenamento dedicado — o Data Warehouse completo do projeto consome apenas **`144 KB`**, operando com mais de **99,98% de margem livre**).
   - Criptografia em trânsito obrigatória via **TLS/SSL (`sslmode=require`)**.
   - Fuso horário padronizado para `America/Sao_Paulo`, janela de manutenção semanal automatizada (`domingo às 03:00 UTC`), auditoria de queries lentas (`log_min_duration_statement = 1000ms`), controle de firewall por lista CIDR (`ip_filter_string`) e tags de governança (`ODS 5`, `ODS 18`, `LGPD`).
2. **Banco de Dados Dimensional (`aiven_pg_database.dw_violencia_ods`):**
   - Cria o banco lógico `dw_violencia_interseccional` com codificação `en_US.UTF-8`, onde residem as **4 Tabelas de Dimensão**, **2 Tabelas Fato** e **2 Views Analíticas** do Esquema Estrela (*Star Schema*).
3. **Segregação de Credenciais e Princípio do Menor Privilégio:**
   - **`aiven_pg_user.etl_pipeline_user` (`etl_ods_writer`):** Usuário de serviço dedicado à escrita em lotes (`chunksize=5000`) pelo Pipeline ETL.
   - **`aiven_pg_user.dashboard_readonly_user` (`analista_ods_reader`):** Usuário de serviço dedicado às consultas de leitura analítica OLAP do Dashboard Streamlit.
4. **Bootstrap Automatizado do Esquema Estrela (`null_resource.bootstrap_star_schema` + pasta `/sql`):**
   - A infraestrutura inclui dentro de `/sql` tanto o script DDL do Esquema Estrela (`sql/schema.sql`) quanto o Dump SQL completo com os 688 registros tratados (`sql/seed_star_schema.sql`), permitindo inicializar toda a estrutura física do banco automaticamente quando `auto_apply_schema = true`.

---

## 2. Diagrama da Infraestrutura Provisionada via Terraform

```mermaid
flowchart TB
    subgraph DevSecOps["🔐 Gestão de Segredos & IaC"]
        TFVARS["Variáveis Seguras\nTF_VAR_aiven_api_token\nterraform.tfvars (ignorado no Git)"]
        TF["HashiCorp Terraform >= 1.3\n• versions.tf (Provider aiven/aiven ~> 4.0)\n• main.tf\n• variables.tf\n• outputs.tf"]
        TFVARS --> TF
    end

    subgraph AivenCloud["☁️ Aiven Cloud — Managed PostgreSQL 16 (Free Tier 1 GB)"]
        PG["aiven_pg.pg_bigdata_ods\nServiço: pg-bigdata-ods5-ods18\nPostgreSQL 16 • SSL/TLS Obrigatório\nFirewall CIDR + Timezone America/Sao_Paulo"]
        DB[("aiven_pg_database.dw_violencia_ods\nBanco: dw_violencia_interseccional\nCollation: en_US.UTF-8")]
        U1["aiven_pg_user.etl_pipeline_user\nUsuário ETL: etl_ods_writer"]
        U2["aiven_pg_user.dashboard_readonly_user\nUsuário BI: analista_ods_reader"]

        PG --> DB
        PG --> U1
        PG --> U2
    end

    subgraph StarSchema["🗄️ Estrutura Física Alocada no Banco (/sql)"]
        DDL["sql/schema.sql (DDL Star Schema)\n• 4 Dimensões: dim_tempo (73), dim_localidade (89),\n  dim_perfil_vitima (11), dim_contexto_crime (39)\n• 2 Fatos: fato_violencia_sinesp (399),\n  fato_vitimas_fogo_cruzado (77)\n• 2 Views: vw_resumo_violencia_sinesp,\n  vw_resumo_interseccional_fogo_cruzado"]
        SEED["sql/seed_star_schema.sql\nCarga Completa (688 registros / 144 KB)"]
        DB --> DDL --> SEED
    end

    TF ==>|"terraform apply"| PG
```

---

## 3. Organização dos Arquivos no Repositório

```text
terraform/
├── versions.tf                 # Definição da versão do Terraform (>= 1.3.0) e providers (aiven/aiven ~> 4.0, null, local)
├── main.tf                     # Declaração dos recursos de infraestrutura do banco PostgreSQL 16, database, usuários e bootstrap SQL
├── variables.tf                # Declaração tipada de todas as variáveis de configuração, rede, plano e segurança (sensitive = true)
├── outputs.tf                  # Exportação segura dos endpoints (host, port, database_name) e URIs SSL para o ETL e Dashboard
├── terraform.tfvars.example    # Template de variáveis para configuração rápida sem expor credenciais reais
├── .gitignore                  # Bloqueio estrito contra commit de .tfstate, .env e arquivos *.tfvars com tokens reais
├── README.md                   # Documentação completa da infraestrutura e guia de provisionamento
└── sql/                        # Estrutura física e dados do Banco de Dados alocados junto à infraestrutura
    ├── schema.sql              # DDL completo do Esquema Estrela (4 Dimensões, 2 Tabelas Fato, Índices B-Tree e 2 Views Analíticas)
    └── seed_star_schema.sql    # Dump SQL completo (DDL + INSERTs dos 688 registros tratados das Capitais em 2025)
```

---

## 4. Detalhamento dos Recursos Terraform (`main.tf`, `variables.tf`, `outputs.tf`)

### 4.1. Recursos Declarados em `main.tf`
| Recurso Terraform | Tipo no Provider | Nome Lógico | Função na Infraestrutura de Armazenamento |
| :--- | :--- | :--- | :--- |
| **Servidor PostgreSQL 16** | `aiven_pg` | `pg_bigdata_ods` | Provisiona a instância gerenciada PostgreSQL 16 na Aiven com TLS/SSL, firewall de IP, janela de manutenção e parâmetros de log/conexão. |
| **Banco Dimensional** | `aiven_pg_database` | `dw_violencia_ods` | Cria o banco `dw_violencia_interseccional` dedicado ao armazenamento do Esquema Estrela. |
| **Usuário do Pipeline ETL** | `aiven_pg_user` | `etl_pipeline_user` | Cria a credencial `etl_ods_writer` utilizada pelo módulo `etl/load.py` para carga em batches. |
| **Usuário Leitura Dashboard** | `aiven_pg_user` | `dashboard_readonly_user` | Cria a credencial `analista_ods_reader` utilizada pela camada de visualização (Streamlit). |
| **Bootstrap do Schema SQL** | `null_resource` | `bootstrap_star_schema` | Executa opcionalmente (`auto_apply_schema = true`) o script `sql/schema.sql` via `psql` assim que o banco fica disponível. |

### 4.2. Variáveis Configuráveis em `variables.tf`
| Variável | Tipo | Valor Padrão | Sensível? | Descrição |
| :--- | :---: | :--- | :---: | :--- |
| `aiven_api_token` | `string` | *(obrigatório)* | **Sim (`true`)** | Token de autenticação da API Aiven Cloud. |
| `aiven_project_name` | `string` | *(obrigatório)* | Não | Nome do projeto na conta Aiven. |
| `cloud_name` | `string` | `"do-nyc"` | Não | Região e provedor de nuvem na Aiven. |
| `service_plan` | `string` | `"free-tier-1gb"` | Não | Plano de serviço PostgreSQL (1 GB gratuito). |
| `service_name` | `string` | `"pg-bigdata-ods5-ods18"` | Não | Nome único da instância PostgreSQL na Aiven. |
| `pg_version` | `string` | `"16"` | Não | Versão principal do PostgreSQL. |
| `database_name` | `string` | `"dw_violencia_interseccional"` | Não | Nome do banco de dados dimensional criado. |
| `db_app_username` | `string` | `"etl_ods_writer"` | Não | Usuário de aplicação para carga ETL. |
| `db_readonly_username` | `string` | `"analista_ods_reader"` | Não | Usuário de leitura para o Dashboard. |
| `allowed_ip_cidrs` | `list(string)` | `["0.0.0.0/0"]` | Não | Blocos CIDR permitidos no firewall da instância. |
| `auto_apply_schema` | `bool` | `false` | Não | Habilita aplicação automática do `sql/schema.sql` após o provisionamento. |

### 4.3. Outputs Exportados em `outputs.tf`
- **`db_host` / `db_port` / `db_name`:** Hostname público, porta SSL e nome do banco dimensional criado.
- **`db_admin_user` / `db_etl_user` / `db_dashboard_readonly_user`:** Usuários provisionados na instância.
- **`database_uri` *(sensitive)*:** String de conexão completa `postgresql://user:pass@host:port/dw_violencia_interseccional?sslmode=require` pronta para injeção no `.env` do Pipeline ETL.
- **`dashboard_readonly_uri` *(sensitive)*:** String de conexão dedicada para os *Secrets* do Streamlit Cloud.

---

## 5. Estrutura do Banco de Dados Alocada na Infraestrutura (`/sql`)

O diretório `/sql` embarca toda a definição física do banco de dados que é hospedado na infraestrutura provisionada:

| Tabela / View Alocada (`sql/schema.sql`) | Tipo | Chave Primária (PK) | Chaves Estrangeiras (FK) | Registros Armazenados (`sql/seed_star_schema.sql`) |
| :--- | :--- | :--- | :--- | :---: |
| **`dim_tempo`** | Dimensão | `id_tempo` (`INTEGER`) | — | **`73`** |
| **`dim_localidade`** | Dimensão | `id_localidade` (`SERIAL`) | — | **`89`** |
| **`dim_perfil_vitima`** | Dimensão | `id_perfil` (`SERIAL`) | — | **`11`** |
| **`dim_contexto_crime`** | Dimensão | `id_contexto` (`SERIAL`) | — | **`39`** |
| **`fato_violencia_sinesp`** | Tabela Fato 1 | `id_fato_sinesp` (`SERIAL`) | `id_tempo`, `id_localidade`, `id_contexto` | **`399`** *(1.233 vítimas femininas nas 27 Capitais)* |
| **`fato_vitimas_fogo_cruzado`** | Tabela Fato 2 | `id_fato_fc` (`SERIAL`) | `id_tempo`, `id_localidade`, `id_perfil`, `id_contexto` | **`77`** *(77 mulheres baleadas 18–45a nas Capitais)* |
| **`vw_resumo_violencia_sinesp`** | View SQL | — | `JOIN` Fato 1 + 3 Dimensões | `399` *(virtual)* |
| **`vw_resumo_interseccional_fogo_cruzado`** | View SQL | — | `JOIN` Fato 2 + 4 Dimensões | `77` *(virtual)* |

---

## 6. Como Executar o Provisionamento da Infraestrutura

```bash
# 1. Configurar as variáveis a partir do template de exemplo
cp terraform.tfvars.example terraform.tfvars
# Edite terraform.tfvars inserindo seu aiven_api_token e aiven_project_name
# (ou exporte TF_VAR_aiven_api_token e TF_VAR_aiven_project_name no terminal)

# 2. Inicializar o diretório e baixar o provider oficial aiven/aiven
terraform init

# 3. Validar a sintaxe e inspecionar o plano de execução
terraform validate
terraform plan

# 4. Provisionar a infraestrutura completa do banco de dados na Aiven Cloud
terraform apply -auto-approve

# 5. Extrair a URI de conexão SSL gerada para uso no Pipeline ETL e no Dashboard
terraform output -raw database_uri
```
