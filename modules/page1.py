import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QApplication)

class Page1(QWidget):
    

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.moduleName = "Page1"

        sys.path.append("./ui/")
        window = __import__("windowPage1")

        self.ui = window.Ui_Form()        
        self.ui.setupUi(self)


def modulename():
    aa = Page1()
    return aa.moduleName
 
def mywindow(parent):
    aa = Page1(parent)
    return aa

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Page1()
    sys.exit(app.exec_())

