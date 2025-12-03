#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct noeud {
    int valeur;
    struct noeud *gauche;
    struct noeud *droite;
    int hauteur;
} Noeud;

int hauteur(Noeud* N) {
    if (N == NULL)
        return 0;
    return N->hauteur;
}

int max(int a, int b) {
    return (a > b) ? a : b;
}

int getFacteurEquilibre(Noeud* N) {
    if (N == NULL)
        return 0;
    return hauteur(N->gauche) - hauteur(N->droite);
}

Noeud* creerNoeud(int valeur) {
    Noeud* nouveau = (Noeud*) malloc(sizeof(Noeud));
    if (nouveau == NULL) {
        perror("Erreur d'allocation memoire");
        exit(EXIT_FAILURE);
    }
    nouveau->valeur = valeur;
    nouveau->gauche = NULL;
    nouveau->droite = NULL;
    nouveau->hauteur = 1;
    return nouveau;
}

Noeud* rotationDroite(Noeud* y) {
    Noeud* x = y->gauche;
    Noeud* T2 = x->droite;

    x->droite = y;
    y->gauche = T2;

    y->hauteur = 1 + max(hauteur(y->gauche), hauteur(y->droite));
    x->hauteur = 1 + max(hauteur(x->gauche), hauteur(x->droite));

    return x;
}

Noeud* rotationGauche(Noeud* x) {
    Noeud* y = x->droite;
    Noeud* T2 = y->gauche;

    y->gauche = x;
    x->droite = T2;

    x->hauteur = 1 + max(hauteur(x->gauche), hauteur(x->droite));
    y->hauteur = 1 + max(hauteur(y->gauche), hauteur(y->droite));

    return y;
}

Noeud* insererAVL(Noeud* racine, int valeur) {
    if (racine == NULL)
        return creerNoeud(valeur);

    if (valeur < racine->valeur)
        racine->gauche = insererAVL(racine->gauche, valeur);
    else if (valeur > racine->valeur)
        racine->droite = insererAVL(racine->droite, valeur);
    else
        return racine;

    racine->hauteur = 1 + max(hauteur(racine->gauche), hauteur(racine->droite));

    int equilibre = getFacteurEquilibre(racine);

    if (equilibre > 1 && valeur < racine->gauche->valeur)
        return rotationDroite(racine);

    if (equilibre < -1 && valeur > racine->droite->valeur)
        return rotationGauche(racine);

    if (equilibre > 1 && valeur > racine->gauche->valeur) {
        racine->gauche = rotationGauche(racine->gauche);
        return rotationDroite(racine);
    }

    if (equilibre < -1 && valeur < racine->droite->valeur) {
        racine->droite = rotationDroite(racine->droite);
        return rotationGauche(racine);
    }

    return racine;
}

// Fonction de recherche rapide
Noeud* rechercherNoeud(Noeud* racine, int valeur) {
    if (racine == NULL || racine->valeur == valeur)
        return racine;

    if (valeur < racine->valeur)
        return rechercherNoeud(racine->gauche, valeur);

    return rechercherNoeud(racine->droite, valeur);
}

Noeud* minValeurNoeud(Noeud* noeud) {
    Noeud* courant = noeud;
    while (courant->gauche != NULL)
        courant = courant->gauche;
    return courant;
}

Noeud* supprimerNoeud(Noeud* racine, int valeur) {
    if (racine == NULL)
        return racine;

    if (valeur < racine->valeur)
        racine->gauche = supprimerNoeud(racine->gauche, valeur);

    else if (valeur > racine->valeur)
        racine->droite = supprimerNoeud(racine->droite, valeur);

    else {
        if ((racine->gauche == NULL) || (racine->droite == NULL)) {
            Noeud* temp = racine->gauche ? racine->gauche : racine->droite;

            if (temp == NULL) {
                temp = racine;
                racine = NULL;
            }
            else
                *racine = *temp;

            free(temp);
        }
        else {
            Noeud* temp = minValeurNoeud(racine->droite);
            racine->valeur = temp->valeur;
            racine->droite = supprimerNoeud(racine->droite, temp->valeur);
        }
    }

    if (racine == NULL)
        return racine;

    racine->hauteur = 1 + max(hauteur(racine->gauche), hauteur(racine->droite));

    int equilibre = getFacteurEquilibre(racine);

    if (equilibre > 1 && getFacteurEquilibre(racine->gauche) >= 0)
        return rotationDroite(racine);

    if (equilibre > 1 && getFacteurEquilibre(racine->gauche) < 0) {
        racine->gauche = rotationGauche(racine->gauche);
        return rotationDroite(racine);
    }

    if (equilibre < -1 && getFacteurEquilibre(racine->droite) <= 0)
        return rotationGauche(racine);

    if (equilibre < -1 && getFacteurEquilibre(racine->droite) > 0) {
        racine->droite = rotationDroite(racine->droite);
        return rotationGauche(racine);
    }

    return racine;
}

void parcoursInfixe(Noeud* racine) {
    if (racine != NULL) {
        parcoursInfixe(racine->gauche);
        printf("%d ", racine->valeur);
        parcoursInfixe(racine->droite);
    }
}

void libererArbre(Noeud* racine) {
    if (racine != NULL) {
        libererArbre(racine->gauche);
        libererArbre(racine->droite);
        free(racine);
    }
}

int main() {
    int n;
    int *tableau = NULL;
    int valeurASupprimer;

    srand(time(NULL));

    printf("Entrez la taille du tableau : ");
    if (scanf("%d", &n) != 1 || n <= 0) {
        printf("Erreur : Le nombre d'elements doit etre un entier positif.\n");
        return 1;
    }

    tableau = (int*) malloc(n * sizeof(int));
    if (tableau == NULL) {
        perror("Erreur d'allocation memoire");
        return 1;
    }

    printf("Generation de %d elements :\n", n);
    for (int i = 0; i < n; i++) {
        tableau[i] = rand() % (2 * n);
        printf("%d ", tableau[i]);
    }
    printf("\n");

    Noeud* racine = NULL;
    clock_t debut = clock();

    for (int i = 0; i < n; i++)
        racine = insererAVL(racine, tableau[i]);

    clock_t fin = clock();

    printf("\nArbre trie (Infixe) : ");
    parcoursInfixe(racine);
    printf("\n");

    double temps_execution = (double)(fin - debut) / CLOCKS_PER_SEC;
    printf("\nTemps d'execution pour la construction de l'AVL : %.6f secondes\n", temps_execution);

    printf("\n----------------------------------\n");
    printf("Entrez une valeur a supprimer de l'arbre : ");
    if (scanf("%d", &valeurASupprimer) != 1) {
        printf("Erreur de lecture de la valeur.\n");
    } else {
        printf("Tentative de suppression de la valeur : %d\n", valeurASupprimer);

        if (rechercherNoeud(racine, valeurASupprimer) == NULL) {
            printf("Erreur : Le nombre %d n'existe pas dans l'arbre.\n", valeurASupprimer);
        } else {
            racine = supprimerNoeud(racine, valeurASupprimer);

            printf("✅ Suppression reussie.\n");
            printf("\nArbre apres suppression (Infixe) : ");
            parcoursInfixe(racine);
            printf("\n");
        }
    }
    printf("----------------------------------\n");

    libererArbre(racine);
    free(tableau);

    return 0;
}