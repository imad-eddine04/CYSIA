def decrypter_cesar_force_brute(texte_chiffre):

    resultats = {}


    for decalage in range(1, 27):
        texte_dechiffre = ""


        for char in texte_chiffre:
            if 'A' <= char <= 'Z':

                char_num = ord(char) - ord('A')


                nouveau_num = (char_num - decalage) % 26

                nouveau_char = chr(nouveau_num + ord('A'))
                texte_dechiffre += nouveau_char
            else:

                texte_dechiffre += char


        resultats[decalage] = texte_dechiffre

    return resultats



TEXTE_CHIFFRE = "RFYM HWDUYT"


decalages_possibles = decrypter_cesar_force_brute(TEXTE_CHIFFRE)


print(f"--- 26 DÉCALAGES POSSIBLES POUR : {TEXTE_CHIFFRE} ---")
print("-" * 50)


for decalage, texte in decalages_possibles.items():

    if decalage == 23:
        print(f"Décalage {decalage:02}: {texte} <-- SOLUTION PROBABLE")
    else:
        print(f"Décalage {decalage:02}: {texte}")

print("-" * 50)