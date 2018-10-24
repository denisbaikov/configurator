import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QGridLayout, QLabel)

class Page1(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.moduleName = "dhcpStatic"
        self.serviceName = "dhcp"

        self.ii = 0
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.parserConfigFile()

    def parserConfigFile(self):
        count=0
        scriptFile=os.popen('../backend/dhcp_getstatic.sh /etc/dhcp/dhcpd.conf')
        readData=scriptFile.read()
        
        stringList = readData.split('\n')
        
        if stringList[0] == "Error":
            print(readData)
            label = QtWidgets.QLabel(self)
            lable.setText("Не найден конфигурационный файл")
            self.gridLayout.addWidget(label, 0, 0, 1, 1)
            scriptFile.close()
            return
            
        len_count = len(stringList)
        i=int(0)
        while i < len_count-1:
            #host.setdefault(stringList[i], [stringList[i+1], stringList[i+2]])
            #i+=3
            self.addUI(stringList[i], stringList[i+1], stringList[i+2])
            i+=3
        scriptFile.close()

    def addUI(self, hostname, mac, ip):
        gridLayout_2 = QtWidgets.QGridLayout(self)
        gridLayout_2.setObjectName("gridLayout_2")
        gridLayout = QtWidgets.QGridLayout(self)
        gridLayout.setObjectName("gridLayout")
        label = QtWidgets.QLabel(self)
        label.setObjectName("label")
        gridLayout.addWidget(label, 0, 0, 1, 1)
        lineEdit = QtWidgets.QLineEdit(self)
        lineEdit.setMinimumSize(QtCore.QSize(400, 0))
        lineEdit.setObjectName("lineEdit")
        gridLayout.addWidget(lineEdit, 0, 1, 1, 1)
        lineEdit_2 = QtWidgets.QLineEdit(self)
        lineEdit_2.setMinimumSize(QtCore.QSize(400, 0))
        lineEdit_2.setObjectName("lineEdit_2")
        gridLayout.addWidget(lineEdit_2, 1, 1, 1, 1)
        label_2 = QtWidgets.QLabel(self)
        label_2.setObjectName("label_2")
        gridLayout.addWidget(label_2, 1, 0, 1, 1)
        label_3 = QtWidgets.QLabel(self)
        label_3.setObjectName("label_3")
        gridLayout.addWidget(label_3, 2, 0, 1, 1)
        lineEdit_3 = QtWidgets.QLineEdit(self)
        lineEdit_3.setMinimumSize(QtCore.QSize(400, 0))
        lineEdit_3.setObjectName("lineEdit_3")
        gridLayout.addWidget(lineEdit_3, 2, 1, 1, 1)
        
        line = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(line.sizePolicy().hasHeightForWidth())
        line.setSizePolicy(sizePolicy)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        
        gridLayout.addWidget(line, 3, 0, 1, 2)
        gridLayout_2.addLayout(gridLayout, 0, 0, 1, 1)
        self.gridLayout.addLayout(gridLayout_2, self.ii, 0, 1, 1)
        self.ii += 1

        label.setText("Имя хоста")
        label_2.setText("MAC адрес")
        label_3.setText("IP адрес")
        lineEdit.setText(hostname)
        lineEdit_2.setText(mac)
        lineEdit_3.setText(ip)


moduleName = "dhcpStatic"
myClass = Page1()
satelliteModules = []
moduleLevel = 1

def getModuleWindowClass():
    return myClass

def getModuleName():
    return moduleName

def getSatelliteModules():
    return satelliteModules

def getModuleLevel():
    return moduleLevel


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Page1()
    sys.exit(app.exec_())

