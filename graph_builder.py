from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QFrame, QMenuBar, QMainWindow, QMenu
from PyQt5.QtCore import Qt, QRect, QSize, QPoint, QRectF
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QListWidget, QGridLayout, QSlider
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtGui import QPainterPath, QRegion, QLinearGradient
from core import module_pool_class_registry, ModulePool, Module

from simple_modules import *
import sys

class QArgPushButton(QPushButton):
    def __init__(self, text, arg):
        super().__init__(text)
        self.arg = arg
        self.callback = None
        self.clicked.connect(self.on_click)
    
    def on_click(self):
        if self.callback:
            self.callback(self)


class ModuleWidget(QFrame):
    def __init__(self, parent, module, pos):
        super().__init__(parent)
        self.module = module
        self.parent = parent
    
        self.move(pos)

        raw_json = module.to_json()
        stripped_json = module.to_stripped_dict()
        input_dict = self.module.get_input_names()
        output_dict = self.module.get_output_names()
        print(stripped_json)

        panel_layout = QGridLayout(self)
        panel_layout.cellRect(max(len(input_dict), len(stripped_json))+1, 5)

        lbl = QLabel(raw_json['type'])
        panel_layout.addWidget(lbl, 0, 0, 1, 3)

        self.input_lbls = {}
        self.output_lbls = {}

        for index, inp in enumerate(input_dict):
            lbl = QArgPushButton(input_dict[inp], inp)
            p = lbl.palette()
            p.setColor(lbl.backgroundRole(), QtGui.QColor(63, 82, 255))
            lbl.setPalette(p)
            lbl.setAutoFillBackground(True)
            panel_layout.addWidget(lbl, index+1, 0, 1, 1)
            self.input_lbls[inp] = lbl
            def on_click(btn):
                self.parent.select(btn)
            lbl.callback = on_click

        for index, prop in enumerate(stripped_json):
            sl = QSlider(Qt.Horizontal)
            if len(input_dict) > 0 and len(output_dict) > 0:
                panel_layout.addWidget(sl, index+1, 1, 1, 3)
            elif len(input_dict) == 0 and len(output_dict) > 0:
                panel_layout.addWidget(sl, index+1, 0, 1, 4)
            elif len(input_dict) > 0 and len(output_dict) == 0:
                panel_layout.addWidget(sl, index+1, 1, 1, 3)
            else:
                panel_layout.addWidget(sl, index+1, 0, 1, 5)

        for index, out in enumerate(output_dict):
            lbl = QArgPushButton(output_dict[out], out)
            p = lbl.palette()
            p.setColor(lbl.backgroundRole(), QtGui.QColor(255, 104, 112))
            lbl.setPalette(p)
            lbl.setAutoFillBackground(True)
            panel_layout.addWidget(lbl, index+1, 4, 1, 1)
            self.output_lbls[out] = lbl 
            def on_click(btn):
                self.parent.select(btn)
            lbl.callback = on_click
            
        width = 0
        if len(input_dict) > 0:
            width += 60
        if len(stripped_json) > 0:
            width += 200
        if len(output_dict) > 0:
            width += 60 
        height = (max(len(input_dict), len(stripped_json))+1) * 30
        self.setGeometry(pos.x(), pos.y(), width, height)
    
        self.show()

    def paintEvent(self, ev):
        painter = QPainter(self)
        #painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        gradient = QLinearGradient(QRectF(self.rect()).topLeft(),QRectF(self.rect()).bottomLeft())
        gradient.setColorAt(0.0, QtGui.QColor(51, 153, 102))
        gradient.setColorAt(0.5, QtGui.QColor(0, 153, 51))
        painter.setBrush(gradient)
        painter.drawRoundedRect(self.rect(), 8.0, 8.0)
        #painter.end()

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()
        super(ModuleWidget, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() == QtCore.Qt.LeftButton:
                currPos = self.mapToGlobal(self.pos())
                globalPos = event.globalPos()
                diff = globalPos - self.__mouseMovePos
                newPos = self.mapFromGlobal(currPos + diff)
                self.move(newPos)
                self.__mouseMovePos = globalPos
            super(ModuleWidget, self).mouseMoveEvent(event)
            self.parent.repaint()
        except:
            pass

    def mouseReleaseEvent(self, event):
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return
        super(ModuleWidget, self).mouseReleaseEvent(event)


class Builder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'NGEN BUILDER'
        self.setGeometry(100, 100, 1000, 1000)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor(0, 0, 0))
        self.setPalette(p)
        self.setAutoFillBackground(True)
        self.show()
        self.mp = ModulePool()
        self.moduleWidgets = {}
        self.reverseModuleWidgets = {}
        self.reset_selection()

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        actions = {}
        for item in module_pool_class_registry:
            actions[contextMenu.addAction(item)] = item
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action is not None:
            mod = module_pool_class_registry[actions[action]](self.mp)
            mw = ModuleWidget(self, mod, event.pos())
            self.moduleWidgets[mod] = mw
            self.reverseModuleWidgets[mw] = mod
        self.repaint()

    def select(self, btn):
        if btn == self.selected:
            if isinstance(btn.arg, Output):
                return
            elif isinstance(btn.arg, Input):
                btn.arg.disconnect()
        if self.selected:
            if isinstance(btn.arg, Output):
                self.selected.arg.connect(btn.arg)
            elif isinstance(btn.arg, Input):
                pass
            self.reset_selection()
        else:
            if isinstance(btn.arg, Input):
                self.selected = btn
        #print(self.selected)
        self.repaint()

    def reset_selection(self):
        self.selected = None
        self.selected_type = None

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):
        qp.setRenderHint(QPainter.Antialiasing, True)
        pen = QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        for module in self.moduleWidgets:
            mw = self.moduleWidgets[module]
            for inp in mw.input_lbls:
                btn = mw.input_lbls[inp]
                pos = btn.pos() + mw.pos() + QPoint(-10, 
                            btn.size().height()/2.0)
                if inp.connection:
                    mwo = self.moduleWidgets[inp.connection.module]
                    if inp.connection in mwo.output_lbls:
                        btno = mwo.output_lbls[inp.connection]
                        pos2 = btno.pos() + mwo.pos() + QPoint(btno.size().width()+10, 
                            btno.size().height()/2.0)
                        pen.setStyle(QtCore.Qt.DashLine)
                        qp.setPen(pen)
                        qp.drawLine(pos.x(), pos.y(), pos2.x(), pos2.y())

        pen = QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)                
        
        qp.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
        for module in self.moduleWidgets:
            mw = self.moduleWidgets[module]
            for inp in mw.input_lbls:
                btn = mw.input_lbls[inp]
                pos = btn.pos() + mw.pos() + QPoint(-10, 
                            btn.size().height()/2.0)
                qp.drawEllipse(pos.x()-5, pos.y()-7, 15, 15)

        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        for module in self.moduleWidgets:
            mw = self.moduleWidgets[module]
            for out in mw.output_lbls:
                btn = mw.output_lbls[out]
                pos = btn.pos() + mw.pos() + QPoint(btn.size().width(), 
                            btn.size().height()/2.0)
                qp.drawEllipse(pos.x(), pos.y()-7, 15, 15)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MiddleButton:
            print()
            print()
            bt_d = json.dumps(self.mp.to_json())
            td_d = json.loads(bt_d)
            json_d = json.dumps(td_d, indent=4, sort_keys=True)
            print(json_d)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Builder()
    app.exec_()