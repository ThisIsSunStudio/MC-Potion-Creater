from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QFileDialog, QButtonGroup, QListWidgetItem, QMenu, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QAction, QCursor, QIcon, QMouseEvent
from qt_material import apply_stylesheet, list_themes
import os, ctypes, webbrowser
from time import *

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

uiLoader = QUiLoader()

class ExceedError(Exception):
    pass

class Application:
    def __init__(self):
        self.ui = uiLoader.load("./ui.ui")

        unitButtonGroup = QButtonGroup(window)
        unitButtonGroup.addButton(self.ui.useTickButton, 1)
        unitButtonGroup.addButton(self.ui.useSecondButton, 2)

        beaconButtonGroup = QButtonGroup(window)
        beaconButtonGroup.addButton(self.ui.beaconRadioButton, 1)
        beaconButtonGroup.addButton(self.ui.unbeaconRadioButton, 2)

        particlesButtonGroup = QButtonGroup(window)
        particlesButtonGroup.addButton(self.ui.particlesRadioButton, 1)
        particlesButtonGroup.addButton(self.ui.noParticlesRadioButton, 2)

        iconButtonGroup = QButtonGroup(window)
        iconButtonGroup.addButton(self.ui.iconRadioButton, 1)
        iconButtonGroup.addButton(self.ui.noIconRadioButton, 2)

        self.ui.useTickButton.setChecked(True)
        self.ui.unbeaconRadioButton.setChecked(True)
        self.ui.particlesRadioButton.setChecked(True)
        self.ui.iconRadioButton.setChecked(True)

        self.ui.idFindButton.clicked.connect(
            lambda: webbrowser.open_new(
                "https://zh.minecraft.wiki/w/%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C#%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C%E5%88%97%E8%A1%A8"
            )
        )
        self.ui.addButton.clicked.connect(
            lambda : self.potionCreate(
                self.ui.idLineEdit.text(),
                self.ui.timeSpinBox.value(),
                self.ui.useTickButton.isChecked(),
                self.ui.levelSpinBox.value(),
                self.ui.beaconRadioButton.isChecked(),
                self.ui.particlesRadioButton.isChecked(),
                self.ui.iconRadioButton.isChecked(),
            )
        )
        self.ui.deleteButton.clicked.connect(self.takeListItem)
        self.ui.createButton.clicked.connect(self.commandCreate)
      
    def potionCreate(self,id,time,unit,level,isBeacon,particles,icon):
        potionString = '{' + f'id:{id},duration:{ time if unit else time*20 },amplifier:{level-1}'
        if isBeacon==True:
            potionString = potionString + f',ambient:true'
        if particles==False:
            potionString = potionString + f',show_particles:false'
        if icon==False:
            potionString = potionString + f',show_icon:false'
        potionString+='}'
        self.ui.potionList.addItem(potionString)
        timeString = strftime("[%Y-%m-%d %X]\n", localtime())
        info = timeString + f'Add Potion\nPotion:{potionString}\n\n'
        self.addTextInInfoEdit(info)
        
    def commandCreate(self):
        player = self.ui.playerLineEdit.text()
        other = self.ui.otherLineEdit.text()
        color = self.ui.colorLineEdit.text()
        potion = []
        for i in range(self.ui.potionList.count()):
            potion.append(self.ui.potionList.item(i).text())
        allPotion=''
        for i in potion:
            allPotion += i
            if i != potion[-1]:
                allPotion += ','
        if color=='':
            command = f'/give {player} minecraft:potion[minecraft:potion_contents:{'{'}custom_effects:[{allPotion}]{'}'}'
        else:
            command = f'/give {player} minecraft:potion[minecraft:potion_contents:{'{'}custom_color:{color},custom_effects:[{allPotion}]{'}'}'
        if other=='':
            command += ']'
        else:
            command += f',{other}]'
        self.ui.commandEdit.setPlainText(command)
    
    def addTextInInfoEdit(self,text):
        string = self.ui.infoEdit.toPlainText()
        self.ui.infoEdit.setPlainText(text+string)

    def takeListItem(self):
        timeString = strftime("[%Y-%m-%d %X]\n", localtime())
        info = timeString + f'Delete Potion\nRow:{self.ui.potionList.currentRow()}\nPotion:{self.ui.potionList.item(self.ui.potionList.currentRow()).text()}\n\n'
        self.addTextInInfoEdit(info)
        self.ui.potionList.takeItem(self.ui.potionList.currentRow())
    
window = QApplication([])
app = Application()

window.setWindowIcon(QIcon("./ico.png"))

extra = {"font_family": "Smiley Sans"}
apply_stylesheet(window, theme="dark_cyan.xml", extra=extra)

app.ui.show()
window.exec()
