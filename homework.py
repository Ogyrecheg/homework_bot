import logging
import os
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

import exceptions

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

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
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}

    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        response_content = response.json()

        if response.status_code == HTTPStatus.OK:
            return response_content
        else:
            raise exceptions.InvalidHttpStatus('Ошибка ответа API')

    except requests.exceptions.RequestException:
        raise exceptions.RequestException('Что-то пошло не так!')


def check_response(response):
    """Проверяем ответ с API на типы данных питона."""
    if not isinstance(response, dict):
        raise TypeError('API вернул что-то не то ...')

    elif 'homeworks' not in response:
        raise ValueError('Не нашли данный ключ в словаре')

    elif not isinstance(response['homeworks'], list):
        raise TypeError('Неправильный тип данных домашки')

    else:
        return response['homeworks']


def parse_status(homework):
    """Парсим ответ АПИшки."""
    if 'homework_name' not in homework:
        raise KeyError('Ключа "homework_name" нет в словаре "homework"')

    homework_name = homework['homework_name']
    homework_status = homework['status']

    if homework_status not in HOMEWORK_VERDICTS:
        raise KeyError('Нет ')

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
        if value is None:
            return False

    return True


def main():
    """Основная логика работы бота."""
    if check_tokens():
        bot = telegram.Bot(token=TELEGRAM_TOKEN)
        current_timestamp = int(time.time())
        last_message = ''

        while True:
            try:
                response = get_api_answer(current_timestamp)
                homeworks = check_response(response)
                message = parse_status(homeworks[0])
                if message != last_message:
                    send_message(bot, message)
                    current_timestamp = ...
                    time.sleep(RETRY_PERIOD)

            except Exception as error:
                message = f'Сбой в работе программы: {error}'
                bot.send_message(TELEGRAM_CHAT_ID, message)
                time.sleep(RETRY_PERIOD)
    else:
        logging.critical('Отсутствии обязательных переменных окружения')


if __name__ == '__main__':
    main()
