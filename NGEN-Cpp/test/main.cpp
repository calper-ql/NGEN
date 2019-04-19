#include <iostream>
#include "NGEN/SimpleModules.h"

int main() {
    std::cout << "Hello, World!" << std::endl;
    NGEN::Module::print_module_table();
    auto mp = new NGEN::ModulePool();
    auto table = NGEN::get_module_registry();
    auto tm = NGEN::get_module_registry()["TestModule"]->create(mp);
    auto tm2 = NGEN::get_module_registry()["TestModule"]->create(mp);
    tm->inputs["test_input"]->connect(tm2->outputs_list[0]);
    std::cout << tm->to_str() << std::endl;

    std::ifstream i("test_graph.json");
    json j;
    i >> j;
    mp->from_json(j);

    NGEN::OutputModule* om = nullptr;
    for(auto pair: mp->modules){
        std::cout << pair.second->to_str() << std::endl;
        if(pair.second->type == "OutputModule"){
            auto temp = (NGEN::OutputModule*) pair.second;
            if(temp->name.value == "test_output_yolo"){
                om = temp;
            }
        }
    }

    if(om){
        auto value = om->input.calculate(1.0, 1.0, 1.0);
        std::cout <<  value << std::endl;
    }

    delete(mp);
    return 0;
}