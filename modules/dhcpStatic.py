import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QGridLayout, QLabel, QPushButton,\
                             QSizePolicy,  QSpacerItem, QLayoutItem )

class Page1(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.moduleName = "dhcpStatic"
        self.serviceName = "dhcp"
        self.dhcpConfigFile = "/etc/dhcp/dhcpd.conf"

        self.groupCount = 0
        self.groupArray = {}
        self.allObjectsOfSection = {}
        self.ii = 2
        self.gridLayout = QtWidgets.QGridLayout(self)


    def deleteObjectsOfSection(self):
        for section in self.allObjectsOfSection.keys():
            grid = self.allObjectsOfSection.get(section)
            if grid is not None:
                for i in (range(grid.count())):
                     child = grid.takeAt(0)
                     if child.widget() is not None:
                         child.widget().hide()
                         child.widget().deleteLater()
                     if child.spacerItem() is not None:
                         grid.removeItem(child)
                grid.deleteLater()
                self.groupArray.pop(section)
    

    def showGUI(self):
        self. deleteObjectsOfSection()
        self.groupCount = 0
        self.groupArray = {}
        self.allObjectsOfSection = {}
        self.ii = 2
        self.parserConfigFile()

    def parserConfigFile(self):
        count=0
        scriptFile=os.popen('./backend/dhcp_getstatic.sh ' + self.dhcpConfigFile + ' read')
        readData=scriptFile.read()
        stringList = readData.split('\n')

        if stringList[0] == "Error":
            print(readData)
            bb = QPushButton()
            label = QtWidgets.QLabel(self)
            lable.setText("Не найден конфигурационный файл '"+self.dhcpConfigFile+"'")
            self.gridLayout.addWidget(label, 0, 0, 1, 1)
            scriptFile.close()
            return

        saveButton = QPushButton()
        saveButton.setObjectName("buttonSave")
        saveButton.setCheckable(False)
        saveButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        saveButton.setText( "Сохранить настройки" )
        saveButton.setMinimumSize(200, 20);
        saveButton.clicked.connect( self.saveConfig )
        self.gridLayout.addWidget( saveButton, 0, 0, 1, 1)

        addButton = QPushButton()
        addButton.setObjectName("buttonAdd")
        addButton.setCheckable(False)
        addButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        addButton.setText( "Добавить секцию" )
        addButton.setMinimumSize(200, 20);
        addButton.clicked.connect( self.addUI )
        self.gridLayout.addWidget( addButton, 0, 1, 1, 1)

        line = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(line.sizePolicy().hasHeightForWidth())
        line.setSizePolicy(sizePolicy)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.gridLayout.addWidget(line, 1, 0, 1, 2)


        spacer = QSpacerItem(0, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacer, *(2, 0), 1, 1)

        self.ii=3


        len_count = len(stringList)
        i=int(0)
        while i < len_count-1:
            self.addUI(0, stringList[i], stringList[i+1], stringList[i+2])
            i+=3
        scriptFile.close()



    def saveConfig(self):
        arr=str('')
        for item in self.groupArray.keys():
            for i in self.groupArray.get(item):
                arr += " " + i.text()
        print("arr = ", arr)

        scriptFile=os.popen('./backend/dhcp_getstatic.sh ' + self.dhcpConfigFile + ' write' + arr)
        readData=scriptFile.read()
        stringList = readData.split('\n')

        if stringList[0] == "Error":
            print(readData)
            bb = QPushButton()
            label = QtWidgets.QLabel(self)
            lable.setText("Не найден конфигурационный файл")
            self.gridLayout.addWidget(label, 0, 0, 1, 1)
            scriptFile.close()
            return



    def addUI(self, dummy, hostname="add", mac="add", ip="add"):
        gridLayout_2 = QtWidgets.QGridLayout()
        #gridLayout_2.setObjectName("gridLayout_2")
        gridLayout = QtWidgets.QGridLayout()
        #gridLayout.setObjectName("gridLayout")

        button = QPushButton()
        button.setObjectName("buttonDelete")
        button.setCheckable(False)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        button.setText( "Удалить секцию" )
        button.setMinimumSize(200, 20);
        #button.setMaximumSize(200, 20);
        button.clicked.connect( self.deleteSection )
        gridLayout.addWidget( button, 0, 2, 1, 2)

        label = QtWidgets.QLabel()
        #label.setObjectName("label")
        gridLayout.addWidget(label, 1, 0, 1, 1)

        lineEdit = QtWidgets.QLineEdit()
        lineEdit.setMinimumSize(QtCore.QSize(400, 0))
        #lineEdit.setObjectName("lineEdit")
        gridLayout.addWidget(lineEdit, 1, 1, 1, 3)

        lineEdit_2 = QtWidgets.QLineEdit()
        lineEdit_2.setMinimumSize(QtCore.QSize(400, 0))
        #lineEdit_2.setObjectName("lineEdit_2")
        gridLayout.addWidget(lineEdit_2, 2, 1, 1, 3)

        label_2 = QtWidgets.QLabel()
        #label_2.setObjectName("label_2")
        gridLayout.addWidget(label_2, 2, 0, 1, 1)
        label_3 = QtWidgets.QLabel()
        #label_3.setObjectName("label_3")
        gridLayout.addWidget(label_3, 3, 0, 1, 1)
        lineEdit_3 = QtWidgets.QLineEdit()
        lineEdit_3.setMinimumSize(QtCore.QSize(400, 0))
        lineEdit_3.setObjectName("lineEdit_3")
        gridLayout.addWidget(lineEdit_3, 3, 1, 1, 3)

        line = QtWidgets.QFrame()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(line.sizePolicy().hasHeightForWidth())
        line.setSizePolicy(sizePolicy)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)

        spacer = QSpacerItem(0, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        gridLayout.addItem(spacer, *(5, 0), 1, 3)

        gridLayout.addWidget(line, 4, 0, 1, 4)
        gridLayout_2.addLayout(gridLayout, 0, 0, 1, 1)

        self.gridLayout.addLayout(gridLayout_2, self.ii, 0, 1, 4)
        self.ii += 1

        label.setText("Имя хоста")
        label_2.setText("MAC адрес")
        label_3.setText("IP адрес")
        lineEdit.setText(str(hostname))
        lineEdit_2.setText(str(mac))
        lineEdit_3.setText(str(ip))

        self.groupArray.setdefault(button, [])
        self.groupArray.get(button).insert(0, lineEdit_3)
        self.groupArray.get(button).insert(0, lineEdit_2)
        self.groupArray.get(button).insert(0, lineEdit)
        self.groupCount += 1

        self.allObjectsOfSection.setdefault(button, gridLayout)


    def deleteSection(self):
        sender = self.sender()
        grid = self.allObjectsOfSection.get(sender)
        if grid is not None:
             for i in reversed(range(grid.count())):
                 print(i)
                 child = grid.takeAt(0)
                 if child.widget() is not None:
                     child.widget().hide()
                     child.widget().deleteLater()
                 if child.spacerItem() is not None:
                     grid.removeItem(child)

             grid.deleteLater()
             self.groupArray.pop(sender)
             self.allObjectsOfSection.pop(sender)

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
