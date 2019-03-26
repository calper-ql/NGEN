//
// Created by calpe on 3/25/2019.
//

#include "Module.h"

namespace NGEN {
    std::map<std::string, ModuleFactory*> Module::module_table;

    void Module::print_module_table(){
        std::cout << "+== MODULE TABLE ==+" << std::endl;
        for(const auto &key: module_table){
            std::cout << "| " << key.first << " -> " << key.second << std::endl;
        }
        std::cout << "+==================+" << std::endl;
    }

    void Module::register_module(std::string s, ModuleFactory* p){
        module_table[s] = p;
    }

    Module::Module(ModulePool* mp) {
        this->mp = mp;
        calculated = false;
        if(mp){
            id = mp->get_id(this);
        } else {
            throw std::runtime_error("Module has recived nullptr pool!");
        }
    }

    Module::~Module(){

    };

    std::string Module::to_str() {
        std::string str = "+== " + this->type + " ==+\n";
        str += "# Properties:\n";
        for(auto prop: this->properties){
            str += "|  " + prop.second->to_str() + "\n";
        }
        str += "# Inputs:\n";
        for(auto inp: this->inputs){
            str += "|  " + inp.second->to_str() + "\n";
        }
        str += "# Outputs:\n";
        for(auto out: this->outputs_list){
            str += "|  " + out->to_str() + "\n";
        }
        str += "+==============+\n";
        return str;
    }

    void Module::reset() {
        calculated = false;
    }

    void Module::calculate() {

    }
}