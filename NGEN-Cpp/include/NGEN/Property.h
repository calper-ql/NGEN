//
// Created by calpe on 3/25/2019.
//

#ifndef NGEN_CPP_PROPERTY_H
#define NGEN_CPP_PROPERTY_H

#include <iostream>

namespace NGEN {
    class Module;

    class Property {
    public:
        std::string name;
        Module* mod;
        Property(Module* mod, std::string name);
        virtual std::string to_str() = 0;
    };

    class FloatProperty : public Property {
    public:
        float value = 0.0;
        FloatProperty(Module* mod, std::string name, float value);
        std::string to_str() override;
    };

    class IntProperty : public Property {
    public:
        int value = 0;
        IntProperty(Module* mod, std::string name, int value);
        std::string to_str() override;
    };

    class SeedProperty : public Property {
    public:
        int value = 0;
        SeedProperty(Module* mod, std::string name, int value);
        std::string to_str() override;
    };

    class BoolProperty : public Property {
    public:
        bool value = false;
        BoolProperty(Module* mod, std::string name, bool value);
        std::string to_str() override;
    };

    class StringProperty : public Property {
    public:
        std::string value = "default";
        StringProperty(Module* mod, std::string name, std::string value);
        std::string to_str() override;
    };
}



#endif //NGEN_CPP_PROPERTY_H
