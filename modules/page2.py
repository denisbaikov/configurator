import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QApplication)

class Page2(QWidget):
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        #super(Page2, self).__init__(parent) 
        self.moduleName = "Page2"

        sys.path.append("./ui/")
        window = __import__("windowPage2")

        self.ui = window.Ui_Form()        
        self.ui.setupUi(self)

moduleName = "Page 2"
myClass = Page2()

def moduleWindowClass():
    return myClass

def modulename():
    return moduleName

