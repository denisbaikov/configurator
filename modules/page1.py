import re
import sys
import os
import configparser

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QMessageBox, QSizePolicy, \
                             QLabel, QGridLayout, QVBoxLayout, QFrame, QTextEdit, QPushButton, QLineEdit)


class Page1(QWidget):
    

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.moduleName = "Page1"
        self.initUI()


    def initUI(self):
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        
        self.pushButton = QtWidgets.QPushButton()
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("1")        
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        
        self.pushButton_2 = QtWidgets.QPushButton()
        self.pushButton_2.setText("2")
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)
        
        self.pushButton_3 = QtWidgets.QPushButton()
        self.pushButton_3.setText("3")
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 0, 1, 1)
        
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.setLayout(self.gridLayout_2)
        self.show()
        #return self


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

