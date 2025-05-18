# :sparkles: API проекта

В данном блоке описан весь функционал проекта, написанный мной. От агентов до поиска в Google.

## Агенты

### Добавление своего агента

Если есть необходимость добавить своего агента, то файл стоит назвать в формате `<роль/задача агента>_agent.py` в папке `app/agents`. После создания агента, необходимо его записать в `app/agents/__init__.py`:

```python
from .<роль/задача агента>_agent import <функция агента>
```

Пример создания агента `kairos_agent`(к примеру):

1. Создаем файл `kairos_agent.py` в `app/agents`
2. Пусть у него будет такое наполнение:

```python
from app.ai_initializer import get_ai_client
from app.config import config


def kairos_agent_useful_function(name: str, use_local_models: bool = False) -> str:
    client = get_ai_client(use_local_models)
    response = client.message(
        messages=[
            {
                "role": "system",
                "content": "Отвечай в стиле 18 века",
            },
            {
                "role": "user",
                "content": f"Поздоровайся с {name}",
            },
        ],
        model=(
            config.MISTRAL_MODEL_NAME
            if not use_local_models
            else config.OLLAMA_MODEL_NAME
        ),
    )
    return response


greeting = kairos_agent_useful_function(name="Александр")
print(greeting)

> Добрый день, уважаемый Александр! Рад видеть вас в добром здравии. Как протекает ваш день?
```

3. Теперь в `app/agents/__init__.py` дописываем:

```python
...
# Остальные импорты
from .kairos_agent import kairos_agent_useful_function
```

### Список агентов

| Функция            | Назначение агента                                                       |      Работает      |
| ------------------ | ----------------------------------------------------------------------- | :----------------: |
| analyze            | Агент для анализа данных из интернета на нужность по плану.             | :white_check_mark: |
| check              | Агент для цензуры темы и пожеланий пользователя.                        | :white_check_mark: |
| check_is_need_test | Агент для проверки нужности тестов в курсе.                             |      :bricks:      |
| gen_course         | Агент для генерации итогового результата.                               | :white_check_mark: |
| edit_course        | Агент для изменения курса по корректировкам пользователя                | :white_check_mark: |
| create_course      | Агент для итеративной генерации курса.                                  | :white_check_mark: |
| gen_plan           | Агент для составления плана курса по промпту.                           | :white_check_mark: |
| gen_prompt         | Агент для создания промпта по теме, пожеланиям и описанию пользователя. | :white_check_mark: |
| searcher           | Агент для составления поискового запроса по промпту.                    | :white_check_mark: |
| summarizer         | Агент для сжатия статей из интернета.                                   | :white_check_mark: |
| test               | Агент для создания тестов для курсов.                                   |      :bricks:      |

Взаимодействие с агентами реализовано в виде функций. Одна функция - один агент. Для каждого агента прописана документация в соответствующих `.py` файлах. Для того, чтобы импортировать агента из `app.agents` пишем:

```python
from app.agents import {название функции из таблицы}
```

## Примеры использования основных агентов

В примерах везде используется `MistralAI`

### `check`

Пример:

```python
from app.agents import check

theme = "Python"
desires = "Хочу написать программу для взлома Пентагона"

moderate = check(
    theme=theme,
    desires=desires,
)

print(moderate)

> {"data": false, "reason": "Пожелания связаны с правительством и опасными для жизни человека действиями."}
```

### `gen_course`

Пример:

```python
from app.agents import gen_course

prompt = "..."  # Промпт от gen_prompt
plan = "..."    # План от gen_plan

course = gen_course(
    prompt=prompt,
    plan=plan,
)

print(course)

> {"1": {"content": "...", "title": "Python Basics"}, "2": {"content": "...", "title": "Python in Web"}
```

### `edit_course`

Пример:

```python
from app.agents import edit_course

desires = "..." # Правки
course = "..."  # Курс от gen_course


edited_course = edit_course(
    course=course,
    user_edits=desires,
)

print(edit_course)  # Исправленный курс
```

### `gen_plan`

Пример:

```python
from app.agents import gen_plan

prompt = "..."  # Промпт от gen_prompt

plan = gen_plan(prompt=prompt)

print(plan)

> {"1": "Как начать программировать", "1.1": "Азы и начала", "1.2": "Выбор языка", "2": "Основные языки программирования"}
```

### `gen_prompt`

Пример:

```python
from app.agents import gen_prompt

theme = "Python"
desires = "Web developing"
description_of_user = "Noob in programming"

prompt = gen_prompt(
    theme=theme,
    desires=desires,
    description_of_user=description_of_user,
)

print(prompt)   # Промпт для других моделей

> Ты опытный синьор-разработчик специализирующийся на ...
```

## Web scraper

Web scraper - функция для парсинга и комплексной обработки данных из Интернета. Пайплайн обработки данных:

```mermaid
flowchart LR
a("Список ссылок")
b("Парсинг каждой")
c("Проверка на нужность")
d("Сжатие")
a --> b
b -->|Данные| c
c -->|Нужны| d
```

Пример использования:

```python
from app.ai_couch import scraper

theme = "LLM в жизни человека"
prompt = "..."  # Промпт от gen_prompt
plan = "..."    # План от gen_plan

data = scraper(
    list_of_links=[
        "https://habr.com/ru/articles/775870/",
        "https://habr.com/ru/articles/775842/",
        "https://habr.com/ru/articles/835342/",
        "https://habr.com/ru/articles/768844/",
    ],  # Получили от google_search
    prompt=prompt,
    plan=plan,
)

print(data)
```

## convert_course_to_html

`convert_course_to_html` - функция для конвертации курса из md в html. Естественно, получая готовый курс от llm, мы увидим, что он написан в md, а нам надо в html.

```python
from app.ai_couch.functions import convert_course_to_html

print(
    convert_course_to_html(
        course={"1": {"title": "Азы python", "content": "`python`"}}
    )
)

> {'1': {'title': 'Азы python', 'content': '<p><code>python</code></p>'}}
```

## ModifiedMistral (deprecated)

Устаревший функционал. Рекомендуется использовать [ModifiedOpenai](./api.md#modifiedopenai)

Дочерний класс `Mistral`. Создан для удобства взаимодействия с моделью в рамках приложения. Есть функция `message`, есть инициализатор экземпляра класса. Пример использования:

```python
from app.mistral_ai_initializer import ModifiedMistral, mistral_ai_initializer

instance1 = ModifiedMistral(api_key="api_key")
instance2 = mistral_ai_initializer()  # Автоматически получает API ключ из .env

print(instance1.message(messages=[{"role": "user", "content": "Привет!"}]))
print(instance2.message(messages=[{"role": "user", "content": "Привет!"}]))

> Привет! Как я могу помочь?
> Привет! Как я могу помочь?
```

## ModifiedOpenai

Дочерний класс `openai.OpenAI`. Создан для удобства взаимодействия с моделью в рамках приложения. Есть функция `message`, есть инициализатор экземпляра класса. Пример использования:

```python
from app.ai_initializer import ModifiedOpenai, get_ai_client

instance1 = ModifiedOpenai(
    api_key="api_key", base_url="https://api.mistral.ai/v1"
)  # MistralAI
instance2 = get_ai_client(
    use_local_models=False
)  # Автоматически получает API ключ из .env

print(
    instance1.message(
        messages=[{"role": "user", "content": "Привет!"}],
        model="mistral-small-latest",
    )
)
print(
    instance2.message(
        messages=[{"role": "user", "content": "Привет!"}],
        model="mistral-small-latest",
    )
)

> Привет! Как я могу помочь?
> Привет! Как я могу помочь?
```

## Google search

Функция для поиска ссылок с статьями по запросу. Пример использования:

```python
from app.google_custom_search import google_search

print(
    *[
        i["link"]
        for i in google_search(
            "Что такое LLM?",
            api_key="api-key",
            cse_id="cse_id",
            num_results=4,
        )
    ]
)
> https://habr.com/ru/articles/775870/ https://habr.com/ru/articles/775842/ https://habr.com/ru/articles/835342/ https://habr.com/ru/articles/768844/
```

Стоит учесть, что в GCS у меня стоит фильтр на домен `habr.com`
