from core import *
from ngen import *
from core import module_pool_class_registry


def register_module(m):
    module_pool_class_registry[m.__name__] = m


class AddModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.A = Input(self)
        self.B = Input(self)
        self.C = Output(self)

    def calculate(self, arg):
        return self.A.get(arg) + self.B.get(arg)


register_module(AddModule)


class SubModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.A = Input(self)
        self.B = Input(self)
        self.C = Output(self)

    def calculate(self, arg):
        return self.A.get(arg) - self.B.get(arg)


register_module(SubModule)


class PerlinModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.A = Output(self)
        self.seed = 42
        self.octave = 8
        self.frequency = 1.0
        self.lacunarity = 2.0
        self.persistance = 0.5

    def calculate(self, arg):
        return perlin(gradient_coherent_noise_3d, arg, self.seed, self.octave,
                      frequency=self.frequency,
                      lacunarity=self.lacunarity,
                      persistance=self.persistance)


register_module(PerlinModule)


class RiggedMultiModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.A = Output(self)
        self.seed = 42
        self.octave = 8
        self.frequency = 1.0
        self.lacunarity = 2.0
        self.exp = -1.0
        self.offset = 1.0

    def calculate(self, arg):
        return rigged_multi(gradient_coherent_noise_3d, arg, self.seed, self.octave,
                            frequency=self.frequency,
                            lacunarity=self.lacunarity,
                            exp=self.exp,
                            offset=self.offset)


register_module(RiggedMultiModule)


class SelectModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.control = Input(self)
        self.A = Input(self)
        self.B = Input(self)
        self.output = Output(self)
        self.bound = 0.0
        self.falloff = 0.1
        self.cutoff = 0.0

    def calculate(self, arg):
        ctrl = self.control.get(arg) - self.cutoff
        lin_val = (ctrl + self.falloff) / ((2 * self.falloff))
        val = self.A.get(arg) * lin_val + self.B.get(arg) * (self.bound - lin_val)
        return val


register_module(SelectModule)


class VoronoiModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.output = Output(self)
        self.seed = 42
        self.frequency = 1.0
        self.displacement = 1.0
        self.distance_enabled = False

    def calculate(self, arg):
        return voronoi(value_noise_3d, arg, self.seed,
                       frequency=self.frequency,
                       displacement=self.displacement,
                       distance_enabled=self.distance_enabled)


register_module(VoronoiModule)

if __name__ == "__main__":
    print(module_pool_class_registry)

    mp = ModulePool()
    pm = PerlinModule(mp)
    vm = VoronoiModule(mp)
    am = AddModule(mp)
    am.inputs[0].connect(pm.outputs[0])
    am.inputs[1].connect(vm.outputs[0])

    jsoned = mp.to_json()
    print(jsoned)

    mp2 = ModulePool()
    print('-----------')
    print(jsoned)
    mp2.from_json(jsoned)
    jsoned2 = mp2.to_json()
    print(jsoned2)

    mp3 = ModulePool()
    print('-----------')
    print(jsoned)
    mp3.from_json(jsoned)
    jsoned3 = mp2.to_json()
    print(jsoned3)

    assert jsoned2 == jsoned
    assert jsoned3 == jsoned
    assert jsoned2 == jsoned3
