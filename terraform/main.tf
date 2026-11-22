# ==============================================================================
# ENTREGÁVEL 4: Infraestrutura como Código (IaC) - Armazenamento do Banco de Dados
# Projeto: Observatório Interseccional da Violência nas Capitais (2025) - ODS 5 & 18
# Provisiona toda a infraestrutura do Data Warehouse PostgreSQL 16 na Aiven Cloud:
#   1. Instância Gerenciada PostgreSQL 16 (aiven_pg) com SSL obrigatório
#   2. Banco de Dados Dimensional (aiven_pg_database: dw_violencia_interseccional)
#   3. Usuários segregados para Pipeline ETL (Escrita) e Dashboard BI (Leitura)
#   4. Bootstrap opcional do Esquema Estrela (sql/schema.sql e sql/seed_star_schema.sql)
# ==============================================================================

locals {
  common_tags = {
    projeto     = "observatorio-interseccional-violencia-capitais-2025"
    ods         = "ods5-genero-ods18-igualdade-etnico-racial"
    entregavel  = "entregavel-4-infraestrutura-terraform"
    modelagem   = "star-schema-postgresql-16"
    governanca  = "lgpd-sha256-kanonimato"
  }
}

# 1. Serviço Gerenciado PostgreSQL 16 na Aiven Cloud (Free Tier 1 GB / Hobbyist / Startup)
resource "aiven_pg" "pg_bigdata_ods" {
  project                 = var.aiven_project_name
  cloud_name              = var.cloud_name
  plan                    = var.service_plan
  service_name            = var.service_name
  maintenance_window_dow  = var.maintenance_window_dow
  maintenance_window_time = var.maintenance_window_time
  termination_protection  = var.termination_protection

  dynamic "tag" {
    for_each = local.common_tags
    content {
      key   = tag.key
      value = tag.value
    }
  }

  pg_user_config {
    pg_version = var.pg_version

    # Controle de Acesso por Filtro de IP (Firewall de Rede)
    ip_filter_string = var.allowed_ip_cidrs

    public_access {
      pg         = true
      prometheus = false
    }

    pg {
      timezone                   = var.db_timezone
      track_activity_query_size  = 2048
      log_min_duration_statement = 1000
      max_connections            = var.pg_max_connections
    }
  }
}

# 2. Banco de Dados Relacional Dedicado ao Data Warehouse (Esquema Estrela / Star Schema)
resource "aiven_pg_database" "dw_violencia_ods" {
  project       = var.aiven_project_name
  service_name  = aiven_pg.pg_bigdata_ods.service_name
  database_name = var.database_name
  lc_collate    = "en_US.UTF-8"
  lc_ctype      = "en_US.UTF-8"
}

# 3. Usuário Dedicado para o Pipeline de ETL (Carga das 4 Dimensões e 2 Tabelas Fato)
resource "aiven_pg_user" "etl_pipeline_user" {
  project      = var.aiven_project_name
  service_name = aiven_pg.pg_bigdata_ods.service_name
  username     = var.db_app_username
}

# 4. Usuário Dedicado de Leitura para o Dashboard Analítico Streamlit (Menor Privilégio)
resource "aiven_pg_user" "dashboard_readonly_user" {
  project      = var.aiven_project_name
  service_name = aiven_pg.pg_bigdata_ods.service_name
  username     = var.db_readonly_username
}

# 5. Aplicação Automatizada Opcional do Esquema Estrela (DDL schema.sql + Carga Inicial)
resource "null_resource" "bootstrap_star_schema" {
  count = var.auto_apply_schema ? 1 : 0

  triggers = {
    schema_sha256 = filesha256("${path.module}/sql/schema.sql")
    database_id   = aiven_pg_database.dw_violencia_ods.id
  }

  provisioner "local-exec" {
    command = "psql \"postgresql://${aiven_pg.pg_bigdata_ods.service_username}:${aiven_pg.pg_bigdata_ods.service_password}@${aiven_pg.pg_bigdata_ods.service_host}:${aiven_pg.pg_bigdata_ods.service_port}/${aiven_pg_database.dw_violencia_ods.database_name}?sslmode=require\" -f \"${path.module}/sql/schema.sql\""
  }

  depends_on = [
    aiven_pg.pg_bigdata_ods,
    aiven_pg_database.dw_violencia_ods,
  ]
}
