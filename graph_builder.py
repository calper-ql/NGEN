from random import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.slider import Slider

from kivy.properties import BooleanProperty, ObjectProperty, ColorProperty
from kivy.core.window import Window


from simple_modules import module_pool_class_registry
from simple_modules import *


class ModuleWidget(Widget):
    def __init__(self, pos_lu, module):
        Widget.__init__(self)
        self.module = module
        #with self.canvas:
        #    Rectangle(color=(1, 0, 0, 1), pos=pos, size=[30, 30])

        sd = module.to_stripped_dict()
        json_d = json.loads(module.to_json())

        pos = pos_lu.copy()
        pos[0] += 50
        pos[1] += 80
        size = [300, 0]

        for key in sd:
            if isinstance(sd[key], (int, float)):
                size[1] -= 30

        with self.canvas:
            Color(1., 0, 0)
            Rectangle(pos=pos, size=size)

        pos = pos_lu.copy()
        pos[0] += 150

        l = Label(text=json_d['type'].replace("Module", ""), 
            pos=pos,
            color=[1, 1, 1, 1],
            size_hint=(1.0, 1.0),
            halign="left", valign="center")
        self.add_widget(l)

        pos = pos_lu.copy()
        pos[0] += 100
        pos[1] -= 30

        
        for key in sd:
            if isinstance(sd[key], (int, float)):
                s = Slider(min=sd[key]-100, max=sd[key]+100, value=sd[key], 
                    pos=pos, width=200)
                self.add_widget(s)
                pos[1] -= 30
                size[1] -= 30

    


#https://gist.github.com/opqopq/15c707dc4cffc2b6455f
class HoverButton(Button):
    hovered = BooleanProperty(False)
    border_point= ObjectProperty(None)
    '''Contains the last relevant point received by the Hoverable. This can
    be used in `on_enter` or `on_leave` in order to know where was dispatched the event.
    '''

    def __init__(self, **kwargs):
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)
        super(HoverButton, self).__init__(**kwargs)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return # do proceed if I'm not displayed <=> If have no parent
        pos = args[1]
        #Next line to_widget allow to compensate for relative layout
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            #We have already done what was needed
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    def on_enter(self):
        pass

    def on_leave(self):
        pass


class SelectionButton(HoverButton):
    def on_enter(self):
        self.last_color = self.background_color
        self.background_color = (0, 0, 1, 1)

    def on_leave(self):
        self.background_color = self.last_color


class CanvasWidget(Widget):
    def __init__(self, **args):
        Widget.__init__(self, **args)

        self.modulePool = ModulePool()
        self.widgets = []
        
        dd = DropDown()
        self.dd = dd

        for item in module_pool_class_registry:
            converted_item = item.replace("Module", "")
            print(item)

            mb = SelectionButton(text=converted_item, text_size=(None, 20), 
                size_hint_y=None, size_hint_x=None, height=20,
                background_color=(80/255, 80/255, 80/255, 1),
                background_normal='',)

            mb.item = item
            mb.bind(on_press=lambda btn: dd.select(btn.item))

            dd.add_widget(mb)
            

        dd_button = SelectionButton(text="+", size_hint=(50, 50), height=50, 
            background_color=(80/255, 80/255, 80/255, 1),
            background_normal='', font_size="36px")
        dd_button.allowed = False
        dd_button.bind(on_release=dd.open)
        dd.bind(on_select=lambda instance, x: self.add_module(x))
        self.add_widget(dd_button)

    def add_module(self, identifier):
        print(identifier)
        module = module_pool_class_registry[identifier](self.modulePool)
        mw = ModuleWidget([100, 100], module)
        self.widgets.append(mw)
        self.add_widget(mw)


class NGENModuleApp(App):
    def build(self):
        parent = CanvasWidget()
        return parent


if __name__ == '__main__':
    NGENModuleApp().run()
