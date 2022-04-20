'''
Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле 
YAML-формата. Для этого:
1. Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, 
второму — целое число, третьему — вложенный словарь, где значение каждого ключа — это целое число с 
юникод-символом, отсутствующим в кодировке ASCII (например, €);

2. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить 
стилизацию файла с помощью параметра default_flow_style, а также установить возможность работы с 
юникодом: allow_unicode = True;

3. Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
'''

import yaml


main_data = {
    'list': ('list1', 'list2'),
    'id': 7,
    'dict': {
        'key1':128, 
        'key2':129,
        },
}

# записываем данные в файл
with open('file.yaml', 'w', encoding='utf-8') as yaml_file:
    yaml.dump(main_data, yaml_file, 
            default_flow_style=True, 
            allow_unicode=True, 
            sort_keys=False)

# считываем данные из файла
with open('file.yaml', encoding='utf-8') as yaml_file:
    F_CONTENT = yaml.load(yaml_file, Loader=yaml.FullLoader)
    print(F_CONTENT)

# сравниваем данные
print(main_data == F_CONTENT)  # True
