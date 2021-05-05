from spanlp.domain.countries import Country
from spanlp.domain.strategies import CosineSimilarity, JaccardIndex, HammingDistance, LevenshteinDistance
from spanlp.domain.strategies import TextToLower, TextToUpper, RemoveUnicodeCharacters, NumbersToVowelsInLowerCase
from spanlp.domain.strategies import NumbersToVowelsInUpperCase, NumbersToConsonantsInLowerCase, \
    NumbersToConsonantsInUpperCase, RemoveNumbers, RemoveExtraSpaces, RemoveUserMentions, RemoveUrls, RemoveHashtags, \
    RemoveTicks, RemoveBackTicks, RemovePunctuation, RemoveAccents, RemoveStopWords, RemoveArticles, RemoveEmoticons, \
    RemovePronouns, RemoveAdverbs, RemoveConjunctions, RemovePrepositions, RemoveAdjectives, RemoveHtmlTags, \
    RemoveEmailAddress, ExpandAbbreviations, RemoveAbbreviations
from spanlp.domain.strategies import Preprocessing
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
    cosine = CosineSimilarity(threshold=0.3, normalize=False)
    palabrota = Palabrota(countries=[Country.COLOMBIA, Country.VENEZUELA], censor_char='-',
                          exclude=[], include=[], distance_metric=cosine)
    result = palabrota.censor(frase)
    assert result != frase


def test_cosine_similarity():
    cosine_similarity = CosineSimilarity()
    assert cosine_similarity.calculate("palabra", "palabra") > 0.9
    assert cosine_similarity.calculate("PALABRA", "palabra") == 0.0


def test_cosine_similarity1():
    cosine_similarity1 = CosineSimilarity(normalize=False)
    assert cosine_similarity1.calculate("PALABRA", "palabra") == 0.0


def test_jaccard_index1():
    jaccard_index = JaccardIndex(n_gram=0)
    assert jaccard_index.calculate("pAlAbrA", "palabra") == 1.0


def test_jaccard_index2():
    jaccard_index = JaccardIndex(n_gram=1)
    assert jaccard_index.calculate("pAlAbrA", "palabra") < 1.0


def test_jaccard_index3():
    jaccard_index = JaccardIndex(normalize=False, n_gram=2)
    assert jaccard_index.calculate("PALABRA", "palabra") == 0.0


def test_contains_palabrota1():
    palabrota = Palabrota(countries=[Country.COLOMBIA])
    assert palabrota.contains_palabrota("huevon")
    assert not palabrota.contains_palabrota("")


def test_supported_countries():
    palabrota = Palabrota()
    assert len(palabrota.supported_countries()) > 0


def test_to_lower():
    strategies = [TextToLower()]
    data = "ESTARE EN MINUSCULA"
    result = Preprocessing(data=data, clean_strategies=strategies).clean()
    assert result == 'estare en minuscula'


def test_to_lower1():
    strategies = [TextToLower()]
    data = "ESTARE EN MINUSCULA"
    result = Preprocessing().clean(data=data, clean_strategies=strategies)
    assert result == 'estare en minuscula'


def test_to_lower2():
    strategies = [TextToLower()]
    data = "ESTARE EN MINUSCULA"
    preprocessor = Preprocessing()
    result = preprocessor.clean(data=data, clean_strategies=strategies)
    assert result == 'estare en minuscula'


def test_to_lower_with_jaccard_index():
    strategies = [TextToLower()]
    jaccard_index = JaccardIndex(normalize=True, clean_strategies=strategies)
    result = jaccard_index.normalize("HOLA ME VOY A NORMALIZAR A MINUSCULA")
    assert result == 'hola me voy a normalizar a minuscula'


def test_to_lower_with_jaccard_index():
    strategies = [TextToLower()]
    jaccard_index = JaccardIndex(normalize=True, clean_strategies=strategies)
    result1 = jaccard_index.calculate("HOLA", "hola")
    result2 = jaccard_index.calculate("hola", "HOLA")
    assert result1 == 1.0
    assert result2 == 1.0


def test_to_lower_with_cosine_distance():
    strategies = [TextToLower()]
    cosine = CosineSimilarity(normalize=True, clean_strategies=strategies)
    result = cosine.normalize("HOLA ME VOY A NORMALIZAR A MINUSCULA")
    assert result == 'hola me voy a normalizar a minuscula'


def test_to_lower_with_cosine_distance():
    strategies = [TextToLower()]
    cosine = CosineSimilarity(normalize=True, clean_strategies=strategies)
    result1 = cosine.calculate("HOLA", "hola")
    result2 = cosine.calculate("hola", "HOLA")
    assert result1 >= 0.9
    assert result2 >= 0.9


def test_text_to_upper():
    strategies = [TextToUpper()]
    pre_processing = Preprocessing(data="estaré en mayuscula", clean_strategies=strategies)
    cleaned = pre_processing.clean()
    assert cleaned == "ESTARÉ EN MAYUSCULA"


def test_remove_unicode_characters():
    strategies = [RemoveUnicodeCharacters()]
    pre_processing = Preprocessing(data="mensaje ¥con ¶ unicodeÆ", clean_strategies=strategies)
    cleaned = pre_processing.clean()
    assert cleaned == "mensaje con  unicode"


def test_numbers_to_vowels_in_lower_case():
    strategies = [NumbersToVowelsInLowerCase()]
    cleaned = Preprocessing().clean(data="H0l4 m4r1c4, c0m0 v4m05", clean_strategies=strategies)
    assert cleaned == "Hola marica, como vamo5"


def test_numbers_to_vowels_in_upper_case():
    strategies = [NumbersToVowelsInUpperCase()]
    cleaned = Preprocessing().clean(data="H0L4 MAR1C4 C0M0 V4M05", clean_strategies=strategies)
    assert cleaned == "HOLA MARICA COMO VAMO5"


def test_numbers_to_consonants_in_lower_case():
    strategies = [NumbersToConsonantsInLowerCase()]
    cleaned = Preprocessing().clean(data="El 9a70 e5 negr0 y ju6u370n", clean_strategies=strategies)
    assert cleaned == "El gat0 es negr0 y jugu3t0n"


def test_numbers_to_consonants_in_upper_case():
    strategies = [NumbersToConsonantsInUpperCase()]
    cleaned = Preprocessing().clean(data="E1 6A70 E5 NE9R0", clean_strategies=strategies)
    assert cleaned == "EL GAT0 ES NEGR0"


def test_remove_numbers():
    strategies = [RemoveNumbers()]
    cleaned = Preprocessing().clean(data="la comida 1234567 estaba 3 rica20", clean_strategies=strategies)
    assert cleaned == "la comida  estaba  "


def test_remove_numbers1():
    strategies = [RemoveNumbers()]
    cleaned = Preprocessing().clean(data="0123456789", clean_strategies=strategies)
    assert cleaned == ""


def test_remove_extra_spaces():
    cleaned = Preprocessing().clean(data="  con    muchos      espacios  ", clean_strategies=[RemoveExtraSpaces()])
    assert cleaned == "con muchos espacios"


def test_remove_extra_spaces1():
    cleaned1 = Preprocessing().clean(data=None, clean_strategies=[RemoveExtraSpaces()])
    cleaned2 = Preprocessing(data=None, clean_strategies=[RemoveExtraSpaces()]).clean()
    assert cleaned1 == ""
    assert cleaned2 == ""


def test_user_mentions():
    strategies = [RemoveUserMentions()]
    message = "Hola @jhon, si viste que @freddy va a lanzar una nueva libreria Python para NLP?"
    expected = "Hola , si viste que  va a lanzar una nueva libreria Python para NLP?"
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_urls():
    strategies = [RemoveUrls()]
    message = "Hola @team miren el link https://whoisjhonpuentes.web.app/ de ejemplo"
    expected = "Hola @team miren el link  de ejemplo"
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_hashtags():
    strategies = [RemoveHashtags()]
    message = "Miren, la #clase de #NLP es muy interesante pueden #aprender un monton de #algoritmos"
    expected = "Miren, la  de  es muy interesante pueden  un monton de "
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_ticks():
    strategies = [RemoveTicks()]
    message = "Vamos pa'lante porque pa'lante es pa' allá"
    expected = "Vamos palante porque palante es pa allá"
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_backticks():
    strategies = [RemoveBackTicks()]
    message = "Vamos pa`lante porque pa`lante es pa` allá"
    expected = "Vamos palante porque palante es pa allá"
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_punctuation():
    strategies = [RemovePunctuation()]
    message = "hola, que mas? esto. tiene varios, signos () de puntuación"
    expected = "hola que mas esto tiene varios signos  de puntuación"
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_numbers():
    strategies = [RemoveNumbers()]
    message = "esto tiene el 1, el 2"
    expected = "esto tiene el , el "
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_accents():
    strategies = [RemoveAccents()]
    message = "Qué te parece la canción que cantó él?"
    expected = "Que te parece la cancion que canto el?"
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_accents():
    strategies = [RemoveStopWords()]
    message = "en los textos hay muchas palabras vacias. y en sobretodo en los chats hay por montones"
    expected = "textos muchas palabras vacias. sobretodo chats montones"
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_articles():
    strategies = [RemoveArticles()]
    message = "en los textos se usan muchos los articulos."
    expected = "en textos se usan muchos articulos."
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_emoticons():
    strategies = [RemoveEmoticons()]
    message = "Los emoticones <3 :) :D ;) son muy usados y esta rosa tambien @}->--"
    expected = "Los emoticones son muy usados y esta rosa tambien"
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_pronouns():
    strategies = [RemovePronouns()]
    message = "Siempre estamos usando los pronombres yo tu usted ella nosotros"
    expected = "Siempre estamos usando los pronombres"
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_adverbs():
    strategies = [RemoveAdverbs()]
    message = "muchos años despues frente al peloton de fusilamiento lentamente recordaba..."
    expected = "muchos años frente al peloton de fusilamiento recordaba..."
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_conjunctions():
    strategies = [RemoveConjunctions()]
    message = "y entonces estaba programando aunque con sueño pero concentrado creando esta libreria"
    expected = "entonces estaba programando con sueño concentrado creando esta libreria"
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_prepositions():
    strategies = [RemovePrepositions()]
    message = "ante todo es mejor cuidar a la naturaleza mediante buenas acciones. entre todos podemos."
    expected = "todo es mejor cuidar la naturaleza buenas acciones. todos podemos."
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_adjectives():
    strategies = [RemoveAdjectives()]
    message = "la voz era tenebrosa y la noche estaba fria y oscura hasta que de pronto algo luminoso apareció y"
    expected = "la voz era y la noche estaba y hasta que de pronto algo apareció y"
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_html_tags():
    strategies = [RemoveHtmlTags()]
    message = "<texto><strong>NLP:</strong> Natural y Limpia Programación ;)<br></texto>"
    expected = "NLP: Natural y Limpia Programación ;)"
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_email_address():
    strategies = [RemoveEmailAddress()]
    message = "Contacto: correo@dominio.com"
    expected = "Contacto: "
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_expand_abbrevations():
    strategies = [ExpandAbbreviations()]
    message = "pero xq tengo es3 si yo estaba bn en clase, ahora me duelen to2 los musculos"
    expected = "pero por que tengo estres si yo estaba bien en clase, ahora me duelen todos los musculos"
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_remove_abbrevations():
    strategies = [RemoveAbbreviations()]
    message = "xfa pongase el tapabocas pq me da es3 verlo sin eso. to2 debemos cuidarnos. chas gracias. salu2"
    expected = "pongase el tapabocas me da verlo sin eso. debemos cuidarnos. gracias."
    cleaned1 = Preprocessing().clean(data=message, clean_strategies=strategies)
    cleaned2 = Preprocessing(data=message, clean_strategies=strategies).clean()
    assert cleaned1 == expected
    assert cleaned2 == expected


def test_hamming_distance():
    hamming = HammingDistance()
    expected = 1
    actually = hamming.calculate("hola", "Hola")
    assert expected == actually
    assert expected > 0


def test_hamming_distance2():
    hamming = HammingDistance()
    expected = 4
    actually = hamming.calculate("hola", "HOLA")
    assert expected == actually
    assert expected > 0


def test_hamming_distance3():
    palabrota = Palabrota(censor_char="*", countries=[Country.VENEZUELA], distance_metric=HammingDistance())
    print(palabrota.censor("Huevon", "huevon"))


def test_levenshtein_distance():
    levenshtein = LevenshteinDistance()
    expected = 1
    actually = levenshtein.calculate("hola", "Hola")
    assert expected == actually
    assert expected > 0


def test_levenshtein_distance1():
    levenshtein = LevenshteinDistance()
    expected = 2
    actually = levenshtein.calculate("hola", "Holaa")
    assert expected == actually
    assert expected > 0


def test_levenshtein_distance2():
    levenshtein = LevenshteinDistance()
    expected = 3
    actually = levenshtein.calculate("holaaa", "Hola")
    assert expected == actually
    assert expected > 0


def test_test_levenshtein_distance3():
    palabrota = Palabrota(censor_char="*", countries=[Country.VENEZUELA], distance_metric=LevenshteinDistance())
    print(palabrota.censor("Huevon", "huevon"))
