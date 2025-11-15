# Quick start
1. Установите значение переменных YC_FOLDER_ID, YC_TOKEN, YC_CLOUD_ID
2. Установите значение для создаваемых ресурсов
```bash
export TF_VAR_token=$YC_TOKEN
export TF_VAR_cloud_id=$YC_CLOUD_ID
export TF_VAR_folder_id=$YC_FOLDER_ID
```
3. Инициализируйте провайдер
```bash
terraform init
```
4. Спланируйте создание ресурсов. Проверьте вывод команды
```bash
terraform plan
```
5. Создайте ресурсы
```bash
terraform apply
```
6. После использования удалите ресурсы
```bash
terraform destroy
```