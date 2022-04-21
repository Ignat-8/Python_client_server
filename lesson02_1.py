'''
Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных 
из файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. 
Для этого:
1. Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие 
и считывание данных. В этой функции из считанных данных необходимо с помощью регулярных выражений 
извлечь значения параметров «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». 
Значения каждого параметра поместить в соответствующий список. Должно получиться четыре списка — 
например, os_prod_list, os_name_list, os_code_list, os_type_list. В этой же функции создать главный 
список для хранения данных отчета — например, main_data — и поместить в него названия столбцов отчета 
в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы». Значения для этих 
столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);

2. Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать 
получение данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий 
CSV-файл;

3. Проверить работу программы через вызов функции write_to_csv().
'''

import csv
import re
from chardet import detect


# ----------------------------------------------------------------------------
def get_data(file_list, os_list):
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы'],]

    for i, file_el in enumerate(file_list):
        i += 1  # т.к. нулевая строка в массиве main_data занята заголовком
        main_data_add =['', '', '', '']  # заполняем пустыми значениями, т.к. кол-во столбцов известно

        # определение кодировки файла
        with open(file_el, 'rb') as file :
            CONTENT = file.read()
            ENCODING = detect(CONTENT)['encoding']
        print(ENCODING)

        with open(file_el, encoding=ENCODING) as csv_file:
            CONTENT = csv.reader(csv_file)
            for row in CONTENT:
                for key in os_list:
                    match = re.search(os_list[key]['pattern'], str(row[0]))
                    if match:
                        os_list[key]['os_list'].append(match[3])
                        j = main_data[0].index(key)
                        main_data_add[j] = match[3]
                        # print(file_el, ',', match[1], ',', match[3])

        main_data.append(main_data_add)
        os_prod_list = os_list['Изготовитель системы']['os_list']
        os_name_list = os_list['Название ОС']['os_list']
        os_code_list = os_list['Код продукта']['os_list']
        os_type_list = os_list['Тип системы']['os_list']

    return main_data, os_prod_list, os_name_list, os_code_list, os_type_list
# ----------------------------------------------------------------------------


def write_to_csv(file_list, os_list):
    main_data, os_prod_list, os_name_list, os_code_list, os_type_list = get_data(file_list, os_list)

    with open('main_data.csv', 'w', encoding='utf-8', newline='') as csv_file:
        F_WRITER = csv.writer(csv_file, quoting=csv.QUOTE_NONNUMERIC, delimiter=";")
        F_WRITER.writerows(main_data)
    
    return main_data, os_prod_list, os_name_list, os_code_list, os_type_list
# ----------------------------------------------------------------------------


file_1 = 'info_1.txt'
file_2 = 'info_2.txt'
file_3 = 'info_3.txt'

file_list = [file_1, file_2, file_3]

os_list = {
    'Изготовитель системы': {
        'pattern': r'(Изготовитель системы:)( +)(.+)',
        'os_list': [],  # os_prod_list
        },  
    'Название ОС': {
        'pattern': r'(Название ОС:)( +)(.+)',
        'os_list': [],  # os_name_list
        },  
    'Код продукта': {
        'pattern': r'(Код продукта:)( +)(.+)',
        'os_list': [],  # os_code_list
    },
    'Тип системы': {
        'pattern': r'(Тип системы:)( +)(.+)',
        'os_list': [],  # os_type_list
    },
    }

main_data, os_prod_list, os_name_list, os_code_list, os_type_list = write_to_csv(file_list, os_list)
# print()
# print(main_data)
# print()
# print(os_prod_list)
# print()
# print(os_name_list)
# print()
# print(os_code_list)
# print()
# print(os_type_list)
# print()