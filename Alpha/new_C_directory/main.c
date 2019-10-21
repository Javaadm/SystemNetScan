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
const char system_path[] = "/home/mikhail/Work_with_documents/Alpha/new_C_directory";


pvector get_pass_variety()
{
    char open_file[] = "";
    strcpy(open_file, system_path);
    strcat(open_file, "image.txt");
    FILE *input = fopen(open_file, "r");
    int rows, columns;
    fscanf(input, "%d %d", &rows, &columns);
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

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < columns; j++) {
            if (matrix_get(&image, i, j) == 255 && matrix_get(&is_used, i, j) == '\0') {
                //creating a new variety
                pvector_free(&current_variety);
                pvector_init(&current_variety);

                pvector for_bfs;
                pvector_init(&for_bfs);
                pvector_push(&for_bfs, get_Point(i, j));
                while(pvector_not_empty(&for_bfs))
                {
                    int x = pvector_top(&for_bfs).x, y = pvector_top(&for_bfs).y;
                    pvector_pop(&for_bfs);
                    //checking x and y
                    if(x < 0 || x >= rows || y < 0 || y >= columns)
                        continue;
                    if((matrix_get(&is_used, x, y) == 1) || (matrix_get(&image, x, y) == 0))
                        continue;

                    //adding current value to variety
                    pvector_push(&current_variety, get_Point(x, y));
                    matrix_set(&is_used, x, y, 1);

                    //trying near points
                    for (int i = -2; i<=2; i++)
                    {
                        for (int j = -2; j<=2; j++)
                        {
                            int new_x = x + i, new_y = y + j;
                            if(new_x < 0 || new_x >= rows || new_y < 0 || new_y >= columns)
                                continue;
                            if((matrix_get(&is_used, new_x, new_y) == 1) || (matrix_get(&image, new_x, new_y) == 0))
                                continue;

                            //adding a new point
                            pvector_push(&for_bfs, get_Point(new_x, new_y));
                        }
                    }
                }
            }
            if(pvector_count(&current_variety) > pvector_count(&biggest_variety))
                biggest_variety = current_variety;
        }
    }
    matrix_free(&image);
    matrix_free(&is_used);
    pvector_free(&current_variety);

    return biggest_variety;
}



int main() {
    pvector pass_variety = get_pass_variety();

    pvector hull = get_convexHull(&pass_variety);

    ppvector lines;
    for(int i = 0; i < pvector_count(&hull); i++)
        for(int j = i+1; j < pvector_count(&hull); j++)
        {
            ppvector_push(&lines, get_doublePoint(pvector_get(&hull, i), pvector_get(&hull, j)));
        }
    qsort(&lines.data, ppvector_count(&lines), sizeof(doublePoint), doublePoint_comparator);

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

    char output_path[] = "";
    strcat(output_path, system_path);
    strcat(output_path, "coordinates_4p.txt");
    FILE *output = fopen(output_path, "w");
    for (int i = 0; i < 2; i++)
    {
        doublePoint dp = ppvector_get(&lines, i);
        fprintf(output, "%d %d ", dp.first.y, dp.first.x);
        fprintf(output, "%d %d ", dp.second.y, dp.second.x);
        if(i == 0)
            fprintf(output, " ");
    }
    ppvector_free(&lines);
    pvector_free(&pass_variety);
    pvector_free(&hull);
    return 0;
}
