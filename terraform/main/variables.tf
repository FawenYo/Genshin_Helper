variable "acr_prefix" {
  type = string
}

variable "app_image" {
  type = string
}

variable "helper_fqdn" {
  type        = string
  description = "FQDN for genshin_helper"
}

variable "token" {
  type        = string
  description = "Tokens for CronJob"
}

variable "line" {
  type = object({
    token  = string
    secret = string
  })
}

variable "tls_crt_key" {
  type = object({
    crt = string
    key = string
  })
}
