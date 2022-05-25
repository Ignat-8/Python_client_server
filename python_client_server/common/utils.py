import json
from  common.settings import MAX_PACKAGE_LENGTH, ENCODING
from common.decors import log


@log
def get_message(client):
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    # print(f'получено сообщение encoded_response = {encoded_response}')
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        if isinstance(json_response, str):
            response = json.loads(json_response)
            if isinstance(response, dict):
                return response
            raise ValueError
        raise ValueError
    raise ValueError


@log
def send_message(sock, message):
    if isinstance(message, dict):
        js_message = json.dumps(message)
        encoded_message = js_message.encode(ENCODING)
        sock.send(encoded_message)
        return True
    raise TypeError
