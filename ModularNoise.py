from tkinter import *
from SimpleModules import *

class SelectionButton:
    def __init__(self, mng, root, x, y, command=None, text="", image=None, font="System 8 bold"):
        self.root = root
        self.mng = mng
        self.x = x
        self.y = y
        self.frame = Frame(bg="#00FF00")
        self.frame.place(x=x, y=y, width=94, height=44)
        self.frame.bind("<ButtonPress-1>", self.on_press)
        self.frame.bind("<B1-Motion>", self.on_move)
        self.frame.bind("<ButtonRelease-1>", self.on_release)
        self.command = command
        
        self.label = Label(self.frame, text=text, bg="#00FF00", font=font)
        self.label.pack()
        
        self.pressed = False

    def on_press(self, event):
        if self.command:
            self.mng.inject(self.command)

    def on_move(self, event):
        if self.command:
            self.mng.inject_move(event.x-100, event.y)

    def on_release(self, event):
        if self.command:
            self.mng.inject_finish()


class SelectionPanel:
    def __init__(self, mng):
        self.mng = mng
        self.frame = Frame(bg="#000000")
        self.frame.place(x=0, y=0, width=100, height=100)
        self.on_resize(None)
        
    def register_modules(self):
        y = 5
        for mi in selection_panel_module_info:
            print(mi)
            SelectionButton(self.mng, self.frame, x=3, y=y,
                text=mi[0], 
                command=mi[1], 
                font=mi[2])
            y+=50


    def on_resize(self, event):
        self.frame.place(x=0, y=0, width=100, height=self.mng.master.winfo_height())

class ModulePanel:
    def __init__(self, mng, callback=None):
        self.mng = mng
        self.canvas = Canvas(width=100, height=100, bg="#383838")
        self.on_resize(None)
        self.selected = None
        self.select_type = None
        self.canvas.bind("<ButtonRelease-1>", self.on_empty_click)
        self.outputModule = None
        self.callback_value = None
        self.callback = callback
        self.current_id = 0

    def on_resize(self, event):
        self.canvas.place(x=100, y=0, width=self.mng.master.winfo_width()-100, height=self.mng.master.winfo_height())
        
    def on_empty_click(self, event):
        pass

    def reset(self):
        self.selected = None
        self.select_type = None
        self.value_update()

    def value_update(self):
        if self.callback:
            if self.outputModule:
                self.outputModule.reset()
                out = self.outputModule.calculate(self.callback_value)
                self.callback(out)

    def get_id(self):
        val = self.current_id
        self.current_id += 1
        return val


class ModularNoiseGUI():
    def __init__(self, master, callback=None):
        self.master = master
        master.title("Modular Noise")
        master.configure(background='#383838')
        master.geometry("600x400")

        master.bind("<Configure>", self.on_resize)

        self.modulePanel = ModulePanel(self, callback=callback)
        self.selectionPanel = SelectionPanel(self)
        self.selectionPanel.register_modules()
        
        self.modules = []
        self.injecting_module = None

    def on_resize(self, event):
        self.selectionPanel.on_resize(event)
        self.modulePanel.on_resize(event)

    def inject_move(self, x, y):
        if self.injecting_module != None:
            self.injecting_module.coords(x, y)

    def inject_finish(self):
        self.modules.append(self.injecting_module)
        self.injecting_module = None

    def inject_out(self):
        if self.modulePanel.outputModule:
            self.injecting_module = self.modulePanel.outputModule
        else:
            self.injecting_module = OutputModuleController(self.modulePanel)
            self.modulePanel.outputModule = self.injecting_module
        
    def inject(self, moduleController):
        if moduleController == OutputModuleController:
            if self.modulePanel.outputModule is None:
                self.injecting_module = moduleController(self.modulePanel)
        else:
            self.injecting_module = moduleController(self.modulePanel)
        
if __name__=='__main__':

    import cv2
    x = create_point_grid([0, 0, 0], [0.5, 0, 0], [0.5, 1, 0], [0, 1, 0], 500, 250)

    def cb(y):
        if y is not None:
            y = scale(y)
            cv2.imshow("y", cp.asnumpy(y))
            cv2.waitKey(1)

    root = Tk()
    my_gui = ModularNoiseGUI(root, callback=cb)
    my_gui.modulePanel.callback_value = x
    root.mainloop()