""" Программа сервера для отправки приветствия сервера и получения ответа """
from http.client import EXPECTATION_FAILED
import sys
import json
import time
from socket import socket, AF_INET, SOCK_STREAM
import logging
from unittest import expectedFailure
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
            return {'200': 'ok', 'message': message['message']}
        CLIENT_LOGGER.debug(f"400: {message['error']}")
        return f"400: {message['error']}"
    raise ValueError


def main():
    try:
        print('sys.argv =', sys.argv)
        server_address = sys.argv[1]
        if server_address in ('-m', '--mode'):
            raise IndexError

        server_port = int(sys.argv[2])
        if server_port in ('-m', '--mode'):
            raise IndexError
        if server_port < 1024 or server_port > 65535:
            raise ValueError
        

    except IndexError:
        server_address = cmnset.DEFAULT_ADDRESS
        server_port = cmnset.DEFAULT_PORT
        CLIENT_LOGGER.info('Использование параметров по умолчанию - DEFAULT_ADDRESS и DEFAULT_PORT')
    except ValueError:
        CLIENT_LOGGER.error('Номер порта должен быть в диапазоне от 1024 до 65535')
        sys.exit(1)

    try:
        client_mode = 'listen'
        if '-m' in sys.argv:
            client_mode = sys.argv[sys.argv.index('-m') + 1]
        
        if '--mode' in sys.argv:
            client_mode = sys.argv[sys.argv.index('--mode') + 1]

        if client_mode not in ('send', 'listen'):
            raise ValueError
    except ValueError:
        CLIENT_LOGGER.error(f'Указано не верное значение аргумента mode')
        print("Допустимое значение аргумента mode = ('send', 'listen')")
        sys.exit(1)

    with socket(AF_INET, SOCK_STREAM) as CLIENT_SOCK:
        CLIENT_SOCK.connect((server_address, server_port))
        
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else:
            print('Режим работы - приём сообщений.')

        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                # Сообщение не должно состоять из пустой строки или пробелов
                msg = ''
                while msg.strip() == '':
                    msg = input('Ваше сообщение или exit для выхода: ')
                if msg == 'exit':
                    CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
                    break

                message_to_server = create_presence()
                message_to_server['message'] = msg
                try:
                    cmnutils.send_message(CLIENT_SOCK, message_to_server)
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)
            
            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    answer = process_ans(cmnutils.get_message(CLIENT_SOCK))
                    CLIENT_LOGGER.debug(f"Сообщение от сервера: '{answer}'")
                    print(f"Сообщение от сервера: '{answer}'")
                except (ValueError, json.JSONDecodeError):
                    CLIENT_LOGGER.error('Не удалось декодировать сообщение сервера.')
                    print('Не удалось декодировать сообщение сервера.')
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    print(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
