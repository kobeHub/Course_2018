#!/usr/bin/python3

import sys
import re
import pyglet
import os
from pyglet.gl import *
from TimeThread import time_thread
import threading
"""
视频窗口的具体实现，由于plglet与QT均可以提供window服务
而无法共享，所以采用两个窗口．

"""

def draw_rec(x,y,width,height):
    """
    矩形
    """
    glLoadIdentity()
    glPushMatrix()
    glBegin(GL_LINE_LOOP)
    glVertex2f(x,y)
    glVertex2f(x+width,y)
    glVertex2f(x+width,y+height)
    glVertex2f(x,y+height)
    glEnd()
    glPopMatrix()


class Button(pyglet.event.EventDispatcher):

    def __init__(self):
        super(Button,self).__init__()
        self.x=y=0  #按钮的位置以及大小
        self.width=height=10
        self.hit=False  #按钮是否被鼠标点击
        self._text=pyglet.text.Label('',anchor_x='center',anchor_y='center')   #初始化是必要的,必须写在__init__中，不然给他赋文本值会当成全局量，最终显示的按钮的文本是最后一个赋值（即，作为私有量）
    
    def draw(self):
        """
        画按钮
        """
        if self.hit:
            glColor3f(0.0,1.0,0.0)
        draw_rec(self.x,self.y,self.width,self.height)
        glColor3f(1.0,1.0,1.0)
        self.draw_label()
    def set_text(self,button_text):
        """
        改变按钮的文本
        """
        self._text.text=button_text
    button_text=property(lambda self: self._text.text,set_text)
    def set_size(self,x,y,width,height):
        """
        改变按钮的位置和大小
        """
        self.x=x
        self.y=y
        self.width=width
        self.height=height

    def on_mouse_press(self,x,y,button,modifiers):
        self.dispatch_event('on_press')   #调度事件
        self.hit=True  #鼠标点击，颜色变化
    def on_mouse_drag(self,x,y,dx,dy,button,modifiers):
        """
        拖动
        """
        self.dispatch_event('on_value_change')
    def on_mouse_release(self,x,y,button,modifiers):
        self.dispatch_event('on_release')
        self.hit=False  #释放鼠标，恢复颜色
    def draw_label(self):
        """
        添加标签
        """
        self._text.x=self.x+self.width/2
        self._text.y=self.y+self.height/2
        self._text.draw()
    def hit_test(self,x,y):
        return (self.x<x<self.x+self.width and self.y < y < self.y+self.height)
        

        
#注册事件类型
Button.register_event_type('on_press')
Button.register_event_type('on_value_change')
Button.register_event_type('on_release')


class Player(pyglet.media.Player):
    width = 10
    height = 10
    
    def load_source(self,uri):
        """
        载入视频资源
        """
        path = os.path.dirname(uri)
        target = os.path.basename(uri)

        resource_path=[path]
        pyglet.resource.path=resource_path
        pyglet.resource.reindex()
        if path:
            for root,dirname,files in os.walk(path):
                for f in files:
                    # pattern = re.compile(r'\w*\.[mp4|rmvb|flv|mpeg|avi|...]', re.I )
                    if f == target:
                        source=pyglet.resource.media(f)
                        self.queue(source)

    def set_locate(self,x=0,y=0):
        """
        设置播放器的位置
        """
        self.x=x
        self.y=y

    def get_and_set_video_size(self):
        """
        获取视频的大小并设置播放器的长宽
        """
        if self.source and self.source.video_format:
            self.width=self.source.video_format.width
            self.height=self.source.video_format.height
        if self.source.video_format.sample_aspect>1:
            self.width*=self.source.video_format.sample_aspect
        else:
            self.height/=self.source.video_format.sample_aspect
        print(self.get_current_time, self.get_duration)
     
    def _get_current_time(self):
        return self.time

    def _duration(self):
        return self.source.duration
    
    @property
    def get_current_time(self):
        time = self._get_current_time()
        minute = int(time//60)
        seconds = int(time)%60

        if minute < 10:
            minute = '0'+str(minute)
        if seconds < 10:
            seconds = '0'+str(seconds)

        return str(minute) + ':' + str(seconds)

    @property 
    def get_duration(self):
        duration = self._duration()
        return str(int(duration//60))+':'+str(int(duration%60))
    
        
class MyPlayer(pyglet.window.Window):
    def __init__(self, caption, argv):
        super(MyPlayer,self).__init__(caption=caption,resizable=True)
        self.padding=20  #默认的间距以及长宽
        self.width=50
        self.height=30

        

        print(argv)
        #下面列出要显示的列表
        self.drawable=[]  #显示列表

        #播放器
        self.player=Player()
        self.player.load_source(argv)
        self.player.set_locate(0,self.padding*2+30)  #播放器显示位置
        self.player.get_and_set_video_size()  #得到视频的大小并设置
        self.player.EOS_NEXT='next'  #按顺序进行播放
        self.player.push_handlers(self)

        #播放/暂停控制按钮
        self.play_pause_control=Button()
        self.play_pause_control.width=50
        self.play_pause_control.height=30
        self.play_pause_control.set_size(self.padding,self.padding,self.play_pause_control.width,self.play_pause_control.height)  #位置以及大小
        self.play_pause_control.button_text='play'  #文本设置
        self.play_pause_control.on_press=lambda:self.on_play_pause()
        self.drawable.append(self.play_pause_control)  #将这个按钮加入到显示列表中

        #快进按钮
        self.forward_button = Button()
        self.forward_button.width = 80
        self.forward_button.height = 30
        self.forward_button.set_size(self.padding*2+self.play_pause_control.width, self.padding, self.forward_button.width,self.forward_button.height)
        self.forward_button.button_text = 'forward'
        self.forward_button.on_press = lambda:self.forward()
        self.drawable.append(self.forward_button)

        # 后退按钮
        self.rewind_button = Button()
        self.rewind_button.width = 80
        self.rewind_button.height = 30
        self.rewind_button.set_size(self.padding*3+self.play_pause_control.width+self.forward_button.width, 
                                            self.padding, 
                                            self.rewind_button.width,
                                            self.rewind_button.height)
        self.rewind_button.button_text = 'rewind'
        self.rewind_button.on_press = lambda:self.rewind()
        self.drawable.append(self.rewind_button)        

        #全屏控制按钮
        self.isscreenfull=Button()
        self.isscreenfull.width=100
        self.isscreenfull.height=30
        self.isscreenfull.set_size(self.padding*4+self.play_pause_control.width+self.forward_button.width+self.rewind_button.width,
                                            self.padding,
                                            self.isscreenfull.width,
                                            self.isscreenfull.height)
        self.isscreenfull.button_text='fullscreen'
        self.isscreenfull.on_press=lambda: self.full_not()
        self.drawable.append(self.isscreenfull)

        self.content = ''
        self.video_time = pyglet.text.Label('now: 00:00',
                                            font_name='Times New Roman',
                                            font_size=18,
                                            x = 500, y = self.padding)
        # self.drawable.append(self.video_time)

        self.video_dur = pyglet.text.Label('duration: '+ self.player.get_duration,
                                            font_name='Times New Roman',
                                            font_size=18,
                                            x = 650, y = self.padding)
        # self.drawable.append(self.video_dur)

        
        # self.video_time.begin_update()
        # self.timer = time_thread(self.player, 0, self.content)
        # self.timer.start()
        # self.video_time.end_update()

        # threading.Thread(self.update()).start()
        # self.update()
        
    def update(self):
        while True:
            if 'now:'+self.content != self.video_time.text:
                self.video_time = pyglet.text.Label('now:'+self.content,
                                            font_name='Times New Roman',
                                            font_size=18,
                                            x = 500, y = self.padding)
        
    def on_draw(self):
        self.clear()
        #显示播放器
        if self.player.source and self.player.source.video_format: 
            self.player.get_texture().blit((self.width-self.player.width)/2,self.player.y,width=self.player.width,height=self.player.height) #注意这里width=,height=不能省略，否则画面不会出现的
            

        #画列表中所有的控制按钮
        if self.drawable:
            for draw_c in self.drawable:
                draw_c.draw()
            self.video_time.draw()
            self.video_dur.draw()

    def on_mouse_press(self,x,y,button,modifiers):
        for dc in self.drawable:
            if dc.hit_test(x,y):
                dc.on_mouse_press(x,y,button,modifiers)
    
    def on_play_pause(self):
        if self.player.playing:
            self.player.pause()
            self.play_pause_control.set_text('pause')    
        else:
            if self.player.time > self.player.source.duration:
                self.player.seek(0)
            self.player.play()
            self.play_pause_control.set_text('play')

    def full_not(self):
        if self.fullscreen:
            self.set_fullscreen(fullscreen = False)
            self.isscreenfull.button_text = 'fullscreen'
        else:
            self.set_fullscreen()
            self.isscreenfull.button_text = 'windowed'
    
    def on_mouse_release(self,x,y,button,modifiers):
        for dc in self.drawable:
            if dc.hit_test(x,y):
                dc.on_mouse_release(x,y,button,modifiers)
    
    def on_resize(self,width,height):
        super(MyPlayer,self).on_resize(width,height)
        if self.player.source:
            video_width,video_height=self.player.width,self.player.height
            
        display_aspect=width/float(height)
        video_aspect=video_width/float(video_height)

        if video_aspect>display_aspect:
            self.player.width=width
            self.player.height=width/video_aspect
        else:
            self.player.height=height
            self.player.width=height * video_aspect
        self.player.x=(width-self.player.width)/2
        self.player.y=(height-self.player.height)/2

    def forward(self, jump_distance= 3):
        time = self.player._get_current_time() + jump_distance
        try:
            if self.player._duration() > time:
                print('[+] Jump to {0} seconds'.format(time))
                self.player.seek(time)
                # self.songtime = time 
            else:
                print('[+]Jump to the end!')
                self.player.seek(self.player._duration() - 1)
        except AttributeError:
            pass

    def rewind(self, jump_distance=3):
        time = self.player._get_current_time() - jump_distance
        try:
            print('[+] Jump to {0} seconds'.format(time))
            self.player.seek(time)
            # self.songtime = time
        except:
            self.player.seek(0)

if __name__ == "__main__":
    wn=MyPlayer('my player', sys.argv[1])
    wn.set_size(int(wn.player.width),int(wn.player.height)) #将窗口的大小设置的和视频一样大小
    wn.set_visible(True)  #可见
    wn.player.play()
    pyglet.app.run()
