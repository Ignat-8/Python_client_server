""" Программа сервера для отправки приветствия сервера и получения ответа """
import sys
import json
import time
from socket import socket, AF_INET, SOCK_STREAM
import logging
import logs.conf_client_log
import common.settings as cmnset
import common.utils as cmnutils
from common.decors import log


# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')

@log
def create_presence(user_name='Guest'):
    out = {
        "action": "presence",
        "time": time.time(),
        "user": {
            "account_name": user_name,
            },
    }
    CLIENT_LOGGER.debug(f'Сформировано сообщение {out} для пользователя {user_name}')
    return out


@log
def process_ans(message):
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if 'response' in message:
        if message['response'] == 200:
            CLIENT_LOGGER.debug(f"'200': 'ok'")
            return {'200': 'ok'}
        CLIENT_LOGGER.debug(f"400: {message['error']}")
        return f"400: {message['error']}"
    raise ValueError


def main():
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = cmnset.DEFAULT_ADDRESS
        server_port = cmnset.DEFAULT_PORT
        CLIENT_LOGGER.info('Использование параметров по умолчанию - DEFAULT_ADDRESS и DEFAULT_PORT')
    except ValueError:
        CLIENT_LOGGER.error('Номер порта должен быть в диапазоне от 1024 до 65535')
        sys.exit(1)

    CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
    CLIENT_SOCK.connect((server_address, server_port))
    message_to_server = create_presence()
    cmnutils.send_message(CLIENT_SOCK, message_to_server)
    
    try:
        answer = process_ans(cmnutils.get_message(CLIENT_SOCK))
        CLIENT_LOGGER.debug(f"Сообщение от сервера: '{answer}'")
        CLIENT_SOCK.close()
    except (ValueError, json.JSONDecodeError):
        CLIENT_LOGGER.error('Не удалось декодировать сообщение сервера.')
        

if __name__ == '__main__':
    main()
