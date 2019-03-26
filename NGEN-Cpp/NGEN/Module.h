//
// Created by calpe on 3/25/2019.
//

#ifndef NGEN_CPP_MODULE_H
#define NGEN_CPP_MODULE_H

#include "ModulePool.h"
#include "Property.h"

namespace NGEN {
    class ModuleFactory;

#define NGEN_FLOAT(name, value) \
    FloatProperty name = FloatProperty(this, #name, value);

#define NGEN_INT(name, value) \
    IntProperty name = IntProperty(this, #name, value);

#define NGEN_SEED(name, value) \
    SeedProperty name = SeedProperty(this, #name, value);

#define NGEN_BOOL(name, value) \
    BoolProperty name = BoolProperty(this, #name, value);

#define NGEN_STRING(name, value) \
    StringProperty name = StringProperty(this, #name, value);

#define NGEN_SET_PROPERTY(property, new_value) \
    this->property.value = new_value;

#define NGEN_INPUT(name) \
    Input name = Input(this, #name, -1, -1);

#define NGEN_OUTPUT(name) \
    Output name = Output(this, #name);

    class Module {
    public:
        static void print_module_table();
        static void register_module(std::string s, ModuleFactory* p);

        std::map<std::string, Property*> properties;
        std::string type = "undefined";

        std::map<std::string, Input*> inputs;
        std::map<std::string, Output*> outputs;
        std::vector<Output*> outputs_list;
        std::vector<Input*> inputs_list;

        ModulePool* mp;
        int id;

        bool calculated;

        Module(ModulePool* mp);
        virtual ~Module();

        virtual void calculate();

        std::string to_str();

        void reset();
    };

    class ModuleFactory {
    public:
        virtual Module *create(ModulePool* mp) = 0;
    };


    std::map<std::string, ModuleFactory*> &get_module_registry();
}


#define NGEN_REGISTER_MODULE(klass) \
    class klass##Factory : public ModuleFactory { \
    public: \
        klass##Factory() \
        { \
            Module::register_module(#klass, this); \
        } \
        virtual Module *create(ModulePool* mp) { \
            auto k = new klass(mp); \
            k->type = #klass;\
            return k;\
        } \
    }; \
    static klass##Factory ngen_global_##klass##Factory;


#endif //NGEN_CPP_MODULE_H
