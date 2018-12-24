#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication, QDesktopWidget,
    QLabel, QLCDNumber, QGridLayout, QLineEdit,
    QHBoxLayout)
from PyQt5.QtGui import (QIcon, QFont, QColor)
from PyQt5.QtCore import (QSize)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        

    def initUI(self):
        self.panicButton = QPushButton('PÂNICO', self)
        self.panicButton.resize(self.panicButton.sizeHint())
        self.panicButton.clicked.connect(self.panicButtonClicked)

        self.modeSwitch = QPushButton('MANUAL', self)
        self.modeSwitch.resize(self.modeSwitch.sizeHint())
        self.modeSwitch.clicked.connect(self.modeSwitchClicked)
        self.modeSwitchState = True

        self.tempLabel = QLabel('Temperatura')
        self.lightSwitchLabel = QLabel('Luz Interna')
        self.lightSwitch2Label = QLabel('Luz Externa')
        self.gateSwitchLabel = QLabel('Portão')
        self.serialInLabel = QLabel('Último dado recebido')
        self.serialOutLabel = QLabel('Último dado enviado')

        self.tempLCD = QLCDNumber()
        self.setTempThreshold = QLineEdit()
        self.setTempThresholdButton = QPushButton('DEFINIR', self)
        self.setTempThresholdButton.clicked.connect(self.temperatureChanged)

        self.airCondSwitch = QPushButton(self)
        self.airCondSwitch.resize(self.airCondSwitch.sizeHint())
        self.airCondSwitch.clicked.connect(self.airCondSwitchClicked)
        self.airCondSwitch.setIcon(QIcon('imgs/airoff.png'))
        self.airCondSwitch.setIconSize(QSize(51,51))
        self.airCondSwitchState = False
        
        self.lightSwitch = QPushButton('', self)
        self.lightSwitch.resize(self.lightSwitch.sizeHint())
        self.lightSwitch.clicked.connect(self.lightSwitchClicked)
        self.lightSwitch.setIcon(QIcon('imgs/luzoff.png'))
        self.lightSwitch.setIconSize(QSize(51,51))
        self.lightSwitchState = False

        self.lightSwitch2 = QPushButton('', self)
        self.lightSwitch2.resize(self.lightSwitch2.sizeHint())
        self.lightSwitch2.clicked.connect(self.lightSwitch2Clicked)
        self.lightSwitch2.setIcon(QIcon('imgs/luzoff.png'))
        self.lightSwitch2.setIconSize(QSize(51,51))
        self.lightSwitch2State = False

        self.gateSwitch = QPushButton(self)
        self.gateSwitch.resize(self.gateSwitch.sizeHint())
        self.gateSwitch.clicked.connect(self.gateSwitchClicked)
        self.gateSwitch.setIcon(QIcon('imgs/gateclosed.png'))
        self.gateSwitch.setIconSize(QSize(46,32))
        self.gateSwitchState = False

        self.serialIn = QLineEdit(self)
        self.serialOut = QLineEdit(self)
        self.serialOut.textChanged.connect(self.newDataSent)
        self.temperatureThresholdLabel = QLabel('Limite de Temperatura')
        self.airCondLabel = QLabel('Ar Condicionado')

        self.layoutGrids()

        self.setWindowIcon(QIcon('imgs/shouse.png'))
        self.setWindowTitle('Controle Residencial')
        self.center()
        self.show()

    def layoutGrids(self):
        gridSpacing = 10

        self.temperatureBox = QHBoxLayout()
        self.temperatureBox.setSpacing(gridSpacing)
        self.temperatureBox.addWidget(self.tempLabel)
        self.temperatureBox.addWidget(self.tempLCD)

        self.temperatureThresholdGrid = QHBoxLayout()
        self.temperatureThresholdGrid.setSpacing(gridSpacing)
        self.temperatureThresholdGrid.addWidget(self.temperatureThresholdLabel)
        self.temperatureThresholdGrid.addWidget(self.setTempThreshold)
        self.temperatureThresholdGrid.addWidget(self.setTempThresholdButton)

        self.airCondGrid = QHBoxLayout()
        self.airCondGrid.setSpacing(gridSpacing)
        self.airCondGrid.addWidget(self.airCondLabel)
        self.airCondGrid.addWidget(self.airCondSwitch)

        self.internalLightGrid = QHBoxLayout()
        self.internalLightGrid.setSpacing(gridSpacing)
        self.internalLightGrid.addWidget(self.lightSwitchLabel)
        self.internalLightGrid.addWidget(self.lightSwitch)

        self.externalLightGrid = QHBoxLayout()
        self.externalLightGrid.setSpacing(gridSpacing)
        self.externalLightGrid.addWidget(self.lightSwitch2Label)
        self.externalLightGrid.addWidget(self.lightSwitch2)

        self.gateGrid = QHBoxLayout()
        self.gateGrid.setSpacing(gridSpacing)
        self.gateGrid.addWidget(self.gateSwitchLabel)
        self.gateGrid.addWidget(self.gateSwitch)

        self.lastTxGrid = QHBoxLayout()
        self.lastTxGrid.setSpacing(gridSpacing)
        self.lastTxGrid.addWidget(self.serialOutLabel)
        self.lastTxGrid.addWidget(self.serialOut)

        self.lastRxGrid = QHBoxLayout()
        self.lastRxGrid.setSpacing(gridSpacing)
        self.lastRxGrid.addWidget(self.serialInLabel)
        self.lastRxGrid.addWidget(self.serialIn)

        grid = QGridLayout()
        grid.setSpacing(gridSpacing)

        gridElements = [self.temperatureThresholdGrid, self.temperatureBox, self.modeSwitch, \
            self.airCondGrid, self.internalLightGrid, self.externalLightGrid, self.gateGrid, \
            self.lastTxGrid, self.lastRxGrid, self.panicButton]
        
        for i in range(len(gridElements)):
            if type(gridElements[i]) == QHBoxLayout:
                grid.addLayout(gridElements[i], i, 0)
            else:
                grid.addWidget(gridElements[i], i, 0)

        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)

    def panicButtonClicked(self):
        print(f'{self.sender().text()} was pressed')
        return
        
    def modeSwitchClicked(self):
        print(f'{self.sender().text()} was pressed')
        self.sender().setText('AUTO' if self.modeSwitchState else 'MANUAL')
        self.modeSwitchState = not self.modeSwitchState
        self.sender().setChecked(False)
        self.disableButtons(not self.modeSwitchState)

        return

    def disableButtons(self, disabled):
        self.airCondSwitch.setDisabled(disabled)
        self.lightSwitch.setDisabled(disabled)
        self.lightSwitch2.setDisabled(disabled)
        self.gateSwitch.setDisabled(disabled)

    def lightSwitchClicked(self):
        print(f'{self.sender().text()} was pressed')
        if self.modeSwitchState or self.commandReceived:
            icon = QIcon('imgs/luzoff.png' if self.lightSwitchState else 'imgs/luzon.png')
            self.sender().setIcon(icon)
            # self.sender().setText('Luz 1 OFF' if self.lightSwitchState else 'Luz 1 ON')
            self.lightSwitchState = not self.lightSwitchState
            self.commandReceived = False
        else:
            return

    def airCondSwitchClicked(self):
        print(f'{self.sender().text()} was pressed')
        if self.modeSwitchState or self.commandReceived:
            icon = QIcon('imgs/airoff.png' if self.airCondSwitchState else 'imgs/airon.png')
            self.sender().setIcon(icon)
            # self.sender().setText('Luz 1 OFF' if self.lightSwitchState else 'Luz 1 ON')
            self.airCondSwitchState = not self.airCondSwitchState
            self.commandReceived = False
        else:
            return

    def lightSwitch2Clicked(self):
        print(f'{self.sender().text()} was pressed')
        if self.modeSwitchState or self.commandReceived:
            icon = QIcon('imgs/luzoff.png' if self.lightSwitch2State else 'imgs/luzon.png')
            self.sender().setIcon(icon)
            # self.sender().setText('Luz 2 OFF' if self.lightSwitch2State else 'Luz 2 ON')
            self.lightSwitch2State = not self.lightSwitch2State
            self.commandReceived = False
        else:
            return

    def gateSwitchClicked(self):
        print(f'{self.sender().text()} was pressed')
        if self.modeSwitchState or self.commandReceived:
            icon = QIcon('imgs/gateclosed.png' if self.gateSwitchState else 'imgs/gateopen.png')
            self.sender().setText('Portão Fechado' if self.gateSwitchState else 'Portão Aberto')
            self.sender().setIcon(icon)
            self.gateSwitchState = not self.gateSwitchState
            self.sender().setChecked(False)
            self.commandReceived = False
        else:
            return

    def luminosityChanged(idx, self):
        return

    def temperatureChanged(self):
        try:
            tempThreshold = int(self.setTempThreshold.text())
        except:
            print('!!!! WARNING !!!! Invalid temperature threshold')
            tempThreshold = self.tempLCD.value()

        if self.tempLCD.value() <= tempThreshold:
            self.setLCDColor(self.tempLCD, 'r')
        else:
            self.setLCDColor(self.tempLCD, 'g')

        return
    
    def newDataReceived(self, data):
        # proccess received data, e.g. call temperatureChanged
        self.serialIn.setText(data)
        return

    def newDataSent(self):
        print(self.serialOut.text()) # debug functionality
        # sent data via serial
        return
    
    def setLCDColor(self, lcd, color = 'r'):
        if color == 'r':
            color = QColor(213, 0, 0)
        elif color == 'g':
            color = QColor(27, 94, 32)
        else:
            return

        palette = lcd.palette()
        # foreground color
        palette.setColor(palette.WindowText, color)
        # background color, default: white
        palette.setColor(palette.Background, QColor(0, 0, 0))
        # 'light' border
        palette.setColor(palette.Light, color)
        # 'dark' border
        palette.setColor(palette.Dark, color)
        lcd.setPalette(palette)

    def center(self):   
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow()

    # USB_PORT = 'USB0'
    # com = serial.Serial(f'/dev/tty{USB_PORT}', 115200)
    sys.exit(app.exec_())