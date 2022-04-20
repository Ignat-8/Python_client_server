'''
Создать текстовый файл test_file.txt, заполнить его тремя строками: 
«сетевое программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию.
Принудительно открыть файл в формате Unicode и вывести его содержимое.
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

print('открытие файла в кодировке utf-8:\n')
with open('test_file.txt', 'r', encoding='utf-8', errors="replace") as file:
    for el in file:
        print(el)
