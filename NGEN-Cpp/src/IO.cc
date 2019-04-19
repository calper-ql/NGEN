//
// Created by calpe on 3/25/2019.
//

#include <NGEN/IO.h>
#include <NGEN/Module.h>

namespace NGEN {

    Output::Output(Module *module, std::string name) {
        this->module = module;
        this->name = name;
        if(module){
            id = static_cast<int>(module->outputs.size());
            module->outputs_list.push_back(this);
            module->outputs[name] = this;
        } else {
            throw std::runtime_error("Module has recived nullptr pool!");
        }
		if (module->outputs.size() > 1) {
			throw std::runtime_error("Module multiple outputs");
		}
        if(module == nullptr) std::runtime_error("Output -> module is null");
    }

    std::string Output::to_str() {
        std::string str = name;
        return str;
    }


    Input::Input(Module *module, std::string name, int module_id, int output_id) {
        this->module = module;
        this->name = name;
        this->module_id = module_id;
        this->output_id = output_id;
        if(module){
            module->inputs_list.push_back(this);
            module->inputs[name] = this;
        } else {
            throw std::runtime_error("Module has recived nullptr pool!");
        }
        if(module == nullptr) std::runtime_error("Input -> module is null");
    }

    std::string Input::to_str() {
        std::string str = name + " -- mod_id: " + std::to_string(module_id) + " out_name: " + std::to_string(output_id);
        return str;
    }

    void Input::get_connection() {
        connection = this->module->mp->modules[module_id]->outputs_list[output_id];
    }

    void Input::connect(Output *out) {
        connection = out;
        module_id = connection->module->id;
        output_id = connection->id;
    }

    float Input::calculate(float x, float y, float z) {
        connection->module->calculate(x, y, z);
        return connection->stored_value;
    }

}