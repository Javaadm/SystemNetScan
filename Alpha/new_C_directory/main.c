#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "point.h"
#include "vector.h"
#include "pvector.h"
#include "ppvector.h"
#include "matrix.h"
// #include <iostream>
// #include <algorithm>
// #include <fstream>
// #include <vector>
// #include <string>
// #include <stack>
// #include <cmath>


// const char system_path[] = "./C_directory/";
// char system_path[] = "/home/mikhail/Work_with_documents/Alpha/new_C_directory";
char system_path[] = "/new_C_directory";

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

pvector get_pass_variety()
{
    char *open_file = NULL;
    char end_file[] = "/image.txt";
    int full_size = sizeof(open_file)+sizeof(system_path)+sizeof(end_file);
    open_file = realloc(open_file, full_size);
    memset(open_file, '\0', full_size);
    strcat(open_file, system_path);
    strcat(open_file, end_file);
    printf("\n *%s* \n", open_file);
    FILE *input = fopen(open_file, "r");
    if(input == NULL)
        perror("In get_pass_variety");
    int rows, columns;
    fscanf(input, "%d %d", &rows, &columns);
    // printf("\n %d, %d \n", rows, columns);
    matrix image;
    matrix_init(&image, rows, columns);
    pvector biggest_variety, current_variety;
    pvector_init(&biggest_variety);
    pvector_init(&current_variety);
    matrix is_used;
    matrix_init(&is_used, rows, columns);

    for (int i = 0; i < rows; i++)
        for (int j = 0; j < columns; j++)
        {
            int pixel;
            fscanf(input, " %d", &pixel);
            matrix_set(&image, i, j, pixel);
        }
    vector size_holder;
    vector_init(&size_holder, sizeof(int));
    // matrix_print(&image);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < columns; j++) {
            if (matrix_get(&image, i, j) == 255 && matrix_get(&is_used, i, j) == '\0') {
                //creating a new variety

                pvector for_bfs;
                pvector_init(&for_bfs);
                pvector_push(&for_bfs, get_Point(i, j));
                while(pvector_not_empty(&for_bfs))
                {
                    int x = pvector_top(&for_bfs).x, y = pvector_top(&for_bfs).y;
                    pvector_pop(&for_bfs);
                    //checking x and y
                    if((x < 0) || (x >= rows) || (y < 0) || (y >= columns))
                        continue;
                    if((matrix_get(&is_used, x, y) == 1) || (matrix_get(&image, x, y) == 0))
                        continue;

                    //adding current value to variety
                    //print(sizeof(current_variety.data));
                    pvector_push(&current_variety, get_Point(x, y));
                    //print(sizeof(current_variety.data));
                    matrix_set(&is_used, x, y, 1);

                    //trying near points
                    for (int i = -2; i<=2; i++)
                    {
                        for (int j = -2; j<=2; j++)
                        {
                            int new_x = x + i, new_y = y + j;
                            if((new_x < 0) || (new_x >= rows) || (new_y < 0) || (new_y >= columns))
                                continue;
                            if((matrix_get(&is_used, new_x, new_y) == 1) || (matrix_get(&image, new_x, new_y) == 0))
                                continue;

                            //adding a new point
                            pvector_push(&for_bfs, get_Point(new_x, new_y));
                        }
                    }
                }
                //print(pvector_count(&current_variety));
                if(pvector_count(&current_variety) > pvector_count(&biggest_variety))
                {
                    // pvector_free(&biggest_variety);
                    // pvector_init(&biggest_variety);
                    // print(pvector_count(&current_variety));
                    pvector_rewrite(&biggest_variety, &current_variety);
                    // printf("\n%d, %d", pvector_count(&biggest_variety), pvector_count(&current_variety));
                    // printf("\n%d, %d", sizeof(biggest_variety.data), sizeof(current_variety.data));
                }
                vector_add(&size_holder, pvector_count(&current_variety));
                pvector_free(&current_variety);
                pvector_init(&current_variety);
                // print(sizeof(current_variety.data));
            }
        }
    }
    // int counter = 0;
    // for(int i = 0; i<rows; i++)
    //     for(int j = 0; j<columns; j++)
    //         if(matrix_get(&image, i, j) == 255)
    //             counter++;
    // print(counter);
    qsort(size_holder.data, vector_count(&size_holder), sizeof(int), int_comp);
    int sum = 0;
    for(int i = 0; i < vector_count(&size_holder); i++)
        sum += vector_get(&size_holder, i);
        // print(vector_get(&size_holder, i));
    // print(sum);
    matrix_free(&image);
    matrix_free(&is_used);
    fclose(input);

    return biggest_variety;
}



int main() {
    pvector pass_variety = get_pass_variety();
    printf("\n%d\n", pvector_count(&pass_variety));
    // print(sizeof(pass_variety.data));
    // Point_print(pvector_get(&pass_variety, pvector_count(&pass_variety)+1));

    pvector hull = get_convexHull(&pass_variety);
    // print(pvector_count(&hull));
    // printf("\n");
    // for(int i=0; i<pvector_count(&hull); i++)
    // {
    //     Point_print(pvector_get(&hull, i));
    // }

    ppvector lines;
    ppvector_init(&lines);
    for(int i = 0; i < pvector_count(&hull); i++)
        for(int j = i+1; j < pvector_count(&hull); j++)
        {
            ppvector_push(&lines, get_doublePoint(pvector_get(&hull, i), pvector_get(&hull, j)));
        }
    qsort(&lines.data[0], ppvector_count(&lines), sizeof(doublePoint), doublePoint_comparator);

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

    char *output_path = NULL;
    char end_file[] = "/coordinates_4p.txt";
    int full_size = sizeof(output_path) + sizeof(system_path) + sizeof(end_file);
    output_path = realloc(output_path, full_size);
    memset(output_path, '\0', full_size);
    strcat(&output_path[0], system_path);
    strcat(output_path, end_file);
    printf("*%s* \n\n", output_path);
    FILE *output = fopen(output_path, "w");
    if(output == NULL)
        perror(output_path);

    for (int i = 0; i < 2; i++)
    {
        doublePoint dp = ppvector_get(&lines, i);
        // doublePoint_print(dp);
        fprintf(output, "%d %d ", dp.first.y, dp.first.x);
        fprintf(output, "%d %d", dp.second.y, dp.second.x);
        if(i == 0)
            fprintf(output, " ");
    }
    ppvector_free(&lines);
    pvector_free(&pass_variety);
    pvector_free(&hull);
    fclose(output);
    return 0;
}
