import hashlib

# Ouverture des fichiers en mode binaire
with open(r'shattered-1.pdf', "rb") as f1, open(r'shattered-2.pdf', "rb") as f2:
    # Calcul du hash pour le premier fichier
    sha1_1 = hashlib.sha1()
    while True:
        data = f1.read(4096)
        if not data:
            break
        sha1_1.update(data)
    hash1 = sha1_1.hexdigest()

    # Calcul du hash pour le deuxième fichier
    sha1_2 = hashlib.sha1()
    while True:
        data = f2.read(4096)
        if not data:
            break
        sha1_2.update(data)
    hash2 = sha1_2.hexdigest()

# Affichage des hashs
print(f"Hash du fichier 1 : {hash1}")
print(f"Hash du fichier 2 : {hash2}")
