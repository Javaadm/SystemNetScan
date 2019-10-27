#include <stdio.h>

void* testF(int height, int width, int* image, int*result) {
    int *arr = (int*)image;
    arr[0] = height;
    arr[1] = width;
    printf("%d, %d\n", height, width);
    // int *a = (int*)&arr[0], *b = (int*)&arr[1], *c = (int*)&arr[2];
    printf("%d, %d, %d\n",arr[0], arr[1], arr[2]);
    return arr;
}
