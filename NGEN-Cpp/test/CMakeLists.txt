add_executable(test_1 main.cpp)
target_link_libraries(test_1 NGEN)

configure_file(test_graph.json ${CMAKE_CURRENT_BINARY_DIR}/test_graph.json COPYONLY)