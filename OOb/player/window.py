#!/usr/bin/python3
"""
GUI界面的实现类，通过与AudioPlayer类进行
组合，调用其内部成员player的各种方法实现音频播放
"""
 
from PyQt5.QtCore import Qt, QUrl, QDir

from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
            QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QMessageBox)
from PyQt5.QtWidgets import QMainWindow,QWidget, QAction
from PyQt5 import QtGui 
import sys

from plCore import AudioPlayer
from TimeThread import time_thread
from label_ import QLabel_alterada

import pyglet
import threading
import os
import time
import re

 
class MvpWindow(QMainWindow):
 
    def __init__(self, parent=None):
        super(MvpWindow, self).__init__(parent)
        self.setWindowTitle("Small mvp")
        self.init_ui()
        self.player = AudioPlayer()
        self.bind_event()
        self.refresh_time()

        self.core = core_thread()
        self.core.start()
        # process_thread(self).start()
        # self.process_bar = threading.Thread()
        # core.join()
        # pyglet.app.run()

    def init_ui(self): 
        self.background = QLabel() 
        src = QtGui.QPixmap('source/1.jpg')
        self.background.setPixmap(src)

        self.play_img = QtGui.QPixmap('source/play.png')
        self.paused_img = QtGui.QPixmap('source/pause.png')
        self.playButton = QLabel_alterada()
        self.playButton.setPixmap(self.paused_img)

        back = QtGui.QPixmap('source/back.png')
        self.backButton =  QLabel_alterada()
        self.backButton.setPixmap(back)

        forward = QtGui.QPixmap('source/forward.png')
        self.forwardButton = QLabel_alterada()
        self.forwardButton.setPixmap(forward)
 
        self.positionSlider = QSlider(Qt.Horizontal)
        # self.positionSlider.setRange(10, 1)
        self.positionSlider.setFocusPolicy(Qt.NoFocus)
        self.positionSlider.sliderMoved.connect(self.changeValue)
        # self.positionSlider.valueChanged.connect(self.changeValue)

        
        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)
 
        # Create new action
        openAction = QAction('&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)
 
        # Create exit action
        exitAction = QAction('&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)
 
        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
 
        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # set time label
        self.time_label = QLabel()
        self.time_label.setText('00:00')

        self.duration_label = QLabel()
        self.duration_label.setText('00:00') 
 
        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.backButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.forwardButton)
        controlLayout.addWidget(self.time_label)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.duration_label)
 
        layout = QVBoxLayout()
        
        layout.addWidget(self.background)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)
        layout.addWidget(self.background)
 
        # Set widget to contain window contents
        wid.setLayout(layout)

    def bind_event(self):
        self.forwardButton.clicked.connect(self.forward)
        self.backButton.clicked.connect(self.rewind)
        self.playButton.clicked.connect(self.play)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())
 
        if fileName != '':
            pattern = re.compile(r'\w*\.[mp4|rmvb|flv|mpeg|avi|...]', re.I )
            if pattern.match(os.path.basename(fileName)):
                try:
                    os.system("gnome-terminal -e 'bash -c \"python3 video.py {0}; exec bash\"'".format(fileName))  
                    self.exitCall()
                except:  
                    print('Program is dead.')
                

            self.player.play_list_add(fileName)
            
    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()

        print('x:{0}, y:{1}'.format(x,y))
            
    def exitCall(self):
        # sys.exit(app.exec_())
        # self.core.stop()
        # self._time.stop()
        os._exit(0)
        
    def play(self):
        if self.player.play_list_is_empty():
            self.slot_error('没有打开歌曲呢，实在是做不到啊！')
            return
        print('Play key was clicked')
        if self.player.paused_flag % 2 == 0:
            self.player.pause()
           
            self.playButton.setPixmap(self.paused_img)
            print(self.player.get_current_time())
        else:
            print('[+]play continue')
            self.player.play()
            
            self.playButton.setPixmap(self.play_img)
            print(self.player.get_current_time())

        self.player.paused_flag += 1
        self.duration_label.setText(self.player.get_duration())
        
        # self.refresh_time()
        # print(self.player.is_playing())

    def slot_error(self, msg):
        error = QMessageBox.information(self,                         #使用infomation信息框  
                                    "Error",  
                                    msg,  
                                    QMessageBox.Ok)  
  
 
    def positionChanged(self, position):
        self.positionSlider.setValue(position)
 
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
 
    def setPosition(self):
        dur = self.positionSlider.maximum()
        pos = self.player.get_current_time()
        hint = pos // self.player.duration
     
        pos_ = dur*hint
        self.positionSlider.setValue(pos_)

    def changeValue(self, value):
        if self.player.play_list_is_empty():
            self.slot_error('我没有对象别惹我！')
            self.positionSlider.setValue(0)
            return
        pos = self.positionSlider.value()
        dur = self.positionSlider.maximum()
        hint = pos/dur 

        self.player.seek(int(hint*self.player.duration))
 
    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

    def forward(self):
        if self.player.play_list_is_empty():
            self.slot_error('这个需求真的做不到了！')
            return
        self.player.forward(3)
        

    def rewind(self):
        if self.player.play_list_is_empty():
            self.slot_error('这个需求真的做不到了！')
            return
        self.player.rewind(3)

    def refresh_time(self):
        self._time = time_thread(self.player, self.time_label, self.positionSlider)
        self._time.start()
               
class core_thread(threading.Thread):
    def __init__(self):
        super(core_thread, self).__init__() 

    def run(self):
        pyglet.app.run()

    def stop(self):
        sys.exit(0)       

"""
class process_thread(threading.Thread):
    def __init__(self, win):
        super(process_thread, self).__init__()
        self.win = win

    def run(self):
        while 1:
            if self.win.player.is_playing():
                self.win.setPosition()

            time.sleep(1)
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MvpWindow()
    player.resize(600, 300)
    player.show()
    sys.exit(app.exec_())


 