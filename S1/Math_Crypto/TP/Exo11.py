def analyser_chaine(chaine):
    nombre_total = len(chaine)
    resultats = {}

    for index, caractere in enumerate(chaine):
        if caractere in resultats:
            resultats[caractere]['compte'] += 1
            resultats[caractere]['emplacements'].append(index)
        else:
            resultats[caractere] = {
                'compte': 1,
                'emplacements': [index]
            }

    print(f"Analyse de la chaîne : '{chaine}'")

    print(f"NOMBRE TOTAL DE CARACTÈRES : {nombre_total}\n")

    print("Détail par caractère unique :")
    for caractere, data in resultats.items():
        compte = data['compte']
        emplacements = ', '.join(map(str, data['emplacements']))

        print(f"  - Le caractère {caractere!r} répeter {compte}")

    return nombre_total, resultats


chaine_utilisateur = input("Veuillez entrer une chaîne de caractères : ")

analyser_chaine(chaine_utilisateur)