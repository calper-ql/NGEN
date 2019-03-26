//
// Created by calpe on 3/25/2019.
//

#ifndef NGEN_CPP_SIMPLEMODULES_H
#define NGEN_CPP_SIMPLEMODULES_H

#include "Module.h"

namespace NGEN {
    class TestModule : public Module {
    public:
        NGEN_FLOAT(test, 0.0)
        NGEN_INT(uwu, 0)
        NGEN_SEED(seed, 0)
        NGEN_BOOL(another_lol, 0)
        NGEN_STRING(name, "random name lul")

        NGEN_INPUT(test_input)
        NGEN_OUTPUT(test_output)

        TestModule(ModulePool* mp) : Module(mp){
            NGEN_SET_PROPERTY(test, 31.0)
        }

        ~TestModule(){
            std::cout << "Deleting test module" << std::endl;
        }
    };

    class OutputModule : public Module {
    public:
        NGEN_STRING(name, "default")
        NGEN_INPUT(input)

        OutputModule(ModulePool* mp) : Module(mp){}
    };

    class PerlinModule : public Module {
    public:

        NGEN_SEED(seed, 42)
        NGEN_INT(octave, 4)
        NGEN_FLOAT(frequency, 1.0)
        NGEN_FLOAT(lacunarity, 1.0)
        NGEN_FLOAT(persistance, 1.0)

        NGEN_OUTPUT(output)

        PerlinModule(ModulePool* mp) : Module(mp){}
    };


    NGEN_REGISTER_MODULE(TestModule);
    NGEN_REGISTER_MODULE(OutputModule);
    NGEN_REGISTER_MODULE(PerlinModule);
}

#endif //NGEN_CPP_SIMPLEMODULES_H
