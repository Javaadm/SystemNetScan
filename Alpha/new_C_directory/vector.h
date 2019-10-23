#ifndef VECTOR_H__
#define VECTOR_H__

#include <stdlib.h>
#include <string.h>

typedef struct vector_ {
    int** data;
    int size;
    int count;
    int char_size;
} vector;

void vector_init(vector *v, int cs)
{
    v->data = NULL;
    v->size = 0;
    v->count = 0;
    v->char_size = cs;
}

int vector_count(vector *v)
{
    return v->count;
}

void vector_add(vector *v, void *e)
{
    if (v->size == 0) {
        v->size = 10;
        v->data = malloc(sizeof(void*) * v->size);
        memset(v->data, '\0', v->char_size * v->size);
    }

    // condition to increase v->data:
    // last slot exhausted
    if (v->size == v->count) {
        v->size *= 2;
        v->data = realloc(v->data, sizeof(void*) * v->size);
    }

    v->data[v->count] = e;
    v->count++;
}

void vector_set(vector *v, int index, void *e)
{
    if (index >= v->count) {
        return;
    }

    v->data[index] = e;
}

void *vector_get(vector *v, int index)
{
    if (index >= v->count) {
        return NULL;
    }

    return v->data[index];
}

void vector_delete(vector *v, int index)
{
    if (index >= v->count) {
        return;
    }

    v->data[index] = NULL;

    int i, j;
    void **newarr = (void**)malloc(sizeof(void*) * v->count * 2);
    for (i = 0, j = 0; i < v->count; i++) {
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
