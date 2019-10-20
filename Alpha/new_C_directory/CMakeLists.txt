cmake_minimum_required(VERSION 3.15)
project(new_C_directory C)

set(CMAKE_C_STANDARD 99)

add_executable(new_C_directory main.c vector.h point.h matrix.h pvector.h ppvector.h)