from collections import Counter
from string import ascii_uppercase
import matplotlib.pyplot as plt

# Nettoyage du texte
def nettoyer_texte(texte):
    """Garde uniquement les lettres majuscules A-Z"""
    return ''.join([c.upper() for c in texte if c.isalpha()])

# Lecture + nettoyage d’un fichier texte
def lire_fichier_texte(path):
    with open(path, 'r', encoding='utf-8') as f:
        return nettoyer_texte(f.read())

# Indice de coïncidence
def indice_coincidence(texte):
    N = len(texte)
    freqs = Counter(texte)
    if N <= 1:
        return 0
    return sum(f * (f - 1) for f in freqs.values()) / (N * (N - 1))

# Estimation naïve de la longueur de la clé
def estimer_longueur_cle(texte, max_longueur=20):
    ic_moyens = {}
    for key_len in range(1, max_longueur + 1):
        blocs = ['' for _ in range(key_len)]
        for i, c in enumerate(texte):
            blocs[i % key_len] += c
        moyenne = sum(indice_coincidence(b) for b in blocs) / key_len
        ic_moyens[key_len] = moyenne
    return max(ic_moyens, key=ic_moyens.get)

# Décalage dominant supposant 'E' comme lettre la plus fréquente
def decalage_frequent(texte):
    freqs = Counter(texte)
    lettre_freq = freqs.most_common(1)[0][0]
    return (ord(lettre_freq) - ord('E')) % 26

# Retrouver la clé
def retrouver_cle(texte, longueur_cle):
    blocs = ['' for _ in range(longueur_cle)]
    for i, c in enumerate(texte):
        blocs[i % longueur_cle] += c
    cle = ''
    for bloc in blocs:
        d = decalage_frequent(bloc)
        cle += ascii_uppercase[d]
    return cle

# Déchiffrement Vigenère
def dechiffrer_vigenere(texte, cle):
    texte_dechiffre = ''
    for i, c in enumerate(texte):
        t = ord(c) - ord('A')
        k = ord(cle[i % len(cle)]) - ord('A')
        texte_dechiffre += chr((t - k + 26) % 26 + ord('A'))
    return texte_dechiffre


def tracer_frequence_lettres(texte, titre="Fréquences des lettres (texte chiffré)"):
    # Nettoyer le texte
    texte = nettoyer_texte(texte)

    # Compter les fréquences
    compteur = Counter(texte)
    lettres = list(ascii_uppercase)
    frequences = [compteur[c] for c in lettres]

    # Tracer l’histogramme
    plt.figure(figsize=(12, 6))
    bars = plt.bar(lettres, frequences, color='cornflowerblue', edgecolor='black')

    # Ajouter les valeurs au-dessus de chaque barre
    for bar, freq in zip(bars, frequences):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1, str(freq),
                 ha='center', va='bottom', fontsize=8)

    plt.title(titre)
    plt.xlabel("Lettre")
    plt.ylabel("Nombre d'occurrences")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.xticks(lettres)
    plt.tight_layout()
    plt.show()


# -------------------
# Programme principal
# -------------------
if __name__ == "__main__":
    chemin_fichier = r"C:\Users\benar\Desktop\message_chiffre.txt"

    texte_chiffre = lire_fichier_texte('message_chiffre.txt')

    # Estimer la longueur de la clé
    longueur = estimer_longueur_cle(texte_chiffre, max_longueur=20)

    # Trouver la clé
    cle_trouvee = retrouver_cle(texte_chiffre, longueur)

    # Déchiffrer
    texte_dechiffre = dechiffrer_vigenere(texte_chiffre, cle_trouvee)

    # Tracer histogramme
    tracer_frequence_lettres(texte_chiffre, "Fréquence des lettres (texte chiffré)")

    # Affichage
    print(" Longueur de clé estimée :", longueur)
    print(" Clé trouvée :", cle_trouvee)
    print(" Début du texte déchiffré :")
    print(texte_dechiffre[:500])
