# Переменные .env


## Пример .env файла

Естественно тут сейчас фейк данные.

```bash
MISTRAL_AI_API_KEY=mistral-ai-api-key
GOOGLE_API_KEY=google-api-key
CSE_ID=cse-id
SECRET_KEY=secret-key
```

## Переменные и назначение

- `MISTRAL_AI_API_KEY` - API-ключ для взаимодействия с MistralAI. На данный момент обязателен, в будущем планируется поддержка локальных моделей. Получить ключ можно на [сайте Mistral](https://console.mistral.ai/api-keys), необходим аккаунт.
- `GOOGLE_API_KEY` и `CSE_ID` - данные для использования поисковика Google. Необходимо получить на [сайте](https://programmablesearchengine.google.com/controlpanel/all). Нужен поиск в Google для поиска статей и парсинга данных из них.
- `SECRET_KEY` - секретный ключ для wtforms. Необходим для корректной работы wtforms. Нужно его создать **собственноручно**.