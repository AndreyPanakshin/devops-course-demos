# Yandex Cloud Functions

Yandex Cloud Functions -- это сервис, который позволяет запускать ваш код в виде функции в безопасном, 
отказоустойчивом и автоматически масштабируемом окружении без создания и обслуживания виртуальных машин.

## Serverless
[Бессерверные вычисления, или Serverless,](https://cloud.ru/blog/kak-rabotayet-serverless) — это модель работы с 
облачными вычислениями, при которой разработчикам не нужно управлять серверами, поэтому они могут полностью 
сосредоточиться на написании кода, построении архитектуры продукта под реализацию задач бизнеса.

## Создание Python функции 
```python
import json
import socket
import datetime

def handler(event, context):
    body = {
        'hostname': socket.gethostname(),
        'timestamp': datetime.datetime.now().isoformat(),
        'message': 'Backend service is running!'
    }
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body)
    }
```