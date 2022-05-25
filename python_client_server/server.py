""" Программа сервера для получения приветствия от клиента и отправки ответа """
import sys
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select
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
    all_clients = []
    with socket(AF_INET, SOCK_STREAM) as SERV_SOCK:

        SERV_SOCK.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        SERV_SOCK.bind((listen_address, listen_port))
        SERV_SOCK.listen(cmnset.MAX_CONNECTIONS)
        SERV_SOCK.settimeout(1)

        while True:
            try:
                client, client_address = SERV_SOCK.accept()
            except OSError as err:
                pass
            else:
                print(f"Получен запрос на соединение от {str(client_address)}")
                all_clients.append(client)
            finally:
                wait = 0
                clients_read = []
                clients_write = []
                try:
                    clients_read, clients_write, errors = select(all_clients, all_clients, [], wait)
                    print("clients_read:\n", clients_read)
                    print("clients_write:\n", clients_write)
                except Exception as e:
                    print(e)

                for client_read in clients_read:
                    message_from_client = cmnutils.get_message(client_read)
                    SERVER_LOGGER.debug("Получено сообщение от клиента %s: %s", client_read, message_from_client)
                    print(f"Получено сообщение от клиента:\n", client, message_from_client)
                    response = process_client_message(message_from_client)
                    # добавляем эхо ответ в сообщение клиенту
                    response['message'] = message_from_client['message'].upper()

                    for client_write in clients_write:
                        try:
                            cmnutils.send_message(client_write, response)
                            # client_write.close()
                            SERVER_LOGGER.debug("Сообщение отправлено клиенту %s", client_write)
                        except:
                            SERVER_LOGGER.error("Не удается отправить сообщение клиенту %s", client_write)
                            client_write.close()
                            all_clients.remove(client_write)
                            


if __name__ == '__main__':
    main()
