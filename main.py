import re
import os, sys
import configparser
import pyautogui 
import subprocess

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import (QWidget, QDialog, QApplication, QDesktopWidget, QMessageBox, QSizePolicy, \
                             QLabel, QGridLayout, QVBoxLayout, QHBoxLayout, QFrame, QTextEdit, QPushButton, QToolButton, \
                             QLineEdit, QTreeWidgetItem, QSpacerItem, QSizePolicy)

defineMenuButtonMain        = 1
defineMenuButtonSatellite   = 2


class ClickableFrame( QFrame ):
    clicked = QtCore.pyqtSignal()
 
    def mouseReleaseEvent(self, event):
        QFrame.mouseReleaseEvent(self, event)
        self.clicked.emit()


class MyWindow( QDialog ):
    def __init__(self, fakeTotleBar=None):
        super(MyWindow, self).__init__()


        self.rowsMainButtons = 0
        self.flagFullScreen = False
        self.current = 0
        self.pressed = False
        self.levelListMainButton = [[], [], []]

        self.modulesWindow = {}
        self.moduleSatellites = {}
        self.ignoreModules = [] 

        path = '.' + os.path.sep + 'ui'
        sys.path.append(path)
        window = __import__("windowMain")
        self.ui = window.Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("Configurator")
        self.setMyStyleSheet()
        self.loadModules()

        path = './ui' + os.path.sep + 'mainWindow.ico'
        self.setWindowIcon( QtGui.QIcon(path) )

        if fakeTotleBar is not None:
            self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
            self.ui.pbFullScreen.clicked.connect( self.windowFullScreen )
            self.ui.pbRoll.clicked.connect( self.windowRoll )
            self.ui.pbClose.clicked.connect( self.windowClose )
            self.setupIconFakeTitle()
        else:
            self.ui.frameTitleBar.hide()
            self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowMinimizeButtonHint| QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowCloseButtonHint )
            self.setContentsMargins(0,9,0,0)


    def setupIconFakeTitle(self):
        path = 'ui' + os.path.sep + 'mainWindow.ico'
        self.setWindowIcon( QtGui.QIcon(path) )
        pixmapIcon = QtGui.QPixmap( path )
        w = self.ui.labelIcon.width()
        h = self.ui.labelIcon.height()
        self.ui.labelIcon.setPixmap( pixmapIcon.scaled(w, h, QtCore.Qt.KeepAspectRatio) )

    def setMyStyleSheet(self):
        try:
            path = '.' + os.path.sep + 'ui' + os.path.sep + 'qssMain'
            fileWithStyle = open( path, "r" )
        except:
            print( "Error! Do not find file 'ui/qssMain'" )
        else:
            with fileWithStyle:
                myStyleSheet = fileWithStyle.read()
                self.setStyleSheet( myStyleSheet )

    def loadModules(self):
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

            if self.ignoreModules.count(moduleName) > 0:
                print( "No satellites" )
                continue
            
            self.addMenuButton(moduleName)

        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.gridLayout_2.addItem( spacer, *(self.rowsMainButtons, 0), 1, 3)
        

    def addMenuButton(self, moduleName):
        #self.modulesList.insert( 0, __import__(moduleName) )
        self.ignoreModules.insert(0, moduleName)
        
        currentModule = __import__(moduleName)
      
        menuButton = QPushButton()
        menuButton.setCheckable(True)
        #menuButton.setMinimumSize(200, 32)
        #menuButton.setMaximumSize(200, 32)
        menuButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
      
        #menuButton.setText( self.modulesList[0].getModuleName() )
        menuButton.setText( currentModule.getModuleName() )
        menuButton.clicked.connect( self.showModelsWindow )
        menuButton.clicked.connect( self.uncheckOtherButtons )
        #path = '.\\' + os.path.sep + 'ui\\' + os.path.sep + 'icon_' + name[:-3] + '.png'
        path = '.\\' + os.path.sep + 'ui\\' + os.path.sep + 'icon_' + moduleName + '.png'
        menuButton.setStyleSheet("QPushButton{"\
                                 "padding: 0 0 2px;"\
                                 "font: 16px \"Trebuchet MS\", Tahoma, Arial, sans-serif;"\
                                 "outline: none;"\
                                 "position: relative;"\
                                 "border-radius: 5px;"\
                                 "color: #555;"\
                                 "border: 1px solid #BBB;"\
                                 "border-top: 1px solid #D0D0D0;"\
                                 "border-bottom: 1px solid #A5A5A5;"\
                                 "background: url('"+ path + "') no-repeat top left;"\
                                 "background-color: rgb(220, 220, 220);"\
                                 "}"\
                                 "QPushButton:pressed, QPushButton:checked {"\
                                 "font: 19px \"Trebuchet MS\", Tahoma, Arial, sans-serif;"\
                                 "background:  QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop:0 rgb(250, 250, 250),"\
                                              "stop: 1 rgb(255, 255, 255)) url('"+ path + "') no-repeat top left; }"\
                                 "}"\
                                 "QPushButton:hover{"\
                                 "background:  QLinearGradient(x1: 0, y1: 0, x2: 0, y2: 1, stop:0 rgb(150, 150, 150),"\
                                              "stop: 1 rgb(255, 255, 255)) url('"+ path + "') no-repeat top left;"\
                                 "}"  )

        moduleLevel = currentModule.getModuleLevel()
        if moduleLevel == 0:
            self.ui.gridLayout_2.addWidget( menuButton, *(self.rowsMainButtons, 0), 1, 2, QtCore.Qt.AlignRight)
            menuButton.setMinimumSize(230, 32)
            menuButton.setMaximumSize(230, 32)        
        elif moduleLevel == 1:
            self.ui.gridLayout_2.addWidget( menuButton, *(self.rowsMainButtons, 1), 1, 1, QtCore.Qt.AlignRight)
            menuButton.setMinimumSize(200, 32)
            menuButton.setMaximumSize(200, 32)
        

        self.levelListMainButton[moduleLevel].insert(0, menuButton)
        self.rowsMainButtons += 1

        self.modulesWindow.setdefault( menuButton, currentModule.getModuleWindowClass() )
        self.modulesWindow.get(menuButton).hide()

        satellites = currentModule.getSatelliteModules()
        if satellites:
            self.moduleSatellites.setdefault( menuButton, [])
            for satellite in satellites:
                self.moduleSatellites.get(menuButton).insert( 0, self.addMenuButton(satellite)  )
        else:
            self.moduleSatellites.setdefault(  menuButton, [])

        return menuButton
    
    def changeVisibleButton(self, button):
        print("button = ", button)
        if button.isVisible():
            button.hide()
            self.FixMainButton.setChecked(False)
            self.modulesWindow.get( self.FixMainButton).hide()
        else:
            button.show()


    def uncheckOtherButtons(self):
        senderButton = self.sender()
        for menuButton in self.modulesWindow.keys():
            if menuButton == senderButton:
                menuButton.setChecked(True)
                if menuButton == self.FixMainButton:
                    satelliteList = self.moduleSatellites.get(menuButton)
                    if satelliteList:
                        print(satelliteList)
                        for ii in satelliteList:
                            self.changeVisibleButton(ii)
            else:
                if menuButton == self.FixMainButton:
                    continue
                
                satelliteList = self.moduleSatellites.get(menuButton)
                if satelliteList:
                    for ii in satelliteList:
                        ii.hide()
                menuButton.setChecked(False)
                    

    def showModelsWindow(self):
        sender = self.sender()

        if self.levelListMainButton[0].count(sender) > 0:
            self.FixMainButton = sender
        
        module  = self.modulesWindow.get(sender)
        if module is not None:
            command = "rpm -qc {0}".format( module.serviceName )
            pipe = os.popen(command)
            requestRes = pipe.read()
            badRequestResult = requestRes.find("не установлен")
            if  badRequestResult != -1:
                QMessageBox.information(self, "Configurator", "Сервис {0} не установлен!".format( module.serviceName ), QMessageBox.Ok)
                return
            child = self.ui.verticalLayout_2.takeAt(0)
            while child is not None:
                widget = child.widget()
                if widget is not None:
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
            newMainWindowWidth += self.ui.gridLayout_2.geometry().width() + 80

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

    def mouseMoveEvent(self, event):
        if self.pressed == True:
            if event.buttons() == QtCore.Qt.LeftButton:             
                self.move(self.mapToGlobal( self.mapFromGlobal(QtGui.QCursor.pos()) - self.current) )
                '''print('QtCore.QCursor.pos()', self.mapFromGlobal(QtGui.QCursor.pos()))                
                print('self.current', self.current)
                print('global', self.mapToGlobal( self.mapFromGlobal(QtGui.QCursor.pos()) - self.current) )
                print('#############')'''


    def eventFilter(self, obj, event):
        if obj == self.ui.frameTitleBar and event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.windowFullScreen()        
        elif obj == self.ui.frameTitleBar and event.type() == QtCore.QEvent.MouseButtonPress:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.pressed = True
                self.current = self.mapFromGlobal(QtGui.QCursor.pos())
                #print('MouseButtonPress')
        elif obj == self.ui.frameTitleBar and event.type() == QtCore.QEvent.MouseButtonRelease:
            self.pressed = False
            self.current = QtCore.QPoint(-1, -1)
            #print('MouseButtonRelease')
            
        return super(MyWindow, self).eventFilter(obj, event)



if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    if len (sys.argv) >= 2:
        w = MyWindow( sys.argv[1] )
    else:
        w = MyWindow()
    w.show()
    app.installEventFilter(w) 
    sys.exit(app.exec_())

