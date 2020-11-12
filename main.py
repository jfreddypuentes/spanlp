from spanlp.palabrota import get_words, censor


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

    r = censor("Hola huevon cochina puta como esta?", country=None)
    print(r)


main()
