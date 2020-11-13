from spanlp.palabrota import Palabrota


def main():

    frase = "Hola huevon cochina como esta?"

    palabrota2 = Palabrota()
    print(palabrota2.censor(frase))
    palabrota2.set_censor_characters("x")
    print(palabrota2.censor(frase))

    print("="*50)

    palabrota3 = Palabrota(countries=["COL"])
    print(palabrota3.censor(frase))
    palabrota3.set_censor_characters("X")
    print(palabrota3.censor(frase))


main()
