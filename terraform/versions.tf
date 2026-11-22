# ==============================================================================
# ENTREGÁVEL 4: Versões e Providers do Terraform (versions.tf)
# Infraestrutura como Código (IaC) para Armazenamento do Data Warehouse
# ==============================================================================

terraform {
  required_version = ">= 1.3.0"

  required_providers {
    aiven = {
      source  = "aiven/aiven"
      version = "~> 4.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.4"
    }
  }
}

provider "aiven" {
  api_token = var.aiven_api_token
}
