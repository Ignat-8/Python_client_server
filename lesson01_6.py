'''
Создать текстовый файл test_file.txt, заполнить его тремя строками: 
«сетевое программирование», «сокет», «декоратор». 
Далее забыть о том, что мы сами только что создали этот файл и исходить из того, 
что перед нами файл в неизвестной кодировке. Задача: открыть этот файл БЕЗ ОШИБОК 
вне зависимости от того, в какой кодировке он был создан.
'''

from chardet import detect


str_1 = 'сетевое программирование'
str_2 = 'сокет'
str_3 = 'декоратор'

str_list = [str_1, str_2, str_3]

# записываем файл с кодировкой по умолчанию
with open('test_file.txt', 'w') as file:
    for el in str_list:
        file.write(el + '\n')

# узнаем кодировку файла
with open('test_file.txt', 'rb') as file:
    CONTENT = file.read()
    ENCODING = detect(CONTENT)['encoding']
    print('\nкодировка файла по умолчанию:', ENCODING, '\n')

print('открытие файла в кодировке по умолчанию:\n')
with open('test_file.txt', 'r', encoding=ENCODING, errors="replace") as file:
    for el in file:
        print(el.strip())
