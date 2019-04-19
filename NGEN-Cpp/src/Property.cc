//
// Created by calpe on 3/25/2019.
//

#include "../include/NGEN/Property.h"
#include "../include/NGEN/Module.h"

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
		if(mod != nullptr) {
			mod->float_properties[name] = this;
		}
    }

    std::string FloatProperty::to_str() {
        return this->name + "(f) = " + std::to_string(this->value);
    }


    IntProperty::IntProperty(Module* mod, std::string name, int value) : Property(mod, name) {
        this->value = value;
		if (mod != nullptr) {
			mod->int_properties[name] = this;
		}
    }

    std::string IntProperty::to_str() {
        return this->name + "(i) = " + std::to_string(this->value);
    }

    SeedProperty::SeedProperty(Module* mod, std::string name, int value) : Property(mod, name) {
        this->value = value;
		if (mod != nullptr) {
			mod->seed_properties[name] = this;
		}
    }

    std::string SeedProperty::to_str() {
        return this->name + "(s) = " + std::to_string(this->value);
    }

    BoolProperty::BoolProperty(Module* mod, std::string name, bool value) : Property(mod, name) {
        this->value = value;
		if (mod != nullptr) {
			mod->bool_properties[name] = this;
		}
    }

    std::string BoolProperty::to_str() {
        return this->name + "(b) = " + std::to_string(this->value);
    }

    StringProperty::StringProperty(Module *mod, std::string name, std::string value) : Property(mod, name) {
        this->value = value;
		if (mod != nullptr) {
			mod->string_properties[name] = this;
		}
    }

    std::string StringProperty::to_str() {
        return this->name + "(str) = " + this->value;
    }
}