'''
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
строкового представления в байтовое и выполнить обратное преобразование 
(используя методы encode и decode).
'''

word_1 = 'разработка'
word_2 = 'администрирование'
word_3 = 'protocol'
word_4 = 'standard'

list_words = [word_1, word_2, word_3, word_4]

for el in list_words:
    el_utf = el.encode("utf-8")
    print(f'"{el}" to bytes = {el_utf}')
    print(f'"{el}" to string = "{el_utf.decode("utf-8")}"')
    print('-' * 80)
