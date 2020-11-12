from spanlp.palabrota import get_words, censor, contains_palabrota


def main():
    r = get_words(country=["COL", "VEN"])
    print(r)
    print(f"Encontro {len(r)} palabras para COL y VEN")

    r = get_words(country=["VEN"])
    print(r)
    print(f"Encontro {len(r)} palabras para VEN")

    r = get_words(country=["COL"])
    print(r)
    print(f"Encontro {len(r)} palabras para COL")

    r = censor("Hola huevon cochina como esta?", country=None)
    print(r)

    r = contains_palabrota("Hola huevon")
    print(r)


main()
