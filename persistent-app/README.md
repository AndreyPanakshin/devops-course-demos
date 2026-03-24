## Отправить слово

```bash
curl -X POST http://localhost:5000/word \
-H "Content-Type: application/json" \
-d '{"word": "hello"}'
```

## Список слов
```bash
curl http://localhost:5000/words
```
