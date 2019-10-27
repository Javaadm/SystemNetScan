//
// Created by mikhail on 19.10.2019.
//

#ifndef NEW_C_DIRECTORY_PVECTOR_H
#define NEW_C_DIRECTORY_PVECTOR_H
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include "vector.h"

typedef struct Point
{
    int x, y;
} Point;

Point get_Point(int x, int y)
{
    Point ret;
    ret.x = x;
    ret.y = y;
    return ret;
}

void Point_print(Point p)
{
    printf("%d, %d\n", p.x, p.y);
}

typedef struct stack{
    int size;
    int count;
    Point* data;
} pvector;

void pvector_init(pvector* s)
{
    s->size = 0;
    s->data = NULL;
    s->count = 0;
}


void pvector_push(pvector *v, Point e) {
    if (v->size == 0) {
        v->size = 10;
        v->data = malloc(sizeof(Point) * v->size);
        memset(v->data, '\0', sizeof(Point) * v->size);
        // printf("\n%d", sizeof((*v).data));
    }

    // condition to increase v->data:
    // last slot exhausted
    if (v->size == v->count) {
        v->size *= 2;
        v->data = realloc(v->data, sizeof(Point) * v->size);
    }

    v->data[v->count] = e;
    v->count++;
}

int pvector_count(pvector*s)
{
    return s->count;
}

void pvector_pop(pvector* s)
{
    s->count--;
}

Point pvector_top(pvector* s)
{
    return s->data[s->count-1];
}

Point pvector_get(pvector *s, int index)
{
    return s->data[index];
}

// vector *pvector_get_vector(pvector* s)
// {
//     vector ret;
//     vector_init(&ret);
//     for(int i = 0; i <= s->count;i++)
//         vector_add(&ret, s->data[i]);
// }

int pvector_not_empty(pvector *v)
{
    return v->count;
}


void pvector_free(pvector *s)
{
    free(s->data);
    pvector_init(s);
}

void pvector_rewrite(pvector *base, pvector *tocopy)
{
    pvector_free(base);
    for(int i=0; i<pvector_count(tocopy); i++)
        pvector_push(base, pvector_get(tocopy, i));
}

#endif //NEW_C_DIRECTORY_PVECTOR_H
