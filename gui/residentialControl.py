#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication, QDesktopWidget,
    QLabel, QLCDNumber, QGridLayout)
from PyQt5.QtGui import (QIcon, QFont)

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        

    def initUI(self):
        panicButton = QPushButton('PÂNICO', self)
        panicButton.resize(panicButton.sizeHint())
        panicButton.clicked.connect(self.panicButtonClicked)

        tempLabel = QLabel('Temperatura')
        lumLabels = [QLabel('Luminosidade 1'), QLabel('Luminosidade 2')]
        lightSwitchLabel = QLabel('Acender/Desligar Luz')
        gateSwitchLabel = QLabel('Abrir/Fechar Portão')

        self.tempLCD = QLCDNumber()
        self.lumLCD = [QLCDNumber(), QLCDNumber()]
        
        lightSwitch = QPushButton("Ligar", self)
        lightSwitch.resize(lightSwitch.sizeHint())
        lightSwitch.clicked.connect(self.lightSwitchClicked)
        self.lightSwitchState = False

        gateSwitch = QPushButton("Abrir", self)
        gateSwitch.resize(gateSwitch.sizeHint())
        gateSwitch.clicked.connect(self.gateSwitchClicked)
        self.gateSwitchState = False

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(tempLabel, 1, 0)
        grid.addWidget(self.tempLCD, 1, 1)
        
        grid.addWidget(lumLabels[0], 2, 0)
        grid.addWidget(self.lumLCD[0], 2, 1)

        grid.addWidget(lumLabels[1], 3, 0)
        grid.addWidget(self.lumLCD[1], 3, 1)

        grid.addWidget(lightSwitchLabel, 4, 0)
        grid.addWidget(lightSwitch, 4, 1)

        grid.addWidget(gateSwitchLabel, 5, 0)
        grid.addWidget(gateSwitch, 5, 1)

        grid.addWidget(panicButton, 6, 1)
        
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)

        self.setWindowIcon(QIcon('imgs/shouse.png'))
        self.setWindowTitle('Controle Residencial')
        self.center()
        self.show()


    def panicButtonClicked(self):
        print(f'{self.sender().text()} was pressed')
        return

    def lightSwitchClicked(self):
        print(f'{self.sender().text()} was pressed')

        self.sender().setText("Ligar" if self.lightSwitchState else "Desligar")
        self.lightSwitchState = not self.lightSwitchState
    
    def gateSwitchClicked(self):
        print(f'{self.sender().text()} was pressed')

        self.sender().setText("Abrir" if self.gateSwitchState else "Fechar")
        self.gateSwitchState = not self.gateSwitchState
        self.sender().setChecked(False)
    
    def luminosityChanged(idx, self):
        return

    def temperatureChanged(self):
        return

    def center(self):   
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow()

    number = input("Type a number: ")
    ex.tempLCD.display(number)

    sys.exit(app.exec_())
