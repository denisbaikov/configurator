import re
import os, sys
import configparser
import pyautogui 


from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import (QWidget, QDialog, QApplication, QDesktopWidget, QMessageBox, QSizePolicy, \
                             QLabel, QGridLayout, QVBoxLayout, QFrame, QTextEdit, QPushButton, QLineEdit, \
                             QTreeWidgetItem, QSpacerItem, QSizePolicy)


class MyWindow( QDialog ):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.flagFullScreen = False
        self.current = 0
        self.pressed = False

        path = '.' + os.path.sep + 'ui'
        sys.path.append(path)
        window = __import__("windowMain")
        self.ui = window.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pbFullScreen.clicked.connect( self.windowFullScreen )
        self.ui.pbRoll.clicked.connect( self.windowRoll )
        self.ui.pbClose.clicked.connect( self.windowClose )

        self.setWindowTitle("Configurator")
        self.setupIcon()

        self.setMyStyleSheet()                
        self.loadModules()
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)


    def setupIcon(self):
        path = 'ui' + os.path.sep + 'mainWindow.ico'
        self.setWindowIcon( QtGui.QIcon(path) )
        pixmapIcon = QtGui.QPixmap( path )
        w = self.ui.labelIcon.width()
        h = self.ui.labelIcon.height()
        self.ui.labelIcon.setPixmap( pixmapIcon.scaled(w, h, QtCore.Qt.KeepAspectRatio) )
        
    def setMyStyleSheet(self):
        try:
            path = 'ui' + os.path.sep + 'styleSheet'
            fileWithStyle = open( path, "r" )
        except:
            print( "Error! Do not find file 'ui/styleSheet'" )
        else:
            with fileWithStyle:
                myStyleSheet = fileWithStyle.read()
                self.setStyleSheet( myStyleSheet )

    def loadModules(self):

        self.modulesList = []
        self.modulesWindow = {}

        modulesDir = '.' + os.path.sep + 'modules'

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

            button = QPushButton()
            button.setMinimumSize(200, 30)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            button.setText( self.modulesList[0].modulename() )
            button.clicked.connect( self.showModelsWindow )
            self.ui.verticalLayout.addWidget( button )

            self.modulesWindow.setdefault( button, self.modulesList[0].moduleWindowClass())
            self.modulesWindow.get(button).hide()

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)        
        self.ui.verticalLayout.addSpacerItem(spacer)


    def showModelsWindow(self):
        sender = self.sender()
        module  = self.modulesWindow.get(sender)
        if module != None:
            child = self.ui.verticalLayout_2.takeAt(0)
            while child != None:                
                widget = child.widget()
                if widget != None:
                    self.ui.verticalLayout_2.removeWidget(widget);
                    widget.hide()
                child = self.ui.verticalLayout_2.takeAt(0)
            
            self.ui.verticalLayout_2.addWidget( module )
            spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding);
            self.ui.verticalLayout_2.addSpacerItem(spacer)
            module.show()
            module.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.ui.scrollArea.setWidgetResizable(True)
            self.ui.scrollArea.adjustSize()

            newMainWindowWidth = module.geometry().width()
            newMainWindowWidth += self.ui.verticalLayout.geometry().width() + 80

            self.resize( newMainWindowWidth , self.geometry().height() )

    def windowRoll(self):
        self.showMinimized()
        
    def windowFullScreen(self):
        if self.flagFullScreen:
            self.flagFullScreen = False
            self.showNormal()
        else:
            self.showFullScreen()
            self.flagFullScreen = True
        
    def windowClose(self):
        sys.exit()

    '''def mousePressEvent(self, event):
        #pyautogui.keyDown('alt')
        print('Press ')
        #self.pressed = True
        #self.current = self.mapFromGlobal(QtGui.QCursor.pos()) #event.pos()

    def mouseReleaseEvent(self, event):
        print('Release')
        #pyautogui.press('alt')
        #pyautogui.keyUp('alt')
        #pyautogui.press('alt')
        #self.pressed = False
        #self.current = QtCore.QPoint(-1, -1)'''

    def mouseMoveEvent(self, event):
        if self.pressed == True:
            if event.buttons() == QtCore.Qt.LeftButton:             
                self.move(self.mapToGlobal( self.mapFromGlobal(QtGui.QCursor.pos()) - self.current) )
                print('QtCore.QCursor.pos()', self.mapFromGlobal(QtGui.QCursor.pos()))                
                print('self.current', self.current)
                print('global', self.mapToGlobal( self.mapFromGlobal(QtGui.QCursor.pos()) - self.current) )
                print('#############')


    def eventFilter(self, obj, event):
        if obj == self.ui.frameTitleBar and event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.windowFullScreen()        
        elif obj == self.ui.frameTitleBar and event.type() == QtCore.QEvent.MouseButtonPress:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.pressed = True
                self.current = self.mapFromGlobal(QtGui.QCursor.pos())
                print('MouseButtonPress')
        elif obj == self.ui.frameTitleBar and event.type() == QtCore.QEvent.MouseButtonRelease:
            self.pressed = False
            self.current = QtCore.QPoint(-1, -1)
            print('MouseButtonRelease')
            
        return super(MyWindow, self).eventFilter(obj, event)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    app.installEventFilter(w) 
    sys.exit(app.exec_())



