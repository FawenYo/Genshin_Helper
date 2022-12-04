output "redis" {
  value = {
    endpoint = "${helm_release.redis.name}-master.${helm_release.redis.namespace}.svc.cluster.local"
    password = random_password.redis_password.result
  }
}