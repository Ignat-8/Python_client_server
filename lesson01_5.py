'''
Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из
байтовового в строковый тип на кириллице.
'''

import platform
import subprocess


urls = ['yandex.ru', 'youtube.com']
code = '-n' if platform.system().lower() == 'windows' else '-c'

for url in urls:
    args = ['ping', code, '4', url]
    ping_results = subprocess.Popen(args, stdout=subprocess.PIPE)
    for line in ping_results.stdout:
        line = line.decode('cp866') if code == '-n' else line.decode('utf-8')
        print(line)
