#!/usr/bin/python3
"""
创建时间进程，用于进行进度条，以及播放时间的更新
"""

import time
import threading
import sys


class time_thread(threading.Thread):
    def __init__(self, audio, label, win):
        threading.Thread.__init__(self)
        self.audio = audio
        self.label = label
        self.slider  = win
        self.time_ = '00:00' 

    def run(self):
        if self.label == 0:				# 作为视频的计时器
            while True:
                self.time_ = self.audio.get_current_time
                self.slider = self.time_
                print(self.time_)
                time.sleep(1)


        else: 				# 作为音频计时器
            while True:
                if self.audio.is_playing():
                    print(self.time_)
                    self.label.setText(self.time_)
                    minute = int(self.audio.get_current_time()//60)
                    seconds = int(self.audio.get_current_time())%60

                    if minute < 10:
                        minute = '0'+str(minute)
                    if seconds < 10:
                        seconds = '0'+str(seconds)

                    self.time_ = str(minute) + ':' + str(seconds)
                
                    dur = self.slider.maximum()
                    now = int(self.audio.get_current_time())
                    hint = now/self.audio.duration 
                    pos = int(dur * hint)
                    print(pos)
                    self.slider.setValue(pos)
                    time.sleep(1)

    def stop(self):
        sys.exit(0) 