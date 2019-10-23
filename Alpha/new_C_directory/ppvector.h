//
// Created by mikhail on 20.10.2019.
//

#ifndef NEW_C_DIRECTORY_PPVECTOR_H
#define NEW_C_DIRECTORY_PPVECTOR_H
#include <stdlib.h>
#include <string.h>

#include "point.h"
#include "vector.h"
#include "pvector.h"

typedef struct doublePoint
{
    Point first, second;
} doublePoint;

doublePoint get_doublePoint(Point x, Point y)
{
    doublePoint ret;
    ret.first = x;
    ret.second = y;
    return ret;
}

int doublePoint_comparator(const void *x, const void *y)
{
    doublePoint dpx = *(doublePoint*)x, dpy = *(doublePoint*)y;
    int len_x = distSq(dpx.first, dpx.second), len_y = distSq(dpy.first, dpy.second);
    return len_x>len_y?0:1;
}

void doublePoint_print(doublePoint dp)
{
    printf("\n");
    Point_print(dp.first);
    Point_print(dp.second);
}

typedef struct ppvector{
    int size;
    int count;
    doublePoint* data;
} ppvector;

void ppvector_init(ppvector* s)
{
    s->size = 0;
    s->data = NULL;
    s->count = 0;
}


void ppvector_push(ppvector *v, doublePoint e) {
    if (v->size == 0) {
        v->size = 10;
        v->data = malloc(sizeof(doublePoint) * v->size);
        memset(v->data, '\0', sizeof(doublePoint) * v->size);
    }

    // condition to increase v->data:
    // last slot exhausted
    if (v->size == v->count) {
        v->size *= 2;
        v->data = realloc(v->data, sizeof(doublePoint) * v->size);
    }

    v->data[v->count] = e;
    v->count++;
}

int ppvector_count(ppvector*s)
{
    return s->count;
}

void ppvector_pop(ppvector* s)
{
    s->count--;
}

doublePoint ppvector_top(ppvector* s)
{
    return s->data[s->count-1];
}

doublePoint ppvector_get(ppvector *s, int index)
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

int ppvector_not_empty(ppvector *v)
{
    return v->count + 1;
}

void ppvector_set(ppvector *v, int index, doublePoint value)
{
    v->data[index] = value;
}

void ppvector_free(ppvector *s)
{
    free(s->data);
}

#endif //NEW_C_DIRECTORY_PPVECTOR_H
