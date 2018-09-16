import re
import os, sys
import configparser


from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import (QWidget, QDialog, QApplication, QDesktopWidget, QMessageBox, QSizePolicy, \
                             QLabel, QGridLayout, QVBoxLayout, QFrame, QTextEdit, QPushButton, QLineEdit, \
                             QTreeWidgetItem, QSpacerItem, QSizePolicy)


class MyWindow( QDialog ):
    def __init__(self):
        super(MyWindow, self).__init__()
        
        sys.path.append("./ui/")
        window = __import__("windowMain")
        self.ui = window.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.setWindowTitle("Configurator")
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
        
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.ui.verticalLayout.addSpacerItem(spacer)


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
            self.resize(self.minimumSize())
    
    
def main():
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()



