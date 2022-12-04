resource "kubernetes_namespace" "ingress-namespace" {
  metadata {
    name = "ingress-nginx"
  }
}

resource "helm_release" "ingress-nginx" {
  depends_on = [
    kubernetes_namespace.ingress-namespace
  ]
  name          = "ingress-nginx"
  namespace     = "ingress-nginx"
  repository    = "https://kubernetes.github.io/ingress-nginx"
  chart         = "ingress-nginx"
}