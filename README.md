# Описание проекта:

Telegram-бот, который обращается к API сервиса Практикум.Домашка и узнаёт статус вашей домашней работы:
взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.

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
