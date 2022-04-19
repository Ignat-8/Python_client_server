'''
Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
проверить тип и содержание соответствующих переменных. Затем с помощью
онлайн-конвертера преобразовать строковые представление в формат Unicode и также
проверить тип и содержимое переменных.
'''


def print_func(list_words):
    for el in list_words:
        print(el, ', type =', type(el))
    print('-'*50)

word_1 = "разработка"
word_2 = "сокет"
word_3 = "декоратор"

list_words = [word_1, word_2, word_3]
print_func(list_words)

word_1_u = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
word_2_u = '\u0441\u043e\u043a\u0435\u0442'
word_3_u = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

list_words_u = [word_1_u, word_2_u, word_3_u]
print_func(list_words_u)
