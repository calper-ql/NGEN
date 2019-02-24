from tkinter import *
from tkinter import simpledialog
import numpy as np

selection_panel_module_info = []

class Module:
    def __init__(self, id):
        self.id = id
        self.inputs = []

    def calculate(self, arg):
        return np.zeros(shape=arg.shape)

    def __str__(self):
        return str(self.id)

    def reset(self):
        for conn in self.inputs:
            conn.reset()

    def update(self):
        pass


class Connection:
    def __init__(self, input, output):
        self.input = input
        self.output = output

    def remove(self):
        self.input.connection = None
        self.output.connections.remove(self)
        self.input.module.inputs.remove(self)
        self.input = None
        self.output = None

    def __str__(self):
        return "connection " + str(self.input) + " " + str(self.output)

    def get(self, arg):
        return self.output.calculate(arg)

    def reset(self):
        self.output.reset()


class Input:
    def __init__(self, module):
        self.module = module
        self.connection = None

    def get(self, arg):
        if self.connection:
            return self.connection.get(arg)
        else:
            return None


class Output:
    def __init__(self, module):
        self.module = module
        self.connections = []
        self.stored_value = None

    def calculate(self, arg):
        if self.stored_value is None:
            self.stored_value = self.module.calculate(arg)
        return self.stored_value

    def reset(self):
        self.stored_value = None
        self.module.reset()


def make_Connection(input, output):
    conn = Connection(input, output)
    if input.connection:
        input.connection.remove()
    input.connection = conn
    output.connections.append(conn)
    input.module.inputs.append(conn)
    return conn


class ConnectionController:
    def __init__(self, mp, connection, input_c, output_c):
        self.mp = mp
        self.input_c = input_c
        self.output_c = output_c
        self.in_coord = self.mp.canvas.coords(self.input_c.base)
        self.out_coord = self.mp.canvas.coords(self.output_c.base)
        self.line = self.mp.canvas.create_line(self.in_coord[0]+10, self.in_coord[1]+10, 
            self.out_coord[0]+10, self.out_coord[1]+10, fill="white", dash=(4, 4))
        for c in self.input_c.connectionControllers:
            c.remove()
        self.input_c.connectionControllers.append(self)
        self.output_c.connectionControllers.append(self)

    def update(self):
        self.in_coord = self.mp.canvas.coords(self.input_c.base)
        self.out_coord = self.mp.canvas.coords(self.output_c.base)
        self.mp.canvas.coords(self.line, self.in_coord[0]+10, self.in_coord[1]+10, 
            self.out_coord[0]+10, self.out_coord[1]+10)

    def remove(self):
        self.mp.canvas.delete(self.line)
        self.input_c.connectionControllers.remove(self)
        self.output_c.connectionControllers.remove(self)


class ModuleController:
    def __init__(self, mp, width, height):
        self.module = Module(mp.get_id())
        self.mp = mp
        self.items = []
        self.width = width
        self.height = height
        self.fill = "#70a5f9"
        self.base = mp.canvas.create_rectangle(0, 0, self.width, self.height, fill=self.fill)
        self.register_move(self.base)

    def register_move(self, part):
        self.mp.canvas.tag_bind(part, "<ButtonPress-1>", self.move_handler_init)
        self.mp.canvas.tag_bind(part, "<B1-Motion>", self.move_handler)
        
    def move_handler_init(self, event):
        self.mhix = event.x - self.mp.canvas.coords(self.base)[0]
        self.mhiy = event.y - self.mp.canvas.coords(self.base)[1]
    
    def move_handler(self, event):
        x = event.x-self.mhix
        y = event.y-self.mhiy
        self.coords(x, y)
        
    def coords(self, x, y):
        self.mp.canvas.coords(self.base, x, y, x+self.width, y+self.height)


class IOController:
    def __init__(self, mp, mc, io, xy):
        self.mp = mp
        self.x = xy[0]
        self.y = xy[1]
        self.dx = 0
        self.dy = 0
        self.size = 20
        self.io = io
        if isinstance(io, Input):
            self.type = "input"
            self.color = "green"
        else:
            self.type = "output"
            self.color = "red"
        self.select_color = "white"
        self.base = self.mp.canvas.create_rectangle(self.x, self.y, self.x+self.size, self.y+self.size)
        self.reset()
        self.mp.canvas.tag_bind(self.base, "<ButtonPress-1>", self.select)
        self.connectionControllers = []

    def reset(self):
        self.mp.canvas.itemconfig(self.base, fill=self.color)

    def coords(self, dx, dy):
        self.dx = dx
        self.dy = dy
        cx = self.x + self.dx
        cy = self.y + self.dy
        self.mp.canvas.coords(self.base, cx, cy, cx+self.size, cy+self.size)
        for c in self.connectionControllers:
            c.update()

    def select(self, event):
        self.mp.canvas.itemconfig(self.base, fill=self.select_color)
        if self.mp.selected:
            if self.mp.selected == self:
                self.reset()
                self.mp.reset()
                if self.type == "input":
                    if self.io.connection:
                        self.io.connection.remove()
                    for c in self.connectionControllers:
                        c.remove()
            else:
                if self.mp.select_type != self.type:
                    if self.type == "input":
                        conn = make_Connection(self.io, self.mp.selected.io)
                        ConnectionController(self.mp, conn, self, self.mp.selected)
                    else:
                        conn = make_Connection(self.mp.selected.io, self.io)
                        ConnectionController(self.mp, conn, self.mp.selected, self)
                    self.reset()
                    self.mp.selected.reset()
                    self.mp.reset()
        else:
            self.mp.selected = self
            self.mp.select_type = self.type

    
class OutputModule(Module):
    def __init__(self, id):
        Module.__init__(self, id)
        self.A = Input(self)

    def calculate(self, arg):
         return self.A.get(arg)


class OutputModuleController(ModuleController):
    def __init__(self, mp):
        ModuleController.__init__(self, mp, 140, 40)
        self.module = OutputModule(mp.get_id())
        self.mp.outputModule = self.module
        self.mp = mp
        self.items = []
        self.text = mp.canvas.create_text(80, 20, text="OUTPUT", font="System 16 bold")
        self.register_move(self.text)
        self.AC = IOController(mp, self, self.module.A, [10, 10])

    def coords(self, x, y):
        ModuleController.coords(self, x, y)
        self.mp.canvas.coords(self.text, x+80, y+20)
        self.AC.coords(x, y)


class IntegerValueBox:
    def __init__(self, mod, value, xy):
        self.mp = mod.mp
        self.mod = mod
        self.value = value
        self.x = xy[0]
        self.y = xy[1]
        self.last_x = self.x
        self.last_y = self.y
        self.text = self.mp.canvas.create_text(self.x, self.y, text=str(self.value), fill="black")
        self.mp.canvas.tag_bind(self.text, "<ButtonPress-1>", self.get_values)
        self.callback = None

    def coords(self, x, y):
        cx = x+self.x
        cy = y+self.y
        self.last_y = cy
        self.last_x = cx
        self.update_view()

    def set_value(self, value):
        self.value = value
        self.update_view()

    def update_view(self):
        self.mp.canvas.coords(self.text, self.last_x, self.last_y)
        self.mp.canvas.itemconfig(self.text, text=str(self.value))
        
    def get_values(self, event):
        value_answer = simpledialog.askinteger("Input", "Value",
                                initialvalue=self.value,
                                parent=self.mp.mng.master)
        if value_answer is None:
            return
        self.set_value(value_answer)
        if self.callback:
            self.callback()
        self.mod.update()


class MinMaxValueBox:
    def __init__(self, mod, low, high, value, xy, format="{:.2f}"):
        self.mp = mod.mp
        self.mod = mod
        self.low = low
        self.high = high
        self.value = value
        self.x = xy[0]
        self.y = xy[1]
        self.last_x = self.x
        self.last_y = self.y
        self.format = format
        self.text = self.mp.canvas.create_text(self.x, self.y, text=self.format.format(low), fill="black")
        self.mp.canvas.tag_bind(self.text, "<ButtonPress-1>", self.get_values)
        self.callback = None

    def coords(self, x, y):
        cx = x+self.x
        cy = y+self.y
        self.last_y = cy
        self.last_x = cx
        self.update_view()

    def set_value(self, value):
        self.value = value
        if self.value < self.low:
            self.value = self.low
        if self.value > self.high:
            self.value = self.high
        self.update_view()

    def update_view(self):
        self.mp.canvas.coords(self.text, self.last_x, self.last_y)
        self.mp.canvas.itemconfig(self.text, text=self.format.format(self.value))
        
    def get_values(self, event):
        low_answer = simpledialog.askfloat("Input", "Low",
                                initialvalue=self.low,
                                parent=self.mp.mng.master)
        if low_answer is None:
            return
        value_answer = simpledialog.askfloat("Input", "Value",
                                initialvalue=self.value,
                                parent=self.mp.mng.master)
        if value_answer is None:
            return
        if value_answer < low_answer:
            return
        high_answer = simpledialog.askfloat("Input", "High",
                                initialvalue=self.high,
                                parent=self.mp.mng.master)
        if high_answer is None:
            return
        if value_answer > high_answer:
            return
        self.low = low_answer
        self.high = high_answer
        self.set_value(value_answer)
        if self.callback:
            self.callback()
        self.mod.update()

class Slider:
    def __init__(self, mod, x, y, size, low=0, high=100, type='float', value_pos=None):
        self.mod = mod
        self.b_c = [x, y, size]
        self.low = low
        self.high = high
        self.value_pos = value_pos
        self.slide_line = mod.mp.canvas.create_rectangle(x, y-2, x+size, y+2, fill="black")
        self.slide = mod.mp.canvas.create_rectangle(x-4, y-10, x+4, y+10, fill="white")
        if self.value_pos is not None:
            self.mmvb = MinMaxValueBox(mod, low, high, low, [x+self.value_pos, y])
            self.mmvb.callback = self.update_view
        self.mod.mp.canvas.tag_bind(self.slide, "<B1-Motion>", self.slide_func)
        self.last_y = y
        self.last_x = x
        self.value = low
        self.last_diff = 0

    def coords(self, x, y):
        cx = x+self.b_c[0]
        cy = y+self.b_c[1]
        self.last_y = cy
        self.last_x = cx
        if self.value_pos is not None:
            self.mmvb.coords(x, y)
        self.mod.mp.canvas.coords(self.slide_line, cx, cy-2, cx+self.b_c[2], cy+2) 
        self.update_view()

    def set_value(self, value):
        self.mmvb.set_value(value)
        self.value = value
        if self.value < self.low:
            self.value = self.low
        if self.value > self.high:
            self.value = self.high
        self.update_view()
        self.mod.update()

    def set_range(self, low, value, high):
        self.value = value
        self.low = low
        self.high = high
        if self.mmvb:
            self.mmvb.low = low
            self.mmvb.value = value
            self.mmvb.high = high
        self.update_view()

    def update_view(self):
        if self.value_pos:
            self.value = self.mmvb.value
            self.low = self.mmvb.low
            self.high = self.mmvb.high
        normal = (self.value - self.low)/(self.high-self.low)
        diff = normal * self.b_c[2]
        cx = self.last_x+diff
        cy = self.last_y
        self.mod.mp.canvas.coords(self.slide, cx-4, cy-10, cx+4, cy+10)
        if self.value_pos:
            self.mmvb.update_view()

    def slide_func(self, event):
        diff =  event.x - self.last_x
        if diff < 0:
            diff = 0
        if diff > self.b_c[2]:
            diff = self.b_c[2]
        self.last_diff = diff
        normal = diff/self.b_c[2]
        self.value = self.low + normal * (self.high-self.low)
        if self.value_pos:
            self.mmvb.set_value(self.value)
        self.update_view()
        self.mod.update()


#REGISTER OUTPUT MODULE
selection_panel_module_info.append(["OUT", OutputModuleController, "System 12 bold"])