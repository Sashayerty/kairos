<p align="center">
  <a href="https://sashayerty.github.io/Kairos/"><img src="./docs/img/kairos-logo.png" alt="Kairos"></a>
</p>
<p align="center">
    <em>Kairos - веб-приложение для генерации курсов с помощью ИИ, написанное на flask</em>
</p>
<p align="center">
<a href="https://github.com/sashayerty/kairos-fastapi" target="_blank">
  <img src="https://img.shields.io/badge/FastAPI-Ver-009485.svg" alt="FastAPI Version">
</a>
<a href="https://flask.palletsprojects.com/en/stable/" target="_blank">
  <img src="https://img.shields.io/badge/Made%20with-Flask-orange.svg" alt="Made with Flask">
</a>
<a href="./LICENSE" target="_blank">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="GitHub License MIT">
</a>
<a href="https://github.com/Sashayerty/commit_maker" target="_blank">
  <img src="https://shields.io/badge/Powered_by-Commit_Maker-orange" alt="Powered by Commit Maker">
</a>
<a href="https://github.com/Sashayerty/Kairos/actions/workflows/black.yml" target="_blank">
  <img src="https://github.com/Sashayerty/Kairos/actions/workflows/black.yml/badge.svg?branch=master&event=push" alt="Black">
</a>
<a href="https://github.com/Sashayerty/Kairos/actions/workflows/flake8.yml" target="_blank">
  <img src="https://github.com/Sashayerty/Kairos/actions/workflows/flake8.yml/badge.svg?branch=master&event=push" alt="Flake8">
</a>
<a href="https://github.com/Sashayerty/Kairos/actions/workflows/tests.yml" target="_blank">
  <img src="https://github.com/Sashayerty/Kairos/actions/workflows/tests.yml/badge.svg?branch=master&event=push" alt="Tests">
</a>
<a href="https://deepwiki.com/Sashayerty/Kairos">
  <img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki">
</a>
</p>

---
**Документация:** [https://sashayerty.github.io/Kairos/](https://sashayerty.github.io/Kairos/)  
**Исходный код:** [https://github.com/Sashayerty/Kairos](https://github.com/Sashayerty/Kairos)  
**FastAPI версия:** [https://github.com/Sashayerty/kairos-fastapi](https://github.com/Sashayerty/kairos-fastapi)  
**Демонстрация:** [https://disk.yandex.ru/i/xtsrACTVPR5HrA](https://disk.yandex.ru/i/xtsrACTVPR5HrA)

---

## Обязательные учетные данные

#### 1. Google Custom Search API (optional)

Начнем с поиска данных в интернете. Для работы поиска нам понадобится CSE id и Google Search API Key. [Инструкция](https://developers.google.com/custom-search/v1/overview?hl=ru) по получению. При создании API ключа стоит учитывать, что вы можете указать список сайтов, которые будут парситься при API, что делает поиск более конкретным, узконаправленным и специфичным. Создать поисковый сервис в Google [тут](https://programmablesearchengine.google.com/controlpanel/all).

#### 2. Mistral AI API

Теперь, главная составляющая проекта - ИИ. Получить API ключ можно на официальном [сайте Mistral](https://console.mistral.ai/api-keys/).

#### 3. Secret Key

Секретный ключ для wtforms. Необходим для корректной работы wtforms. Нужно его создать **собственноручно**. Лучше всего для ключа подойдет `uuid4`. Сгенерировать можно или через python библиотеку `uuid`, или на [сайте](https://www.uuidgenerator.net/version4).  
P.S. В документации Flask [рекомендуется](https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY) использовать рандомный набор байтов. Ниже **пример**:

```bash
python -c 'import secrets; print(secrets.token_hex())'

> 192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf
```

## Пример `.env` файла

`.env` файл должен лежать в корне проекта.

```.env
MISTRAL_AI_API_KEY=mistral-ai-api-key
GOOGLE_API_KEY=google-api-key
CSE_ID=cse-id
SECRET_KEY=secret-key
```

## Установка

### Клонируем

```bash
git clone https://github.com/sashayerty/Kairos
cd ./Kairos
```

### С помощью pip

#### 1. Создаем виртуальное окружение python

```bash
# Windows
python -m venv venv
# Linux/MacOS
python3 -m venv venv
```

#### 2. Активируем виртуальное окружение

```bash
# Windows
venv/Scripts/activate
# Linux/MacOS
source venv/bin/activate
```

#### 3. Устанавливаем зависимости проекта

```bash
# Windows
pip install -r ./requirements.txt
# Linux/MacOS
pip3 install -r ./requirements.txt
```

#### 4. Запускаем локальный сервер flask

```bash
# Windows
python run.py
# Linux/MacOS
python3 run.py
```

### С помощью uv (рекомендуемое)

#### 1. Подтягиваем зависимости

```bash
uv sync # .venv создается автоматически
```

#### 2. Запускаем проект

```bash
uv run run.py
```

### Переходим на [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Взаимодействие с кодом

### ModifiedMistral (deprecated)

Это кастомный класс **Mistral**. Был он создан для того, чтобы при взаимодействии с ИИ убрать лишнюю рутинную работу. Код [тут](https://github.com/Sashayerty/Kairos/blob/master/app/mistral_ai_initializer/mistral_custom_class.py).

### ModifiedOpenAI

Пришел на смену **Mistral**. Код [тут](https://github.com/Sashayerty/Kairos/blob/master/app/ai_initializer/modified_openai.py).

### Список агентов

| В схеме | Функция            | Назначение агента                                                       |      Работает      |
| :-----: | ------------------ | ----------------------------------------------------------------------- | :----------------: |
|    1    | check              | Агент для цензуры темы и пожеланий пользователя.                        | :white_check_mark: |
|    2    | gen_prompt         | Агент для создания промпта по теме, пожеланиям и описанию пользователя. | :white_check_mark: |
|    3    | searcher           | Агент для составления поискового запроса по промпту.                    | :white_check_mark: |
|    4    | check_is_need_test | Агент для проверки нужности тестов в курсе.                             |      :bricks:      |
|    5    | gen_plan           | Агент для составления плана курса по промпту.                           | :white_check_mark: |
|    6    | analyze            | Агент для анализа данных из интернета на нужность по плану.             | :white_check_mark: |
|    7    | test               | Агент для создания тестов для курсов.                                   |      :bricks:      |
|    8    | summarizer         | Агент для сжатия статей из интернета.                                   | :white_check_mark: |
|    9    | gen_course         | Агент для генерации итогового результата.                               | :white_check_mark: |
|    *    | edit_course        | Агент для изменения курса по корректировкам пользователя                | :white_check_mark: |
|    *    | create_course      | Агент для итеративной генерации курса.                                  | :white_check_mark: |

`*` - вспомогательный агент

### [google_search](https://github.com/Sashayerty/Kairos/blob/master/app/google_custom_search/search_function.py)

Функция для поиска в Google Custom Search. Подробнее [тут](#1-google-custom-search-api-optional)

## Схема логики приложения со стороны агентов

![Логика](./docs/img/logic.png)

## База данных проекта

![База данных проекта](./docs/img/kairos.png)

## License

Kairos лицензирован [MIT](https://github.com/Sashayerty/Kairos/blob/master/LICENSE)
