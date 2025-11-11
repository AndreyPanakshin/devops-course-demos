# Yandex API Gateway
API-шлюз — это интерфейс взаимодействия с сервисами внутри Yandex Cloud или в интернете.

Интеграции с сервисами Yandex Cloud - https://yandex.cloud/ru/docs/api-gateway/concepts/extensions/

## Размещение сайта 
```yaml
openapi: 3.0.0
info:
  title: DevOps demo website
  version: 1.0.0
paths:
  /:
    get:
      x-yc-apigateway-integration:
        type: object_storage
        bucket: devops-demo
        object: index.html
        error_object: error.html
  /api/info:
    get:
      x-yc-apigateway-integration:
        type: cloud_functions
        function_id: d4edhf0elffidq89kr17
        tag: "$latest"
```