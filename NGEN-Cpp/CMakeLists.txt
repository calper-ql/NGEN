cmake_minimum_required(VERSION 3.1)
project(NGEN_Cpp)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(NGEN)

add_executable(test_v1 main.cpp)
target_link_libraries(test_v1 NGEN)