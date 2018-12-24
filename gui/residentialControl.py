#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import serial
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication, QDesktopWidget,
    QLabel, QLCDNumber, QGridLayout, QLineEdit)
from PyQt5.QtGui import (QIcon, QFont, QColor)
from PyQt5.QtCore import (QSize)

class MainWindow(QWidget):
    def __init__(self, port = None):
        super().__init__()
    
        self.com = port
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

        airCondSwitch = QPushButton('Temperatura', self)
        airCondSwitch.resize(airCondSwitch.sizeHint())
        airCondSwitch.clicked.connect(self.airCondSwitchClicked)
        airCondSwitch.setIcon(QIcon('imgs/airoff.png'))
        airCondSwitch.setIconSize(QSize(51,51))
        self.airCondSwitchState = False
        
        lightSwitch = QPushButton('', self)
        lightSwitch.resize(lightSwitch.sizeHint())
        lightSwitch.clicked.connect(self.lightSwitchClicked)
        lightSwitch.setIcon(QIcon('imgs/luzoff.png'))
        lightSwitch.setIconSize(QSize(51,51))
        self.lightSwitchState = False

        lightSwitch2 = QPushButton('', self)
        lightSwitch2.resize(lightSwitch2.sizeHint())
        lightSwitch2.clicked.connect(self.lightSwitch2Clicked)
        lightSwitch2.setIcon(QIcon('imgs/luzoff.png'))
        lightSwitch2.setIconSize(QSize(51,51))
        self.lightSwitch2State = False

        gateSwitch = QPushButton('Portão Fechado', self)
        gateSwitch.resize(gateSwitch.sizeHint())
        gateSwitch.clicked.connect(self.gateSwitchClicked)
        gateSwitch.setIcon(QIcon('imgs/gateclosed.png'))
        gateSwitch.setIconSize(QSize(46,32))
        self.gateSwitchState = False

        self.serialIn = QLineEdit(self)
        self.serialOut = QLineEdit(self)
        self.serialOut.textChanged.connect(self.newDataSent)

        grid = QGridLayout()
        grid.setSpacing(10)

        # grid.addWidget(tempLabel, 1, 0)
        grid.addWidget(airCondSwitch, 1, 0)
        grid.addWidget(self.tempLCD, 1, 1)
        grid.addWidget(QLabel('Limite de Temperatura'), 1, 2)
        grid.addWidget(self.setTempThreshold, 1, 3)
        
        # grid.addWidget(lumLabels[0], 2, 0)
        # grid.addWidget(self.lumLCD[0], 2, 1)

        # grid.addWidget(lumLabels[1], 3, 0)
        # grid.addWidget(self.lumLCD[1], 3, 1)

        grid.addWidget(lightSwitchLabel, 2, 2)
        grid.addWidget(lightSwitch, 3, 2)
        grid.addWidget(lightSwitch2Label, 2, 3)
        grid.addWidget(lightSwitch2, 3, 3)

        # grid.addWidget(gateSwitchLabel, 4, 2)
        grid.addWidget(gateSwitch, 4, 3)

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
        return

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

    def newDataReceived(self, data):
        # proccess received data, e.g. call temperatureChanged
        self.serialIn.setText(data)
        return

    def newDataSent(self):
        print(self.serialOut.text()) # debug functionality
        # sent data via serial
        return

    def requestData(self):
        c = 'x'
        msg = []
        self.commandReceived = True
        if self.com:
            com.write('R')
            while c != '\n':
                c = self.com.read()
                msg.append(c)
            msg = msg.split()
            temp = int(msg[0])
            self.tempLCD.display(temp)
            if int(msg[1]):
                self.lightSwitchState = False
                self.lightSwitchClicked()
            else:
                self.lightSwitchState = True
                self.lightSwitchClicked()
            if int(msg[2]):
                self.lightSwitch2State = False
                self.lightSwitch2Clicked()
            else:
                self.lightSwitch2State = True
                self.lightSwitch2Clicked()
            if int(msg[3]):
                self.airCondSwitchState = False
                self.airCondSwitchClicked()
            else:
                self.airCondSwitchState = True
                self.airCondSwitchClicked()
        self.commandReceived = False
            
if __name__ == '__main__':
    # USB_PORT = ['USB0', 'USB1', 'ACM0', 'ACM1']
    # for usb in USB_PORT:
    #     try:
    #         com = serial.Serial(f'/dev/tty{usb}', 115200)
    #     except:
    #         print("Tentativa...")
    #         com = []
    #     if com:
    #         break
    # if not com:
    #     raise Exception("Não há nenhuma porta serial disponível")

    app = QApplication(sys.argv)
    ex = MainWindow()

    number = input('Type a number: ')
    ex.tempLCD.display(number)
    ex.newDataReceived('C')
    ex.temperatureChanged()
    sys.exit(app.exec_())