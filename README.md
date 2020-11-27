# spanlp
spanlp es una librería escrita en Python para detectar, censurar  y limpiar groserías, vulgaridades, palabras de odio, racismo y xenofobia en textos en **Español**.
Puedes usar la librería y aplicarla a palabras de cualquiera de los más de **20 paises** de habla hispana.

Incluye:
1. Argentina
2. Bolivia
3. Chile
4. Colombia
5. Costa Rica
6. Cuba
7. Ecuador
8. El Salvador
9. España
10. Guatemala
11. Guinea Ecuatorial
12. Honduras
13. Mexico
14. Nicaragua
15. Panamá
16. Paraguay
17. Perú
18. Puerto Rico
19. Dominicana
20. Uruguay
21. Venezuela

## Casos de uso
* Censurar vulgaridades en un texto.
* Detectar y censurar vulgaridades en una sala de chat en linea.
* Encontrar y censurar frases y palabras de odio, racismo y xenofia. (Se deben incluir como parámetros)
* Censurar comentarios groseros o insultos en algún blog o aplicación web o sitio web.
* Censurar malas palabras en un sistema de recolección de opiniones, sugerencias, quejas y reclamos.
* Limpiar textos antes de ser publicados.
* Detectar y eliminar vulgaridades en textos que serán leidos y/o vistos por niños.
* Limpiar una base de datos con mucho texto.

## Instalación
**Nota:** Esta versión se encuentra en Beta. No la use en producción aún. 
Te recomiendo que la instales, pruebes y haz doble check sobre los resultados.
Si encuentras algún problema escribeme o puedes crear un issue [aquí](https://github.com/jfreddypuentes/spanlp/issues/new)

```console
pip install -i https://test.pypi.org/simple/ spanlp
```

## ¿Cómo funciona?
Los algoritmos y modulos se personalizan de forma dinámica y muy flexible. Veamos algunos usos.

### Uso básico

Validar si una palabra o frase contiene o no una palabrota:
```python
from spanlp.palabrota import Palabrota
palabrota = Palabrota()
print(palabrota.contains_palabrota("Hola huevon cómo está?"))
# salida: True
```

```python
from spanlp.palabrota import Palabrota
palabrota = Palabrota()
print(palabrota.contains_palabrota("Hola a todos ¿cómo están?"))
# salida: False
```

Censurar una frase con los parámetros por defecto:

```python
from spanlp.palabrota import Palabrota

palabrota = Palabrota()
print(palabrota.censor("Hola huevon cómo está?"))

# salida: Hola !$%#@! cómo está?
```

Censurar la misma frase, configurando carácteres propios

```python
from spanlp.palabrota import Palabrota

palabrota = Palabrota(censor_char="*")
print(palabrota.censor("Hola huevon como está?"))

# salida: Hola ****** cómo está?
```

Censurar otra frase, configurando carácteres propios y país

```python
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country

palabrota = Palabrota(censor_char="@", countries=[Country.COLOMBIA, Country.VENEZUELA])
print(palabrota.censor("Hola huevon marico cómo está?"))

# salida: Hola @@@@@@ @@@@@@ cómo está?
```

Censuremos la misma frase pero solo con el país de Venezuela
```python
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country

palabrota = Palabrota(censor_char="@", countries=[Country.VENEZUELA])
print(palabrota.censor("Hola huevon marico cómo está?"))

# salida: Hola huevon @@@@@@ cómo está?
```

Censuremos la misma frase pero incluyendo "huevon" al vocabulario de Venezuela
```python
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country

palabrota = Palabrota(censor_char="@", countries=[Country.VENEZUELA], include=["huevon"])
print(palabrota.censor("Hola huevon marico cómo está?"))

# salida: Hola @@@@@@ @@@@@@ cómo está?
```

Censuremos la misma frase incluyendo "huevon" al vocabulario de Venezuela y excluyendo "marico"
```python
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country

palabrota = Palabrota(censor_char="@", countries=[Country.VENEZUELA], include=["huevon"], exclude=["marico"])
print(palabrota.censor("Hola huevon marico cómo está?"))

# salida: Hola huevon marico cómo está?
```

Censuremos la misma frase incluyendo ""Hola" y "huevon" al vocabulario de Venezuela y excluyendo "marico"
```python
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country

palabrota = Palabrota(censor_char="-", countries=[Country.VENEZUELA], include=["huevon"], exclude=["marico"])
print(palabrota.censor("Hola huevon marico cómo está?"))

# salida: ---- ---- marico cómo está?
```

### Uso Avanzado
El uso avanzado incluye usar metricas de distancia y similitud para encontrar, comparar, censurar palabras.
Estas son las metrcias usadas a la fecha:
1. [Indice de Jaccard](https://es.wikipedia.org/wiki/%C3%8Dndice_Jaccard) ([Jaccard Index](https://en.wikipedia.org/wiki/Jaccard_index))
2. [Similitud del coseno](https://es.wikipedia.org/wiki/Similitud_coseno) ([Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity))

Próximos releases:
* Hamming...
* Levenstein...
* Bag distance...
* Sorensen-Dice coefficient...
* Tversky index...
* Overlap index...
* Tanimoto distance...


Censuremos la frase usando Cosine Similarity 
```python
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country
from spanlp.domain.strategies import CosineSimilarity

palabrota = Palabrota(censor_char="*", countries=[Country.VENEZUELA], distance_metric=CosineSimilarity())
print(palabrota.censor("Hola huevo maric cómo está?"))

# salida: Hola huevo ***** cómo está?
```
A pesar de que "maric" no está en el dataset, al algoritmo la censuró dado que por la métrica de distancia es muy similar. 


Censuremos la frase usando **Cosine Similarity** manipulando los parámetros
```python
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country
from spanlp.domain.strategies import CosineSimilarity

# Indicamos que tenga en cuenta palabras similares en al menos 30% y que normalice los datos (poner en minusculas, remover acentos)
cosine = CosineSimilarity(0.9, normalize=True) 
palabrota = Palabrota(censor_char="*", countries=[Country.VENEZUELA], distance_metric=cosine)
print(palabrota.censor("Hola huevon MARIC cómo está?"))

# salida: hola huevon ***** **** esta? => Censuró "como" porque en el dataset está "cono" y son similares en más del 90%
```

Censuremos la frase usando **JaccardIndex** con los parámetros por defecto
```python
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country
from spanlp.domain.strategies import JaccardIndex

palabrota = Palabrota(censor_char="*", countries=[Country.VENEZUELA], distance_metric=JaccardIndex())
print(palabrota.censor("Hola huevo maric cómo está?"))

# salida: Hola huevo ***** cómo está?
```
El indice de Jaccard usa por defecto los siguientes parámetros:
* `threshold=0.8` - Indica que censurará palabras con una similitud del 80% o más.
* `normalize=False` - False indica que no pasará el texto a minuscula y no removerá acentos.
* `n_gram=2` - Usa 2 subsecuencias de la palabra. (Ver [N-grama](https://es.wikipedia.org/wiki/N-grama))

Censuremos la frase usando **JaccardIndex** y modifiquemos los parámetros
```python
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country
from spanlp.domain.strategies import JaccardIndex

jaccard = JaccardIndex(threshold=0.9, normalize=True, n_gram=1)
palabrota = Palabrota(censor_char="*", countries=[Country.VENEZUELA], distance_metric=jaccard)
print(palabrota.censor("Hola huevon marica cómo vamos?"))

# salida: hola huevon ****** **** vamos?
```

Ahora, sin normalizar los datos
```python
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country
from spanlp.domain.strategies import JaccardIndex

jaccard = JaccardIndex(threshold=0.9, normalize=False, n_gram=1)
palabrota = Palabrota(censor_char="*", countries=[Country.VENEZUELA], distance_metric=jaccard)
print(palabrota.censor("Hola huevon marica cómo vamos?"))

# salida: Hola huevon ****** cómo vamos? => "moco" y "cómo" ahora son muy diferentes.
```

Ahora, bajemos el `threshold` a `0.6`
```python
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country
from spanlp.domain.strategies import JaccardIndex

jaccard = JaccardIndex(threshold=0.6, normalize=False, n_gram=1)
palabrota = Palabrota(censor_char="*", countries=[Country.VENEZUELA], distance_metric=jaccard)
print(palabrota.censor("Hola huevon marica cómo vamos?"))

# salida: Hola ****** ****** cómo vamos? => Ha censurado una palabra más.
```

Aumentemos la cantidad de `n_gram` a `3` con el `threshold=0.7` y con `normalize=False`
```python
from spanlp.palabrota import Palabrota
from spanlp.domain.countries import Country
from spanlp.domain.strategies import JaccardIndex

jaccard = JaccardIndex(threshold=0.7, normalize=False, n_gram=3)
palabrota = Palabrota(censor_char="*", countries=[Country.VENEZUELA], distance_metric=jaccard)
print(palabrota.censor("Hola huevon marica cómo vamos?"))

# salida: Hola huevon marica cómo vamos? => No censuró nada.
```


## Beta Testing
¿Eres betatester? ¿quieres automatizar pruebas? o ¿simplemente aprender del open source y de las pruebas? Aventurate ya y ayudame a mejorar este proyecto!
A continuación encontrarás algunas pautas para implementar pruebas exitosas que permitarán encontrar posibles errores y mejoras.

### 1. ¿Por donde empezar?
* Instalar python.
* Instalar la librería. Esto lo logras ejecutando en la terminal el comando: `pip install -i https://test.pypi.org/simple/ spanlp`
* Abre un nuevo script de python, importa la librería y empieza a experimentar.

### 2. ¿Qué tipos de pruebas puedo realizar?
Excelente pregunta! no hay limite para la creatividad; Así que haz todas las pruebas que quieras e imagines. Sin embargo, aquí te dejo algunas pautas:

* **Pruebas de caja negra** => Una vez instales la librería y hayas leido la documentación; Trata de usarla sin preocuparte como funciona o como obtuvo el resultado (Las pruebas no se hacen en base al código, sino a la interfaz); Eso si, valida que la salida o el resultado sea el que esperas. Te puedes guiar (pero no mucho) de las pruebas unitarias que están en: `/spanlp/tests/test_palabrota.py`

* **Pruebas de caja blanca** => Si quieres vez como funciona la libreria, estas pruebas son las tuyas. Intenta entender la estructura, los algoritmos y flujos. Una vez los comprendas, "a dar palo", trata de quebar o romper la lógica, observa y encuentra si hay posibles formas de hacer que falle, prueba diferentes parametros, flujos, tipos de datos. Haz que falle, haz que se ponga lento! y me cuentas. ;)

* **Pruebas de carga y stress** => Si lo tuyo son las pruebas de requisitos no funcionales, te invito a que sigas estos pasos para estresar la libreria y medir que tan escalable es frente a procesos de alta carga, mide la velocidad y que tan bien se comparta con miles o millones de hilos usandola al tiempo.

Sigue estos pasos:

1. Crear una API Rest súper simple. Crea el siguiente script y llámalo `server.py` 

```console
pip install flask
```

```python
from flask_cors import CORS, cross_origin
from flask import request
from flask import json

from spanlp.palabrota import Palabrota

app = Flask(__name__)
cors = CORS(app)

@app.route('/api/v1/nlp/text/censor', methods = ['POST'])
@cross_origin()
def censor():
    try:
        body = request.json     
        in_message = body['message']
        
        if in_message and len(str(in_message).strip()):
            palabrota = Palabrota()
            censored = palabrota.censor(in_message)
            response = {
                "success": True,
                "message": "OK",
                "error_code": 0,
                "data": {
                    'message': in_message,
                    'censored': censored
                }
            }
            return response
        else:
            return {
                "success": False,
                "message": "Bad Request - message is required",
                "error_code": 400,
                "data": {}
            }
    except Exception as e:
        return {
            "success": False,
            "message": "Internal Server Error - "+str(e),
            "error_code": 500,
            "data": {}
        }


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
```


```
python server.py
```

y listo!! 


2. Consume la API desde algún cliente http como [Postman](https://www.postman.com/), [Insomnia](https://insomnia.rest/download/) y/o [SOAP UI](https://www.soapui.org/). Tambien puedes usar alguna herramienta como [Apache JMeter](https://jmeter.apache.org/); o tambien puedes crear un script python con muchos hilos que consuma la API.


### 3. ¿quieres escibrir unit tests y ejecutarlo de forma automática?
Clona el repositorio en tu máquina, abre el proyecto en tu editor favorito, ve al archivo `/spanlp/tests/test_palabrota.py` y empieza a escribir tus propios tests unitarios. Escribe cuantos quieras.
Una vez tengas los tests listos, ejecuta el siguiente comando en la raiz del proyecto (`/spanlp/`):

```console
pytest -ra
```

Esto ejecutará de forma automática todas las pruebas programadas e indicará si algun test falló.


## ¿Cómo reportar un bug/falla/error?
Si encuentras algún problema (por muy mínimo que sea) reportalo [aquí](https://github.com/jfreddypuentes/spanlp/issues/new). Solo necesitarás poner título y describir la falla y aportará un montón a que este proyecto mejore su calidad.


## Contacto
¿Alguna duda? escribeme por email:  [jfredypuentes@gmail.com](mailto:jfredypuentes@gmail.com)

Cuentame en ([@jfreddypuentes](https://twitter.com/jfreddypuentes)) ¿qué te parece está librería? ¿cómo la estás usando? ¿Qué le mejorarías?

<br>
<br>


**Hecho con ❤️️ de Colombia para el mundo.**
