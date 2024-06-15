import csv

'''
     FUNCIONALIDAD
     -------------
     Este programa se encarga de agregar las malas palabras de ambos generos con solo leer un archivo que contenga el ejemplo de uno.


     Es decir, si en un archivo aparece la palabra 'linda', el programa agrega la palabra 'lindo' automaticamente. Y asi con todas las que terminen en 'o' o en 'a'.

     Asi no es necesario escribir a mano el mismo insulto dos veces.

     OBSERVACION
     -----------
     Si hay palabras que terminan en 'o' o en 'a' pero su opuesto no compone una palabra, tiene que eliminarse del archivo [pais].txt
'''


# Lee el archivo que entra como parametro y retorna todas las palabras que tienen genero pero con el genero opuesto.
# Ejemplo: Ante ['feo', 'tarado'] devuelve ['fea', 'tarada']
def read_csv(path):
     res = []
     with open(path, 'r') as csv_file:
          reader = csv.reader(csv_file, delimiter='\n')

          listaPalabras = list(reader)

          for p in listaPalabras:
               word = p[0]
               if word[len(word)-1:len(word)] == 'a':
                    res.append(word[:len(word)-1]+'o')
               elif word[len(word)-1:len(word)] == 'o':
                    res.append(word[:len(word)-1]+'a')

          csv_file.close()
     write_csv(path, res)

# Escribe las palabras.
def write_csv(path, wordList):
     with open(path, 'a', newline='\n') as csv_file:
          for i in wordList:
               csv_file.write(i)
               csv_file.write('\n')
          csv_file.close()