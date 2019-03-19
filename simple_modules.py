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
        self.seed = SeedProperty()
        self.octave = IntProperty()
        self.frequency = FloatProperty()
        self.lacunarity = FloatProperty()
        self.persistance = FloatProperty()

    def calculate(self, arg):
        return perlin(gradient_coherent_noise_3d, arg, self.seed.get(), self.octave.get(),
                      frequency=self.frequency.get(),
                      lacunarity=self.lacunarity.get(),
                      persistance=self.persistance.get())


register_module(PerlinModule)


class RiggedMultiModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.A = Output(self)
        self.seed = SeedProperty()
        self.octave = IntProperty()
        self.frequency = FloatProperty()
        self.lacunarity = FloatProperty()
        self.exp = FloatProperty()
        self.offset = FloatProperty()

    def calculate(self, arg):
        return rigged_multi(gradient_coherent_noise_3d, arg, self.seed.get(), self.octave.get(),
                            frequency=self.frequency.get(),
                            lacunarity=self.lacunarity.get(),
                            exp=self.exp.get(),
                            offset=self.offset.get())


register_module(RiggedMultiModule)


class SelectModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.control = Input(self)
        self.A = Input(self)
        self.B = Input(self)
        self.output = Output(self)
        self.bound = FloatProperty()
        self.falloff = FloatProperty()
        self.cutoff = FloatProperty()

    def calculate(self, arg):
        ctrl = self.control.get(arg) - self.cutoff.get()
        lin_val = (ctrl + self.falloff.get()) / ((2 * self.falloff.get()))
        val = self.A.get(arg) * lin_val + self.B.get(arg) * (self.bound.get() - lin_val)
        return val


register_module(SelectModule)


class VoronoiModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.output = Output(self)
        self.seed = SeedProperty()
        self.frequency = FloatProperty()
        self.displacement = FloatProperty()
        self.distance_enabled = BoolProperty()

    def calculate(self, arg):
        return voronoi(value_noise_3d, arg, self.seed.get(),
                       frequency=self.frequency.get(),
                       displacement=self.displacement.get(),
                       distance_enabled=self.distance_enabled.get())


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

    print(FloatProperty(10, 0.3, 13.0).to_json())