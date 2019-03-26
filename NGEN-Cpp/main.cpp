#include <iostream>
#include "NGEN/SimpleModules.h"

int main() {
    std::cout << "Hello, World!" << std::endl;
    NGEN::Module::print_module_table();
    auto mp = new NGEN::ModulePool();
    auto tm = NGEN::Module::module_table["TestModule"]->create(mp);
    auto tm2 = NGEN::Module::module_table["TestModule"]->create(mp);
    tm->inputs["test_input"]->connect(tm2->outputs_list[0]);
    std::cout << tm->to_str() << std::endl;

    std::ifstream i("test_graph.json");
    json j;
    i >> j;
    mp->from_json(j);


    for(auto m: mp->modules){
        std::cout << m.second->to_str() << std::endl;
    }

    delete(mp);
    return 0;
}