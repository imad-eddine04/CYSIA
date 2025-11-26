# importer pandas avec l’alias pd
import pandas as pd

data = [(1, 2.0, "Hello"), (2, 3.0, "World")] # chaque élément du tableau représente une ligne dans le dataframe
df = pd.DataFrame(data) # méthode 1 : avec index et nom de colonnes par défaut
print(df)
# affiche 0 1 2 1 1 2.0 Hello 2 2 3.0 World
df1 = pd.DataFrame(data, index=["premier", "second"], columns=["A", "B", "C"]) # méthode 2 : avec une liste d’index et une liste de colonnes
print(df1)
# affiche A B C premier 1 2.0 Hello second 2 3.0 World


d = {"one": [1.0, 2.0, 3.0], "two": [4.0, 3.0, 2.0]}
df = pd.DataFrame(d) # méthode 1 : avec index par défaut. Les clés du dictionnaire
représentent les noms des colonnes
print(df)
# affiche
one two
0 1.0 4.0
1 2.0 3.0
2 3.0 2.0
df1 = pd.DataFrame(d, index=["a", "b", "c"]) # méthode 2 : avec une liste d’index
print(df1)
# affiche one two a 1.0 4.0 b 2.0 3.0 c 3.0 2.0