'''
Создать текстовый файл test_file.txt, заполнить его тремя строками: 
«сетевое программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
'''

import locale


str_1 = 'сетевое программирование'
str_2 = 'сокет'
str_3 = 'декоратор'

str_list = [str_1, str_2, str_3]

with open('test_file.txt', 'w') as f:
    for el in str_list:
        f.write(el + '\n')

# # определение кодировки системы по умолчанию

default_encoding = locale.getpreferredencoding()
print(default_encoding)

with open('test_file.txt', 'r', encoding='utf-8') as f:
    for el in f:
        print(el)
