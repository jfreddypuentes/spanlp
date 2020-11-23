# Author: Jhon Freddy Puentes <jfredypuentes@gmail.com>


import enum


class Country(enum.Enum):
    """
    Lista de paises de habla hispana soportados en la libreria.
    los codigos de pais fueron tomados en Octubre de 2020 en base al estandar ISO-3166 alpha-3
    @see https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
    """
    ARGENTINA = 'ARG'
    BOLIVIA = 'BOL'
    CHILE = 'CHL'
    COLOMBIA = 'COL'
    COSTA_RICA = 'CRI'
    CUBA = 'CUB'
    ECUADOR = 'ECU'
    EL_SALVADOR = 'SLV'
    ESPANA = 'ESP'
    GUATEMALA = 'GTM'
    GUINEA_ECUATORIAL = 'GNQ'
    HONDURAS = 'HND'
    MEXICO = 'MEX'
    NICARAGUA = 'NIC'
    PANAMA = 'PAN'
    PARAGUAY = 'PRY'
    PERU = 'PER'
    PUERTO_RICO = 'PRI'
    REPUBLICA_DOMINICANA = 'DOM'
    URUGUAY = 'URY'
    VENEZUELA = 'VEN'

    @staticmethod
    def all():
        return list(map(lambda c: c.value, Country))
