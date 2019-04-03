from core import *
from ngen import *
from core import module_pool_class_registry


def register_module(m):
    module_pool_class_registry[m.__name__] = m

class OutputModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.input = Input(self)
        self.name = StringProperty()

    def calculate(self, arg):
        return self.input.get(arg)

register_module(OutputModule)


class RGBOutputModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.name = StringProperty()
        self.R = Input(self)
        self.G = Input(self)
        self.B = Input(self)
        self.r_mult = FloatProperty(1.0, 0.0, 1.0)
        self.g_mult = FloatProperty(1.0, 0.0, 1.0)
        self.b_mult = FloatProperty(1.0, 0.0, 1.0)

    def calculate(self, arg):
        return [self.R.get(arg)*self.r_mult.value, 
        self.G.get(arg)*self.g_mult.value, 
        self.B.get(arg)*self.b_mult.value]

register_module(RGBOutputModule)


class AddModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.A = Input(self)
        self.B = Input(self)
        self.C = Output(self)

    def calculate(self, arg):
        return self.A.get(arg) + self.B.get(arg)

register_module(AddModule)


class MultiplyModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.A = Input(self)
        self.B = Input(self)
        self.C = Output(self)

    def calculate(self, arg):
        return self.A.get(arg) * self.B.get(arg)

register_module(MultiplyModule)


class SubModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.A = Input(self)
        self.B = Input(self)
        self.C = Output(self)

    def calculate(self, arg):
        return self.A.get(arg) - self.B.get(arg)


register_module(SubModule)


class ConstantModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.output = Output(self)
        self.value = FloatProperty(1.0, -1.0, 1.0)

    def calculate(self, arg):
        return self.value.value

register_module(ConstantModule)


class PerlinModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.output = Output(self)
        self.seed = SeedProperty()
        self.octave = IntProperty(value=4, min=1, max=20)
        self.frequency = FloatProperty(1, 0.5, 100)
        self.lacunarity = FloatProperty(2.0, 1.0, 3.0)
        self.persistance = FloatProperty(0.5, 0.001, 0.999)

    def calculate(self, arg):
        return perlin(gradient_coherent_noise_3d, arg, self.seed.get(), self.octave.get(),
                      frequency=self.frequency.get(),
                      lacunarity=self.lacunarity.get(),
                      persistance=self.persistance.get())


register_module(PerlinModule)


class RiggedMultiModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.output = Output(self)
        self.seed = SeedProperty()
        self.octave = IntProperty(4, 1, 20)
        self.frequency = FloatProperty(1, 0.5, 100)
        self.lacunarity = FloatProperty(2.0, 1.0, 3.0)
        self.exp = FloatProperty(-3.0, 0.0, -3.0)
        self.offset = FloatProperty(0.0, -3.0, 3.0)

    def calculate(self, arg):
        return rigged_multi(gradient_coherent_noise_3d, arg, self.seed.get(), self.octave.get(),
                            frequency=self.frequency.get(),
                            lacunarity=self.lacunarity.get(),
                            exp=self.exp.get(),
                            offset=self.offset.get())


register_module(RiggedMultiModule)


def SCurve5(a):
    a3 = a * a * a
    a4 = a3 * a
    a5 = a4 * a
    return (6.0 * a5) - (15.0 * a4) + (10.0 * a3)

class SelectModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.control = Input(self)
        self.A = Input(self)
        self.B = Input(self)
        self.output = Output(self)
        self.falloff = FloatProperty(0.001, 0.001, 0.9)
        self.low_bound = FloatProperty(0.0, -3.0, 3.0)
        self.high_bound = FloatProperty(1.0, -3.0, 3.0)

    def calculate(self, arg):
        ctrl = self.control.get(arg)
        val = cp.zeros(ctrl.shape)
        a_val = self.A.get(arg)
        b_val = self.B.get(arg)
        
        lb = self.low_bound.get()
        fo = self.falloff.get()
        hb = self.high_bound.get()

        mask1 = ctrl < lb-fo
        mask2 = cp.logical_xor(ctrl < lb+fo, mask1)
        mask3 = cp.logical_xor(ctrl < hb-fo, ctrl < lb+fo)
        mask4 = cp.logical_xor(ctrl < hb+fo, ctrl < hb-fo)
        mask5 = ctrl >= hb+fo

        #mask2 = ctrl >= high_curve
        #mask3 = cp.logical_not(p.logical_or(mask1, mask2))

        alpha1 = SCurve5((ctrl - (lb-fo))/((lb+fo) - (lb-fo)))[mask2]
        alpha2 = SCurve5((ctrl - (hb-fo))/((hb+fo) - (hb-fo)))[mask4]

        val[mask1] = a_val[mask1]
        val[mask2] = b_val[mask2] * alpha1 + a_val[mask2] * (1.0 - alpha1)
        val[mask3] = b_val[mask3]
        val[mask4] = a_val[mask4] * alpha2 + b_val[mask4] * (1.0 - alpha2)
        val[mask5] = a_val[mask5]


        
        #val[mask3] = a_val[mask3] * alpha + b_val[mask3] * (1.0 - alpha)


        return val


        #lin_val = (ctrl + self.falloff.get()) / ((2 * self.falloff.get()))
        #val = self.A.get(arg) * lin_val + self.B.get(arg) * (self.bound.get() - lin_val)
        #return val


register_module(SelectModule)


class VoronoiModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.output = Output(self)
        self.seed = SeedProperty()
        self.frequency = FloatProperty(1, 0.5, 100)
        self.displacement = FloatProperty(0.0, 0.0, 1.0)
        self.distance_enabled = BoolProperty()

    def calculate(self, arg):
        return voronoi(value_noise_3d, arg, self.seed.get(),
                       frequency=self.frequency.get(),
                       displacement=self.displacement.get(),
                       distance_enabled=self.distance_enabled.get())


register_module(VoronoiModule)

class RadNormModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.output = Output(self)
        self.input = Input(self)

    def calculate(self, arg):
        return self.input.get(radnorm_arg(arg))  


register_module(RadNormModule)

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