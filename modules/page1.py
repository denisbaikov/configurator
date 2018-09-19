import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QApplication)



class Page1(QWidget):
    

    def __init__(self):

        QWidget.__init__(self)
        #super(Page1, self).__init__(parent) 
        #self.moduleName = "Page1"

        sys.path.append("./ui/")
        window = __import__("windowPage1")

        self.ui = window.Ui_Form()        
        self.ui.setupUi(self)


moduleName = "Page 1"
myClass = Page1()

def moduleWindowClass():
    return myClass

def modulename():
    return moduleName



