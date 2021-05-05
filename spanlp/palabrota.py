"""
Estrategias para encontrar, limpiar y censurar groserias, vulgaridades y obscenidades en textos en Español.
====================================
Este modulo/clase implementa las siguientes funciones:
    - censor
    - constains_palabrota
    - algoritmos matematicos de distancia y similitud entre palabras
"""


import os
import re
import random

from spanlp.domain.countries import Country
from spanlp.domain.strategies import TextDistanceStrategy, DistanceMetricStrategy

_ROOT = os.path.abspath(os.path.dirname(__file__))


class Palabrota(object):
    """
    It contains all functions for manipulate, calculate and censor words.
    ...
    Attributes
    ----------
    _dataset_extension : str
        It represents file extension of datasets.
    _words : str
        It saves words used for censor.
    _censor_chars : str
        Characters for censor in string.
    _censor_pool : list
        In memory object for replace characters in phrase or word.
    _countries : list
        countries used for censor. Depending on country, censor will get word of that country.
    _exclude : list
        words to ignore in censor of document or phrase.
    _include : list
        words to add to dataset in censor of document or phrase.
    _distance_metric : TextDistanceStrategy
        strategy used for calculate similarity or distance between words.
    ...
    Methods
    -------
    set_censor_characters(new_censor_chars="")
        set new and different characters used for censoring words.

    censor(input_text="", censor_char=None, countries=None, exclude=None, include=None,
    distance_metric: TextDistanceStrategy = None) -> str
        censor words in document or phrase according to parameters.

    contains_palabrota(self, text) -> bool
        returns if a document, phrase or word contains or not vulgarity or words included in parameter `include`

    supported_countries() -> list
        returns a list with names of supported countries in this library.
    """
    _dataset_extension = '.txt'
    _words = None
    _censor_chars = '@#$%!'
    _censor_pool = []
    _countries = [c for c in Country]
    _exclude = []
    _include = []
    _distance_metric = None

    def __init__(self, censor_char=None, countries=None, exclude=None, include=None,
                 distance_metric: TextDistanceStrategy = None) -> None:
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
                Countries: {}
                Exclude words: {}
                Include words: {}
                Distance metric: {}""".format(self._censor_chars, self._countries,
                                              self._exclude, self._include,
                                              self._distance_metric)

    @staticmethod
    def __get_data(path):
        return os.path.join(_ROOT, 'dataset', path)

    def set_censor_characters(self, new_censor_chars="") -> None:
        global _censor_chars
        if len(new_censor_chars) == 0:
            new_censor_chars = " "
        self._censor_chars = new_censor_chars

    def __load_words(self) -> None:
        global _words
        word_list = []
        try:
            if self._countries and len(self._countries) > 0:
                working_set = []
                for country in self._countries:
                    try:
                        filename = self.__get_data(country.value + self._dataset_extension)
                        with open(filename) as infile:
                            working_set += infile.readlines()
                    except Exception as e:
                        print(f"[WARNING]: {country.value} does not exists in dataset. Message: {e}")

                word_list = working_set
                word_list = [sub.replace('\n', '') for sub in word_list]
                word_list = [w.strip() for w in word_list if w and w not in self._exclude]
                if self._include and len(self._include) > 0:
                    word_list.extend(self._include)
        except Exception as e:
            print(f"[WARNING]: could not load word lists. Check the error message and send the parameters correctly. "
                  f"Message: {e}")
            word_list = []
        _words = word_list

    def __get_words(self) -> list:
        self.__load_words()
        return _words

    def __get_censor_char(self) -> list:
        if not self._censor_pool:
            self._censor_pool = list(self._censor_chars)
        return self._censor_pool.pop(random.randrange(len(self._censor_pool)))

    def censor(self, input_text="", censor_char=None, countries=None,
               exclude=None, include=None, distance_metric: TextDistanceStrategy = None) -> str:
        """
            Censor words in document or phrase according to parameters.
            If the argument `countries` is not passed in, all countries will be used.
            If the argument `distance_metric` is not passed in, the algorithm of search and comparison of the words will
            try to find the equality between the words of the parameter `input_text` and the words of the dataset.

            Parameters
            ----------
            :param input_text : str, mandatory
                document, message, text you want to check and clean by censoring.
            :param censor_char : str, optional
                characters used for censoring words found in `input_text`
            :param countries: list, optional
                indicates the countries from which the vulgarities will be used for censoring.
            :param exclude: list, optional
                indicates words that you want to exclude and not take into account as vulgarity or word to censor
            :param include: list, optional
                indicates words that you want to include as new vulgarity or new word to censor it.
            :param distance_metric: TextDistanceStrategy, optional (recommended to pass it)

            Returns
            -------
            :return: input_text : str
                return `input_text` with the censored words.
           """

        if len(input_text.strip()) == 0:
            return ""

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

        if self._distance_metric and self._distance_metric.normalize_text:
            input_text = self._distance_metric.normalize(input_text)

        working_text = input_text
        words = self.__get_words()

        # Default
        if not self._distance_metric:
            for word in words:
                curse_word = re.compile(re.escape(word), re.IGNORECASE)
                cen = "".join(self.__get_censor_char() for i in list(word))
                working_text = curse_word.sub(cen, working_text)
            return working_text

        # Distance metric
        working_words = re.findall(r'\w+', working_text)

        for word in words:
            for working_word in working_words:
                distance = self._distance_metric.calculate(word, working_word)
                replace = False

                if self._distance_metric.name == DistanceMetricStrategy.HammingDistance.name \
                or self._distance_metric.name == DistanceMetricStrategy.LevenshteinDistance.name:
                    if distance <= self._distance_metric.threshold:
                        replace = True
                else:
                    if distance >= self._distance_metric.threshold:
                        replace = True

                if replace:
                    working_text = working_text.replace(
                        working_word, "".join(self.__get_censor_char() for i in list(working_word)))

        return working_text

    def contains_palabrota(self, text) -> bool:
        return text != self.censor(text)

    @staticmethod
    def supported_countries() -> list:
        return [c for c in Country]
