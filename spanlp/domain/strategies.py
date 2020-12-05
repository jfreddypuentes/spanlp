# -*- coding: utf-8 -*-
import enum
from .constant import SPANISH_STOP_WORDS, ARTICLES, EMOTICONS, PRONOUNS, \
    ADVERBS, CONJUNCTIONS, PREPROSITIONS, ADJECTIVES, ABBREVIATIONS
from abc import abstractmethod
import re
import string


class DistanceMetricStrategy(enum.Enum):
    JaccardIndex = 'JaccardIndex'
    CosineSimilarity = 'CosineSimilarity'


class CleanDataStrategy:

    @classmethod
    def remove_dynamic_tokens(cls, data: str, words: [str] = None):
        if data:
            result = ' '.join([word for word in data.split(' ') if word not in words])
            return result
        return ""

    @abstractmethod
    def clean(self, data: str):
        pass


class TextDistanceStrategy(object):
    name = ''
    threshold = 0.0
    normalize_text = False
    clean_strategies: [CleanDataStrategy] = None

    def __init__(self, name, threshold, normalize=False, clean_strategies: [CleanDataStrategy] = None) -> None:
        self.name = name
        self.threshold = threshold
        self.normalize_text = normalize
        self.clean_strategies = clean_strategies

    def calculate(self, word1: str, word2: str) -> float:
        pass

    @classmethod
    def word2vec(cls, word):
        from collections import Counter
        from math import sqrt

        cw = Counter(word)
        sw = set(cw)
        lw = sqrt(sum(c * c for c in cw.values()))

        return cw, sw, lw

    def normalize(self, text: str):
        if len(text.strip()) == 0:
            return ""
        if self.normalize_text and self.clean_strategies and len(self.clean_strategies) > 0:
            for clean_strategy in self.clean_strategies:
                text = clean_strategy.clean(text)
        if self.normalize_text and (self.clean_strategies is None or len(self.clean_strategies) == 0):
            raise Exception("Si indica normalize=True debe enviar al menos una estrategia de limpieza de datos.")
        return text

    def __str__(self):
        return " Name: {}, threshold: {} ".format(self.name, self.threshold)


class JaccardIndex(TextDistanceStrategy):
    n_gram = 2

    def __init__(self, threshold=0.8, n_gram=2, normalize=False, clean_strategies: [CleanDataStrategy] = None) -> None:
        super().__init__(name=DistanceMetricStrategy.JaccardIndex.name, threshold=threshold, normalize=normalize,
                         clean_strategies=clean_strategies)
        self.n_gram = n_gram

    def calculate(self, word1: str, word2: str) -> float:
        if word1 == word2:
            return 1
        if (len(word1) == 0) or (len(word2) == 0):
            return 0
        if self.normalize_text:
            word1 = self.normalize(word1)
            word2 = self.normalize(word2)
        return self.jaccard_index(word1, word2, self.n_gram)

    @classmethod
    def jaccard_index(cls, word1: str, word2: str, n_gram=2):
        if word1 == word2:
            return 1

        len1, len2 = len(word1), len(word2)

        if (len1 == 0) or (len2 == 0):
            return 0

        first_set = set()
        second_set = set()

        for i in range(len1 - 1):
            if ' ' not in word1[i:i + n_gram] and len(word1[i:i + n_gram]) == n_gram:
                first_set.add(word1[i:i + n_gram])

        for i in range(len2 - 1):
            if ' ' not in word2[i:i + n_gram] and len(word2[i:i + n_gram]) == n_gram:
                second_set.add(word2[i:i + n_gram])

        if first_set and second_set:
            intersection_cardinality = len(first_set.intersection(second_set))
            union_cardinality = len(first_set.union(second_set))
            return intersection_cardinality / float(union_cardinality)

        else:
            raise Exception(f"No se encontraron {n_gram} n-gramas. Escoja un valor menor que {n_gram} para n_gram.")


class CosineSimilarity(TextDistanceStrategy):

    def __init__(self, threshold=0.9, normalize=False, clean_strategies: [CleanDataStrategy] = None) -> None:
        super().__init__(name=DistanceMetricStrategy.CosineSimilarity.name, threshold=threshold, normalize=normalize,
                         clean_strategies=clean_strategies)

    def calculate(self, word1: str, word2: str) -> float:
        if self.normalize_text:
            word1 = self.normalize(word1)
            word2 = self.normalize(word2)

        word_vec1 = self.word2vec(word1)
        word_vec2 = self.word2vec(word2)
        return self.cosine_distance(word_vec1, word_vec2)

    @classmethod
    def cosine_distance(cls, v1, v2):
        common = v1[1].intersection(v2[1])
        return sum(v1[0][ch] * v2[0][ch] for ch in common) / v1[2] / v2[2]


class Preprocessing:

    def __init__(self, data: str = None, clean_strategies: [CleanDataStrategy] = None) -> None:
        self._text = data
        self._clean_strategies = clean_strategies

    def clean(self, data: str = None, clean_strategies: [CleanDataStrategy] = None):
        if data is not None:
            self._text = data

        if clean_strategies is not None:
            self._clean_strategies = clean_strategies

        if self._text is None or len(self._text.strip()) == 0:
            return ""

        if self._clean_strategies and len(self._clean_strategies) > 0:
            for clean_strategy in self._clean_strategies:
                self._text = clean_strategy.clean(self._text)
            return self._text
        else:
            raise Exception("Debe enviar al menos una estrategia de pre-procesamiento o limpieza de datos.")


class TextToLower(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return data.lower()
        return ""


class TextToUpper(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return data.upper()
        return ""


class RemoveUnicodeCharacters(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return data.encode('ascii', 'ignore').decode()
        return ""


class NumbersToVowelsInLowerCase(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return data.replace("4", "a").replace("3", "e").replace("1", "i").replace("0", "o")
        return ""


class NumbersToVowelsInUpperCase(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return data.replace("4", "A").replace("3", "E").replace("1", "I").replace("0", "O")
        return ""


class NumbersToConsonantsInLowerCase(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return data.replace("9", "g").replace("7", "t").replace("5", "s").replace("2", "z")\
                .replace("1", "l").replace("6", "g")
        return ""


class NumbersToConsonantsInUpperCase(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return data.replace("8", "B").replace("6", "G").replace("5", "S").replace("2", "Z")\
                .replace("1", "L").replace("9", "G").replace("7", "T")
        return ""


class RemoveExtraSpaces(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return re.sub(" +", " ", data).strip()
        return ""


class RemoveUserMentions(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return re.sub(r'@\w+', '', data)
        return ""


class RemoveUrls(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return re.sub(r'http\S+', '', data)
        return ""


class RemoveHashtags(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return re.sub("#\\S+", "", data)
        return ""


class RemoveTicks(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return data.replace("'", "")
        return ""


class RemoveBackTicks(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return data.replace("`", "")
        return ""


class RemovePunctuation(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return re.sub('[%s]' % re.escape(string.punctuation), '', data)
        return ""


class RemoveNumbers(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return re.sub(r'\w*\d+\w*', '', data)
        return ""


class RemoveAccents(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            data = data.replace("á", "a").replace("é", "e").replace("í", "i")\
                .replace("ó", "o").replace("ú", "u").replace("ñ", "n")
            data = data.replace("Á", "a").replace("É", "e").replace("Í", "i")\
                .replace("Ó", "o").replace("Ú", "u").replace("Ñ", "N")
            return data
        return ""


class RemoveStopWords(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return self.remove_dynamic_tokens(data=data, words=SPANISH_STOP_WORDS)
        return ""


class RemoveArticles(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return self.remove_dynamic_tokens(data=data, words=ARTICLES)
        return ""


class RemoveEmoticons(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return self.remove_dynamic_tokens(data=data, words=EMOTICONS)
        return ""


class RemovePronouns(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return self.remove_dynamic_tokens(data=data, words=PRONOUNS)
        return ""


class RemoveAdverbs(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return self.remove_dynamic_tokens(data=data, words=ADVERBS)
        return ""


class RemoveConjunctions(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return self.remove_dynamic_tokens(data=data, words=CONJUNCTIONS)
        return ""


class RemovePrepositions(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return self.remove_dynamic_tokens(data=data, words=PREPROSITIONS)
        return ""


class RemoveAdjectives(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            return self.remove_dynamic_tokens(data=data, words=ADJECTIVES)
        return ""


class RemoveHtmlTags(CleanDataStrategy):
    def clean(self, data: str) -> str:
        if data:
            cleaner = re.compile('<.*?>')
            return re.sub(cleaner, '', data)
        return ""


class RemoveEmailAddress(CleanDataStrategy):
    def clean(self, data: str):
        if data:
            return re.sub(r'\S*@\S*\s*', '', data)
        return ""


class ExpandAbbreviations(CleanDataStrategy):
    def clean(self, data: str):
        if data:
            result = data
            for word in data.split(' '):
                if word in ABBREVIATIONS:
                    result = result.replace(word, ABBREVIATIONS[word])
            return result
        return ""


class RemoveAbbreviations(CleanDataStrategy):
    def clean(self, data: str):
        if data:
            return self.remove_dynamic_tokens(data=data, words=list(ABBREVIATIONS.keys()))
        return ""
