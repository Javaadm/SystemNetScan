#ifndef VECTOR_H__
#define VECTOR_H__

#include <stdlib.h>
#include <string.h>

typedef struct vector_ {
    int** data;
    int size;
    int count;
} vector;


void vector_init(vector *v)
{
    v->data = NULL;
    v->size = 0;
    v->count = 0;
}

int vector_count(vector *v)
{
    return v->count;
}

void vector_add(vector *v, int *e)
{
    if (v->size == 0) {
        v->size = 10;
        v->data = malloc(sizeof(int*) * v->size);
        memset(v->data, '\0', sizeof(int*) * v->size);
    }

    // condition to increase v->data:
    // last slot exhausted
    if (v->size == v->count) {
        v->size *= 2;
        v->data = realloc(v->data, sizeof(int*) * v->size);
    }

    v->data[v->count] = e;
    v->count++;
}

void vector_set(vector *v, int index, int *e)
{
    if (index >= v->count) {
        printf("Error! Setting value out of vector range!");
        return;
    }

    v->data[index] = e;
}

int *vector_get(vector *v, int index)
{
    if (index >= v->count) {
        printf("Error! Trying to get value out of vector range!");
        return NULL;
    }

    return v->data[index];
}

void vector_delete(vector *v, int index)
{
    if (index >= v->count) {
        return;
    }

    int i, j;
    int **newarr = (int**)malloc(sizeof(int*) * (v->size - 1));
    for (i = 0, j = 0; i < v->size; i++) {
        if (i != index) {
            newarr[j] = v->data[i];
            j++;
        }
    }

    free(v->data);

    v->data = newarr;
    v->count--;
}

void vector_pop(vector *v)
{
    v->count--;
}

void vector_free(vector *v)
{
    free(v->data);
}

#endif
