<h1 align="center">spanlp</h1>

<p align="center">
  <br>
  <i>spanlp es una librería escrita en Python para detectar, censurar  y limpiar groserías, <br>
      vulgaridades, palabras de odio, racismo, xenofobia y bullying en textos escritos en <strong>Español</strong>.
    </i>
  <br>
  
  <p align="center">
    <a href="https://test.pypi.org/project/spanlp/">
      <img src="https://img.shields.io/badge/version-v1.1.0-green"/>
    </a>
    <a href="https://test.pypi.org/project/spanlp/">
      <img src="https://img.shields.io/badge/status-stable-blue"/>
    </a>
  <a href="https://test.pypi.org/project/spanlp/">
      <img src="https://img.shields.io/badge/release-v1.1.0-brightgreen"/>
    </a>
    <a href="https://test.pypi.org/project/spanlp/">
      <img src="https://img.shields.io/badge/test--pypi-v0.0.7-yellow"/>
    </a>
  <a href="https://test.pypi.org/project/spanlp/">
      <img src="https://img.shields.io/badge/license-MIT-brightgreen"/>
    </a>
  </p>
  
  <p align="center">
    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/jfreddypuentes/spanlp?style=social">
  </p>
</p>

<hr>

## Indice
- [Indice](#indice)
- [Sobre la librería](#sobre-la-librería)
- [Casos de uso](#casos-de-uso)
- [Status Desarrollo](#status-desarrollo)
- [Instalación](#instalación)
- [Funcionamiento](#funcionamiento)
  - [Uso básico](#uso-basico)
  - [Uso avanzado](#uso-avanzado)
  - [Pre-procesamiento de datos](#preprocesamiento-de-texto)
- [Testing](#testing)
- [Reportar un bug](#reportar-un-bug)
- [Contribuidorxs](#contribuidorxs)
- [Contacto](#contacto)

<hr>

## Sobre la librería
spanlp es una librería escrita en Python para detección de groserías, vulgaridades, palabras de odio, racismo, xenofobia y bullying en textos escritos en Español. Puedes usar la librería y aplicarla a palabras de cualquiera de los más de **20 paises** de habla hispana.

Incluye:
1. Argentina 🇦🇷
2. Bolivia 🇧🇴
3. Chile 🇨🇱
4. Colombia 🇨🇴
5. Costa Rica 🇨🇷
6. Cuba 🇨🇺
7. Ecuador 🇪🇨
8. El Salvador 🇸🇻
9. España 🇪🇸
10. Guatemala 🇬🇹
11. Guinea Ecuatorial 🇬🇶
12. Honduras 🇭🇳
13. México 🇲🇽
14. Nicaragua 🇳🇮
15. Panamá 🇵🇦
16. Paraguay 🇵🇾
17. Perú 🇵🇪
18. Puerto Rico 🇵🇷
19. República Dominicana 🇩🇴
20. Uruguay 🇺🇾
21. Venezuela 🇻🇪

## Casos de uso
* Censurar vulgaridades en un texto.
* Detectar y censurar vulgaridades en una sala de chat en linea.
* Encontrar y censurar frases y palabras de odio, racismo, xenofia, bullying. (Se deben incluir como parámetros)
* Censurar comentarios groseros o insultos en algún blog o aplicación web o sitio web.
* Censurar malas palabras en un sistema de recolección de opiniones, sugerencias, quejas y reclamos.
* Limpiar textos antes de ser publicados.
* Detectar y eliminar vulgaridades en textos que serán leidos y/o vistos por niños.
* Limpiar una base de datos con mucho texto.

## Status Desarrollo

| Funcionalidad                     | Desarrollo |   Pruebas   | Release  |
|-----------------------------------|------------|-------------|-----------
| Soporte de tokens con números     |     ✓      |      ✓      | v0.0.5   |  
| Estrategias de limpieza de datos  |     ✓      |      ✓      | v0.0.5   |
| Completar dataset                 |     ✓      |      ✓      | v1.0.1   |
| Hamming                           |     ✓      |      ✓      | v1.0.2   |
| Levenstein                        |     ✓      |      ✓      | v1.1.0   |
| Bag distance                      |     -      |             |    -     |
| Sorensen-Dice coefficient         |     -      |             |    -     |
| Tversky index                     |     -      |             |    -     |
| Overlap index                     |     -      |             |    -     |
| Tanimoto distance                 |     -      |             |    -     |
| Ampliación datasets               |  Progreso  |      -      |    -     |


## Instalación
Para instalar la última versión use:
```console
pip install spanlp
```

Para instalar una versión específica use (por ejemplo):
```
pip install spanlp==1.1.0
```

## Funcionamiento
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
Estas son las metricas usadas a la fecha:
1. [ES-Indice de Jaccard](https://es.wikipedia.org/wiki/%C3%8Dndice_Jaccard) ([EN-Jaccard Index](https://en.wikipedia.org/wiki/Jaccard_index))
2. [ES-Similitud del coseno](https://es.wikipedia.org/wiki/Similitud_coseno) ([EN-Cosine Similarity](https://en.wikipedia.org/wiki/Cosine_similarity))
3. [ES-Levenshtein](https://es.wikipedia.org/wiki/Distancia_de_Levenshtein)([EN-Levenshtein](https://en.wikipedia.org/wiki/Levenshtein_distance))
4. [ES-Damerau-Levenshtein](https://es.wikipedia.org/wiki/Distancia_de_Damerau-Levenshtein)([EN-Damerau-Levenshtein](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance))

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

## Preprocesamiento de texto
Siempre será necesario limpiar los datos antes de empezar a trabajar. Aqui te presento la clase `Preprocessing` y las 28 estratégias de limpieza de datos.

¿Cuantas estrategias hay y cuales son?

Son 28 algoritmos y son:

1. `TextToLower` **input**: "HOLA QUE MÁS?" **output:** "hola que más?"
2. `TextToUpper` **input:** "hola ¿cómo están?" **output:** "HOLA ¿CÓMO ESTÁN?"
3. `RemoveUnicodeCharacters` **input:** "hola çcomo ªvan?" **output:** "hola como van"  ([Unicode characters](https://www.rapidtables.com/code/text/unicode-characters.html))
4. `NumbersToVowelsInLowerCase` **input:** "h0l4 qu3 t4l?" **ouput:** "hola que tal?"
5. `NumbersToVowelsInUpperCase` **input:** "H0l4 c0m0 v4n?" **output:** "HOlA cOmO vAn?"
6. `NumbersToConsonantsInLowerCase` **input:** "C0m0 e574n? 8i3n?" **output:** "Como estan? bien?"
7. `NumbersToConsonantsInUpperCase` **input:** "C0m0 e574n? 8i3n?" **output:** "COMO ESTAN? BIEN?"
8. `RemoveExtraSpaces` **input:** "Hola   como están?   " **output:** "Hola como están?"
9. `RemoveUserMentions` **input:** "Hola @channel como van?" **output:** "Hola como van?"
10. `RemoveUrls`  **input:** "Revisen este recurso https://github.com/jfreddypuentes/spanlp" **output:** "Revisen este recurso "
11. `RemoveHashtags` **input:** "Hola #equipo bienvenidos" **output:** "Hola  bienvenidos"
12. `RemoveTicks` **input:** "Hola, que' más'" **output:** "Hola, que más"
13. `RemoveBackTicks` **input:** "Hola, que` más`" **output:** "Hola, que más"
14. `RemovePunctuation`  **input:** "Mensaje...,con, puntos" **output:** "Mensaje con puntos"
15. `RemoveNumbers` **input:** "Hay 12 patacones  y 20 yucas" **output:** "Hay patacones y yucas"
16. `RemoveAccents` **input:** "La canción es una sensación" **output:** "La cancion es una sensacion"
17. `RemoveStopWords` **input:** "La canción y la letra es buena" **output:** "canción letra buena"
18. `RemoveArticles` **input:** "La canción y la letra es buena" **output:** "canción y letra es buena"
19. `RemoveEmoticons` **input:** "Hola ;) como estás? XD" **output:** "Hola como estás?"
20. `RemovePronouns` **input:** "Yo pienso que ella debería ser como él" **output:** "pienso que debería ser como"
21. `RemoveAdverbs` **input:** "muchos años despues frente al peloton de fusilamiento lentamente recordaba..." **output:** "muchos años frente al peloton de fusilamiento recordaba..."
22. `RemoveConjunctions` **input:** "y entonces estaba programando aunque con sueño pero concentrado creando esta libreria" **output:** "entonces estaba programando con sueño concentrado creando esta libreria"
23. `RemovePrepositions` **input:** "ante todo es mejor cuidar a la naturaleza mediante buenas acciones. entre todos podemos." **output:** "todo es mejor cuidar la naturaleza buenas acciones. todos podemos."
24. `RemoveAdjectives` **input:** "la voz era tenebrosa y la noche estaba fria y oscura hasta que de pronto algo luminoso apareció y" **output:** "la voz era y la noche estaba y hasta que de pronto algo apareció y"
25. `RemoveHtmlTags` **input:** "Hola <strong>USUARIO</strong> que tal?" **output:** "Hola USUARIO que tal?"
26. `RemoveEmailAddress` **input:** "Hola Pepito, el correo es contacto@domain.com" **output:** "Hola Pepito, el correo es "
27. `ExpandAbbreviations` **input:** "pero xq tengo es3 si yo estaba bn en clase, ahora me duelen to2 los musculos" **output:** "pero por que tengo estres si yo estaba bien en clase, ahora me duelen todos los musculos"
28. `RemoveAbbreviations` **input:** "xfa pongase el tapabocas pq me da es3 verlo sin eso. to2 debemos cuidarnos. chas gracias. salu2" **output:** "pongase el tapabocas me da verlo sin eso. debemos cuidarnos. gracias."


La nueva clase `Preprocessing` implementa de manera flexible y dinámica cualquier estrategia de limpieza de una manera muy simple. Se puede aplicar dentro de una metrica de distancia como `JaccardIndex` o `CosineSimilarity` para darle más poder a la busqueda, dismunir el riesgo de no encontrar las palabras a censurar y aumentar la posibilidad de censurar las palabras que son por el hecho de estar limpias.


Veamos algunos ejemplos:

```python
from spanlp.domain.strategies import Preprocessing, TextToLower

strategies = [TextToLower()] # Defino mis estrategias de limpieza o pre-procesamiento
data = "ESTARE EN MINUSCULA" # Tengo mis datos
result = Preprocessing(data=data, clean_strategies=strategies).clean() # Invoco a Preprocessing
print(result)

# salida: estare en minuscula
```

Tambien se puede así:
```python
from spanlp.domain.strategies import Preprocessing, TextToLower

strategies = [TextToLower()]
data = "ESTARE EN MINUSCULA" 
result = Preprocessing().clean(data=data, clean_strategies=strategies) # Envio los datos y las estragias al clean()
print(result)

# salida: estare en minuscula
```

Y tambien así:
```python
from spanlp.domain.strategies import Preprocessing, TextToLower

strategies = [TextToLower()]
data = "ESTARE EN MINUSCULA"
preprocessor = Preprocessing(data=data, clean_strategies=strategies)
result = preprocessor.clean()
print(result)

# salida: estare en minuscula
```

Y así:
```python
from spanlp.domain.strategies import Preprocessing, TextToLower

result = Preprocessing(data="ESTARE EN MINUSCULA", clean_strategies=[TextToLower()]).clean()
print(result)

# salida: estare en minuscula
```

**¿Cómo aplico una estrategia para que pre-preprocese mis datos dentro de la métrica de distancia?**


Aplicar la metrica de distancia con una estrategia de pre-procesado:
```python
from spanlp.domain.strategies import JaccardIndex, TextToLower

strategies = [TextToLower()]
jaccard_index = JaccardIndex(normalize=True, clean_strategies=strategies)
result = jaccard_index.calculate("HOLA", "hola")

print(result)

# salida: 1
```

Usar la métrica como interface para ejecutar la estrategia:

```python
from spanlp.domain.strategies import JaccardIndex, TextToLower

strategies = [TextToLower()]
jaccard_index = JaccardIndex(normalize=True, clean_strategies=strategies)
result = jaccard_index.normalize("HOLA ME VOY A NORMALIZAR A MINUSCULA")

print(result)

# salida: hola me voy a normalizar a minuscula
```

**Usar varias estrategias de limpieza de datos**
Nota: Las estrategias se ejecutan en el orden enviado en la lista. Recomiendo analizar primero como desea que funcione: Si primero elimina espacios extras y despues elimina signos de puntuación y luego stop words etc.. esto dependerá de su necesidad concreta; Por lo que se pueden obtener diferentes resultados si cambia el orden de las estrategias.

Enviando varias estrategias para limpiar mis datos:

```python
from spanlp.domain.strategies import Preprocessing, TextToLower, RemoveUserMentions, RemovePunctuation

strategies = [RemoveUserMentions(), TextToLower(), RemovePunctuation()]
tweet = "Hola @jhon, si viste que @freddy va a lanzar una nueva libreria Python para NLP?"
cleaned = Preprocessing().clean(data=tweet, clean_strategies=strategies)

print(cleaned)

#salida: hola  si viste que  va a lanzar una nueva libreria python para nlp
```

**Limpiemos emoticones, pronombres y pasemos a minuscula**

```python
from spanlp.domain.strategies import Preprocessing, RemoveEmoticons, TextToLower, RemovePronouns

strategies = [RemoveEmoticons(), TextToLower(), RemovePronouns()]
message = "Segun ella Los emoticones <3 :) :D ;) son muy usados y esta rosa tambien @}->--"
cleaned = Preprocessing().clean(data=message, clean_strategies=strategies)

print(cleaned)

# salida: segun los emoticones son muy usados y esta rosa tambien
```


## Testing
¿Eres tester? ¿quieres automatizar pruebas? o ¿simplemente aprender del open source y de las pruebas? Aventurate ya y ayudame a mejorar este proyecto!
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

o tambien el comando:

```
python -m pytest
```

Esto ejecutará de forma automática todas las pruebas programadas e indicará si algún test falló.


## Reportar un bug
Si encuentras algún problema (por muy mínimo que sea) reportalo [aquí](https://github.com/jfreddypuentes/spanlp/issues/new). Solo necesitarás poner título y describir la falla y aportará un montón a que este proyecto mejore su calidad.


## Contacto
¿Alguna duda? escribeme por email:  [jfredypuentes@gmail.com](mailto:jfredypuentes@gmail.com)

Cuentame en ([@jfreddypuentes](https://twitter.com/jfreddypuentes)) ¿qué te parece está librería? ¿cómo la estás usando? ¿Qué le mejorarías?

<br>

## Contribuidorxs
* [@vivianamarquez](https://github.com/vivianamarquez) en Github, [@vivmarquez](https://twitter.com/vivmarquez) en Twitter (Data Scientist) - Contribución al diseño y funcionalidades de la librería.
* [@normacalamartinez](https://github.com/normacalamartinez) en Github (BI Developer) - Contribución al dataset de vulgaridades por país de habla hispana.

<br>


**Hecho con ❤️️ de Colombia para el mundo.**
