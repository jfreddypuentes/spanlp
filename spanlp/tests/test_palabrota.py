from spanlp.domain.countries import Country
from spanlp.domain.strategies import CosineSimilarity
from spanlp.domain.strategies import JaccardIndex
from spanlp.palabrota import Palabrota


def test_censor1():
    frase = "hola huevon"
    palabrota = Palabrota(countries=[Country.COLOMBIA], censor_char='*', exclude=[], include=[], distance_metric=None)
    result = palabrota.censor(frase)
    assert result == "hola ******"
    assert len(result) == len(frase)


def test_censor2():
    frase = "hola huevon flojo"
    palabrota = Palabrota(countries=[Country.VENEZUELA], censor_char='.', exclude=["huevon"], include=[],
                          distance_metric=None)
    result = palabrota.censor(frase)
    assert result == "hola huevon ....."
    assert len(result) == len(frase)


def test_censor3():
    frase = "hola flojo"
    palabrota = Palabrota(countries=[Country.VENEZUELA], censor_char='.', exclude=["hola", "flojo"], include=[],
                          distance_metric=None)
    result = palabrota.censor(frase)
    assert result == frase


def test_censor4():
    frase = "hola flojo boludo"
    palabrota = Palabrota(countries=[Country.VENEZUELA], censor_char='-', exclude=["hola"], include=["boludo"],
                          distance_metric=None)
    result = palabrota.censor(frase)
    assert result == "hola ----- ------"


def test_censor5():
    frase = "HoLa FlOjO BoLuDo"
    cosine = CosineSimilarity(threshold=0.9, normalize=False)
    palabrota = Palabrota(countries=[Country.COLOMBIA, Country.VENEZUELA], censor_char='-',
                          exclude=[], include=[], distance_metric=cosine)
    result = palabrota.censor(frase)
    assert result == frase


def test_censor6():
    frase = "HoLa FlOjO BoLuDo"
    cosine = CosineSimilarity(threshold=0.3, normalize=True)
    palabrota = Palabrota(countries=[Country.COLOMBIA, Country.VENEZUELA], censor_char='-',
                          exclude=[], include=[], distance_metric=cosine)
    result = palabrota.censor(frase)
    assert result != frase


def test_cosine_similarity():
    cosine_similarity = CosineSimilarity()
    assert cosine_similarity.calculate("palabra", "palabra") > 0.9
    assert cosine_similarity.calculate("PALABRA", "palabra") == 0.0


def test_cosine_similarity1():
    cosine_similarity1 = CosineSimilarity(normalize=True)
    assert cosine_similarity1.calculate("PALABRA", "palabra") > 0.9


def test_jaccard_index1():
    jaccard_index = JaccardIndex(n_gram=0)
    assert jaccard_index.calculate("pAlAbrA", "palabra") == 1.0


def test_jaccard_index2():
    jaccard_index = JaccardIndex(n_gram=1)
    assert jaccard_index.calculate("pAlAbrA", "palabra") < 1.0


def test_jaccard_index3():
    jaccard_index = JaccardIndex(normalize=True, n_gram=2)
    assert jaccard_index.calculate("PALABRA", "palabra") == 1.0


def test_contains_palabrota1():
    palabrota = Palabrota(countries=[Country.COLOMBIA])
    assert palabrota.contains_palabrota("huevon")
    assert not palabrota.contains_palabrota("")


def test_supported_countries():
    palabrota = Palabrota()
    assert len(palabrota.supported_countries()) > 0
