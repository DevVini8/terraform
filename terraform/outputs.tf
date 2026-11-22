# ==============================================================================
# ENTREGÁVEL 4: Outputs do Provisionamento (outputs.tf)
# Exporta metadados da instância, endpoints e URIs SSL para o ETL e Dashboard
# ==============================================================================

output "service_name" {
  description = "Nome do serviço PostgreSQL 16 provisionado na Aiven"
  value       = aiven_pg.pg_bigdata_ods.service_name
}

output "service_state" {
  description = "Estado operacional da instância PostgreSQL na Aiven"
  value       = aiven_pg.pg_bigdata_ods.state
}

output "cloud_region" {
  description = "Provedor e região de nuvem onde o banco está hospedado"
  value       = aiven_pg.pg_bigdata_ods.cloud_name
}

output "service_plan" {
  description = "Plano de capacidade contratado/alocado na Aiven"
  value       = aiven_pg.pg_bigdata_ods.plan
}

output "db_host" {
  description = "Hostname público do servidor PostgreSQL na Aiven"
  value       = aiven_pg.pg_bigdata_ods.service_host
}

output "db_port" {
  description = "Porta TCP/SSL de conexão do servidor PostgreSQL na Aiven"
  value       = aiven_pg.pg_bigdata_ods.service_port
}

output "db_name" {
  description = "Nome do banco de dados dimensional (Star Schema) criado"
  value       = aiven_pg_database.dw_violencia_ods.database_name
}

output "db_admin_user" {
  description = "Usuário administrador principal da instância (avnadmin)"
  value       = aiven_pg.pg_bigdata_ods.service_username
}

output "db_admin_password" {
  description = "Senha do usuário administrador principal (sensível)"
  value       = aiven_pg.pg_bigdata_ods.service_password
  sensitive   = true
}

output "db_etl_user" {
  description = "Usuário de aplicação provisionado para o Pipeline ETL"
  value       = aiven_pg_user.etl_pipeline_user.username
}

output "db_dashboard_readonly_user" {
  description = "Usuário provisionado para leitura pelo Dashboard Analítico"
  value       = aiven_pg_user.dashboard_readonly_user.username
}

output "database_uri" {
  description = "URI completa de conexão PostgreSQL (Admin/ETL) com criptografia SSL obrigatória (sslmode=require)"
  value       = "postgresql://${aiven_pg.pg_bigdata_ods.service_username}:${aiven_pg.pg_bigdata_ods.service_password}@${aiven_pg.pg_bigdata_ods.service_host}:${aiven_pg.pg_bigdata_ods.service_port}/${aiven_pg_database.dw_violencia_ods.database_name}?sslmode=require"
  sensitive   = true
}

output "dashboard_readonly_uri" {
  description = "URI completa de conexão PostgreSQL exclusiva para o Dashboard BI com SSL obrigatório"
  value       = "postgresql://${aiven_pg_user.dashboard_readonly_user.username}:${aiven_pg_user.dashboard_readonly_user.password}@${aiven_pg.pg_bigdata_ods.service_host}:${aiven_pg.pg_bigdata_ods.service_port}/${aiven_pg_database.dw_violencia_ods.database_name}?sslmode=require"
  sensitive   = true
}
