cmake_minimum_required(VERSION 3.1)
project(NGEN)

find_package(Threads REQUIRED)

set(CMAKE_CXX_FLAGS "-Wall")
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

set(SOURCES Property.h Property.cc ModulePool.h ModulePool.cc Module.h Module.cc SimpleModules.h IO.cc IO.h noise.cc noise.h)

add_library(NGEN ${SOURCES})
target_link_libraries(NGEN ${CMAKE_THREAD_LIBS_INIT})

