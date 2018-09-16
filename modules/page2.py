import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import (QWidget, QApplication)

class Page2(QWidget):
    
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.moduleName = "Page2"

        sys.path.append("./ui/")
        window = __import__("windowPage2")

        self.ui = window.Ui_Form()        
        self.ui.setupUi(self)
        #self.ui.show()


def modulename():
    aa = Page2()
    return aa.moduleName
 
def mywindow(parent):
    aa = Page2(parent)
    return aa

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Page1()
    sys.exit(app.exec_())

