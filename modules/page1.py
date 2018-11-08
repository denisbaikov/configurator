import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QApplication)



class Page1(QWidget):
    

    def __init__(self):

        QWidget.__init__(self)
        self.moduleName = "Page1"
        self.serviceName = "sshd"

        sys.path.append("./ui/")
        window = __import__("windowPage1")

        self.ui = window.Ui_Form()        
        self.ui.setupUi(self)
        self.showGUI()

    def showGUI(self):
        print()


moduleName = "Page 1"
myClass = Page1()
satelliteModules = ['data1', 'flag1']
moduleLevel = 0

def getModuleWindowClass():
    return myClass

def getModuleName():
    return moduleName

def getSatelliteModules():
    return satelliteModules

def getModuleLevel():
    return moduleLevel

