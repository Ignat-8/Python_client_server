""" Программа сервера для получения приветствия от клиента и отправки ответа """
import sys
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import logging
import logs.conf_server_log
import common.settings as cmnset
import common.utils as cmnutils
from common.decors import log


# Инициализация серверного логера
SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message):
    SERVER_LOGGER.info(f'проверка сообщения от клента')
    if 'action' in message and message['action'] == 'presence' and 'time' in message \
        and 'user' in message and message['user']['account_name'] == 'Guest':
        SERVER_LOGGER.debug(f'сообщение от клента правильное')
        return {'response': 200}

    SERVER_LOGGER.error(f'сообщение от клента не правильное')
    return {
        'response': 400,
        'error': 'bad request'
    }


def main():
    SERVER_LOGGER.info(f'Определяем параметры сервера')

    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            if listen_port < 1024 and listen_port > 65535:
                raise ValueError
        else:
            SERVER_LOGGER.debug('Используется порт по умолчанию %d', cmnset.DEFAULT_PORT)
            listen_port = cmnset.DEFAULT_PORT
    except IndexError:
        SERVER_LOGGER.error(f'После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.error(f'Номер порта за пределами диапазона 1024-65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = int(sys.argv[sys.argv.index('-a') + 1])
        else:
            SERVER_LOGGER.info(f'Используется адрес по умолчанию')
            listen_address = ''
    except IndexError:
        SERVER_LOGGER.error('После параметра -\'а\' необходимо указать адрес для прослушивания сервером.')
        sys.exit(1)
    

    # готовим сокет
    SERVER_LOGGER.info(f'Готовим сокет')
    SERV_SOCK = socket(AF_INET, SOCK_STREAM)
    SERV_SOCK.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    SERV_SOCK.bind((listen_address, listen_port))
    SERV_SOCK.listen(cmnset.MAX_CONNECTIONS)

    while True:
        client, client_address = SERV_SOCK.accept()
        message_from_client = cmnutils.get_message(client)
        SERVER_LOGGER.debug("Получено сообщение от клиента %s: %s", client, message_from_client)
        response = process_client_message(message_from_client)

        try:
            cmnutils.send_message(client, response)
            client.close()
            SERVER_LOGGER.debug("Сообщение отправлено клиенту")
        except:
            SERVER_LOGGER.error("Не удается отправить сообщение клиенту")
            client.close()
            sys.exit(1)


if __name__ == '__main__':
    main()
