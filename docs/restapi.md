# :dizzy: RestAPI Docs

Документация для RestAPI Kairos. `RestAPI` — это стандартизированный подход к созданию веб-сервисов, который использует HTTP-протокол для взаимодействия между клиентом и сервером.

## Проверить тему пользователя и пожелания

```bash
POST /api/check
```

Проверяет тему пользователя и пожелания на наличие нецензурного содержания.

### Параметры

- `theme`: (required) Тема курса для проверки
- `desires`: (optional) Пожелания к курсу

### Пример

#### Status `200`

Запрос:

```bash
curl -X POST http://127.0.0.1:5000/api/check -H "Content-Type: application/json" -d '{
  "theme": "Learning Python",
  "desires": "Understand the basics of Python programming"
}'
```

Ответ:

```bash
{
    "message": "Theme is good",
    "theme_is_good": true
}
```

#### Status `400`

Запрос:

```bash
curl -X POST http://127.0.0.1:5000/api/check -H "Content-Type: application/json" -d '{
  "theme": "Что-то незаконное",
  "desires": "Что-то незаконное"
}'
```

Ответ:

```bash
{
    "message": "Тема пользователя связана с чем-то незаконным.",
    "theme_is_good": false
}
```

## Сгенерировать курс

```bash
POST /api/gen
```

Генерирует курс по теме, пожеланию и описанию пользователя.

### Параметры

- `theme`: (required) Тема курса для проверки
- `desires`: (optional) Пожелания к курсу
- `description_of_user`: (optional) Описание пользователя

### Пример

#### Status `200`

Запрос:

```bash
curl -X POST http://127.0.0.1:5000/api/gen -H "Content-Type: application/json" -d '{
    "theme": "Learning Python",
    "desires": "Understand the basics of Python programming",
    "description_of_user": "Beginner in programming"
  }'
```

Ответ:

```bash
{
    "theme": "Learning Python",
    "desires": "Understand the basics of Python programming",
    "description_of_user": "Beginner in programming",
    "answer_from_censor": {
        "data": true
    },
    "prompt_from_llm": ...,
    "plan": {...},
    "course": {...}
}
```

#### Status `400`

Запрос:

```bash
curl -X POST http://127.0.0.1:5000/api/gen -H "Content-Type: application/json" -d '{
    "theme": "Что-то незаконное",
    "desires": "Что-то незаконное"
  }'
```

Ответ:

```bash
{
    "message": "Тема пользователя связана с чем-то незаконным.",
    "theme_is_good": false
}
```
