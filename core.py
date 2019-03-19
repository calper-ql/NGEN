import numpy as np
import json

module_pool_class_registry = {}


def __module_json_stripper(json):
    del json_d["id"]
    del json_d["type"]
    del json_d["inputs"]
    del json_d["outputs"]
    return json


class ModulePool:
    def __init__(self):
        self.id_counter = 0
        self.modules = {}

    def get_id(self, module):
        # self.find_max()
        temp = self.id_counter
        self.id_counter += 1
        self.modules[temp] = module
        return temp

    def find_max(self):
        self.id_counter = 0
        for m in self.modules:
            if self.modules[m].id > self.id_counter:
                self.id_counter = self.modules[m].id + 1

    def to_json(self):
        p = []
        for key in self.modules:
            p.append(self.modules[key].to_json())
        d = {"modules": p}
        return d

    def from_json(self, json_d):
        copy = json_d.copy()
        self.id_counter = 0
        self.modules = {}
        mods = copy["modules"]
        for mod in mods:
            self.construct_module(mod)
        self.find_max()
        for m in self.modules:
            for inp in self.modules[m].inputs:
                inp._get_connection()

    def construct_module(self, json_do):
        json_d = json_do.copy()
        id = json_d["id"]
        tp = json_d["type"]
        inps = json_d["inputs"]
        on = json_d["outputs"]
        del json_d["id"]
        del json_d["type"]
        del json_d["inputs"]
        del json_d["outputs"]

        mod = module_pool_class_registry[tp](self)
        assert len(mod.outputs) == on

        mod.id = id
        self.modules[id] = mod
        for i in range(len(inps)):
            mod.inputs[i].connect_idx(inps[i]["module"], inps[i]["output_id"])

        for key in json_d:
            setattr(mod, key, json_d[key])


class Module:
    def __init__(self, module_pool):
        self.module_pool = module_pool
        self.id = module_pool.get_id(self)
        self.inputs = []
        self.outputs = []

    def calculate(self, arg, output_id):
        pass

    def reset(self):
        for conn in self.inputs:
            conn.reset()

    def to_json(self):
        d = self.__dict__
        n = {}
        for key in d:
            if not hasattr(d[key], '__dict__'):
                n[key] = d[key]
        ins = []
        for inp in self.inputs:
            ins.append(inp.to_json())
        n['inputs'] = ins
        n['outputs'] = len(self.outputs)
        n['type'] = type(self).__name__
        return n

    def to_stripped_dict(self):
        d = self.__dict__
        n = {}
        for key in d:
            if not hasattr(d[key], '__dict__'):
                n[key] = d[key]
        if 'inputs' in n: del n['inputs']
        if 'outputs' in n: del n['outputs']
        if 'type' in n: del n['type']
        if 'id' in n: del n['id']
        return n

    def get_input_names(self):
        d = self.__dict__
        n = {}
        for key in d:
            if isinstance(d[key], Input):
                n[d[key]] = key
        return n

    def get_output_names(self):
        d = self.__dict__
        n = {}
        for key in d:
            if isinstance(d[key], Output):
                n[d[key]] = key
        return n

    def update(self):
        pass

    def register(self, io):
        if isinstance(io, Input):
            io.id = len(self.inputs)
            self.inputs.append(io)
        elif isinstance(io, Output):
            io.id = len(self.outputs)
            self.outputs.append(io)


class Input:
    def __init__(self, module):
        self.id = None
        self.module = module
        self.module.register(self)
        self.connection = None
        self.cp = None  # connection param

    def get(self, arg):
        if self.connection:
            return self.connection.get(arg)
        else:
            if self.cp:
                self._get_connection()
                return self.connection.get(arg)
            return None

    def to_json(self):
        name = self.module.get_input_names()[self]
        self._get_connection()
        if not self.connection:
            return {"module": -1, "output_id": -1, "name":name}
        else:
            return {"module": self.connection.module.id, "output_id": self.connection.id, "name":name}

    def connect(self, output):
        if output.module != self.module:
            if output.module.module_pool == self.module.module_pool:
                self.connection = output

    def connect_idx(self, mod_id, out_id):
        if mod_id != self.module.id:
            self.cp = [mod_id, out_id]

    def _get_connection(self):
        if self.cp:
            if len(self.module.module_pool.modules) > self.cp[0]:
                if len(self.module.module_pool.modules[self.cp[0]].outputs) > self.cp[1]:
                    self.connection = self.module.module_pool.modules[self.cp[0]].outputs[self.cp[1]]

    def reset(self):
        if self.connection:
            self.connection.reset()

    def disconnect(self):
        self.connection = None
        self.cp = None


class Output:
    def __init__(self, module):
        self.id = None
        self.module = module
        self.module.register(self)
        self.stored_value = None

    def set(self, value):
        self.stored_value = value

    def get(self, arg):
        if self.stored_value is None:
            self.module.calculate(arg, self.id)
        return self.stored_value

    def reset(self):
        self.stored_value = None
        self.module.reset()


class Property:
    def get(self):
        return None


class BoolProperty(Property):
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value


class SeedProperty(Property):
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value


class IntProperty(Property):
    def __init__(self, value, range=[0, 100]):
        self.value = value
        self.range = range

    def get(self):
        return self.value


class FloatProperty(Property):
    def __init__(self, value, range=[-1.0, 1.0]):
        self.value = value
        self.range = range

    def get(self):
        return self.value