//
// Created by calpe on 3/25/2019.
//

#ifndef NGEN_CPP_IO_H
#define NGEN_CPP_IO_H

#include <map>
#include <iostream>

namespace NGEN {
    class Module;

    class Output {
    public:
        Module* module;
        std::string name;
        float stored_value;
        int id;
        Output(Module* module, std::string name);
        std::string to_str();
    };

    class Input {
    public:
        Module* module;
        std::string name;
        Output* connection = nullptr;
        int module_id;
        int output_id;
        Input(Module* module, std::string name, int module_id, int output_id);
        std::string to_str();
        void get_connection();
        void connect(Output* out);
        float calculate(float x, float y, float z);
    };


}


#endif //NGEN_CPP_IO_H
