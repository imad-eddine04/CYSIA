#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#define pp printf("\n-------------------------------------------------------------------------------------------\n");

int comparisons = 0, mouvements = 0, recursiveTas = 0;


void echange(int *a, int *b) {
	int tmp = *a;
	*a = *b;
	*b = tmp;
}

void per(int t[], int n, int i) {
	int g, d, p, max, tmp;
	g = i*2 + 1;
	d = i*2 + 2;
	max = i;
	if(g < n && t[g] > t[max]) max = g;
	comparisons+=2;
	if(d < n && t[d] > t[max]) max = d;
	comparisons+=2;
	if(max != i){
		echange(&t[max], &t[i]);
		comparisons++;
		mouvements++;
		recursiveTas++;
		per(t, n, max);
	}
}

void tas(int t[], int n) {
	int i;
	for(i=n/2 - 1; i>=0; i--) {
		comparisons++;
		per(t, n, i);
	}
	comparisons++;
}

void tri(int t[], int n) {
	int i;
    for(i=n-1; i>0; i--) {
    	printf("%d ", t[0]);
        echange(&t[0], &t[i]);
        per(t, i, 0);
    }
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
	printf("Avant tas:\n");
	aff(t, n);
	pp
	printf("Apres tas:\n");
	QueryPerformanceFrequency(&f);
	QueryPerformanceCounter(&st);
	tas(t, n);
	QueryPerformanceCounter(&et);
	aff(t, n);
	pp
	printf("Apres tri:\n");
	QueryPerformanceCounter(&s);
	tri(t, n);
	QueryPerformanceCounter(&e);
	pp
	printf("\nTemp de tas: %.20f\n", (double)(et.QuadPart - st.QuadPart) / f.QuadPart);
	printf("Temp de tri: %.20f\n", (double)(e.QuadPart - s.QuadPart) / f.QuadPart);
	printf("Nombre de comparaisons de Tas: %d\nNombre de mouvements de Tas: %d\nNombre d appels recursive de Tas: %d\n",
		comparisons, mouvements, recursiveTas
	);
	comparisons = 0;
	mouvements = 0;
	recursiveTas = 0;
	pp
}

void inversees(int n) {
	int i;
	int t[n];
	LARGE_INTEGER f, s, e, st, et;
	for(i=0; i<n; i++) {
		t[i] = i;
	}
	printf("Avant tas:\n");
	aff(t, n);
	pp
	printf("Apres tas:\n");
	QueryPerformanceFrequency(&f);
	QueryPerformanceCounter(&st);
	tas(t, n);
	QueryPerformanceCounter(&et);
	aff(t, n);
	pp
	printf("Apres tri:\n");
	QueryPerformanceCounter(&s);
	tri(t, n);
	QueryPerformanceCounter(&e);
	pp
	printf("\nTemp de tas: %.20f\n", (double)(et.QuadPart - st.QuadPart) / f.QuadPart);
	printf("Temp de tri: %.20f\n", (double)(e.QuadPart - s.QuadPart) / f.QuadPart);
	printf("Nombre de comparaisons de Tas: %d\nNombre de mouvements de Tas: %d\nNombre d appels recursive de Tas: %d\n",
		comparisons, mouvements, recursiveTas
	);
	comparisons = 0;
	mouvements = 0;
	recursiveTas = 0;
	pp
}

void triees(int n) {
	int i;
	int t[n];
	LARGE_INTEGER f, s, e;
	for(i=0; i<n; i++) {
		t[i] = n - i;
	}
	printf("Avant tas:\n");
	aff(t, n);
	pp
	printf("Apres tas:\n");
	QueryPerformanceFrequency(&f);
	QueryPerformanceCounter(&s);
	tas(t, n);
	QueryPerformanceCounter(&e);
	aff(t, n);
	printf("\nTemp de tas: %.20f\n", (double)(e.QuadPart - s.QuadPart) / f.QuadPart);
	printf("Nombre de comparaisons de Tas: %d\nNombre de mouvements de Tas: %d\nNombre d appels recursive de Tas: %d\n",
		comparisons, mouvements, recursiveTas
	);
	comparisons = 0;
	mouvements = 0;
	recursiveTas = 0;
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
