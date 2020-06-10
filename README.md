# NGEN

Inspired by [libnoise](http://libnoise.sourceforge.net/)

NGEN is a procedural generation library that uses vectorization in python to generate values depending on a computational graph

NGEN utilizes various noise techniques such as Perlin Noise or Voronoi Noise. NGEN also comes with a built in graph creation UI and the ability to save and load graphs.

## How does it work ?
NGEN has the following components:
* ModulePool
* Module
* Input
* Output

Also some basic properties:
* SeedProperty
* BoolProperty
* IntProperty
* FloatProperty

## Computation Graph
![Imgur](https://i.imgur.com/GP6Dx6V.png)
## Result
### Perlin -> Perlin -> RiggedMulti -> Selective(control as first Perlin)
![Imgur](https://i.imgur.com/nKtFKqa.png)

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

Any new module core and controller can be added to the SimpleModules.py

If written with pure NGEN components, A UI interface for a given Module will be automatically rendered. In addition to this the module can be saved and loaded onto json,  Here is an example with Voronoi Noise:

```Python
class VoronoiModule(Module):
    def __init__(self, mp):
        Module.__init__(self, mp)
        self.output = Output(self)
        self.seed = SeedProperty()
        # Float and Int properties use [value, min, max] as constructor args
        self.frequency = FloatProperty(1, 0.5, 100)
        self.displacement = FloatProperty(0.0, 0.0, 1.0)
        self.distance_enabled = BoolProperty()

    def calculate(self, arg):
        # voronoi function seen here is internal... 
        return voronoi(value_noise_3d, arg, self.seed.get(),
                       frequency=self.frequency.get(),
                       displacement=self.displacement.get(),
                       distance_enabled=self.distance_enabled.get())


register_module(VoronoiModule)
```

![Imgur](https://i.imgur.com/kjJWd5a.png)

```Json
{
    "displacement": {
        "max": 1.0,
        "min": 0.0,
        "type": "FloatProperty",
        "value": 0.0
    },
    "distance_enabled": {
        "type": "BoolProperty",
        "value": false
    },
    "frequency": {
        "max": 100,
        "min": 0.5,
        "type": "FloatProperty",
        "value": 1
    },
    "id": 0,
    "inputs": [],
    "outputs": 1,
    "seed": {
        "type": "SeedProperty",
        "value": 42
    },
    "type": "VoronoiModule"
}

```

The computation library used for this project is 
[CuPy](https://cupy.chainer.org/) 
![Cupy](https://raw.githubusercontent.com/cupy/cupy/master/docs/image/cupy_logo_1000px.png)
However this can be quickly swapped with regular 
[numpy](http://www.numpy.org/).

# UI
NGEN can be extended both in core level and UI however the Module definitions can already be rendered without additional code ([Computation Graph](https://i.imgur.com/GP6Dx6V.png))


