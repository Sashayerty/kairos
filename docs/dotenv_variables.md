# :lock: Переменные .env

`.env` файл - файл конфигурации локальных переменных для работы приложения. Ни в коем случае не передавайте содержимое своего файла 3-м лицам!

## Пример .env файла

Естественно тут сейчас фейк данные.

```bash
MISTRAL_AI_API_KEY=mistral-ai-api-key
GOOGLE_API_KEY=google-api-key
CSE_ID=cse-id
SECRET_KEY=secret-key
```

P.S. В файле можно прописать значения для `DEBUG` и `DATABASE_PATH`, но это необязательно. 

## Переменные и назначение

- `MISTRAL_AI_API_KEY` - API-ключ для взаимодействия с MistralAI. На данный момент обязателен, в будущем планируется поддержка локальных моделей. Получить ключ можно на [сайте Mistral](https://console.mistral.ai/api-keys), необходим аккаунт.
- `GOOGLE_API_KEY` и `CSE_ID` (**опционально**) - данные для использования поисковика Google. Необходимо получить на [сайте](https://programmablesearchengine.google.com/controlpanel/all). Нужен поиск в Google для поиска статей и парсинга данных из них.
- `SECRET_KEY` - секретный ключ для wtforms. Необходим для корректной работы wtforms. Нужно его создать **собственноручно**. Лучше всего для ключа подойдет `uuid4`. Сгенерировать можно или через python библиотеку `uuid`, или на [сайте](https://www.uuidgenerator.net/version4).  
    P.S. В документации Flask [рекомендуется](https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY) использовать рандомный набор байтов. Ниже **пример**:

    ```bash
    python -c 'import secrets; print(secrets.token_hex())'

    > 192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf
    ```

