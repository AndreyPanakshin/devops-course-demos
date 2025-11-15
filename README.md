# Terraform

## Quick Start
https://yandex.cloud/ru/docs/terraform/quickstart

## Установка 
https://yandex.cloud/ru/docs/terraform/quickstart#install-terraform

```bash
wget https://hashicorp-releases.yandexcloud.net/terraform/1.14.0-rc2/terraform_1.14.0-rc2_linux_amd64.zip
unzip terraform_1.14.0-rc2_linux_amd64.zip
sudo mv terraform /usr/local/bin
terraform --version
```

## Создание SA
```bash
yc iam service-account create --name devops-course-demo --format json > sa.json
SA_ID=$(jq -r .id sa.json)
FOLDER_ID=$(jq -r .folder_id sa.json)

yc resource-manager folder add-access-binding $FOLDER_ID \
  --role admin \
  --subject serviceAccount:$SA_ID
  
echo "export YC_TOKEN=$(yc iam create-token --impersonate-service-account-id $SA_ID)" >> .env
echo "export YC_CLOUD_ID=$(yc config get cloud-id)"  >> .env
echo "export YC_FOLDER_ID=$(yc config get folder-id)" >> .env
```

## Настройка провайдера
```bash
mv ~/.terraformrc ~/.terraformrc.old

tee ~/.terraformrc > /dev/null <<EOF 
provider_installation {
  network_mirror {
    url = "https://terraform-mirror.yandexcloud.net/"
    include = ["registry.terraform.io/*/*"]
  }
  direct {
    exclude = ["registry.terraform.io/*/*"]
  }
}
EOF
```

## Настройка таймаута доступа к облаку
```bash
export TF_HTTP_TIMEOUT=240s
```