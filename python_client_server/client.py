""" Программа сервера для отправки приветствия сервера и получения ответа """
# from http.client import EXPECTATION_FAILED
import sys
import json
import time
from socket import socket, AF_INET, SOCK_STREAM
import logging
from threading import Thread
from unittest import expectedFailure
import logs.conf_client_log
import common.settings as cmnset
import common.utils as cmnutils
from common.decors import log
import common.errors as my_err

# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')


@log
def create_message(user_name='Guest', action='presence', text='', destination=''):
    """Функция создаёт словарь с сообщением.
    По умолчанию это регистрационное сообщение presence"""
    
    message = {
        'action': action,
        'time': time.time(),
        'user': {
            'account_name': user_name,
            },
    }

    if text and destination:
        message['text'] = text
        message['destination'] = destination

    CLIENT_LOGGER.debug('Сформировано сообщение %s', message)
    return message


@log
def process_ans(message):
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if 'response' in message:
        if message['response'] == 200:
            CLIENT_LOGGER.debug(f"'200': 'ok'")
            if 'text' in message and message['text']:
                return {'200': 'ok', 'message': message['text']}
            else:
                return {'200': 'ok'}

        CLIENT_LOGGER.debug(f"400: {message['error']}")
        raise my_err.ServerError(f"400: {message['error']}")
    raise my_err.ReqFieldMissingError('response')


def main():
    try:
        key_names = ('-m', '--mode', '-n', '--name')
        # print('sys.argv =', sys.argv)
        server_address = sys.argv[1]
        if server_address in key_names:
            raise IndexError

        server_port = int(sys.argv[2])
        if server_port in key_names:
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
        user_name = ''
        if '-n' in sys.argv:
            user_name = sys.argv[sys.argv.index('-n') + 1]
        
        if '--name' in sys.argv:
            user_name = sys.argv[sys.argv.index('--name') + 1]

    except ValueError:
        CLIENT_LOGGER.error('Указано не верное значение аргумента')
        print("Указано не верное значение аргумента")
        sys.exit(1)
    
    """Сообщаем о запуске"""
    print(f'Консольный месседжер. Клиентский модуль. Имя пользователя: {user_name}')

    # Если имя пользователя не было задано, необходимо запросить пользователя.
    if not user_name:
        user_name = input('Введите имя пользователя: ')

    CLIENT_LOGGER.info(
        f'Запущен клиент с параметрами: адрес сервера: {server_address}, '
        f'порт: {server_port}, имя пользователя: {user_name}')

    with socket(AF_INET, SOCK_STREAM) as CLIENT_SOCK:
        CLIENT_SOCK.connect((server_address, server_port))
        
        try:  # регистрируемся на сервере
            message_to_server = create_message(user_name=user_name, action='presence', text='', destination='')
            cmnutils.send_message(CLIENT_SOCK, message_to_server)
            server_answer = process_ans(cmnutils.get_message(CLIENT_SOCK))
            
            CLIENT_LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {server_answer}')
            print(f'Установлено соединение с сервером. Ответ сервера:\n{server_answer}')
        except json.JSONDecodeError:
            CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
            print('Не удалось декодировать полученную Json строку.')
            sys.exit(1)
        except my_err.ServerError as error:
            CLIENT_LOGGER.error(f'При установки соединения сервер вернул ошибку: {error.text}')
            print(f'При установки соединения сервер вернул ошибку: {error.text}')
            sys.exit(1)
        except my_err.ReqFieldMissingError as missing_error:
            CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
            print(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
            sys.exit(1)
        except (ConnectionRefusedError, ConnectionError):
            CLIENT_LOGGER.critical(
                f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                f'конечный компьютер отверг запрос на подключение.')
            print(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                    f'конечный компьютер отверг запрос на подключение.')
            sys.exit(1)



        while True:
            pass

        #     message_to_server = create_presence()
        #     message_to_server['text'] = msg
        #     try:
        #         cmnutils.send_message(CLIENT_SOCK, message_to_server)
        #     except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
        #         CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
        #         sys.exit(1)
            
        #     # Режим работы приём:
            
        #     try:
        #         answer = process_ans(cmnutils.get_message(CLIENT_SOCK))
        #         CLIENT_LOGGER.debug(f"Сообщение от сервера: '{answer}'")
        #         print(f"Сообщение от сервера: '{answer}'")
        #     except (ValueError, json.JSONDecodeError):
        #         CLIENT_LOGGER.error('Не удалось декодировать сообщение сервера.')
        #         print('Не удалось декодировать сообщение сервера.')
        #         CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
        #         print(f'Соединение с сервером {server_address} было потеряно.')
        #         sys.exit(1)


if __name__ == '__main__':
    main()
