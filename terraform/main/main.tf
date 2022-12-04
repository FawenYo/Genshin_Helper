terraform {
  required_providers {
    helm = {
      source  = "hashicorp/helm"
      version = "=2.7.1"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "2.16.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "=3.4.3"
    }
  }
}

module "ingress-nginx" {
  source = "../ingress"
}

module "redis" {
  source = "../redis"
}

module "genshin_helper" {
  depends_on = [
    module.ingress-nginx,
    module.redis
  ]

  source      = "../genshin_helper"
  acr_prefix  = var.acr_prefix
  app_image   = var.app_image
  helper_fqdn = var.helper_fqdn
  token       = var.token
  redis       = module.redis.redis
  line        = var.line
  tls_crt_key = var.tls_crt_key
}
