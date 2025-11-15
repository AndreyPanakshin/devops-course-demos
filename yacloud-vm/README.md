# Quick start
1. Установите значение переменных YC_FOLDER_ID, YC_TOKEN, YC_CLOUD_ID
2. Инициализируйте провайдер
```bash
terraform init
```
3. Сгенерируйте ключи для доступа к ВМ по ssh
```bash
ssh-keygen -t rsa -C "terraform-demo" -f terraform_demo_rsa -N ""
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