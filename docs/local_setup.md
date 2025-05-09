# :rocket: Локальный запуск

Инструкция по локальному запуску проекта.

## Если зависимости были установлены через pip

```bash
# Windows
python run.py
# Linux/MacOS
python3 run.py
```

## Если зависимости были установлены через uv

```bash
uv run run.py
```

## После запуска

В командной строке должен появиться следующий вывод:

```bash
 * Подключение к базе данных по адресу sqlite:///./database/kairos.db?check_same_thread=False
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Подключение к базе данных по адресу sqlite:///./database/kairos.db?check_same_thread=False
 * Debugger is active!
```

Это значит, что сервер Flask запущен успешно и все работает.

## Переходим на [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
