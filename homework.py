import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

import exceptions

load_dotenv()

PRACTICUM_TOKEN = os.getenv('TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGA_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def send_message(bot, message):
    """Бот отправляет сообщение об изменении статуса домашки."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)

    except Exception as error:
        logging.error(f'Ошибка при отправке сообщения: {error}')

    else:
        logging.debug('Сообщение отправлено!')


def get_api_answer(current_timestamp):
    """Делаем запрос к API практикума."""
    params = {'from_date': current_timestamp}

    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        response_content = response.json()

        if response.status_code != HTTPStatus.OK:
            raise exceptions.InvalidHttpStatus('Ошибка ответа API')

        return response_content

    except requests.exceptions.RequestException:
        raise exceptions.RequestException('Что-то пошло не так!')


def check_response(response):
    """Проверяем ответ с API на типы данных питона."""
    if not isinstance(response, dict):
        raise TypeError('API вернул что-то не то ...')

    if 'homeworks' not in response:
        raise ValueError('Не нашли данный ключ в словаре')

    if not isinstance(response['homeworks'], list):
        raise TypeError('Неправильный тип данных домашки')

    return response['homeworks']


def parse_status(homework):
    """Парсим ответ АПИшки."""
    if 'homework_name' not in homework:
        raise KeyError('Ключа "homework_name" нет в словаре "homework"')

    if 'status' not in homework:
        raise KeyError('Ключа "homework_status" нет в словаре "homework"')

    homework_name = homework['homework_name']
    homework_status = homework['status']

    if homework_status not in HOMEWORK_VERDICTS:
        raise KeyError('Homework_status отсутсвует в HOMEWORK_VERDICTS')

    verdict = HOMEWORK_VERDICTS[homework_status]

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяем доступность переменных окружения."""
    tokens = {
        'practicum_token': PRACTICUM_TOKEN,
        'telegram_token': TELEGRAM_TOKEN,
        'telegram_chat_id': TELEGRAM_CHAT_ID,
    }

    for key, value in tokens.items():
        if not value:
            logging.critical(f'Отсутсвует переменная окружения {key}')
            return False

    return True


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        sys.exit()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = 0
    last_message = ''

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            message = parse_status(homeworks[0])
            if message != last_message:
                send_message(bot, message)
                last_message = message
                current_timestamp = response.get('current_date')

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            bot.send_message(TELEGRAM_CHAT_ID, message)

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    main()
