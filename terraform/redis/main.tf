########################
# Kubernetes Namespace #
########################

resource "kubernetes_namespace" "genshin_helper" {
  metadata {
    name = var.namespace
  }
}

##################
# Redis Database #
##################

resource "random_password" "redis_password" {
  length      = 64
  special     = false
  min_lower   = 1
  min_numeric = 1
  min_upper   = 1
}

resource "helm_release" "redis" {
  depends_on = [
    kubernetes_namespace.genshin_helper,
    random_password.redis_password,
  ]

  name          = "genshin-helper-redis"
  namespace     = var.namespace
  chart         = "https://charts.bitnami.com/bitnami/redis-17.3.13.tgz"
  recreate_pods = true
  max_history   = 3

  set {
    name = "master.persistence.size"
    value = "1Gi"
    type = "string"
  }

  set {
    name = "replica.persistence.size"
    value = "1Gi"
    type = "string"
  }

  set {
    name  = "replica.replicaCount"
    value = 1
    type  = "auto"
  }

  set_sensitive {
    name  = "auth.password"
    value = random_password.redis_password.result
    type  = "string"
  }
}