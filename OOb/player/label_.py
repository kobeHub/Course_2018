#!/usr/bin/python3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QApplication
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)


class QLabel_alterada(QLabel):
    """
    Define the label which canbe clicked
    """
    clicked=pyqtSignal()
    def __init__(self, parent=None):
        QLabel.__init__(self, parent)

    def mousePressEvent(self, ev):
        self.clicked.emit()

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.label = QLabel_alterada()
        self.label.setText('test')

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        wid = QWidget(self)
        wid.setLayout(layout)
        self.label.clicked.connect(self.dosomestuff) 

    def dosomestuff(self):
        print("click")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
