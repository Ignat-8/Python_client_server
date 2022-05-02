""" Программа сервера для получения приветствия от клиента и отправки ответа """
import sys
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import common.settings as cmnset
import common.utils as cmnutils


def process_client_message(message):
    if 'action' in message and message['action'] == 'presence' and 'time' in message \
        and 'user' in message and message['user']['account_name'] == 'Guest':
        return {'response': 200}
    return {
        'response': 400,
        'error': 'bad request'
    }


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            if listen_port < 1024 and listen_port > 65535:
                raise ValueError
        else:
            listen_port = cmnset.DEFAULT_PORT
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print('Номер порта должен быть в диапазоне от 1024 до 65535.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = int(sys.argv[sys.argv.index('-a') + 1])
        else:
            listen_address = ''
    except IndexError:
        print('После параметра -\'а\' необходимо указать адрес для прослушивания сервером.')
        sys.exit(1)
    

    # готовим сокет
    SERV_SOCK = socket(AF_INET, SOCK_STREAM)
    SERV_SOCK.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    SERV_SOCK.bind((listen_address, listen_port))
    SERV_SOCK.listen(cmnset.MAX_CONNECTIONS)

    while True:
        client, client_address = SERV_SOCK.accept()
        message_from_client = cmnutils.get_message(client)
        print(f"Сообщение от клиента '{client}': '{message_from_client}'")
        response = process_client_message(message_from_client)

        if response['response'] == 400:
            print("от пользователя получено не верное сообщение")

        try:
            cmnutils.send_message(client, response)
            client.close()
        except:
            print("Не удается отправить сообщение клиенту")
            client.close()
            sys.exit(1)


if __name__ == '__main__':
    main()
