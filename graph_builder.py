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
from simple_modules import module_pool_class_registry


class ModuleWidget(Widget):
    def __init__(self, pos):
        Widget.__init__(self)
        with self.canvas:
            Rectangle(color=(1, 0, 0, 1), pos=pos, size=[30, 30])

    def on_touch_down(self, touch):
        print(touch)


class CanvasWidget(Widget):
    def __init__(self, **args):
        Widget.__init__(self, **args)
        
        dd = DropDown()
        self.dd = dd
        for item in module_pool_class_registry:
            mb = Button(text=item, size_hint_y=None, height=44)
            mb.bind(on_release=lambda btn: dd.select(mb.text))
            dd.add_widget(mb)
            print(item)

        dd_button = Button(text="+", size_hint=(None, None))
        dd_button.bind(on_release=dd.open)
        dd.bind(on_select=lambda instance, x: setattr(dd_button, 'text', x))
        self.add_widget(dd_button)

    def on_touch_down(self, touch):
        Widget.on_touch_down(self, touch)
        print(touch)
        #self.add_widget(ModuleWidget(pos=touch.pos))



class NGENModuleApp(App):
    def build(self):
        parent = CanvasWidget()

        return parent


if __name__ == '__main__':
    NGENModuleApp().run()
