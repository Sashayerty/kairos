# Kairos -

Простой проект для создания индивидуального плана обучения с помощью ИИ.

## Required credentials

### 1. Google Custom Search API

Начнем с поиска данных в интернете. Для работы поиска нам понадобится CSE id и Google Search API Key. [Инструкция](https://developers.google.com/custom-search/v1/overview?hl=ru) по получению. При создании API ключа стоит учитывать, что вы можете указать список сайтов, которые будут парсится при API, что делает поиск более конкретным, узконаправленным и специфичным.

### 2. Mistral AI API

Теперь, главная составляющая проекта - ИИ. Получить API ключ можно на официальном [сайте Mistral](https://console.mistral.ai/api-keys/).

## Пример .env-файла

.env-файл должен лежать в корне.

```bash
MISTRAL_AI_API_KEY=your-data
GOOGLE_API_KEY=your-data
CSE_ID=your-data
```

## Логика приложения со стороны агентов

![Логика](logic.png)