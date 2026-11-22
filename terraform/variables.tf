# ==============================================================================
# ENTREGÁVEL 4: Variáveis de Infraestrutura (variables.tf)
# Parametrização completa do provisionamento do Banco de Dados PostgreSQL na Aiven
# ==============================================================================

variable "aiven_api_token" {
  description = "Token de autenticação da API Aiven (injetar via TF_VAR_aiven_api_token ou GitHub Secrets; nunca versionar em texto puro)"
  type        = string
  sensitive   = true
}

variable "aiven_project_name" {
  description = "Nome do projeto cadastrado na plataforma Aiven Cloud"
  type        = string
}

variable "cloud_name" {
  description = "Provedor e região de nuvem na Aiven (ex: do-nyc no Free Tier, aws-sa-east-1 ou google-southamerica-east1)"
  type        = string
  default     = "do-nyc"
}

variable "service_plan" {
  description = "Plano de capacidade do serviço PostgreSQL na Aiven ('free-tier-1gb' para limite gratuito de 1 GB, 'hobbyist' ou 'startup-4')"
  type        = string
  default     = "free-tier-1gb"
}

variable "service_name" {
  description = "Nome identificador único do serviço PostgreSQL na Aiven"
  type        = string
  default     = "pg-bigdata-ods5-ods18"
}

variable "pg_version" {
  description = "Versão do motor relacional PostgreSQL"
  type        = string
  default     = "16"
}

variable "database_name" {
  description = "Nome do banco de dados dimensional (Star Schema: 4 Dimensões, 2 Tabelas Fato e 2 Views)"
  type        = string
  default     = "dw_violencia_interseccional"
}

variable "db_app_username" {
  description = "Usuário de serviço dedicado para execução do Pipeline de ETL (carga em lotes)"
  type        = string
  default     = "etl_ods_writer"
}

variable "db_readonly_username" {
  description = "Usuário de serviço dedicado para leitura analítica pelo Dashboard Streamlit"
  type        = string
  default     = "analista_ods_reader"
}

variable "db_timezone" {
  description = "Fuso horário padrão do servidor PostgreSQL"
  type        = string
  default     = "America/Sao_Paulo"
}

variable "pg_max_connections" {
  description = "Limite máximo de conexões simultâneas no pool do PostgreSQL"
  type        = number
  default     = 20
}

variable "allowed_ip_cidrs" {
  description = "Lista de blocos CIDR autorizados a acessar o PostgreSQL (padrão 0.0.0.0/0 para permitir acesso do Streamlit Cloud e GitHub Actions com SSL obrigatório)"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "maintenance_window_dow" {
  description = "Dia da semana para janela de manutenção automática na Aiven"
  type        = string
  default     = "sunday"
}

variable "maintenance_window_time" {
  description = "Horário para janela de manutenção automática (UTC)"
  type        = string
  default     = "03:00:00"
}

variable "termination_protection" {
  description = "Habilita proteção contra exclusão acidental da instância do banco de dados"
  type        = bool
  default     = false
}

variable "auto_apply_schema" {
  description = "Quando true, executa automaticamente o script DDL sql/schema.sql via provisioner local-exec após criar o banco"
  type        = bool
  default     = false
}
