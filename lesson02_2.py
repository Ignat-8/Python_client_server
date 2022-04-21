'''
Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах. 
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity), 
цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря 
в файл orders.json. 
При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
'''

import json


def write_order_to_json(item, quantity, price, buyer, date):
    # читаем ранее записанный словарь
    with open('orders.json', encoding='utf-8') as json_file:
        orders = json.load(json_file)
    
    # добавляем новую запись к уже существующим
    orders['orders'].append([item, quantity, price, buyer, date])

    # перезаписываем файл
    with open('orders.json', 'w', encoding='utf-8') as json_file:
        json.dump(orders, json_file, sort_keys=True, indent=4, ensure_ascii=False)
# ------------------------------------------------------------------


item = 'товар 2'
quantity = 1
price = 125
buyer = 'покупатель 1'
date = '20-04-2022'

write_order_to_json(item, quantity, price, buyer, date) 
