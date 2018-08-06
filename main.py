'''
Created on 8 дек. 2017 г.

@author: Greg
'''

# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import uic

from goprocam import GoProCamera
from goprocam import constants

import sys, requests

class MainGui(QMainWindow):
    
    gpCam = 0
    path = "c:/"
    filter = 400
    
    def __init__ (self, parent = None):
        super(MainGui, self).__init__(parent)
        if hasattr(sys, '_MEIPASS'):
            uic.loadUi(getattr(sys, '_MEIPASS') + "\gopro_remote.ui", self)
        else: uic.loadUi("gopro_remote.ui", self)
        
        #==================================SIGNALS======================================
        self.folderButton.clicked.connect(self.open_folder)
        self.powerButton.clicked.connect(self.power)
        self.photoButton.clicked.connect(self.takePhoto)
        #===============================================================================
        
        self.gpCam = GoProCamera.GoPro(constants.gpcontrol)
        self.statusBar().showMessage('scae 2017')
        self.textBrowser.append('>> Please enter the object name, insert filter ' + str(self.filter) + ' nm and press "take photo"')
    
    def open_folder(self):
        self.path = QFileDialog.getExistingDirectory(self, 'Open Folder', 'C:/')
        
    def power(self):
        if self.powerButton.text() == 'power on':
            self.gpCam.power_on()
            self.powerButton.setText('power off')
            self.nameEdit.setDisabled(False)
            self.textBrowser.clear()
            self.textBrowser.append('>> Please enter the object name, insert filter ' + str(self.filter) + ' nm and press "take photo"')
            self.photoButton.setDisabled(False)
        else:
            self.filter = 400
            self.gpCam.power_off()
            self.powerButton.setText('power on')
            self.textBrowser.clear()
            self.textBrowser.append('Camera is off')
            self.photoButton.setDisabled(True)
             
    def takePhoto(self):
        self.nameEdit.setDisabled(True)
        self.photoButton.setDisabled(True)
        self.repaint()
        
        link = self.gpCam.take_photo()
        filename = '/' + self.nameEdit.text() + '_' + str(self.filter) + '.jpg'
        
        file = requests.get(link)
        with open(self.path + filename, "wb") as code:
            code.write(file.content)
        
        self.filter += 50
        self.photoButton.setDisabled(False)
            
        if self.filter == 900:
            self.filter = 400
            self.textBrowser.clear()
            self.textBrowser.append('>> Please enter the object name, insert filter ' + str(self.filter) + ' nm and press "take photo"')
            self.nameEdit.setDisabled(False)
        else:
            self.textBrowser.append('>> Please insert filter ' + str(self.filter) + ' nm and press "take photo"')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainGui = MainGui()
    mainGui.move(app.desktop().screenGeometry().width()//4, app.desktop().screenGeometry().height()//4)
    mainGui.show()
    sys.exit(app.exec_())