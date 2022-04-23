""" Программа сервера для отправки приветствия сервера и получения ответа """

import sys
import json
import time
from socket import socket, AF_INET, SOCK_STREAM
import common.settings as cmnset
import common.utils as cmnutils


def create_presence(user_name='Guest'):
    out = {
        "action": "presence",
        "time": time.time(),
        "user": {
            "account_name": user_name,
            },
    }
    return out


def process_ans(message):
    if 'response' in message:
        if message['response'] == 200:
            return {'200': 'ok'}
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
        server_port = cmnset.DEFAUL_PORT
    except ValueError:
        print('Номер порта должен быть в диапазоне от 1024 до 65535')
        sys.exit(1)

    CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
    CLIENT_SOCK.connect((server_address, server_port))
    message_to_server = create_presence()
    cmnutils.send_message(CLIENT_SOCK, message_to_server)
    
    try:
        answer = process_ans(cmnutils.get_message(CLIENT_SOCK))
        print(f"Сообщение от сервера: '{answer}'")
        CLIENT_SOCK.close()
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')
        

if __name__ == '__main__':
    main()
