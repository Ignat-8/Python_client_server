"""
Служебный скрипт запуска/останова нескольких клиентских приложений
"""

from subprocess import Popen, CREATE_NEW_CONSOLE


PROCESS_LIST = []

while True:
    ACTION = input("Запустить клиентов (s) / Закрыть клиентов (x) / Выйти (q) ")

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS_LIST.append(Popen('python server.py', creationflags=CREATE_NEW_CONSOLE))

        for _ in range(2):
            PROCESS_LIST.append(Popen('python client.py -m send', creationflags=CREATE_NEW_CONSOLE))
        
        for _ in range(5):
            PROCESS_LIST.append(Popen('python client.py -m listen', creationflags=CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        for p in PROCESS_LIST:
            p.kill()
        PROCESS_LIST.clear()