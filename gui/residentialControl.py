#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication, QDesktopWidget,
    QLabel, QLCDNumber, QGridLayout, QLineEdit)
from PyQt5.QtGui import (QIcon, QFont, QColor)
from PyQt5.QtCore import (QSize)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        

    def initUI(self):
        panicButton = QPushButton('PÂNICO', self)
        panicButton.resize(panicButton.sizeHint())
        panicButton.clicked.connect(self.panicButtonClicked)

        modeSwitch = QPushButton('MANUAL', self)
        modeSwitch.resize(modeSwitch.sizeHint())
        modeSwitch.clicked.connect(self.modeSwitchClicked)
        self.modeSwitchState = True

        # tempLabel = QLabel('Temperatura')
        lumLabels = [QLabel('Luz Interna'), QLabel('Luz Externa')]
        lightSwitchLabel = QLabel('Luz Interna')
        lightSwitch2Label = QLabel('Luz Externa')
        # gateSwitchLabel = QLabel('Portão')
        serialInLabel = QLabel('Último dado recebido')
        serialOutLabel = QLabel('Último dado enviado')

        self.tempLCD = QLCDNumber()
        self.setTempThreshold = QLineEdit()
        # self.lumLCD = [QLCDNumber(), QLCDNumber()]

        self.airCondSwitch = QPushButton('Temperatura', self)
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

        self.gateSwitch = QPushButton('Portão Fechado', self)
        self.gateSwitch.resize(self.gateSwitch.sizeHint())
        self.gateSwitch.clicked.connect(self.gateSwitchClicked)
        self.gateSwitch.setIcon(QIcon('imgs/gateclosed.png'))
        self.gateSwitch.setIconSize(QSize(46,32))
        self.gateSwitchState = False

        self.serialIn = QLineEdit(self)
        self.serialOut = QLineEdit(self)
        self.serialOut.textChanged.connect(self.newDataSent)

        grid = QGridLayout()
        grid.setSpacing(10)

        # grid.addWidget(tempLabel, 1, 0)
        grid.addWidget(self.airCondSwitch, 1, 0)
        grid.addWidget(self.tempLCD, 1, 1)
        grid.addWidget(QLabel('Limite de Temperatura'), 1, 2)
        grid.addWidget(self.setTempThreshold, 1, 3)
        
        # grid.addWidget(lumLabels[0], 2, 0)
        # grid.addWidget(self.lumLCD[0], 2, 1)

        # grid.addWidget(lumLabels[1], 3, 0)
        # grid.addWidget(self.lumLCD[1], 3, 1)

        grid.addWidget(lightSwitchLabel, 2, 2)
        grid.addWidget(self.lightSwitch, 3, 2)
        grid.addWidget(lightSwitch2Label, 2, 3)
        grid.addWidget(self.lightSwitch2, 3, 3)

        # grid.addWidget(gateSwitchLabel, 4, 2)
        grid.addWidget(self.gateSwitch, 4, 3)

        grid.addWidget(panicButton, 5, 1)

        grid.addWidget(serialInLabel, 5, 2)
        grid.addWidget(self.serialIn, 5, 3)

        grid.addWidget(serialOutLabel, 6, 2)
        grid.addWidget(self.serialOut, 6, 3)

        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)

        self.setWindowIcon(QIcon('imgs/shouse.png'))
        self.setWindowTitle('Controle Residencial')
        self.center()
        self.show()


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
            color = QColor(255, 0, 0)
        elif color == 'g':
            color = QColor(0, 255, 0)
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
    number = input('Type a number: ')
    ex.tempLCD.display(number)
    ex.newDataReceived('C')
    ex.temperatureChanged()
    sys.exit(app.exec_())