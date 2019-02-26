from tkinter import *
from InternalComponents import *
from InternalComponents import selection_panel_module_info
from ngen import *

class AddModule(Module):
    def __init__(self, id):
        Module.__init__(self, id)
        self.A = Input(self)
        self.B = Input(self)
        self.C = Output(self)

    def calculate(self, arg):
         return self.A.get(arg) + self.B.get(arg)

class AddModuleController(ModuleController):
    def __init__(self, mp):
        ModuleController.__init__(self, mp, 100, 70)
        self.module = AddModule(mp.get_id())
        self.mp = mp
        self.items = []
        self.text = mp.canvas.create_text(50, 35, text="+", font="System 20 bold")
        self.register_move(self.text)
        self.AC = IOController(mp, self, self.module.A, [10, 10])
        self.BC = IOController(mp, self, self.module.B, [10, 40])
        self.CC = IOController(mp, self, self.module.C, [70, 10])
        
    def coords(self, x, y):
        ModuleController.coords(self, x, y)
        self.mp.canvas.coords(self.text, x+50, y+35)
        self.AC.coords(x, y)
        self.BC.coords(x, y)
        self.CC.coords(x, y)

selection_panel_module_info.append(["+", AddModuleController, "System 20 bold"])


class SubModule(Module):
    def __init__(self, id):
        Module.__init__(self, id)
        self.A = Input(self)
        self.B = Input(self)
        self.C = Output(self)

    def calculate(self, arg):
         return self.A.get(arg) - self.B.get(arg)

class SubModuleController(ModuleController):
    def __init__(self, mp):
        ModuleController.__init__(self, mp, 100, 70)
        self.module = SubModule(mp.get_id())
        self.mp = mp
        self.items = []
        self.text = mp.canvas.create_text(50, 35, text="-", font="System 20 bold")
        self.register_move(self.text)
        self.AC = IOController(mp, self, self.module.A, [10, 10])
        self.BC = IOController(mp, self, self.module.B, [10, 40])
        self.CC = IOController(mp, self, self.module.C, [70, 10])
        
    def coords(self, x, y):
        ModuleController.coords(self, x, y)
        self.mp.canvas.coords(self.text, x+50, y+35)
        self.AC.coords(x, y)
        self.BC.coords(x, y)
        self.CC.coords(x, y)

selection_panel_module_info.append(["-", SubModuleController, "System 20 bold"])


class PerlinModule(Module):
    def __init__(self, id):
        Module.__init__(self, id)
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

class PerlinModuleController(ModuleController):
    def __init__(self, mp):
        ModuleController.__init__(self, mp, 250, 200)
        self.module = PerlinModule(mp.get_id())
        self.AC = IOController(mp, self, self.module.A, [100+70+50, 10])
        self.mp = mp
        self.items = []
        self.text = mp.canvas.create_text(40, 20, text="PERLIN", font="System 15 bold")
        self.register_move(self.text)
        self.seed_box = IntegerValueBox(self, self.module.seed, [140, 50])
        self.seed_box_text = mp.canvas.create_text(30, 50, text="SEED", font="System 15 bold")
        self.octave_box = IntegerValueBox(self, self.module.octave, [140, 50+30])
        self.octave_box_text = mp.canvas.create_text(37, 50+30, text="OCTAVE", font="System 15 bold")
        self.frequency_slider = Slider(self, 60, 50+60, 140, 0.1, 10, value_pos=100+70)
        self.frequency_slider_text = mp.canvas.create_text(30, 50, text="FREQ", font="System 15 bold")
        self.lacunarcity_slider = Slider(self, 60, 80+60, 140, 1.0, 3.0, value_pos=100+70)
        self.lacunarcity_slider_text = mp.canvas.create_text(30, 50, text="LAC", font="System 15 bold")
        self.persistance_slider = Slider(self, 60, 110+60, 140, 0.001, 1.0, value_pos=100+70)
        self.persistance_slider_text = mp.canvas.create_text(30, 50, text="PERS", font="System 15 bold")
        self.frequency_slider.set_range(0.1, self.module.frequency, 100)
        self.lacunarcity_slider.set_range(1.0, self.module.lacunarity, 3.0)
        self.persistance_slider.set_range(0.0, self.module.persistance, 1.0)
        
    def coords(self, x, y):
        ModuleController.coords(self, x, y)
        self.mp.canvas.coords(self.text, x+40, y+20)
        self.AC.coords(x, y)
        self.frequency_slider.coords(x, y)
        self.lacunarcity_slider.coords(x, y)
        self.persistance_slider.coords(x, y)
        self.mp.canvas.coords(self.frequency_slider_text, x+30, y+50+60)
        self.mp.canvas.coords(self.lacunarcity_slider_text, x+30, y+80+60)
        self.mp.canvas.coords(self.persistance_slider_text, x+30, y+110+60)
        self.seed_box.coords(x, y)
        self.octave_box.coords(x, y)
        self.mp.canvas.coords(self.seed_box_text, x+30, y+50)
        self.mp.canvas.coords(self.octave_box_text, x+37, y+50+30)

    def update(self):
        self.frequency_slider.update_view()
        self.lacunarcity_slider.update_view()
        self.persistance_slider.update_view()
        self.module.frequency = self.frequency_slider.value
        self.module.lacunarity = self.lacunarcity_slider.value
        self.module.persistance = self.persistance_slider.value
        self.module.seed = self.seed_box.value
        if self.octave_box.value > 20:
            self.octave_box.set_value(20)
        self.module.octave = self.octave_box.value
        self.mp.value_update()

selection_panel_module_info.append(["Perlin", PerlinModuleController, "System 12 bold"])


class RiggedMultiModule(Module):
    def __init__(self, id):
        Module.__init__(self, id)
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
            offset=self.offset
            )


class RiggedMultiModuleController(ModuleController):
    def __init__(self, mp):
        ModuleController.__init__(self, mp, 250, 220)
        self.module = RiggedMultiModule(mp.get_id())
        self.AC = IOController(mp, self, self.module.A, [100+70+50, 10])
        self.mp = mp
        self.items = []
        self.text = mp.canvas.create_text(40, 20, text="RIGMULT", font="System 15 bold")
        self.register_move(self.text)
        self.seed_box = IntegerValueBox(self, self.module.seed, [140, 50])
        self.seed_box_text = mp.canvas.create_text(30, 50, text="SEED", font="System 15 bold")
        self.octave_box = IntegerValueBox(self, self.module.octave, [140, 50+30])
        self.octave_box_text = mp.canvas.create_text(37, 50+30, text="OCTAVE", font="System 15 bold")
        self.frequency_slider = Slider(self, 60, 50+60, 140, 0.1, 10, value_pos=100+70)
        self.frequency_slider_text = mp.canvas.create_text(30, 50, text="FREQ", font="System 15 bold")
        self.lacunarcity_slider = Slider(self, 60, 80+60, 140, 1.0, 3.0, value_pos=100+70)
        self.lacunarcity_slider_text = mp.canvas.create_text(30, 50, text="LAC", font="System 15 bold")
        self.exp_slider = Slider(self, 60, 110+60, 140, 0.001, 1.0, value_pos=100+70)
        self.exp_slider_text = mp.canvas.create_text(30, 50, text="EXP", font="System 15 bold")
        self.offset_slider = Slider(self, 60, 110+90, 140, 0.001, 1.0, value_pos=100+70)
        self.offset_slider_text = mp.canvas.create_text(30, 50, text="OFFSET", font="System 15 bold")
        self.frequency_slider.set_range(0.1, self.module.frequency, 100)
        self.lacunarcity_slider.set_range(1.0, self.module.lacunarity, 3.0)
        self.exp_slider.set_range(-1.0, self.module.exp, 0.0)
        self.offset_slider.set_range(-1.0, self.module.offset, 1.0)
        
    def coords(self, x, y):
        ModuleController.coords(self, x, y)
        self.mp.canvas.coords(self.text, x+40, y+20)
        self.AC.coords(x, y)
        self.frequency_slider.coords(x, y)
        self.lacunarcity_slider.coords(x, y)
        self.exp_slider.coords(x, y)
        self.offset_slider.coords(x, y)
        self.mp.canvas.coords(self.frequency_slider_text, x+30, y+50+60)
        self.mp.canvas.coords(self.lacunarcity_slider_text, x+30, y+80+60)
        self.mp.canvas.coords(self.exp_slider_text, x+30, y+110+60)
        self.mp.canvas.coords(self.offset_slider_text, x+30, y+110+60+30)
        self.seed_box.coords(x, y)
        self.octave_box.coords(x, y)
        self.mp.canvas.coords(self.seed_box_text, x+30, y+50)
        self.mp.canvas.coords(self.octave_box_text, x+37, y+50+30)

    def update(self):
        self.frequency_slider.update_view()
        self.lacunarcity_slider.update_view()
        self.exp_slider.update_view()
        self.offset_slider.update_view()
        self.module.frequency = self.frequency_slider.value
        self.module.lacunarity = self.lacunarcity_slider.value
        self.module.exp = self.exp_slider.value
        self.module.offset = self.offset_slider.value
        self.module.seed = self.seed_box.value
        if self.octave_box.value > 20:
            self.octave_box.set_value(20)
        self.module.octave = self.octave_box.value
        self.mp.value_update()

selection_panel_module_info.append(["RiggedMulti", RiggedMultiModuleController, "System 12 bold"])


class SelectModule(Module):
    def __init__(self, id):
        Module.__init__(self, id)
        self.control = Input(self)
        self.A = Input(self)
        self.B = Input(self)
        self.output = Output(self)
        self.bound = 0.0
        self.falloff = 0.1
        self.cutoff = 0.0
    
    def calculate(self, arg):
        ctrl = self.control.get(arg) - self.cutoff
        lin_val = (ctrl+self.falloff)/((2*self.falloff))
        val = self.A.get(arg) * lin_val + self.B.get(arg)  * (self.bound-lin_val)
        return val 

class SelectModuleController(ModuleController):
    def __init__(self, mp):
        ModuleController.__init__(self, mp, 280, 130)
        self.module = SelectModule(mp.get_id())
        self.mp = mp
        self.items = []
        self.text = mp.canvas.create_text(70, 20, text="Select", font="System 12 bold")
        self.register_move(self.text)
        self.control = IOController(mp, self, self.module.control, [10, 10])
        self.A = IOController(mp, self, self.module.A, [10, 40])
        self.B = IOController(mp, self, self.module.B, [10, 70])
        self.output = IOController(mp, self, self.module.output, [250, 10])
        self.bound_slider = Slider(self, 100, 50, 120, value_pos=160)
        self.bound_slider_text = mp.canvas.create_text(70, 50, text="BOUND", font="System 15 bold")
        self.falloff_slider = Slider(self, 100, 80, 120, value_pos=160)
        self.falloff_slider_text = mp.canvas.create_text(70, 50, text="FALL", font="System 15 bold")
        self.cutoff_slider = Slider(self, 50, 110, 170, value_pos=190)
        self.cutoff_slider_text = mp.canvas.create_text(70, 80, text="CUT", font="System 15 bold")
        self.bound_slider.set_range(0.0, self.module.bound, 10.0)
        self.falloff_slider.set_range(0.0, self.module.falloff, 1.0)
        self.cutoff_slider.set_range(-3.0, self.module.cutoff, 3.0)

    def coords(self, x, y):
        ModuleController.coords(self, x, y)
        self.mp.canvas.coords(self.text, x+70, y+20)
        self.control.coords(x, y)
        self.A.coords(x, y)
        self.B.coords(x, y)
        self.output.coords(x, y)
        self.bound_slider.coords(x, y)
        self.falloff_slider.coords(x, y)
        self.cutoff_slider.coords(x, y)
        self.mp.canvas.coords(self.bound_slider_text, x+70, y+50)
        self.mp.canvas.coords(self.falloff_slider_text, x+70, y+80)
        self.mp.canvas.coords(self.cutoff_slider_text, x+30, y+110)

    def update(self):
        self.bound_slider.update_view()
        self.falloff_slider.update_view()
        self.cutoff_slider.update_view()
        self.module.bound = self.bound_slider.value
        self.module.falloff = self.falloff_slider.value
        self.module.cutoff = self.cutoff_slider.value
        self.mp.value_update()


selection_panel_module_info.append(["Select", SelectModuleController, "System 12 bold"])


class VoronoiModule(Module):
    def __init__(self, id):
        Module.__init__(self, id)
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


class VoronoiModuleController(ModuleController):
    def __init__(self, mp):
        ModuleController.__init__(self, mp, 250, 130)
        self.module = VoronoiModule(mp.get_id())
        self.AC = IOController(mp, self, self.module.output, [100+70+50, 10])
        self.mp = mp
        self.items = []
        self.text = mp.canvas.create_text(40, 20, text="VORONOI", font="System 15 bold")
        self.register_move(self.text)
        self.seed_box = IntegerValueBox(self, self.module.seed, [100, 50])
        self.seed_box_text = mp.canvas.create_text(30, 40, text="SEED", font="System 15 bold")
        self.disp_box = CheckBox(self, [200, 40])
        self.disp_box_text = mp.canvas.create_text(140+30, 50, text="DISP", font="System 15 bold")
        self.frequency_slider = Slider(self, 60, 50+30, 140, value_pos=100+70)
        self.frequency_slider_text = mp.canvas.create_text(30, 50+30, text="FREQ", font="System 15 bold")
        self.frequency_slider.set_range(0.1, self.module.frequency, 10.0)
        self.disp_slider = Slider(self, 60, 50+60, 140, value_pos=100+70)
        self.disp_slider_text = mp.canvas.create_text(30, 50+60, text="DISP", font="System 15 bold")
        self.disp_slider.set_range(0.0, self.module.frequency, 3.0)

    def coords(self, x, y):
        ModuleController.coords(self, x, y)
        self.mp.canvas.coords(self.text, x+40, y+20)
        self.AC.coords(x, y)
        self.seed_box.coords(x, y)
        self.mp.canvas.coords(self.seed_box_text, x+30, y+50)
        self.disp_box.coords(x, y)
        self.mp.canvas.coords(self.disp_box_text, x+140+30, y+50)
        self.frequency_slider.coords(x, y)
        self.mp.canvas.coords(self.frequency_slider_text, x+30, y+50+30)
        self.disp_slider.coords(x, y)
        self.mp.canvas.coords(self.disp_slider_text, x+30, y+50+60)


    def update(self):
        self.module.seed = self.seed_box.value
        self.module.distance_enabled = self.disp_box.value
        self.module.frequency = self.frequency_slider.value
        self.module.displacement = self.disp_slider.value
        self.mp.value_update()

selection_panel_module_info.append(["Voronoi", VoronoiModuleController, "System 12 bold"])