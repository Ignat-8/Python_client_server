'''
Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в
последовательность кодов (не используя методы encode и decode) и определить тип,
содержимое и длину соответствующих переменных.
'''


def get_type_element(el):
    return ('содержимое =', el, ', тип =', type(el), ', длина =', len(el))


word_1 = b'class'
word_2 = b'function'
word_3 = b'method'

list_words = [word_1, word_2, word_3]

for el in list_words:
    print(get_type_element(el))
