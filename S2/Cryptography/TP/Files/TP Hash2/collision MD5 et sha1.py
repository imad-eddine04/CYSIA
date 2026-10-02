import hashlib

# Générer une collision pour MD5

    # Deux chaînes différentes ayant la même valeur de hachage MD5
s1 = 'd131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70'
s2 = 'd131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70'

    # Calculer le hachage MD5 de s1 et s2import hashlib

#
# # Convertir les chaînes hexadécimales en octets
b1 = bytes.fromhex(s1)
b2 = bytes.fromhex(s2)
#
# # Calculer le hachage MD5 des octets
h1 = hashlib.md5(b1).hexdigest()
h2 = hashlib.md5(b2).hexdigest()
#
# # Comparer les deux hachages MD5
if h1 == h2:
    print("Les deux chaînes ont le même hachage MD5 :", h1)
else:
    print("Les deux chaînes n'ont pas le même hachage MD5.")
# Afficher les résultats
print("MD5 collision:")
print(f"  s1 : {s1}")
print(f"  h1 : {h1}")
print(f"  s2 : {s2}")
print(f"  h2 : {h2}")