//
// Created by calpe on 3/25/2019.
//

#include "Property.h"
#include "Module.h"

namespace NGEN {

    Property::Property(Module* mod, std::string name) {
        this->name = name;
        this->mod = mod;
        if(mod != nullptr){
            mod->properties[name] = this;
        }
    }

    FloatProperty::FloatProperty(Module* mod, std::string name, float value) : Property(mod, name) {
        this->value = value;
    }

    std::string FloatProperty::to_str() {
        return this->name + "(f) = " + std::to_string(this->value);
    }


    IntProperty::IntProperty(Module* mod, std::string name, int value) : Property(mod, name) {
        this->value = value;
    }

    std::string IntProperty::to_str() {
        return this->name + "(i) = " + std::to_string(this->value);
    }

    SeedProperty::SeedProperty(Module* mod, std::string name, int value) : Property(mod, name) {
        this->value = value;
    }

    std::string SeedProperty::to_str() {
        return this->name + "(s) = " + std::to_string(this->value);
    }

    BoolProperty::BoolProperty(Module* mod, std::string name, bool value) : Property(mod, name) {
        this->value = value;
    }

    std::string BoolProperty::to_str() {
        return this->name + "(b) = " + std::to_string(this->value);
    }

    StringProperty::StringProperty(Module *mod, std::string name, std::string value) : Property(mod, name) {
        this->value = value;
    }

    std::string StringProperty::to_str() {
        return this->name + "(str) = " + this->value;
    }
}