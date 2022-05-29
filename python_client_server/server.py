""" Программа сервера для получения приветствия от клиента и отправки ответа """
import sys
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from select import select
import logging
from urllib import response
import logs.conf_server_log
import common.settings as cmnset
import common.utils as cmnutils
from common.decors import log


# Инициализация серверного логера
SERVER_LOGGER = logging.getLogger('server')


@log
def process_client_message(message, messages, client, clients):
    SERVER_LOGGER.info(f'проверка сообщения от клента')
    if 'action' in message \
            and 'time' in message \
            and 'user' in message:

        if message['action'] == 'presence':
            # регистрация пользователя
            if message['user']['account_name'] not in messages.keys():
                messages[message['user']['account_name']] = {'socket': client}
                response = {'response': 200}
                cmnutils.send_message(client, response)
            else:
                clients.remove(client)
                SERVER_LOGGER.error('Имя пользователя %s уже занято', message['user']['account_name'])
                response = {'response': 300,
                            'error': 'Имя пользователя уже занято'}
                cmnutils.send_message(client, response)
                # client.close()
                return response

        if message['action'] == 'message' \
                and 'destination' in message \
                and 'text' in message:

            if client == messages[message['user']['account_name']]['socket']:
                messages[message['user']['account_name']]['message'] = message
                # {account_name:{'socket': client, 
                #               'message': message}}
            else:
                SERVER_LOGGER.error('Пользователь %s с сокетом %s не зарегистрирован', message['user']['account_name'], client)
                response = {'response': 400,
                        'error': 'Пользователь не зарегистрирован'}
                return response

        if message['action'] == 'exit':
            clients.remove(client)
            client.close()
            del messages[message['user']['account_name']]

        SERVER_LOGGER.debug('сообщение от клента правильное')
        return {'response': 200}
    else:
        SERVER_LOGGER.error('сообщение от клента не правильное')
        return {'response': 400,
                'error': 'bad request'}
#---------------------------------------------------------------------------------

    
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
    with socket(AF_INET, SOCK_STREAM) as SERV_SOCK:
        clients = []
        messages = dict()
        # {account_name:{'socket': client, 
        #               'message': message}}

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
                clients.append(client)
            finally:
                wait = 0
                clients_read = []
                clients_write = []
                try:
                    clients_read, clients_write, errors = select(clients, clients, [], wait)
                    # print("clients_read:\n", clients_read)
                    # print("clients_write:\n", clients_write)
                except Exception as e:
                    print(e)

                for client_read in clients_read:
                    try:
                        message_from_client = cmnutils.get_message(client_read)
                        SERVER_LOGGER.debug("Получено сообщение от клиента %s: %s", client_read, message_from_client)
                        print(f"Получено сообщение от клиента:\n", client, message_from_client)
                    except Exception:
                        SERVER_LOGGER.info(f'Клиент {client_read} отключился от сервера.')
                        print(f'Клиент {client_read} отключился от сервера.')
                        clients.remove(client_read)
                    else:
                        print('Параметры функции process_client_message:')
                        print('message_from_client:', message_from_client)
                        print('messages:', messages)
                        print('client_read:', client_read)
                        print('clients:', clients)
                        response = process_client_message(message_from_client, messages, client_read, clients)
                        print(f'Ответ клиенту {client_read}:\n{response}')

                    # for client_write in clients_write:
                    #     try:
                    #         cmnutils.send_message(client_write, response)
                    #         # client_write.close()
                    #         SERVER_LOGGER.debug("Сообщение отправлено клиенту %s", client_write)
                    #     except:
                    #         SERVER_LOGGER.error("Не удается отправить сообщение клиенту %s", client_write)
                    #         client_write.close()
                    #         clients.remove(client_write)
                            


if __name__ == '__main__':
    main()
