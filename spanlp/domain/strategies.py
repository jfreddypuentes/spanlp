# -*- coding: utf-8 -*-
import enum


class Strategy(enum.Enum):
    JaccardIndex = 'JaccardIndex'
    CosineSimilarity = 'CosineSimilarity'


class TextDistanceStrategy(object):
    name = ''
    threshold = 0.0
    normalize_text = False

    def __init__(self, name, threshold, normalize=False) -> None:
        self.name = name
        self.threshold = threshold
        self.normalize_text = normalize

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

    @classmethod
    def normalize(cls, text: str):
        if len(text.strip()) == 0:
            return ""
        text = text.lower()
        text = text.replace("  ", " ").replace("   ", " ")
        text = text.replace("á", "a").replace("é", "e").replace("í", "i")\
            .replace("ó", "o").replace("ú", "u").replace("ñ", "n")
        return text

    def __str__(self):
        return " Name: {}, threshold: {} ".format(self.name, self.threshold)


class JaccardIndex(TextDistanceStrategy):
    n_gram = 2

    def __init__(self, threshold=0.8, normalize=False, n_gram=2) -> None:
        super().__init__(Strategy.JaccardIndex.name, threshold, normalize=normalize)
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

    def __init__(self, threshold=0.9, normalize=False) -> None:
        super().__init__(Strategy.CosineSimilarity.name, threshold, normalize)

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
