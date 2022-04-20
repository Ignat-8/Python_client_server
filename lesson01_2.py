'''
Каждое из слов «class», «function», «method» записать в байтовом типе. 
Сделать это необходимо в автоматическом, а не ручном режиме, с помощью добавления литеры b к текстовому значению, 
(т.е. ни в коем случае не используя методы encode, decode или функцию bytes) и определить тип, 
содержимое и длину соответствующих переменных.
'''


def get_type_element(el):
    return ('содержимое =', el, ', тип =', type(el), ', длина =', len(el))


word_1 = 'class'
word_2 = 'function'
word_3 = 'method'

list_words = [word_1, word_2, word_3]

for el in list_words:
    el = eval(f"b'{el}'")
    print(get_type_element(el))
