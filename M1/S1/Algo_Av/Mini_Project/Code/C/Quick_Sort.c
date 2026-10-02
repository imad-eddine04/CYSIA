#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <string.h>

long long comparisons = 0;
long long movements = 0;
long long recursive_calls = 0;

double elapsed_ms(LARGE_INTEGER s, LARGE_INTEGER e, LARGE_INTEGER f) {
    return (double)(e.QuadPart - s.QuadPart) * 1000.0 / f.QuadPart;
}

int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        comparisons++;
        if (arr[j] <= pivot) {
            i++;
            int tmp = arr[i];
            arr[i] = arr[j];
            arr[j] = tmp;
            movements += 3;
        }
    }

    int tmp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = tmp;
    movements += 3;

    return i + 1;
}

void quickSort(int arr[], int low, int high) {
    recursive_calls++;
    if (low < high) {
        int p = partition(arr, low, high);
        quickSort(arr, low, p - 1);
        quickSort(arr, p + 1, high);
    }
}

void run_quick(int n, const char *type, int run_id) {
    comparisons = movements = recursive_calls = 0;

    int *arr = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) {
        if (strcmp(type, "random") == 0) arr[i] = rand() % n;
        else if (strcmp(type, "sorted") == 0) arr[i] = i;
        else arr[i] = n - i - 1;
    }

    LARGE_INTEGER f, s, e;
    QueryPerformanceFrequency(&f);
    QueryPerformanceCounter(&s);

    quickSort(arr, 0, n - 1);

    QueryPerformanceCounter(&e);

    printf("QuickSort,%s,%d,%d,%.6f,%lld,%lld,%lld\n",
           type, n, run_id, elapsed_ms(s, e, f),
           comparisons, movements, recursive_calls);

    free(arr);
}

int main() {
    srand(GetTickCount());

    printf("algorithm,data_type,n,run_id,time_ms,comparisons,swaps_or_movements,recursive_calls\n");

    int sizes[] = {100, 500, 1000, 5000, 10000, 50000};
    const char *types[] = {"random", "sorted", "reversed"};

    for (int i = 0; i < 6; i++)
        for (int t = 0; t < 3; t++)
            for (int r = 1; r <= 3; r++)
                run_quick(sizes[i], types[t], r);

    return 0;
}
