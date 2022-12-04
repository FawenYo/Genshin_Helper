export KUBE_CONFIG_PATH=~/.kube/config

pushd main;
terraform init;
terraform apply -var-file=../config/settings.tfvars $* 2>&1;