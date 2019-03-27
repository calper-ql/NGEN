//
// Created by calpe on 3/25/2019.
//

#include "ModulePool.h"
#include "Module.h"

namespace NGEN {

    ModulePool::ModulePool() {
        id_counter = 0;
    }

    ModulePool::~ModulePool() {
        clear();
    }

    int ModulePool::get_id(Module *m) {
        int temp = id_counter;
        modules[temp] = m;
        id_counter += 1;
        return  temp;
    }

    void ModulePool::find_max() {
        id_counter = 0;
        for(auto m: modules){
            if(m.first >= id_counter) id_counter = m.first+1;
        }
    }

    void ModulePool::clear() {
        id_counter = 0;
        for(std::pair<const int, Module*> &m: modules) {
            delete m.second;
        }
        modules.clear();
    }

    void ModulePool::reset() {
        for(auto m: modules) {
            m.second->reset();
        }
    }

    void ModulePool::from_json(json dict) {
        clear();
        try {
            auto mods = dict["modules"];
            for(auto m: mods){
                auto mod = NGEN::get_module_registry()[m["type"]]->create(this);
                mod->id = m["id"];
                auto props = m["properties"];
                auto inputs = m["inputs"];

                for(const auto& [key, value]: props.items()){
                    //std::cout << value << std::endl;
                    if(value["type"] == "StringProperty"){
                        ((StringProperty*)mod->properties[key])->value = value["value"];
                    }
                    if(value["type"] == "FloatProperty"){
                        ((FloatProperty*)mod->properties[key])->value = value["value"];
                    }
                    if(value["type"] == "IntProperty"){
                        ((IntProperty*)mod->properties[key])->value = value["value"];
                    }
                    if(value["type"] == "BoolProperty"){
                        ((BoolProperty*)mod->properties[key])->value = value["value"];
                    }
                    if(value["type"] == "SeedProperty"){
                        ((SeedProperty*)mod->properties[key])->value = value["value"];
                    }
                }

                for(const auto& [key, value]: inputs.items()){
                    //std::cout << key << " " << value << std::endl;
                    mod->inputs[value["name"]]->module_id = value["module"];
                    mod->inputs[value["name"]]->output_id = value["output_id"];
                }

            }
            find_max();

            for(auto m: modules) {
                for(auto inp: m.second->inputs){
                    inp.second->get_connection();
                }
            }

        } catch (std::exception &e) {
            std::cout << e.what() << std::endl;
            throw std::runtime_error("Module from json failure");
        }

    }
}
