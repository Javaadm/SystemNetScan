#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <assert.h>
#include "point.h"
#include "pvector.h"
#include "ppvector.h"
#include "matrix.h"


void print(int a)
{
    printf("\n%d", a);
}

int int_comp(const void *a, const void *b)
{
    int c = *(int*)a, d = *(int*)b;
    return c>d?1:0;
}

// void concatenate(char **first, char *second)
// {
//     *first = realloc(*first, sizeof(*first)+sizeof(second));
//     strcat(*first, second);
// }

void get_pass_variety(int rows, int columns, int* arr, pvector *biggest_variety)
{
    matrix image, is_used;
    pvector current_variety;
    // int counter = 0;
    // for(int i = 0; i < rows * columns; i++)
    //     counter += (arr[i] != 0);
    // print(counter);
    printf("start of initialization\n");
    // matrix_init(&image, rows, columns);
    matrix_init(&is_used, rows, columns);
    pvector_init(biggest_variety);
    pvector_init(&current_variety);
    printf("matrix assignation\n");
    image.rows = rows;
    image.cols = columns;
    image.data = arr;
    // for (int i = 0; i < rows; i++)
    //     for (int j = 0; j < columns; j++)
    //     {
    //         matrix_set(&image, i, j, arr[i * columns + j]);
    //     }
    // printf("success with matrix\n");
    // print(matrix_get(&image, 0, 0));
    // print(matrix_get(&image, 0, 1));
    // print(matrix_get(&image, 0, 2));
    // matrix_print(&image);
    // printf("start of looking for pass variety\n");
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < columns; j++) {
            if (matrix_get(&image, i, j) != 0 && matrix_get(&is_used, i, j) == '\0') {
                if (matrix_get(&image, i, j) != 255)
                    printf("Alert!%d, %d with %d\n", i, j, matrix_get(&image, i, j));
                // printf("creating a new variety\n");
                pvector for_bfs;
                pvector_init(&for_bfs);
                pvector_push(&for_bfs, get_Point(i, j));
                while(pvector_not_empty(&for_bfs))
                {
                    int x = pvector_top(&for_bfs).x, y = pvector_top(&for_bfs).y;
                    pvector_pop(&for_bfs);
                    // printf("checking x and y\n");
                    if((x < 0) || (x >= rows) || (y < 0) || (y >= columns))
                        continue;
                    if((matrix_get(&is_used, x, y) == 1) || (matrix_get(&image, x, y) == 0))
                        continue;
                    // if (matrix_get(&image, i, j) != 255);
                    //     printf("Alert!%d, %d\n", i, j);
                    // printf("adding current value to variety\n");
                    //print(sizeof(current_variety.data));
                    pvector_push(&current_variety, get_Point(x, y));
                    //print(sizeof(current_variety.data));
                    matrix_set(&is_used, x, y, 1);
                    // printf("trying near points\n");
                    for (int i = -2; i<=2; i++)
                    {
                        for (int j = -2; j<=2; j++)
                        {
                            int new_x = x + i, new_y = y + j;
                            if((new_x < 0) || (new_x >= rows) || (new_y < 0) || (new_y >= columns))
                                continue;
                            if((matrix_get(&is_used, new_x, new_y) == 1) || (matrix_get(&image, new_x, new_y) == 0))
                                continue;
                            // printf("adding a new point\n");
                            pvector_push(&for_bfs, get_Point(new_x, new_y));
                            // printf("added\n");
                        }
                    }
                }
                if(pvector_count(&current_variety) > pvector_count(biggest_variety))
                {
                    // printf("rewriting biggest variety\n");
                    pvector_rewrite(biggest_variety, &current_variety);
                }
                // printf("freeing current and bfs varieties\n");
                // printf("%d\n", pvector_count((&current_variety)));
                pvector_free(&current_variety);
                // printf("%d\n", pvector_count((&for_bfs)));
                pvector_free(&for_bfs);
            }
        }
    }
    printf("freeing matrix\n");
    // matrix_free(&image);
    matrix_free(&is_used);
    return;
}


void mainF(int height, int width, int *arr, int *result) {
    print(height);
    print(width);
    pvector pass_variety;
    get_pass_variety(height, width, arr, &pass_variety);
    printf("\n%d\n", pvector_count(&pass_variety));

    pvector hull;
    get_convexHull(&pass_variety, &hull);
    print(pvector_count(&hull));
    ppvector lines;
    ppvector_init(&lines);
    for(int i = 0; i < pvector_count(&hull); i++)
        for(int j = i+1; j < pvector_count(&hull); j++)
        {
            ppvector_push(&lines, get_doublePoint(pvector_get(&hull, i), pvector_get(&hull, j)));
        }
    printf("\nqsort is going\n");
    qsort(&lines.data[0], ppvector_count(&lines), sizeof(doublePoint), doublePoint_comparator);

    // for(int i = 0; i < ppvector_count(&lines); i++)
    // {
    //     doublePoint_print(ppvector_get(&lines, i));
    // }
    Point line1, line2;
    doublePoint line1dp = ppvector_get(&lines, 0);
    line1.x = line1dp.first.x - line1dp.second.x;
    line1.y = line1dp.first.y - line1dp.second.y;

    for (int i = 0; i < ppvector_count(&lines); i++)
    {
        doublePoint linedp = ppvector_get(&lines, i);
        line2.x = linedp.first.x - linedp.second.x;
        line2.y = linedp.first.y - linedp.second.y;
        double angle1 = atan2((double)line1.y, (double)line1.x);
        if(angle1 < 0)
            angle1 += M_PI;
        double angle2 = atan2((double)line2.y, (double)line2.x);
        if(angle2 < 0)
            angle2 += M_PI;

        double dif = fabs(angle1 - angle2);
        if(dif > 0.2 && dif < 2.94)
        {
            ppvector_set(&lines, 1, ppvector_get(&lines, i));
            break;
        }
    }

    // printf("\n almost end\n");
    // int *result = malloc(sizeof(int)*8);
    for (int i = 0; i < 2; i++)
    {
        // printf("%d start", i);
        doublePoint dp = ppvector_get(&lines, i);
        // printf("first");
        result[4*i + 0] = dp.first.x;
        result[4*i + 1] = dp.first.y;
        // printf("second");
        result[4*i + 2] = dp.second.x;
        result[4*i + 3] = dp.second.y;
        // printf("%d end", i);
    }
    printf("end");
    ppvector_free(&lines);
    pvector_free(&pass_variety);
    pvector_free(&hull);
    // return result;
}
