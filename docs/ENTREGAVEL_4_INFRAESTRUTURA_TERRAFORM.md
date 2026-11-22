# ☁️ Entregável 4: Infraestrutura como Código (Terraform) — Armazenamento do Banco de Dados

**Projeto:** Observatório Interseccional da Violência contra a Mulher nas Capitais do Brasil (2025)  
**Alinhamento Agenda 2030:** **ODS 5** (Igualdade de Gênero) e **ODS 18** (Igualdade Étnico-Racial)  
**Repositório Dedicado da Infraestrutura (Entregável 4):** [`https://github.com/DevVini8/terraform`](https://github.com/DevVini8/terraform)  
**Provedor de Nuvem & Banco de Dados:** **Aiven Cloud — Managed PostgreSQL 16 (`free-tier-1gb`)**  
**Ferramenta de IaC:** **HashiCorp Terraform (`>= 1.3.0`)** com Provider Oficial **`aiven/aiven` (`~> 4.0`)**

---

## 1. Visão Geral da Infraestrutura de Armazenamento

Toda a infraestrutura responsável por hospedar e armazenar o **Data Warehouse Dimensional (`dw_violencia_interseccional`)** foi codificada de forma declarativa, versionável e reprodutível utilizando **Terraform** e publicada no repositório [`https://github.com/DevVini8/terraform`](https://github.com/DevVini8/terraform).

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
   - A infraestrutura inclui dentro de `terraform/sql/` tanto o script DDL do Esquema Estrela (`sql/schema.sql`) quanto o Dump SQL completo com os 688 registros tratados (`sql/seed_star_schema.sql`), permitindo inicializar toda a estrutura física do banco automaticamente quando `auto_apply_schema = true`.

---

## 2. Organização dos Arquivos no Repositório `https://github.com/DevVini8/terraform`

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

## 3. Detalhamento dos Recursos Terraform (`main.tf`, `variables.tf`, `outputs.tf`)

| Recurso Terraform | Tipo no Provider | Nome Lógico | Função na Infraestrutura de Armazenamento |
| :--- | :--- | :--- | :--- |
| **Servidor PostgreSQL 16** | `aiven_pg` | `pg_bigdata_ods` | Provisiona a instância gerenciada PostgreSQL 16 na Aiven com TLS/SSL, firewall de IP, janela de manutenção e parâmetros de log/conexão. |
| **Banco Dimensional** | `aiven_pg_database` | `dw_violencia_ods` | Cria o banco `dw_violencia_interseccional` dedicado ao armazenamento do Esquema Estrela. |
| **Usuário do Pipeline ETL** | `aiven_pg_user` | `etl_pipeline_user` | Cria a credencial `etl_ods_writer` utilizada pelo módulo `etl/load.py` para carga em batches. |
| **Usuário Leitura Dashboard** | `aiven_pg_user` | `dashboard_readonly_user` | Cria a credencial `analista_ods_reader` utilizada pela camada de visualização (Streamlit). |
| **Bootstrap do Schema SQL** | `null_resource` | `bootstrap_star_schema` | Executa opcionalmente (`auto_apply_schema = true`) o script `sql/schema.sql` via `psql` assim que o banco fica disponível. |
