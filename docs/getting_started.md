# :memo: Начало

Подготовка к запуску: получение обязательных данных, создание папок, создание файлов и установка зависимостей.

## Обязательные учетные данные

### 1. Google Custom Search Credentials (optional)

Интеграция в проект в планах, но функционал уже реализован. Для работы поиска нам понадобится `CSE id` и `Google Search API Key`. [Инструкция](https://developers.google.com/custom-search/v1/overview?hl=ru) по получению. При создании API ключа стоит учитывать, что вы можете указать домены, по которым будет происходить поиск. Создать поисковый сервис в Google [тут](https://programmablesearchengine.google.com/controlpanel/all).

### 2. MistralAI API key

Теперь, главная составляющая проекта - ИИ. Получить API ключ можно на официальном [сайте Mistral](https://console.mistral.ai/api-keys/).

### 3. Secret key

`SECRET_KEY` - переменная для корректной работы `wtforms`. Лучше всего для ключа подойдет `uuid4`. Сгенерировать можно или через python библиотеку `uuid`, или на [сайте](https://www.uuidgenerator.net/version4).

P.S. В документации Flask [рекомендуется](https://flask.palletsprojects.com/en/stable/config/#SECRET_KEY) использовать рандомный набор байтов. Ниже **пример**:

```bash
python -c 'import secrets; print(secrets.token_hex())'

> 192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf
```

## Обязательные действия в проекте

### Создаем директорию `database` в корне

Для корректной работы создаем в корне проекта директорию `database` любым удобным Вам способом. Вот пример через командную строку:

```bash
mkdir database
```

### Создаем файл `.env`

Создаем файл `.env` со следующим содержанием:

```bash
MISTRAL_AI_API_KEY=mistral-ai-api-key
GOOGLE_API_KEY=google-api-key
CSE_ID=cse-id
SECRET_KEY=secret-key
DEBUG=True # к примеру
DATABASE_PATH=./database/kairos.db
```

Данные заменяем на свои. Подробное описание содержания файла находиться в блоке ["Переменные .env"](./dotenv_variables.md)

## Установка зависимостей

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

### С помощью uv

#### Подтягиваем зависимости

```bash
uv sync # .venv создается автоматически
```

uv под капотом создал виртуальное окружение и установил все зависимости.
