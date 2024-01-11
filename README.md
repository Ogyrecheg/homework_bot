# Описание проекта:

Реализован REST API CRUD для основных моделей проекта, для аутентификации примненяются JWT-токены.
В проекте реализованы пермишены, фильтрации, сортировки и поиск по запросам клиентов,
реализована пагинация ответов от API, установлено ограничение количества запросов к API.

## Запуск проекта:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Ogyrecheg/homework_bot.git
```

```
cd homework_bot
```

Cоздать и активировать виртуальное окружение:

```
py -3.7 -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить проект:

```
python3 homework.py
```

**Технологии:**
- Python
- python-telegram-bot
- python-dotenv

### Автор проекта:
студент когорты №17 [Шевченко Александр](https://github.com/Ogyrecheg)
