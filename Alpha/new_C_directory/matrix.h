//
// Created by mikhail on 18.10.2019.
//
#include <stdlib.h>
#include <stdio.h>

#ifndef NEW_C_DIRECTORY_MATRIX_H
#define NEW_C_DIRECTORY_MATRIX_H

typedef struct matrix{
    int* data;
    int rows;
    int cols;
} matrix;

void matrix_init(matrix *mat, int rows, int cols)
{
    mat->rows = rows;
    mat->cols = cols;
    mat->data = malloc(sizeof(int*) * rows * cols);
    memset(mat->data, '\0', sizeof(int*) * rows * cols);
}

void matrix_check(matrix *mat, int row, int col)
{
    if(mat->cols <= col)
        printf("Matrix column out of range!!!\n");
    if(mat->rows <= row)
        printf("Matrix row out of range!!!\n");
}

void matrix_set(matrix *mat, int row, int col, int value)
{
    matrix_check(mat, row, col);
    mat->data[row*mat->cols + col] = value;
}

int matrix_get (matrix *mat, int row, int col)
{
    matrix_check(mat, row, col);
    return mat->data[row*mat->cols + col];
}

void matrix_print(matrix *mat)
{
    for(int i = 0; i < mat->rows; i++)
    {
        for(int j = 0; j < mat->cols; j++)
            printf("%d, ", matrix_get(mat, i, j));
        printf("\n");
    }
}

void matrix_free(matrix *mat)
{
    free(mat->data);
}

#endif //NEW_C_DIRECTORY_MATRIX_H
