import re
import os, sys
import configparser
#import page1
#import page3
from mainWindow import Ui_Dialog

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QMessageBox, QSizePolicy, \
                             QLabel, QGridLayout, QVBoxLayout, QFrame, QTextEdit, QPushButton, QLineEdit, \
                             QTreeWidgetItem, QSpacerItem)


class MyWindow( QtWidgets.QDialog):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.ui = Ui_Dialog()        
        self.ui.setupUi(self)

        #self.pushButton = QtWidgets.QPushButton()
        #self.pushButton.setObjectName("pushButton")
        #self.pushButton.setText("1")
        #page1.mywindow()
        #page_1=page3.DHCP(self)
        #self.widget = QtWidgets.QWidget(page_1)
        #self.ui.gridLayout.addWidget(page_1, 0, 1, 1, 1)
        #self.ui.verticalLayout_2.addWidget(page_1)       

        self.loadModules()


    def loadModules(self):

        self.modulesList = []
        self.modulesWindow = {}

        modulesDir = "./modules/"

        if os.path.isdir(modulesDir) == False:
           print( "Error! Not found directory 'modules' with modules!" )
           sys.exit()

        print( "Found directory with modules!" )
        print( "Start reading" )

        sys.path.append(modulesDir)
        for name in os.listdir(modulesDir):
            fullpath = os.path.join( modulesDir, name)

            if os.path.isdir( fullpath ):
                continue

            moduleName = re.sub(r'.py', '', name)
            print( "***  moduleName = ", moduleName )
            self.modulesList.insert( 0, __import__(moduleName) )

            #print( self.modulesList[0].myModuleName() )
            #print( dir(self.modulesList[0]) )

            button = QPushButton()
            button.setText( self.modulesList[0].modulename() )
            button.clicked.connect( self.showModelsWindow )
            self.ui.verticalLayout.addWidget( button )

            #self.ui.verticalLayout_2.addWidget( self.modulesList[0].mywindow() )
            
            self.modulesWindow.setdefault( button, self.modulesList[0] )

        '''button1 = QPushButton()
        button1.setText('Button1')
        self.ui.verticalLayout.addWidget(button1)

        button2 = QPushButton()
        button2.setText('Button2')'''
        
        #self.ui.verticalLayout.addWidget(button2)

        #QSpacerItem *item = new QSpacerItem(1,1, QSizePolicy::Expanding, QSizePolicy::Fixed);
        #hlayout->addSpacerItem(item);
        #QSizePolicy::Expanding, QSizePolicy::Expanding
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.ui.verticalLayout.addSpacerItem(spacer)
        '''topLevelItem = QTreeWidgetItem()
        self.ui.treeView.addTopLevelItem(topLevelItem)
        topLevelItem.setText(0, 'sss')
        item = QTreeWidgetItem(topLevelItem);
        item.setText(0,"Под итем");
        self.ui.treeView.addTopLevelItem(topLevelItem)'''

    def showModelsWindow(self):
        sender = self.sender()
        modelsWindow = self.modulesWindow.get(sender)
        if modelsWindow != None:             
            child = self.ui.verticalLayout_2.takeAt(0)
            while child != None:
                widget = child.widget()
                if widget != None:
                    self.ui.verticalLayout_2.removeWidget(widget);
                    widget.deleteLater()
                    widget = None
                child = self.ui.verticalLayout_2.takeAt(0)

            self.ui.verticalLayout_2.addWidget( modelsWindow.mywindow(self) )
            spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding);
            self.ui.verticalLayout_2.addSpacerItem(spacer)
    
    
def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



