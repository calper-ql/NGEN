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
        self.addModule = AddModule(mp.get_id())
        self.mp = mp
        self.items = []
        self.text = mp.canvas.create_text(50, 35, text="+", font="System 20 bold")
        self.register_move(self.text)
        self.AC = IOController(mp, self, self.addModule.A, [10, 10])
        self.BC = IOController(mp, self, self.addModule.B, [10, 40])
        self.CC = IOController(mp, self, self.addModule.C, [70, 10])
        
    def coords(self, x, y):
        ModuleController.coords(self, x, y)
        self.mp.canvas.coords(self.text, x+50, y+35)
        self.AC.coords(x, y)
        self.BC.coords(x, y)
        self.CC.coords(x, y)

selection_panel_module_info.append(["+", AddModuleController, "System 20 bold"])


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
