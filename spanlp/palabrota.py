import os
import re
import random

words = None
_censor_chars = '@#$%!'
_default_country = "COL"
_censor_pool = []
_countries = ["COL", "VEN"]

_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_data(path):
    return os.path.join(_ROOT, 'dataset', path)


def load_words(country=None):
    global words
    word_list = []
    try:
        if not country:
            country = _countries
        if country:
            output_file = get_data("working_set.txt")
            with open(output_file, 'w') as outfile:
                for name in country:
                    filename = get_data(name + '.txt')
                    print(filename)
                    with open(filename) as infile:
                        outfile.write(infile.read().lower())
                    outfile.write("\n")

            filename = get_data(output_file)
            f = open(filename)
            word_list = f.readlines()
            word_list = [w.strip() for w in word_list if w]
    except Exception as e:
        print(e)
        word_list = []
    words = word_list


def get_words(country=None) -> list:
    load_words(country=country)
    return words


def get_censor_char():
    global _censor_pool
    if not _censor_pool:
        _censor_pool = list(_censor_chars)
    return _censor_pool.pop(random.randrange(len(_censor_pool)))


def censor(input_text, country=None):
    """ Returns the input string with profanity replaced with a random string
    of characters plucked from the censor_characters pool.
    """
    ret = input_text
    _words = get_words(country=country)
    for word in _words:
        curse_word = re.compile(re.escape(word), re.IGNORECASE)
        cen = "".join(get_censor_char() for i in list(word))
        ret = curse_word.sub(cen, ret)
    return ret


def contiene_palabrotas(texto=None, pais=None, incluir=None, exluir=None, censor_char=None) -> tuple:
    return 'menso' in texto, texto

