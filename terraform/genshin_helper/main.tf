resource "helm_release" "app" {
  name          = "genshin-helper-app"
  namespace     = var.namespace
  chart         = "${path.module}/charts"
  recreate_pods = true
  max_history   = 3

  set {
    name  = "ACR_PREFIX"
    value = var.acr_prefix
  }

  set {
    name  = "APP_IMAGE"
    value = var.app_image
  }

  set {
    name  = "HELPER_FQDN"
    value = var.helper_fqdn
  }

  set {
    name  = "REDIS_URL"
    value = var.redis.endpoint
    type  = "string"
  }

  set_sensitive {
    name  = "LINE_CHANNEL_ACCESS_TOKEN"
    value = var.line.token
    type  = "string"
  }

  set_sensitive {
    name  = "LINE_CHANNEL_SECRET"
    value = var.line.secret
    type  = "string"
  }

  set_sensitive {
    name  = "REDIS_PASSWORD"
    value = var.redis.password
    type  = "string"
  }

  set_sensitive {
    name  = "TOKEN"
    value = var.token
    type  = "string"
  }

  set_sensitive {
    name  = "TLS_SIDECAR_CRT"
    value = var.tls_crt_key.crt
    type  = "string"
  }

  set_sensitive {
    name  = "TLS_SIDECAR_KEY"
    value = var.tls_crt_key.key
    type  = "string"
  }
}
