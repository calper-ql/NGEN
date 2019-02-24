# NGEN
NGEN is a procedural generation library that uses vectorization in python to generate values depending on a computational graph

NGEN utilizes various noise techniques such as Perlin Noise or Voronoi Noise. NGEN also comes with a built in graph creation UI and the ability to save and load graphs.

## How does it work ?
NGEN has the following components:
* Module
* Input
* Output

(Following capture is from an early development phase and will be updated when full functionality is implemented)

![Imgur](https://i.imgur.com/KgGaXmi.gif)

# Module
A module is a base class that wraps a set of inputs and outputs. Here is a simple module:

```Python
class AddModule(Module):
    def __init__(self, id):
        Module.__init__(self, id)
        self.A = Input(self)
        self.B = Input(self)
        self.C = Output(self)

    def calculate(self, arg):
         return self.A.get(arg) + self.B.get(arg)
```

Inputs and outputs can be created and the module will override the calculate function. Each module can have a multiple inputs and outputs but it will direct the singular computation result to each output so there are no reasons to use multiple outputs.

The computation library used for this project is 
[CuPy](https://cupy.chainer.org/) 
<p align="center">
<img src="https://cupy.chainer.org/images/cupy.png" style="background-color:#000000;" >
</p>

However this can be quickly swapped with regular 
[numpy](http://www.numpy.org/). How to do so will be explained soon.

# UI
NGEN can be extended both in core level and UI
Here is an example for the AddModule:

```Python
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

# register for the left panel
selection_panel_module_info.append(["+", AddModuleController, "System 20 bold"])
```

Any new module core and controller can be added to the SimpleModules.py