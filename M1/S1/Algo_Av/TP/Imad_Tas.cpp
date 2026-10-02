#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void echanger(int arr[], int i, int j) {
    int temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}

void tasMax(int arr[], int n, int i) {
    int plusGrand = i;
    int gauche = 2 * i + 1;
    int droite = 2 * i + 2;

    if (gauche < n && arr[gauche] > arr[plusGrand])
        plusGrand = gauche;
    if (droite < n && arr[droite] > arr[plusGrand])
        plusGrand = droite;

    if (plusGrand != i) {
        echanger(arr, i, plusGrand);
        tasMax(arr, n, plusGrand);
    }
}

void heapSort(int arr[], int n) {
    for (int i = n / 2 - 1; i >= 0; i--)
        tasMax(arr, n, i);

    for (int i = n - 1; i > 0; i--) {
        echanger(arr, 0, i);
        tasMax(arr, i, 0);
    }
}

void afficher(int arr[], int n) {
    for (int i = 0; i < n; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

int main() {
    int n;
    printf("Entrez le nombre d'elements : ");
    scanf("%d", &n);

    int arr[n];
    srand(time(NULL));

    for (int i = 0; i < n; i++)
        arr[i] = rand() % 100;

    printf("Tableau avant tri :\n");
    afficher(arr, n);

    clock_t start = clock();
    heapSort(arr, n);
    clock_t end = clock();

    double temps = ((double)(end - start) / CLOCKS_PER_SEC) * 1000.0;

    printf("Tableau apres tri par tas :\n");
    afficher(arr, n);

    printf("Temps d'execution : %.4f ms\n", temps);

    return 0;
}
