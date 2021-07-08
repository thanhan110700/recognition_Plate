from PyQt5.QtWidgets import *
import sys
from PyQt5 import QtGui

class CheckCar(QWidget):
    def initUI(self,mainWindow):
        self.title = "Xe chưa thoát khỏi hệ thống"
        self.left = 500
        self.top = 200
        self.width = 400
        self.height = 500
        mainWindow.setWindowTitle(self.title)
        mainWindow.setGeometry(self.left, self.top, self.width, self.height)

        d = QHBoxLayout()
        label = QPushButton("hahaa")
        label.setStyleSheet("color:black")
        d.addWidget(label)
        self.setLayout(d)




