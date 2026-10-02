#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#define pp printf("\n-------------------------------------------------------------------------------------------\n");

int comparisons = 0, recursiveABR = 0;

typedef struct abr{
	int val;
	struct abr *g, *d;
} abr;

void insert(abr **t, int e) {
	if(*t == NULL) {
		comparisons++;
		*t = malloc(sizeof(abr));
		(*t)->val = e;
		(*t)->g = NULL;
		(*t)->d = NULL;
	}
	else {
		comparisons++;
		recursiveABR++;
		if((*t)->val > e) {
			insert(&(*t)->g, e);
		}
		else {
			insert(&(*t)->d, e);
		}
	}
}

void afficher(abr *t) {
	if(t != NULL) {
		afficher(t->g);
		printf("%d ", t->val);
		afficher(t->d);
	}
}

void aff(int t[], int n) {
	int i;
	for(i=0; i<n; i++) {
		printf("%d ", t[i]);
	}
}

void aleatoire(int n) {
	abr *tete = NULL;
	int i;
	int t[n];
	LARGE_INTEGER f, s, e;
	for(i=0; i<n; i++) {
		t[i] = rand() % n;
	}
	printf("Avant ABR:\n");
	aff(t, n);
	pp
	printf("Apres ABR:\n");
	QueryPerformanceFrequency(&f);
	QueryPerformanceCounter(&s);
	for(i=0; i<n; i++) {
		insert(&tete, t[i]);
	}
	QueryPerformanceCounter(&e);
	afficher(tete);
	pp
	printf("Temp de creation ABR: %.20f\n", (double)(e.QuadPart - s.QuadPart) / f.QuadPart);
	printf("Nombre de comparaisons de ABR: %d\nNombre d appels recursive de ABR: %d\n",
		comparisons, recursiveABR
	);
	comparisons = 0;
	recursiveABR = 0;
	pp
}

void triees(int n) {
	abr *tete = NULL;
	int i;
	int t[n];
	LARGE_INTEGER f, s, e;
	for(i=0; i<n; i++) {
		t[i] = i;
	}
	printf("Avant ABR:\n");
	aff(t, n);
	pp
	printf("Apres ABR:\n");
	QueryPerformanceFrequency(&f);
	QueryPerformanceCounter(&s);
	for(i=0; i<n; i++) {
		insert(&tete, t[i]);
	}
	QueryPerformanceCounter(&e);
	afficher(tete);
	pp
	printf("Temp de creation ABR: %.20f\n", (double)(e.QuadPart - s.QuadPart) / f.QuadPart);
	printf("Nombre de comparaisons de ABR: %d\nNombre d appels recursive de ABR: %d\n",
		comparisons, recursiveABR
	);
	comparisons = 0;
	recursiveABR = 0;
	pp
}

void inversees(int n) {
	abr *tete = NULL;
	int i;
	int t[n];
	LARGE_INTEGER f, s, e;
	for(i=0; i<n; i++) {
		t[i] = n-i-1;
	}
	printf("Avant ABR:\n");
	aff(t, n);
	pp
	printf("Apres ABR:\n");
	QueryPerformanceFrequency(&f);
	QueryPerformanceCounter(&s);
	for(i=0; i<n; i++) {
		insert(&tete, t[i]);
	}
	QueryPerformanceCounter(&e);
	afficher(tete);
	pp
	printf("Temp de creation ABR: %.20f\n", (double)(e.QuadPart - s.QuadPart) / f.QuadPart);
	printf("Nombre de comparaisons de ABR: %d\nNombre d appels recursive de ABR: %d\n",
		comparisons, recursiveABR
	);
	comparisons = 0;
	recursiveABR = 0;
	pp
}

void sw_case(int n) {
	printf("Choisissez le type de donnees\n1:Aleatoires		2:Triees		3:Inversees\n");
	switch(getch()) {
		case '1':
			aleatoire(n);
			break;
		case '2':
			triees(n);
			break;
		case '3':
			inversees(n);
			break;
		default:
			printf("Erreur!\n");
			break;
	}
}

int main() {
	int n;
	do{
		printf("Choisissez la taille de tableau\n1:100		2:500		3:1000		4:5000		5:10000		6:50000		9:Cls		0:Exit\n");
		switch(getch()) {
			case '1': n = 100; sw_case(n); break;
			case '2': n = 500; sw_case(n); break;
			case '3': n = 1000; sw_case(n); break;
			case '4': n = 5000; sw_case(n); break;
			case '5': n = 10000; sw_case(n); break;
			case '6': n = 50000; sw_case(n); break;
			case '9': system("cls");break;
			case '0':
				printf("Fin \1\n");
				exit(0);
				break;
			default:
				printf("Erreur!\n");
				break;
		}
	}while(1);
	return 0;
}