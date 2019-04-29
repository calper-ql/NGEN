//
// Created by calpe on 3/25/2019.
//

#ifndef NGEN_CPP_MODULEPOOL_H
#define NGEN_CPP_MODULEPOOL_H

#include <map>
#include <string>
#include <iostream>
#include <fstream>

#include "IO.h"

#include "json.hpp"
using json = nlohmann::json;

namespace NGEN  {
    class Module;

    class ModulePool {
    public:
        std::map<int, Module*> modules;
        int id_counter;

        ModulePool();
        virtual ~ModulePool();

        int get_id(Module* m);
        void find_max();

        void clear();
        void reset();

        void from_json(json dict);
    };
}

#endif //NGEN_CPP_MODULEPOOL_H
