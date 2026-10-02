#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <windows.h>
#define pp printf("\n-------------------------------------------------------------------------------------------\n");

int comparisons = 0, mouvements = 0;

void echange(int *a, int *b) {
	int tmp = *a;
	*a = *b;
	*b = tmp;
	mouvements++;
}

void tri_bulles(int t[], int n) {
	bool per;
	int i;
	do{
		per = false;
		for(i=0; i<n-1; i++) {
			comparisons++;
			if(t[i] > t[i+1]) {
				echange(&t[i], &t[i+1]);
				per = true;
			}
		}
		comparisons++;
	}while(per);
}

void aff(int t[], int n) {
	int i;
	for(i=0; i<n; i++) {
		printf("%d ", t[i]);
	}
}

void aleatoire(int n) {
	int i;
	int t[n];
	LARGE_INTEGER f, s, e, st, et;
	for(i=0; i<n; i++) {
		t[i] = rand() % n;
	}
	printf("Avant tri:\n");
	aff(t, n);
	pp
	printf("Apres tri:\n");
	QueryPerformanceFrequency(&f);
	QueryPerformanceCounter(&s);
	tri_bulles(t, n);
	QueryPerformanceCounter(&e);
	aff(t, n);
	pp
	printf("Temp de tri: %.20f\n", (double)(e.QuadPart - s.QuadPart) / f.QuadPart);
	printf("Nombre de comparaisons de tri: %d\nNombre mouvements de tri: %d\n",
		comparisons, mouvements
	);
	comparisons = 0;
	mouvements = 0;
	pp
}

void inversees(int n) {
	int i;
	int t[n];
	LARGE_INTEGER f, s, e, st, et;
	for(i=0; i<n; i++) {
		t[i] = n-i-1;
	}
	printf("Avant tri:\n");
	aff(t, n);
	pp
	printf("Apres tri:\n");
	QueryPerformanceFrequency(&f);
	QueryPerformanceCounter(&s);
	tri_bulles(t, n);
	QueryPerformanceCounter(&e);
	aff(t, n);
	pp
	printf("Temp de tri: %.20f\n", (double)(e.QuadPart - s.QuadPart) / f.QuadPart);
	printf("Nombre de comparaisons de tri: %d\nNombre mouvements de tri: %d\n",
		comparisons, mouvements
	);
	comparisons = 0;
	mouvements = 0;
	pp
}

void triees(int n) {
	int i;
	int t[n];
	LARGE_INTEGER f, s, e, st, et;
	for(i=0; i<n; i++) {
		t[i] = i;
	}
	printf("Avant tri:\n");
	aff(t, n);
	pp
	printf("Apres tri:\n");
	QueryPerformanceFrequency(&f);
	QueryPerformanceCounter(&s);
	tri_bulles(t, n);
	QueryPerformanceCounter(&e);
	aff(t, n);
	pp
	printf("Temp de tri: %.20f\n", (double)(e.QuadPart - s.QuadPart) / f.QuadPart);
	printf("Nombre de comparaisons de tri: %d\nNombre mouvements de tri: %d\n",
		comparisons, mouvements
	);
	comparisons = 0;
	mouvements = 0;
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
