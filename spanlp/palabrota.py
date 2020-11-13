"""
Estrategias para encontrar, limpiar y censurar groserias, vulgaridades y obscenidades en textos en Español.
====================================
Este modulo/clase implementa las siguientes funciones:
    - censor
    - constains_palabrota
    - algoritmos matematicos de distancia y similitud entre palabras
"""

# Author: Jhon Freddy Puentes <jhonf.puentesn@konradlorenz.edu.co>

import os
import re
import random

_ROOT = os.path.abspath(os.path.dirname(__file__))


class Palabrota():
    # TODO documentar
    _words = None
    _censor_chars = '@#$%!'
    _censor_pool = []
    _countries = ["COL", "VEN"]
    _exclude = []
    _include = []
    _distance_metric = None

    def __init__(self, censor_char=None, countries=None, exclude=None, include=None, distance_metric=None) -> None:
        super().__init__()
        if censor_char:
            self._censor_chars = censor_char
        if countries:
            self._countries = countries
        if exclude:
            self._exclude = exclude
        if include:
            self._include = include
        if distance_metric:
            self._distance_metric = distance_metric

    def __str__(self) -> str:
        return """\
                Censor Chars: {}
                Countries: {}""".format(self._censor_chars, self._countries)

    @staticmethod
    def __get_data(path):
        return os.path.join(_ROOT, 'dataset', path)

    def set_censor_characters(self, new_censor_chars) -> None:
        # TODO documentar
        global _censor_chars
        if len(new_censor_chars) == 0:
            new_censor_chars = " "
        self._censor_chars = new_censor_chars

    def __load_words(self, country=None) -> None:
        # TODO documentar
        # TODO mejorar forma de almacenar los datos con que se trabajara. Pasarlo a memoria.
        global _words
        word_list = []
        try:
            if not country:
                country = self._countries
            if country:
                output_file = self.__get_data("working_set.txt")
                with open(output_file, 'w') as outfile:
                    for name in country:
                        filename = self.__get_data(name + '.txt')
                        with open(filename) as infile:
                            outfile.write(infile.read().lower())
                        outfile.write("\n")

                filename = self.__get_data(output_file)
                f = open(filename)
                word_list = f.readlines()
                word_list = [w.strip() for w in word_list if w]
        except Exception as e:
            print(e)
            word_list = []
        # TODO validar/usar exclude, include
        _words = word_list

    def __get_words(self, country=None) -> list:
        self.__load_words(country=country)
        return _words

    def __get_censor_char(self) -> list:
        if not self._censor_pool:
            self._censor_pool = list(self._censor_chars)
        return self._censor_pool.pop(random.randrange(len(self._censor_pool)))

    def censor(self, input_text, country=None) -> str:
        # TODO documentar
        # TODO validar/usar exclude, include
        ret = input_text
        words = self.__get_words(country=country)
        for word in words:
            curse_word = re.compile(re.escape(word), re.IGNORECASE)
            cen = "".join(self.__get_censor_char() for i in list(word))
            ret = curse_word.sub(cen, ret)
        return ret

    def contains_palabrota(self, text) -> bool:
        # TODO documentar
        # TODO validar/usar exclude, include
        return text != self.censor(text)

    # Metricas de distancias:
    # Ver: https://www.kdnuggets.com/2019/01/comparison-text-distance-metrics.html
    def levenshtein(self):
        # TODO documentar
        # TODO convertir en un modulo aparte.
        pass
