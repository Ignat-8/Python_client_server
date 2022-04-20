'''
Определить, какие из слов «attribute», «класс», «функция», «type» 
невозможно записать в байтовом типе.
'''


def is_convert_to_bytes(el):
    try:
        el.encode('ascii')
        return 'possible'
    except UnicodeEncodeError:
        return 'not possible'


word_1 = 'attribute'
word_2 = 'класс'
word_3 = 'функция'
word_4 = 'type'

list_words = [word_1, word_2, word_3, word_4]

for el in list_words:
    print(el, '-', is_convert_to_bytes(el), ' convert to bytes')
